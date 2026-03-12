"""
战斗场景 - 即时战斗界面
"""
import pygame
import math
import random
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, FACTION_COLORS
from ui.button import Button
from entities.army import Army
from systems.battle import BattleSystem
from scenes.base_scene import BaseScene


class BattleScene(BaseScene):
    """战斗场景类"""

    def __init__(self, game_manager, attacker=None, defender=None, city=None):
        """初始化战斗场景

        Args:
            game_manager: 游戏管理器
            attacker: 攻击方势力名
            defender: 防守方势力名
            city: 目标城市对象
        """
        super().__init__(game_manager)
        self.battle_system = BattleSystem()

        # 战斗参数
        self.attacker_faction = attacker
        self.defender_faction = defender if defender else (city.faction if city else '敌军')
        self.target_city = city

        # 创建军队
        self.attacker_army = self._create_attacker_army()
        self.defender_army = self._create_defender_army()

        # 战斗单位
        self.attacker_units = []
        self.defender_units = []
        self._init_units()

        # 战斗状态
        self.battle_time = 0
        self.battle_paused = False
        self.battle_speed = 1
        self.battle_result = None
        self.battle_log = []

        # 特效
        self.effects = []

        # 创建UI
        self._create_ui()

    def _create_attacker_army(self):
        """创建攻击方军队"""
        army = Army(self.attacker_faction, "主将", 100, 300)
        army.infantry = 3000
        army.cavalry = 1500
        army.archer = 500
        return army

    def _create_defender_army(self):
        """创建防守方军队"""
        if self.target_city:
            army = Army(self.defender_faction, "守将", 700, 300)
            army.infantry = min(3000, self.target_city.soldiers)
            army.cavalry = min(1000, self.target_city.soldiers // 3)
            army.archer = min(500, self.target_city.soldiers // 5)
            return army
        return Army(self.defender_faction, "守将", 700, 300)

    def _init_units(self):
        """初始化战斗单位"""
        # 攻击方单位
        for i in range(10):
            self.attacker_units.append({
                'x': 150 + random.randint(-30, 30),
                'y': 200 + i * 40,
                'type': random.choice(['infantry', 'cavalry', 'archer']),
                'hp': 100,
                'faction': self.attacker_faction,
                'target': None,
                'attacking': False,
            })

        # 防守方单位
        for i in range(10):
            self.defender_units.append({
                'x': WINDOW_WIDTH - 150 + random.randint(-30, 30),
                'y': 200 + i * 40,
                'type': random.choice(['infantry', 'cavalry', 'archer']),
                'hp': 100,
                'faction': self.defender_faction,
                'target': None,
                'attacking': False,
            })

    def _create_ui(self):
        """创建UI元素"""
        self.buttons = {
            'pause': Button(WINDOW_WIDTH // 2 - 200, 10, 80, 35, "暂停", self._on_pause),
            'speed_up': Button(WINDOW_WIDTH // 2 - 110, 10, 80, 35, "加速", self._on_speed_up),
            'retreat': Button(WINDOW_WIDTH // 2 - 20, 10, 80, 35, "撤退", self._on_retreat),
            'auto': Button(WINDOW_WIDTH // 2 + 70, 10, 80, 35, "自动", self._on_auto),
            'confirm': Button(WINDOW_WIDTH // 2 + 160, 10, 80, 35, "确认", self._on_confirm),
        }

    def _on_pause(self):
        """暂停/继续"""
        self.game_manager.play_sound('click')
        self.battle_paused = not self.battle_paused
        self.buttons['pause'].text = "继续" if self.battle_paused else "暂停"

    def _on_speed_up(self):
        """加速"""
        self.game_manager.play_sound('click')
        self.battle_speed = min(4, self.battle_speed + 1)
        self._add_log(f"战斗速度: x{self.battle_speed}")

    def _on_retreat(self):
        """撤退"""
        self.game_manager.play_sound('cancel')
        self.battle_result = {'winner': 'defender', 'reason': 'retreat'}
        self._add_log("攻击方撤退！")

    def _on_auto(self):
        """自动战斗"""
        self.game_manager.play_sound('click')
        self._auto_battle()

    def _on_confirm(self):
        """确认战斗结果"""
        if self.battle_result:
            # 播放胜利/失败音效
            if self.battle_result['winner'] == 'attacker':
                self.game_manager.play_sound('victory')
                # 攻击方胜利，更新城市归属
                if self.target_city:
                    old_faction = self.target_city.faction
                    self.target_city.faction = self.attacker_faction
                    # 扣除攻击方兵力损耗
                    attacker_losses = self.battle_result.get('attacker_losses', 0)
                    self.target_city.soldiers = max(0, self.target_city.soldiers - attacker_losses)
                    # 保存战斗结果供地图场景使用
                    self.game_manager.set_shared_data('battle_result', {
                        'winner': 'attacker',
                        'city_name': self.target_city.name,
                        'new_faction': self.attacker_faction,
                        'old_faction': old_faction,
                    })
            else:
                self.game_manager.play_sound('defeat')
                # 防守方胜利，保存战斗结果
                if self.target_city:
                    self.game_manager.set_shared_data('battle_result', {
                        'winner': 'defender',
                        'city_name': self.target_city.name,
                    })

            self.game_manager.scene_manager.load_scene('map')

    def _auto_battle(self):
        """自动战斗"""
        result = self.battle_system.simulate_battle(self.attacker_army, self.defender_army)
        self.battle_result = result
        for log in result.get('log', []):
            self._add_log(log)

    def _add_log(self, text):
        """添加战斗日志"""
        self.battle_log.append(text)
        if len(self.battle_log) > 8:
            self.battle_log.pop(0)

    def _add_effect(self, x, y, effect_type):
        """添加特效"""
        self.effects.append({
            'x': x,
            'y': y,
            'type': effect_type,
            'time': 30,
            'frame': 0,
        })

    def handle_event(self, event):
        """处理事件"""
        for button in self.buttons.values():
            button.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._on_pause()
            elif event.key == pygame.K_ESCAPE:
                self._on_retreat()

    def update(self):
        """更新战斗状态"""
        if self.battle_result:
            return

        if not self.battle_paused:
            for _ in range(self.battle_speed):
                self.battle_time += 1
                self._update_battle()

        # 更新特效
        for effect in self.effects[:]:
            effect['time'] -= 1
            effect['frame'] += 1
            if effect['time'] <= 0:
                self.effects.remove(effect)

        # 更新按钮
        for button in self.buttons.values():
            button.update()

    def _update_battle(self):
        """更新战斗"""
        # 更新单位
        for unit in self.attacker_units:
            if unit['hp'] > 0:
                self._update_unit(unit, self.defender_units)

        for unit in self.defender_units:
            if unit['hp'] > 0:
                self._update_unit(unit, self.attacker_units)

        # 检查战斗结束
        attacker_alive = sum(1 for u in self.attacker_units if u['hp'] > 0)
        defender_alive = sum(1 for u in self.defender_units if u['hp'] > 0)

        if attacker_alive == 0:
            self.battle_result = {'winner': 'defender', 'reason': 'annihilation'}
            self._add_log("防守方胜利！")
            self.game_manager.play_sound('defeat')
        elif defender_alive == 0:
            self.battle_result = {'winner': 'attacker', 'reason': 'annihilation'}
            self._add_log("攻击方胜利！")
            self.game_manager.play_sound('victory')

    def _update_unit(self, unit, enemies):
        """更新单位"""
        # 找最近的敌人
        min_dist = float('inf')
        target = None
        for enemy in enemies:
            if enemy['hp'] > 0:
                dist = math.sqrt((unit['x'] - enemy['x'])**2 + (unit['y'] - enemy['y'])**2)
                if dist < min_dist:
                    min_dist = dist
                    target = enemy

        if target:
            if min_dist > 50:
                # 移动向目标
                dx = target['x'] - unit['x']
                dy = target['y'] - unit['y']
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    speed = 3 if unit['type'] == 'cavalry' else 2
                    unit['x'] += (dx / dist) * speed
                    unit['y'] += (dy / dist) * speed
                unit['attacking'] = False
            else:
                # 攻击
                unit['attacking'] = True
                if random.random() < 0.02:
                    damage = random.randint(5, 15)
                    target['hp'] -= damage
                    self._add_effect(target['x'], target['y'], 'hit')
                    # 播放攻击音效
                    if random.random() < 0.3:  # 降低音效频率
                        self.game_manager.play_sound('attack')

    def render(self, screen):
        """渲染战斗场景"""
        # 绘制背景
        self._draw_background(screen)

        # 绘制战场
        self._draw_battlefield(screen)

        # 绘制单位
        self._draw_units(screen)

        # 绘制特效
        self._draw_effects(screen)

        # 绘制UI
        self._draw_ui(screen)

        # 绘制战斗结果
        if self.battle_result:
            self._draw_result(screen)

    def _draw_background(self, screen):
        """绘制背景"""
        # 使用基类的渐变背景方法（战场色调）
        self._draw_gradient_background(screen, (40, 60, 40), (60, 90, 60))

    def _draw_battlefield(self, screen):
        """绘制战场"""
        center_x = WINDOW_WIDTH // 2

        # 攻方区域
        attacker_color = FACTION_COLORS.get(self.attacker_faction, (150, 50, 50))
        pygame.draw.rect(screen, (*attacker_color, 100), (30, 100, 250, WINDOW_HEIGHT - 200), border_radius=15)

        # 守方区域
        defender_color = FACTION_COLORS.get(self.defender_faction, (50, 50, 150))
        pygame.draw.rect(screen, (*defender_color, 100), (WINDOW_WIDTH - 280, 100, 250, WINDOW_HEIGHT - 200), border_radius=15)

        # 中央战场
        pygame.draw.rect(screen, (60, 50, 40), (center_x - 200, 150, 400, WINDOW_HEIGHT - 250), border_radius=10)
        pygame.draw.rect(screen, (80, 70, 50), (center_x - 200, 150, 400, WINDOW_HEIGHT - 250), 3, border_radius=10)

        # 势力标签
        font = self.resource_loader.get_font('large')

        # 攻方标签
        attacker_text = font.render(f"攻方: {self.attacker_faction}", True, COLORS['white'])
        screen.blit(attacker_text, (50, 110))

        # 守方标签
        defender_text = font.render(f"守方: {self.defender_faction}", True, COLORS['white'])
        screen.blit(defender_text, (WINDOW_WIDTH - 260, 110))

    def _draw_units(self, screen):
        """绘制单位"""
        unit_colors = {
            'infantry': COLORS['white'],
            'cavalry': COLORS['yellow'],
            'archer': COLORS['green'],
        }

        # 攻击方单位
        for unit in self.attacker_units:
            if unit['hp'] > 0:
                color = FACTION_COLORS.get(self.attacker_faction, COLORS['red'])
                self._draw_unit(screen, unit, color)

        # 防守方单位
        for unit in self.defender_units:
            if unit['hp'] > 0:
                color = FACTION_COLORS.get(self.defender_faction, COLORS['blue'])
                self._draw_unit(screen, unit, color)

    def _draw_unit(self, screen, unit, color):
        """绘制单个单位"""
        x, y = int(unit['x']), int(unit['y'])
        size = 12 if unit['type'] == 'cavalry' else 10

        # 单位主体
        if unit['type'] == 'infantry':
            pygame.draw.rect(screen, color, (x - size//2, y - size//2, size, size))
        elif unit['type'] == 'cavalry':
            pygame.draw.polygon(screen, color, [
                (x, y - size), (x + size, y), (x, y + size), (x - size, y)
            ])
        else:  # archer
            pygame.draw.circle(screen, color, (x, y), size // 2)

        # 攻击动画
        if unit['attacking']:
            pygame.draw.circle(screen, COLORS['gold'], (x, y), size + 3, 2)

        # 血条
        hp_width = int((unit['hp'] / 100) * 20)
        pygame.draw.rect(screen, COLORS['red'], (x - 10, y - size - 5, 20, 3))
        pygame.draw.rect(screen, COLORS['green'], (x - 10, y - size - 5, hp_width, 3))

    def _draw_effects(self, screen):
        """绘制特效"""
        for effect in self.effects:
            alpha = int(255 * (effect['time'] / 30))
            if effect['type'] == 'hit':
                size = 10 + effect['frame'] // 2
                surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (*COLORS['gold'], alpha), (size, size), size)
                screen.blit(surface, (int(effect['x']) - size, int(effect['y']) - size))

    def _draw_ui(self, screen):
        """绘制UI"""
        # 按钮
        for button in self.buttons.values():
            button.render(screen, self.resource_loader)

        # 战斗信息
        self._draw_battle_info(screen)

        # 战斗日志
        self._draw_battle_log(screen)

    def _draw_battle_info(self, screen):
        """绘制战斗信息"""
        font = self.resource_loader.get_font('default')

        # 战斗时间
        minutes = self.battle_time // 3600
        seconds = (self.battle_time // 60) % 60
        time_text = font.render(f"时间: {minutes:02d}:{seconds:02d}", True, COLORS['white'])
        screen.blit(time_text, (WINDOW_WIDTH // 2 - 40, 60))

        # 军队状态
        attacker_hp = sum(u['hp'] for u in self.attacker_units if u['hp'] > 0)
        defender_hp = sum(u['hp'] for u in self.defender_units if u['hp'] > 0)

        attacker_text = font.render(f"兵力: {self.attacker_army.total_soldiers}", True, COLORS['white'])
        screen.blit(attacker_text, (50, WINDOW_HEIGHT - 80))

        defender_text = font.render(f"兵力: {self.defender_army.total_soldiers}", True, COLORS['white'])
        screen.blit(defender_text, (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 80))

    def _draw_battle_log(self, screen):
        """绘制战斗日志"""
        font = self.resource_loader.get_font('small')

        # 日志面板
        panel_x = 10
        panel_y = WINDOW_HEIGHT - 150
        panel_width = 300
        panel_height = 130

        surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (*COLORS['panel_bg'], 200), (0, 0, panel_width, panel_height), border_radius=5)
        pygame.draw.rect(surface, COLORS['panel_border'], (0, 0, panel_width, panel_height), 2, border_radius=5)
        screen.blit(surface, (panel_x, panel_y))

        # 日志标题
        title = font.render("战斗日志", True, COLORS['gold'])
        screen.blit(title, (panel_x + 10, panel_y + 5))

        # 日志内容
        for i, log in enumerate(self.battle_log[-5:]):
            text = font.render(log[:35], True, COLORS['white'])
            screen.blit(text, (panel_x + 10, panel_y + 25 + i * 20))

    def _draw_result(self, screen):
        """绘制战斗结果"""
        # 遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # 结果面板
        panel_width = 400
        panel_height = 250
        panel_x = (WINDOW_WIDTH - panel_width) // 2
        panel_y = (WINDOW_HEIGHT - panel_height) // 2

        pygame.draw.rect(screen, COLORS['panel_bg'], (panel_x, panel_y, panel_width, panel_height), border_radius=15)
        pygame.draw.rect(screen, COLORS['gold'], (panel_x, panel_y, panel_width, panel_height), 3, border_radius=15)

        # 结果文字
        font = self.resource_loader.get_font('title')
        if self.battle_result['winner'] == 'attacker':
            result_text = "战斗胜利！"
            color = COLORS['gold']
        else:
            result_text = "战斗失败"
            color = COLORS['red']

        title = font.render(result_text, True, color)
        title_rect = title.get_rect(centerx=WINDOW_WIDTH // 2, centery=panel_y + 60)
        screen.blit(title, title_rect)

        # 详细信息
        info_font = self.resource_loader.get_font('large')
        reason = self.battle_result.get('reason', '')
        reason_text = info_font.render(f"原因: {reason}", True, COLORS['white'])
        reason_rect = reason_text.get_rect(centerx=WINDOW_WIDTH // 2, centery=panel_y + 120)
        screen.blit(reason_text, reason_rect)

        # 提示
        hint_font = self.resource_loader.get_font('default')
        hint = hint_font.render("点击「确认」返回地图", True, COLORS['light_gray'])
        hint_rect = hint.get_rect(centerx=WINDOW_WIDTH // 2, centery=panel_y + 180)
        screen.blit(hint, hint_rect)