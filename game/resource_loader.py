"""
资源加载器 - 管理游戏资源的加载和缓存
"""
import os
import pygame
from config import ASSETS_DIR, DATA_DIR, FONT_SIZE_NORMAL
from utils.logger import get_logger

logger = get_logger()


class ResourceLoader:
    """资源加载器类"""

    def __init__(self):
        """初始化资源加载器"""
        self.images = {}
        self.fonts = {}
        self.sounds = {}
        self.data = {}

        # 加载默认字体
        self._load_default_fonts()

    def _load_default_fonts(self):
        """加载默认字体"""
        # 尝试加载系统中文字体
        font_names = [
            'SimHei',  # 黑体
            'Microsoft YaHei',  # 微软雅黑
            'PingFang SC',  # 苹方
            'WenQuanYi Micro Hei',  # 文泉驿
            'Noto Sans CJK SC',  # Noto中文字体
        ]

        font_loaded = False
        for font_name in font_names:
            try:
                self.fonts['default'] = pygame.font.SysFont(font_name, FONT_SIZE_NORMAL)
                self.fonts['small'] = pygame.font.SysFont(font_name, 16)
                self.fonts['large'] = pygame.font.SysFont(font_name, 28)
                self.fonts['title'] = pygame.font.SysFont(font_name, 48)
                font_loaded = True
                logger.info(f"成功加载字体: {font_name}")
                break
            except Exception as e:
                logger.debug(f"无法加载字体 {font_name}: {e}")
                continue

        if not font_loaded:
            # 使用默认字体
            self.fonts['default'] = pygame.font.Font(None, FONT_SIZE_NORMAL)
            self.fonts['small'] = pygame.font.Font(None, 16)
            self.fonts['large'] = pygame.font.Font(None, 28)
            self.fonts['title'] = pygame.font.Font(None, 48)

    def load_image(self, name, path):
        """加载图片"""
        if name not in self.images:
            full_path = os.path.join(ASSETS_DIR, 'images', path)
            try:
                image = pygame.image.load(full_path).convert_alpha()
                self.images[name] = image
            except FileNotFoundError:
                logger.warning(f"图片文件未找到: {full_path}")
                # 创建一个占位图片
                self.images[name] = self._create_placeholder(name)
        return self.images[name]

    def _create_placeholder(self, name):
        """创建占位图片"""
        surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        surface.fill((100, 100, 100, 200))
        return surface

    def get_font(self, name='default'):
        """获取字体"""
        return self.fonts.get(name, self.fonts['default'])

    def load_sound(self, name, path):
        """加载音效"""
        if name not in self.sounds:
            full_path = os.path.join(ASSETS_DIR, 'sounds', path)
            try:
                sound = pygame.mixer.Sound(full_path)
                self.sounds[name] = sound
            except FileNotFoundError:
                logger.warning(f"音效文件未找到: {full_path}")
                return None
        return self.sounds.get(name)

    def cleanup(self):
        """清理资源"""
        self.images.clear()
        self.sounds.clear()
        self.data.clear()