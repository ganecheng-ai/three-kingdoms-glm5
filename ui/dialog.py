"""
对话框UI组件
"""
import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT
from ui.button import Button


class Dialog:
    """对话框类"""

    def __init__(self, title, message, buttons=None):
        """初始化对话框

        Args:
            title: 标题
            message: 消息内容
            buttons: 按钮列表 [(文本, 回调), ...]
        """
        self.title = title
        self.message = message
        self.visible = False

        # 对话框尺寸
        self.width = 400
        self.height = 200
        self.x = (WINDOW_WIDTH - self.width) // 2
        self.y = (WINDOW_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # 按钮
        self.buttons = []
        if buttons:
            button_width = 100
            button_height = 35
            total_width = len(buttons) * button_width + (len(buttons) - 1) * 20
            start_x = self.x + (self.width - total_width) // 2

            for i, (text, callback) in enumerate(buttons):
                btn_x = start_x + i * (button_width + 20)
                btn_y = self.y + self.height - 50
                self.buttons.append(Button(btn_x, btn_y, button_width, button_height, text, callback))

    def show(self):
        """显示对话框"""
        self.visible = True

    def hide(self):
        """隐藏对话框"""
        self.visible = False

    def handle_event(self, event):
        """处理事件"""
        if not self.visible:
            return

        for button in self.buttons:
            button.handle_event(event)

    def render(self, screen, resource_loader):
        """渲染对话框"""
        if not self.visible:
            return

        # 绘制遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        # 绘制对话框背景
        pygame.draw.rect(screen, COLORS['panel_bg'], self.rect, border_radius=10)
        pygame.draw.rect(screen, COLORS['gold'], self.rect, 3, border_radius=10)

        # 绘制标题
        font = resource_loader.get_font('large')
        title_surface = font.render(self.title, True, COLORS['gold'])
        title_rect = title_surface.get_rect(centerx=self.rect.centerx, top=self.rect.top + 15)
        screen.blit(title_surface, title_rect)

        # 绘制消息
        msg_font = resource_loader.get_font('default')
        msg_surface = msg_font.render(self.message, True, COLORS['white'])
        msg_rect = msg_surface.get_rect(centerx=self.rect.centerx, centery=self.rect.centery)
        screen.blit(msg_surface, msg_rect)

        # 绘制按钮
        for button in self.buttons:
            button.render(screen, resource_loader)