"""
主菜单场景
"""
import pygame
import math
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, VERSION
from ui.button import Button
from ui.panel import Panel
from game.game_state import GameState


class MainMenuScene:
    """主菜单场景类"""

    def __init__(self, game_manager):
        """初始化主菜单场景"""
        self.game_manager = game_manager
        self.resource_loader = game_manager.resource_loader
        self.game_state = GameState(game_manager)

        # 动画相关
        self.animation_time = 0
        self.title_y_offset = 0

        # 粒子效果
        self.particles = []
        self._init_particles()

        # 存档选择状态
        self.showing_saves = False
        self.save_slots = []
        self.selected_slot = None

        # 创建UI元素
        self._create_ui()

    def _init_particles(self):
        """初始化粒子效果"""
        import random
        for _ in range(50):
            self.particles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, WINDOW_HEIGHT),
                'speed': random.uniform(0.5, 2),
                'size': random.randint(1, 3),
                'alpha': random.randint(50, 150),
            })

    def _create_ui(self):
        """创建UI元素"""
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2

        # 主菜单按钮
        button_width = 220
        button_height = 55
        button_x = center_x - button_width // 2

        self.main_buttons = {
            'new_game': Button(
                button_x, center_y + 20, button_width, button_height,
                "开始新游戏", self._on_new_game
            ),
            'load_game': Button(
                button_x, center_y + 90, button_width, button_height,
                "读取存档", self._on_load_game
            ),
            'quit': Button(
                button_x, center_y + 160, button_width, button_height,
                "退出游戏", self._on_quit
            ),
        }

        # 存档选择按钮
        self.save_buttons = {}
        for i in range(5):
            self.save_buttons[i + 1] = Button(
                center_x - 150, 200 + i * 70, 300, 55,
                f"存档 {i + 1} - 空", lambda slot=i + 1: self._on_select_save(slot)
            )

        self.back_button = Button(
            center_x - 100, WINDOW_HEIGHT - 80, 200, 45,
            "返回", self._on_back
        )

        self.confirm_button = Button(
            center_x + 120, WINDOW_HEIGHT - 80, 150, 45,
            "确认读取", self._on_confirm_load
        )

    def _on_new_game(self):
        """新游戏按钮回调"""
        # 播放确认音效
        self.game_manager.play_sound('confirm')
        # 初始化新游戏
        self.game_manager.scene_manager.load_scene('map', new_game=True)

    def _on_load_game(self):
        """读取游戏按钮回调"""
        # 播放点击音效
        self.game_manager.play_sound('click')
        self.showing_saves = True
        self._refresh_save_slots()

    def _refresh_save_slots(self):
        """刷新存档槽位显示"""
        saves = self.game_state.list_saves()
        for i, save_info in enumerate(saves):
            slot = i + 1
            if save_info:
                self.save_buttons[slot].text = f"存档 {slot}: {save_info['player_faction']} - 第{save_info['turn']}回合"
            else:
                self.save_buttons[slot].text = f"存档 {slot} - 空"

    def _on_select_save(self, slot):
        """选择存档槽位"""
        self.selected_slot = slot
        for s, btn in self.save_buttons.items():
            if s == slot:
                btn.color = COLORS['gold']
            else:
                btn.color = COLORS['button_normal']

    def _on_confirm_load(self):
        """确认读取存档"""
        if self.selected_slot:
            data = self.game_state.load_game(self.selected_slot)
            if data:
                self.game_manager.play_sound('load')
                self.game_manager.scene_manager.load_scene('map', save_data=data)
                self.showing_saves = False

    def _on_back(self):
        """返回主菜单"""
        self.game_manager.play_sound('cancel')
        self.showing_saves = False
        self.selected_slot = None

    def _on_quit(self):
        """退出游戏按钮回调"""
        self.game_manager.play_sound('cancel')
        self.game_manager.quit_game()

    def handle_event(self, event):
        """处理事件"""
        if self.showing_saves:
            for button in self.save_buttons.values():
                button.handle_event(event)
            self.back_button.handle_event(event)
            self.confirm_button.handle_event(event)
        else:
            for button in self.main_buttons.values():
                button.handle_event(event)

    def update(self):
        """更新场景"""
        # 更新动画
        self.animation_time += 1
        self.title_y_offset = math.sin(self.animation_time * 0.03) * 5

        # 更新粒子
        for p in self.particles:
            p['y'] -= p['speed']
            if p['y'] < 0:
                p['y'] = WINDOW_HEIGHT
                p['x'] = p['x'] % WINDOW_WIDTH

        # 更新按钮
        if self.showing_saves:
            for button in self.save_buttons.values():
                button.update()
            self.back_button.update()
            self.confirm_button.update()
        else:
            for button in self.main_buttons.values():
                button.update()

    def render(self, screen):
        """渲染场景"""
        # 绘制背景
        self._draw_background(screen)

        # 绘制粒子
        self._draw_particles(screen)

        if self.showing_saves:
            # 绘制存档选择界面
            self._draw_save_selection(screen)
        else:
            # 绘制主菜单
            self._draw_main_menu(screen)

        # 绘制版本信息
        self._draw_version(screen)

    def _draw_background(self, screen):
        """绘制背景"""
        # 创建渐变背景
        for y in range(WINDOW_HEIGHT):
            # 从深蓝到深紫的渐变
            ratio = y / WINDOW_HEIGHT
            r = int(20 + ratio * 30)
            g = int(30 + ratio * 15)
            b = int(60 + ratio * 20)
            pygame.draw.line(screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

        # 绘制装饰性线条
        for i in range(5):
            y = 100 + i * 150
            alpha = 30 + int(20 * math.sin(self.animation_time * 0.02 + i))
            for x in range(0, WINDOW_WIDTH, 20):
                pygame.draw.circle(screen, (255, 215, 0), (x, y), 1)

    def _draw_particles(self, screen):
        """绘制粒子效果"""
        for p in self.particles:
            color = (255, 215, 0)
            pygame.draw.circle(screen, color, (int(p['x']), int(p['y'])), p['size'])

    def _draw_main_menu(self, screen):
        """绘制主菜单"""
        center_x = WINDOW_WIDTH // 2

        # 绘制标题
        title_font = self.resource_loader.get_font('title')

        # 标题阴影
        shadow_text = title_font.render("三国霸业", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(centerx=center_x + 3, centery=130 + 3 + self.title_y_offset)
        screen.blit(shadow_text, shadow_rect)

        # 标题文字
        title_text = title_font.render("三国霸业", True, COLORS['gold'])
        title_rect = title_text.get_rect(centerx=center_x, centery=130 + self.title_y_offset)
        screen.blit(title_text, title_rect)

        # 绘制副标题
        subtitle_font = self.resource_loader.get_font('large')
        subtitle_text = subtitle_font.render("经典策略游戏", True, COLORS['light_gray'])
        subtitle_rect = subtitle_text.get_rect(centerx=center_x, centery=180 + self.title_y_offset)
        screen.blit(subtitle_text, subtitle_rect)

        # 绘制装饰边框
        border_y = 250
        pygame.draw.line(screen, COLORS['gold'], (center_x - 200, border_y), (center_x - 50, border_y), 2)
        pygame.draw.line(screen, COLORS['gold'], (center_x + 50, border_y), (center_x + 200, border_y), 2)
        pygame.draw.circle(screen, COLORS['gold'], (center_x, border_y), 8)

        # 绘制按钮
        for button in self.main_buttons.values():
            button.render(screen, self.resource_loader)

    def _draw_save_selection(self, screen):
        """绘制存档选择界面"""
        center_x = WINDOW_WIDTH // 2

        # 绘制标题
        title_font = self.resource_loader.get_font('title')
        title_text = title_font.render("选择存档", True, COLORS['gold'])
        title_rect = title_text.get_rect(centerx=center_x, top=50)
        screen.blit(title_text, title_rect)

        # 绘制存档按钮
        for slot, button in self.save_buttons.items():
            button.render(screen, self.resource_loader)

        # 绘制底部按钮
        self.back_button.render(screen, self.resource_loader)
        self.confirm_button.render(screen, self.resource_loader)

    def _draw_version(self, screen):
        """绘制版本信息"""
        font = self.resource_loader.get_font('small')
        version_text = font.render(f"v{VERSION}", True, COLORS['light_gray'])
        screen.blit(version_text, (WINDOW_WIDTH - 60, WINDOW_HEIGHT - 30))