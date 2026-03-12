"""
三国霸业游戏配置文件
"""
import os

# 窗口设置
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "三国霸业"
FPS = 60

# 版本信息
VERSION = "0.4.0"

# 颜色定义
COLORS = {
    'background': (20, 30, 40),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gold': (255, 215, 0),
    'red': (200, 50, 50),
    'blue': (50, 100, 200),
    'green': (50, 150, 50),
    'yellow': (200, 180, 50),
    'purple': (150, 50, 200),
    'orange': (200, 120, 50),
    'gray': (100, 100, 100),
    'dark_gray': (50, 50, 50),
    'light_gray': (150, 150, 150),
    'panel_bg': (40, 50, 60),
    'panel_border': (80, 90, 100),
    'button_normal': (60, 80, 100),
    'button_hover': (80, 100, 130),
    'button_pressed': (40, 60, 80),
}

# 势力颜色
FACTION_COLORS = {
    '魏': (0, 100, 200),
    '蜀': (200, 50, 50),
    '吴': (50, 150, 50),
    '袁绍': (180, 150, 100),
    '袁术': (150, 100, 180),
    '刘表': (100, 150, 200),
    '马腾': (200, 150, 50),
    '公孙瓒': (150, 200, 200),
    '吕布': (200, 100, 150),
    '董卓': (100, 50, 50),
}

# 字体设置
FONT_SIZE_SMALL = 16
FONT_SIZE_NORMAL = 20
FONT_SIZE_LARGE = 28
FONT_SIZE_TITLE = 48

# 资源路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 游戏设置
MAP_SCROLL_SPEED = 10
MAP_ZOOM_MIN = 0.5
MAP_ZOOM_MAX = 2.0
MAP_ZOOM_STEP = 0.1

# 武将属性范围
GENERAL_ATTR_MIN = 1
GENERAL_ATTR_MAX = 100

# 军队设置
ARMY_BASE_MOVE_SPEED = 5

# 资源设置
RESOURCE_TICK = 60  # 资源增长间隔（秒）

# 音效设置
SOUND_ENABLED = True
MUSIC_VOLUME = 0.7
SFX_VOLUME = 1.0
MASTER_VOLUME = 1.0