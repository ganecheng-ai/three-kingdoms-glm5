"""
场景管理器 - 管理游戏中的各个场景
"""
from scenes.main_menu import MainMenuScene
from scenes.map_scene import MapScene
from scenes.battle_scene import BattleScene
from scenes.city_scene import CityScene
from scenes.settings_scene import SettingsScene


class SceneManager:
    """场景管理器类"""

    def __init__(self, game_manager):
        """初始化场景管理器"""
        self.game_manager = game_manager
        self.current_scene = None
        self.scenes = {}

        # 注册场景
        self._register_scenes()

    def _register_scenes(self):
        """注册所有场景"""
        self.scenes = {
            'main_menu': MainMenuScene,
            'map': MapScene,
            'battle': BattleScene,
            'city': CityScene,
            'settings': SettingsScene,
        }

    def load_scene(self, scene_name, **kwargs):
        """加载场景"""
        if scene_name in self.scenes:
            scene_class = self.scenes[scene_name]
            self.current_scene = scene_class(self.game_manager, **kwargs)
            return True
        return False

    def handle_event(self, event):
        """处理事件"""
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self):
        """更新当前场景"""
        if self.current_scene:
            self.current_scene.update()

    def render(self, screen):
        """渲染当前场景"""
        if self.current_scene:
            self.current_scene.render(screen)