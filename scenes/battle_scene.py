"""
战斗场景
"""
import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT
from ui.button import Button
from ui.panel import Panel


class BattleScene:
    """战斗场景类"""

    def __init__(self, game_manager, attacker=None, defender=None, city=None):
        """初始化战斗场景"""
        self.game_manager = game_manager
        self.resource_loader = game_manager.resource_loader

        # 战斗参数
        self.attacker = attacker
        self.defender = defender
        self.city = city

        # 战斗状态
        self.battle_time = 0
        self.battle_paused = False
        self.battle_result = None

        # 创建UI
        self._create_ui()

    def _create_ui(self):
        """创建UI元素"""
        self.buttons = {
            'pause': Button(10, 10, 80, 35, "暂停", self._on_pause),
            'speed_up': Button(100, 10, 80, 35, "加速", self._on_speed_up),
            'retreat': Button(190, 10, 80, 35, "撤退", self._on_retreat),
            'auto': Button(280, 10, 80, 35, "自动", self._on_auto),
        }

    def _on_pause(self):
        """暂停/继续"""
        self.battle_paused = not self.battle_paused
        self.buttons['pause'].text = "继续" if self.battle_paused else "暂停"

    def _on_speed_up(self):
        """加速"""
        print("战斗加速")

    def _on_retreat(self):
        """撤退"""
        self.game_manager.scene_manager.load_scene('map')

    def _on_auto(self):
        """自动战斗"""
        print("自动战斗模式")

    def handle_event(self, event):
        """处理事件"""
        for button in self.buttons.values():
            button.handle_event(event)

    def update(self):
        """更新战斗状态"""
        if not self.battle_paused:
            self.battle_time += 1

    def render(self, screen):
        """渲染战斗场景"""
        # 背景
        screen.fill((50, 80, 50))

        # 绘制战场
        self._draw_battlefield(screen)

        # 绘制UI
        for button in self.buttons.values():
            button.render(screen, self.resource_loader)

        # 绘制战斗信息
        self._draw_battle_info(screen)

    def _draw_battlefield(self, screen):
        """绘制战场"""
        # 绘制简化的战场
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2

        # 攻方区域（左侧）
        pygame.draw.rect(screen, (100, 50, 50), (50, 100, 300, 400), border_radius=10)

        # 守方区域（右侧）
        pygame.draw.rect(screen, (50, 50, 100), (WINDOW_WIDTH - 350, 100, 300, 400), border_radius=10)

        # 中央战场
        pygame.draw.rect(screen, (80, 80, 50), (center_x - 200, 150, 400, 300), border_radius=10)

        # 绘制势力标签
        font = self.resource_loader.get_font('large')
        if self.attacker:
            attacker_text = font.render(f"攻方: {self.attacker}", True, COLORS['white'])
            screen.blit(attacker_text, (70, 110))

        if self.defender:
            defender_text = font.render(f"守方: {self.defender}", True, COLORS['white'])
            screen.blit(defender_text, (WINDOW_WIDTH - 330, 110))

    def _draw_battle_info(self, screen):
        """绘制战斗信息"""
        font = self.resource_loader.get_font('default')

        # 战斗时间
        minutes = self.battle_time // 3600
        seconds = (self.battle_time // 60) % 60
        time_text = font.render(f"战斗时间: {minutes:02d}:{seconds:02d}", True, COLORS['white'])
        screen.blit(time_text, (WINDOW_WIDTH // 2 - 60, 20))