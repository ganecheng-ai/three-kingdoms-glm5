"""
面板UI组件
"""
import pygame
from config import COLORS


class Panel:
    """面板类"""

    def __init__(self, x, y, width, height, title=None):
        """初始化面板

        Args:
            x: X坐标
            y: Y坐标
            width: 宽度
            height: 高度
            title: 标题（可选）
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title

        # 颜色
        self.bg_color = (*COLORS['panel_bg'], 230)  # 带透明度
        self.border_color = COLORS['panel_border']
        self.title_color = COLORS['gold']

    def render(self, screen, resource_loader):
        """渲染面板"""
        # 创建半透明表面
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.bg_color,
                         (0, 0, self.rect.width, self.rect.height), border_radius=8)

        # 绘制到屏幕
        screen.blit(surface, self.rect.topleft)

        # 绘制边框
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=8)

        # 绘制标题
        if self.title:
            font = resource_loader.get_font('large')
            title_surface = font.render(self.title, True, self.title_color)
            title_rect = title_surface.get_rect(centerx=self.rect.centerx, top=self.rect.top + 10)
            screen.blit(title_surface, title_rect)