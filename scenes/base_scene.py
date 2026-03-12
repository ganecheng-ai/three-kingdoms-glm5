"""
场景基类 - 提供场景类的公共接口和通用功能
"""
from abc import ABC, abstractmethod
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from utils.logger import get_logger


class BaseScene(ABC):
    """场景基类，定义场景的公共接口和通用功能"""

    def __init__(self, game_manager):
        """初始化场景基类

        Args:
            game_manager: 游戏管理器实例
        """
        self.game_manager = game_manager
        self.resource_loader = game_manager.resource_loader
        self.logger = get_logger()
        self._background_cache = None

    @abstractmethod
    def handle_event(self, event):
        """处理事件

        Args:
            event: pygame事件对象
        """
        pass

    @abstractmethod
    def update(self):
        """更新场景状态"""
        pass

    @abstractmethod
    def render(self, screen):
        """渲染场景

        Args:
            screen: pygame屏幕对象
        """
        pass

    def _draw_gradient_background(self, screen, color_start=(20, 30, 60), color_end=(50, 45, 80)):
        """绘制渐变背景（带缓存）

        Args:
            screen: pygame屏幕对象
            color_start: 起始颜色 (R, G, B)
            color_end: 结束颜色 (R, G, B)
        """
        if self._background_cache is None:
            self._background_cache = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            for y in range(WINDOW_HEIGHT):
                ratio = y / WINDOW_HEIGHT
                r = int(color_start[0] + ratio * (color_end[0] - color_start[0]))
                g = int(color_start[1] + ratio * (color_end[1] - color_start[1]))
                b = int(color_start[2] + ratio * (color_end[2] - color_start[2]))
                pygame.draw.line(self._background_cache, (r, g, b), (0, y), (WINDOW_WIDTH, y))

        screen.blit(self._background_cache, (0, 0))

    def invalidate_cache(self):
        """使缓存失效，强制重新渲染背景"""
        self._background_cache = None