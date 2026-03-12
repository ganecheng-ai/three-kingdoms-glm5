"""
音效管理器 - 管理游戏音效和背景音乐
"""
import os
import pygame
import random
from config import ASSETS_DIR


class SoundManager:
    """音效管理器类"""

    def __init__(self):
        """初始化音效管理器"""
        # 初始化音频系统
        self.audio_available = False
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                self.audio_available = True
            except pygame.error:
                # 音频设备不可用，使用静默模式
                self.audio_available = False
        else:
            self.audio_available = True

        self.sounds_dir = os.path.join(ASSETS_DIR, 'sounds')
        self.music_dir = os.path.join(ASSETS_DIR, 'music')

        # 确保目录存在
        os.makedirs(self.sounds_dir, exist_ok=True)
        os.makedirs(self.music_dir, exist_ok=True)

        # 音效缓存
        self.sounds = {}

        # 音量设置
        self.master_volume = 1.0
        self.music_volume = 0.7
        self.sfx_volume = 1.0

        # 当前播放的音乐
        self.current_music = None
        self.music_playlist = []

        # 是否静音
        self.muted = False

        # 加载音效
        self._load_sounds()

    def _load_sounds(self):
        """加载所有音效"""
        # 定义游戏需要的音效
        sound_files = {
            # UI音效
            'click': 'click.wav',
            'hover': 'hover.wav',
            'confirm': 'confirm.wav',
            'cancel': 'cancel.wav',

            # 游戏音效
            'battle_start': 'battle_start.wav',
            'attack': 'attack.wav',
            'defend': 'defend.wav',
            'victory': 'victory.wav',
            'defeat': 'defeat.wav',

            # 内政音效
            'recruit': 'recruit.wav',
            'build': 'build.wav',
            'gold': 'gold.wav',

            # 系统音效
            'save': 'save.wav',
            'load': 'load.wav',
            'turn_end': 'turn_end.wav',
            'message': 'message.wav',
        }

        for name, filename in sound_files.items():
            self.load_sound(name, filename)

    def load_sound(self, name, filename):
        """加载单个音效

        Args:
            name: 音效名称
            filename: 文件名
        """
        if not self.audio_available:
            self.sounds[name] = None
            return

        filepath = os.path.join(self.sounds_dir, filename)
        try:
            if os.path.exists(filepath):
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(self.sfx_volume * self.master_volume)
                self.sounds[name] = sound
            else:
                # 创建一个静默的占位音效
                self.sounds[name] = None
        except Exception:
            self.sounds[name] = None

    def play(self, sound_name):
        """播放音效

        Args:
            sound_name: 音效名称
        """
        if self.muted or not self.audio_available:
            return

        sound = self.sounds.get(sound_name)
        if sound:
            try:
                sound.set_volume(self.sfx_volume * self.master_volume)
                sound.play()
            except Exception as e:
                pass  # 静默处理音频播放错误

    def play_random(self, sound_names):
        """随机播放一个音效

        Args:
            sound_names: 音效名称列表
        """
        if sound_names:
            self.play(random.choice(sound_names))

    def play_music(self, filename, loops=-1):
        """播放背景音乐

        Args:
            filename: 音乐文件名
            loops: 循环次数，-1表示无限循环
        """
        if self.muted or not self.audio_available:
            return

        filepath = os.path.join(self.music_dir, filename)
        try:
            if os.path.exists(filepath):
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
                pygame.mixer.music.play(loops)
                self.current_music = filename
        except Exception:
            pass  # 静默处理音频播放错误

    def stop_music(self, fade_out_ms=1000):
        """停止背景音乐

        Args:
            fade_out_ms: 淡出时间（毫秒）
        """
        try:
            if fade_out_ms > 0:
                pygame.mixer.music.fadeout(fade_out_ms)
            else:
                pygame.mixer.music.stop()
            self.current_music = None
        except Exception:
            pass

    def pause_music(self):
        """暂停背景音乐"""
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass

    def resume_music(self):
        """恢复背景音乐"""
        if self.muted:
            return
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass

    def set_music_volume(self, volume):
        """设置音乐音量

        Args:
            volume: 音量 (0.0 - 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        except Exception:
            pass

    def set_sfx_volume(self, volume):
        """设置音效音量

        Args:
            volume: 音量 (0.0 - 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.sfx_volume * self.master_volume)

    def set_master_volume(self, volume):
        """设置主音量

        Args:
            volume: 音量 (0.0 - 1.0)
        """
        self.master_volume = max(0.0, min(1.0, volume))
        self.set_music_volume(self.music_volume)
        self.set_sfx_volume(self.sfx_volume)

    def toggle_mute(self):
        """切换静音状态"""
        self.muted = not self.muted
        if self.muted:
            self.stop_music(0)
        else:
            if self.current_music:
                self.play_music(self.current_music)
        return self.muted

    def is_music_playing(self):
        """检查音乐是否正在播放"""
        return pygame.mixer.music.get_busy()

    def play_scene_music(self, scene_name):
        """根据场景播放对应的背景音乐

        Args:
            scene_name: 场景名称
        """
        music_map = {
            'main_menu': 'menu_theme.ogg',
            'map': 'map_theme.ogg',
            'battle': 'battle_theme.ogg',
            'city': 'city_theme.ogg',
        }

        music_file = music_map.get(scene_name)
        if music_file:
            if self.current_music != music_file:
                self.stop_music(500)
                self.play_music(music_file)

    def cleanup(self):
        """清理资源"""
        self.stop_music()
        self.sounds.clear()
        self.current_music = None


# 全局音效管理器实例
_sound_manager = None


def get_sound_manager():
    """获取全局音效管理器实例"""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager