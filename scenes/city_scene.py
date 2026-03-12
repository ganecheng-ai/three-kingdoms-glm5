"""
城市场景 - 城市管理界面
"""
import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT
from ui.button import Button
from ui.panel import Panel


class CityScene:
    """城市场景类"""

    def __init__(self, game_manager, city_name=None):
        """初始化城市场景"""
        self.game_manager = game_manager
        self.resource_loader = game_manager.resource_loader
        self.city_name = city_name

        # 当前选中的标签页
        self.current_tab = 'overview'

        # 创建UI
        self._create_ui()

    def _create_ui(self):
        """创建UI元素"""
        # 返回按钮
        self.buttons = {
            'back': Button(10, 10, 80, 35, "返回", self._on_back),
        }

        # 标签页按钮
        tab_y = 60
        self.tab_buttons = {
            'overview': Button(100, tab_y, 100, 35, "概览", lambda: self._switch_tab('overview')),
            'generals': Button(210, tab_y, 100, 35, "武将", lambda: self._switch_tab('generals')),
            'army': Button(320, tab_y, 100, 35, "军队", lambda: self._switch_tab('army')),
            'buildings': Button(430, tab_y, 100, 35, "建筑", lambda: self._switch_tab('buildings')),
        }

    def _on_back(self):
        """返回地图"""
        self.game_manager.scene_manager.load_scene('map')

    def _switch_tab(self, tab_name):
        """切换标签页"""
        self.current_tab = tab_name

    def handle_event(self, event):
        """处理事件"""
        for button in self.buttons.values():
            button.handle_event(event)
        for button in self.tab_buttons.values():
            button.handle_event(event)

    def update(self):
        """更新场景"""
        for button in self.buttons.values():
            button.update()
        for button in self.tab_buttons.values():
            button.update()

    def render(self, screen):
        """渲染场景"""
        # 背景
        screen.fill(COLORS['background'])

        # 绘制城市名称
        font = self.resource_loader.get_font('title')
        title = font.render(self.city_name or "城市管理", True, COLORS['gold'])
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 10))

        # 绘制按钮
        for button in self.buttons.values():
            button.render(screen, self.resource_loader)

        # 绘制标签页
        for name, button in self.tab_buttons.items():
            if name == self.current_tab:
                button.color = COLORS['gold']
            else:
                button.color = COLORS['button_normal']
            button.render(screen, self.resource_loader)

        # 根据标签页绘制内容
        if self.current_tab == 'overview':
            self._render_overview(screen)
        elif self.current_tab == 'generals':
            self._render_generals(screen)
        elif self.current_tab == 'army':
            self._render_army(screen)
        elif self.current_tab == 'buildings':
            self._render_buildings(screen)

    def _render_overview(self, screen):
        """渲染概览页面"""
        font = self.resource_loader.get_font('default')

        info_lines = [
            "城市概览",
            "",
            "人口: 50,000",
            "金钱: 10,000",
            "粮草: 20,000",
            "兵员: 5,000",
            "",
            "税收: +500/月",
            "粮食产量: +1000/月",
        ]

        for i, line in enumerate(info_lines):
            text = font.render(line, True, COLORS['white'])
            screen.blit(text, (100, 120 + i * 30))

    def _render_generals(self, screen):
        """渲染武将页面"""
        font = self.resource_loader.get_font('default')

        info_lines = [
            "武将列表",
            "",
            "关羽 - 武力: 97 智力: 75 统率: 95",
            "张飞 - 武力: 98 智力: 45 统率: 70",
            "赵云 - 武力: 96 智力: 76 统率: 88",
        ]

        for i, line in enumerate(info_lines):
            text = font.render(line, True, COLORS['white'])
            screen.blit(text, (100, 120 + i * 30))

    def _render_army(self, screen):
        """渲染军队页面"""
        font = self.resource_loader.get_font('default')

        info_lines = [
            "军队管理",
            "",
            "步兵: 3,000",
            "骑兵: 1,500",
            "弓兵: 500",
            "",
            "总兵力: 5,000",
        ]

        for i, line in enumerate(info_lines):
            text = font.render(line, True, COLORS['white'])
            screen.blit(text, (100, 120 + i * 30))

    def _render_buildings(self, screen):
        """渲染建筑页面"""
        font = self.resource_loader.get_font('default')

        info_lines = [
            "建筑管理",
            "",
            "农田 Lv.3 - 产量: +1000/月",
            "市场 Lv.2 - 税收: +300/月",
            "兵营 Lv.2 - 招募: +100/月",
            "城墙 Lv.1 - 防御: +10%",
        ]

        for i, line in enumerate(info_lines):
            text = font.render(line, True, COLORS['white'])
            screen.blit(text, (100, 120 + i * 30))