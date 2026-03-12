"""
游戏管理器 - 管理游戏的核心逻辑和状态
"""
import pygame
from config import COLORS
from game.scene_manager import SceneManager
from game.resource_loader import ResourceLoader


class GameManager:
    """游戏管理器类"""

    def __init__(self, screen):
        """初始化游戏管理器"""
        self.screen = screen
        self.running = True

        # 初始化资源加载器
        self.resource_loader = ResourceLoader()

        # 初始化场景管理器
        self.scene_manager = SceneManager(self)

        # 加载初始场景（主菜单）
        self.scene_manager.load_scene('main_menu')

    def handle_event(self, event):
        """处理事件"""
        self.scene_manager.handle_event(event)

    def update(self):
        """更新游戏状态"""
        self.scene_manager.update()

    def render(self):
        """渲染游戏画面"""
        self.scene_manager.render(self.screen)

    def cleanup(self):
        """清理资源"""
        self.resource_loader.cleanup()

    def quit_game(self):
        """退出游戏"""
        self.running = False