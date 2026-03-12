"""
主菜单场景
"""
import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT
from ui.button import Button
from ui.panel import Panel


class MainMenuScene:
    """主菜单场景类"""

    def __init__(self, game_manager):
        """初始化主菜单场景"""
        self.game_manager = game_manager
        self.resource_loader = game_manager.resource_loader

        # 创建UI元素
        self._create_ui()

    def _create_ui(self):
        """创建UI元素"""
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2

        # 标题面板
        self.title_panel = Panel(
            center_x - 200, 50, 400, 100,
            title="三国霸业"
        )

        # 菜单按钮
        button_width = 200
        button_height = 50
        button_x = center_x - button_width // 2

        self.buttons = {
            'new_game': Button(
                button_x, center_y, button_width, button_height,
                "新游戏", self._on_new_game
            ),
            'load_game': Button(
                button_x, center_y + 70, button_width, button_height,
                "读取游戏", self._on_load_game
            ),
            'settings': Button(
                button_x, center_y + 140, button_width, button_height,
                "设置", self._on_settings
            ),
            'quit': Button(
                button_x, center_y + 210, button_width, button_height,
                "退出游戏", self._on_quit
            ),
        }

    def _on_new_game(self):
        """新游戏按钮回调"""
        self.game_manager.scene_manager.load_scene('map')

    def _on_load_game(self):
        """读取游戏按钮回调"""
        print("加载游戏功能待实现")

    def _on_settings(self):
        """设置按钮回调"""
        print("设置功能待实现")

    def _on_quit(self):
        """退出游戏按钮回调"""
        self.game_manager.quit_game()

    def handle_event(self, event):
        """处理事件"""
        for button in self.buttons.values():
            button.handle_event(event)

    def update(self):
        """更新场景"""
        for button in self.buttons.values():
            button.update()

    def render(self, screen):
        """渲染场景"""
        # 绘制背景
        self._draw_background(screen)

        # 绘制标题
        self.title_panel.render(screen, self.resource_loader)

        # 绘制按钮
        for button in self.buttons.values():
            button.render(screen, self.resource_loader)

        # 绘制版本信息
        self._draw_version(screen)

    def _draw_background(self, screen):
        """绘制背景"""
        # 创建渐变背景
        for y in range(WINDOW_HEIGHT):
            # 从深蓝到深紫的渐变
            ratio = y / WINDOW_HEIGHT
            r = int(20 + ratio * 20)
            g = int(30 + ratio * 10)
            b = int(60 - ratio * 20)
            pygame.draw.line(screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

    def _draw_version(self, screen):
        """绘制版本信息"""
        font = self.resource_loader.get_font('small')
        version_text = font.render("v0.1.0", True, COLORS['light_gray'])
        screen.blit(version_text, (WINDOW_WIDTH - 60, WINDOW_HEIGHT - 30))