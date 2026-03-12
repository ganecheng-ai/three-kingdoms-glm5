"""
按钮UI组件
"""
import pygame
from config import COLORS


class Button:
    """按钮类"""

    def __init__(self, x, y, width, height, text, callback=None):
        """初始化按钮

        Args:
            x: X坐标
            y: Y坐标
            width: 宽度
            height: 高度
            text: 按钮文本
            callback: 点击回调函数
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

        # 按钮状态
        self.hovered = False
        self.pressed = False
        self.enabled = True

        # 颜色
        self.color = COLORS['button_normal']
        self.hover_color = COLORS['button_hover']
        self.pressed_color = COLORS['button_pressed']
        self.disabled_color = COLORS['gray']

    def handle_event(self, event):
        """处理事件"""
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed and self.hovered:
                self.pressed = False
                if self.callback:
                    self.callback()
            self.pressed = False

    def update(self):
        """更新按钮状态"""
        pass

    def render(self, screen, resource_loader):
        """渲染按钮"""
        # 确定颜色
        if not self.enabled:
            color = self.disabled_color
        elif self.pressed:
            color = self.pressed_color
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.color

        # 绘制按钮背景
        pygame.draw.rect(screen, color, self.rect, border_radius=5)

        # 绘制边框
        border_color = COLORS['gold'] if self.hovered else COLORS['panel_border']
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=5)

        # 绘制文本
        font = resource_loader.get_font('default')
        text_surface = font.render(self.text, True, COLORS['white'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)