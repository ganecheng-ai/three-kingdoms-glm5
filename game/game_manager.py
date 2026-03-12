"""
游戏管理器 - 管理游戏的核心逻辑和状态
"""
import pygame
from config import COLORS, SOUND_ENABLED
from game.scene_manager import SceneManager
from game.resource_loader import ResourceLoader
from game.sound_manager import get_sound_manager


class GameManager:
    """游戏管理器类"""

    def __init__(self, screen):
        """初始化游戏管理器"""
        self.screen = screen
        self.running = True

        # 共享数据存储（用于场景间数据传递）
        self.shared_data = {}

        # 初始化资源加载器
        self.resource_loader = ResourceLoader()

        # 初始化音效管理器
        if SOUND_ENABLED:
            self.sound_manager = get_sound_manager()
        else:
            self.sound_manager = None

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
        if self.sound_manager:
            self.sound_manager.cleanup()

    def quit_game(self):
        """退出游戏"""
        self.running = False

    def play_sound(self, sound_name):
        """播放音效"""
        if self.sound_manager:
            self.sound_manager.play(sound_name)

    def play_scene_music(self, scene_name):
        """播放场景音乐"""
        if self.sound_manager:
            self.sound_manager.play_scene_music(scene_name)

    def set_shared_data(self, key, value):
        """设置共享数据"""
        self.shared_data[key] = value

    def get_shared_data(self, key, default=None):
        """获取共享数据"""
        return self.shared_data.get(key, default)