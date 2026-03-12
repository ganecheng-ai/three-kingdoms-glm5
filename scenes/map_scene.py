"""
地图场景 - 游戏主地图界面
"""
import pygame
import math
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, MAP_SCROLL_SPEED, MAP_ZOOM_MIN, MAP_ZOOM_MAX, MAP_ZOOM_STEP, FACTION_COLORS
from ui.button import Button
from ui.panel import Panel
from entities.city import City
from entities.general import General
from entities.faction import Faction
import json
import os


class MapScene:
    """地图场景类"""

    def __init__(self, game_manager):
        """初始化地图场景"""
        self.game_manager = game_manager
        self.resource_loader = game_manager.resource_loader

        # 地图状态
        self.map_offset_x = 0
        self.map_offset_y = 0
        self.map_zoom = 1.0
        self.dragging = False
        self.drag_start = (0, 0)
        self.drag_offset = (0, 0)

        # 选中的实体
        self.selected_city = None
        self.selected_army = None

        # 游戏数据
        self.factions = {}
        self.cities = {}
        self.generals = {}

        # 初始化游戏数据
        self._init_game_data()

        # 创建UI
        self._create_ui()

    def _init_game_data(self):
        """初始化游戏数据"""
        # 创建势力
        faction_data = [
            ('魏', '曹操', '许昌'),
            ('蜀', '刘备', '成都'),
            ('吴', '孙权', '建业'),
        ]

        for name, leader, capital in faction_data:
            self.factions[name] = Faction(name, leader, capital)

        # 创建城市
        city_data = [
            # 城市名, 势力, 人口, 金钱, 粮草, 兵员, x坐标, y坐标
            ('许昌', '魏', 50000, 10000, 20000, 5000, 600, 280),
            ('洛阳', '魏', 80000, 15000, 30000, 8000, 500, 220),
            ('邺城', '魏', 40000, 8000, 15000, 4000, 580, 150),
            ('成都', '蜀', 60000, 12000, 25000, 6000, 280, 380),
            ('汉中', '蜀', 30000, 6000, 12000, 3000, 320, 320),
            ('建业', '吴', 55000, 11000, 22000, 5500, 680, 420),
            ('柴桑', '吴', 35000, 7000, 14000, 3500, 600, 400),
            ('襄阳', '魏', 45000, 9000, 18000, 4500, 480, 350),
            ('江陵', '魏', 35000, 7000, 14000, 3500, 420, 380),
            ('长安', '魏', 70000, 14000, 28000, 7000, 380, 250),
        ]

        for data in city_data:
            name, faction, pop, gold, food, soldiers, x, y = data
            city = City(name, faction, pop, gold, food, soldiers, x, y)
            self.cities[name] = city
            if faction in self.factions:
                self.factions[faction].add_city(name)

        # 创建武将
        general_data = [
            # 武将名, 势力, 武力, 智力, 统率, 政治, 所在城市
            ('曹操', '魏', 72, 91, 96, 94, '许昌'),
            ('夏侯惇', '魏', 85, 55, 78, 45, '洛阳'),
            ('夏侯渊', '魏', 88, 50, 75, 42, '邺城'),
            ('张辽', '魏', 90, 68, 85, 55, '许昌'),
            ('许褚', '魏', 95, 35, 50, 30, '许昌'),
            ('刘备', '蜀', 65, 75, 80, 85, '成都'),
            ('关羽', '蜀', 97, 75, 95, 60, '成都'),
            ('张飞', '蜀', 98, 45, 70, 35, '汉中'),
            ('赵云', '蜀', 96, 76, 88, 55, '成都'),
            ('诸葛亮', '蜀', 38, 100, 95, 98, '成都'),
            ('孙权', '吴', 70, 85, 75, 90, '建业'),
            ('周瑜', '吴', 75, 96, 95, 80, '建业'),
            ('陆逊', '吴', 65, 95, 92, 88, '柴桑'),
            ('甘宁', '吴', 92, 48, 72, 35, '建业'),
            ('太史慈', '吴', 90, 62, 78, 50, '柴桑'),
        ]

        for data in general_data:
            name, faction, force, intel, command, politics, city = data
            general = General(name, faction, force, intel, command, politics, city)
            self.generals[name] = general
            if city in self.cities:
                self.cities[city].add_general(name)

    def _create_ui(self):
        """创建UI元素"""
        # 底部信息面板
        self.info_panel = Panel(10, WINDOW_HEIGHT - 120, 300, 110, title="信息")

        # 右侧控制面板
        self.control_panel = Panel(WINDOW_WIDTH - 220, 10, 210, 300, title="控制")

        # 控制按钮
        self.buttons = {
            'menu': Button(WINDOW_WIDTH - 210, 50, 90, 35, "菜单", self._on_menu),
            'end_turn': Button(WINDOW_WIDTH - 110, 50, 90, 35, "回合结束", self._on_end_turn),
        }

        # 缩放按钮
        self.zoom_in_btn = Button(WINDOW_WIDTH - 210, 100, 90, 35, "放大", self._on_zoom_in)
        self.zoom_out_btn = Button(WINDOW_WIDTH - 110, 100, 90, 35, "缩小", self._on_zoom_out)

    def _on_menu(self):
        """菜单按钮回调"""
        self.game_manager.scene_manager.load_scene('main_menu')

    def _on_end_turn(self):
        """回合结束按钮回调"""
        print("回合结束")
        # 更新资源等

    def _on_zoom_in(self):
        """放大地图"""
        self.map_zoom = min(MAP_ZOOM_MAX, self.map_zoom + MAP_ZOOM_STEP)

    def _on_zoom_out(self):
        """缩小地图"""
        self.map_zoom = max(MAP_ZOOM_MIN, self.map_zoom - MAP_ZOOM_STEP)

    def handle_event(self, event):
        """处理事件"""
        # 处理按钮事件
        for button in self.buttons.values():
            button.handle_event(event)
        self.zoom_in_btn.handle_event(event)
        self.zoom_out_btn.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键
                # 检查是否点击了城市
                self._check_city_click(event.pos)
            elif event.button == 3:  # 右键拖拽
                self.dragging = True
                self.drag_start = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                dx = event.pos[0] - self.drag_start[0]
                dy = event.pos[1] - self.drag_start[1]
                self.map_offset_x += dx
                self.map_offset_y += dy
                self.drag_start = event.pos

        elif event.type == pygame.MOUSEWHEEL:
            # 鼠标滚轮缩放
            if event.y > 0:
                self._on_zoom_in()
            else:
                self._on_zoom_out()

    def _check_city_click(self, pos):
        """检查是否点击了城市"""
        for city in self.cities.values():
            city_x = city.x * self.map_zoom + self.map_offset_x
            city_y = city.y * self.map_zoom + self.map_offset_y
            distance = math.sqrt((pos[0] - city_x) ** 2 + (pos[1] - city_y) ** 2)
            if distance < 30:
                self.selected_city = city
                print(f"选中城市: {city.name}")
                return

    def update(self):
        """更新场景"""
        for button in self.buttons.values():
            button.update()
        self.zoom_in_btn.update()
        self.zoom_out_btn.update()

    def render(self, screen):
        """渲染场景"""
        # 绘制地图背景
        self._draw_map_background(screen)

        # 绘制城市
        self._draw_cities(screen)

        # 绘制UI
        self._draw_ui(screen)

    def _draw_map_background(self, screen):
        """绘制地图背景"""
        # 绘制渐变背景模拟地图
        screen.fill((34, 85, 51))  # 深绿色

        # 绘制简化的地图轮廓（黄河、长江等）
        self._draw_river(screen)

        # 绘制势力区域
        self._draw_territories(screen)

    def _draw_river(self, screen):
        """绘制河流"""
        # 黄河
        river_points_yellow = [
            (100, 200), (200, 180), (350, 200), (500, 170),
            (650, 200), (750, 180), (850, 200)
        ]
        # 长江
        river_points_yangtze = [
            (50, 350), (150, 370), (280, 350), (400, 370),
            (550, 360), (700, 380), (850, 350)
        ]

        # 根据缩放和偏移调整坐标
        def transform_points(points):
            return [(int(p[0] * self.map_zoom + self.map_offset_x),
                     int(p[1] * self.map_zoom + self.map_offset_y)) for p in points]

        # 绘制黄河
        if len(river_points_yellow) > 1:
            pygame.draw.lines(screen, (100, 150, 200), False,
                              transform_points(river_points_yellow), 3)

        # 绘制长江
        if len(river_points_yangtze) > 1:
            pygame.draw.lines(screen, (80, 130, 180), False,
                              transform_points(river_points_yangtze), 4)

    def _draw_territories(self, screen):
        """绘制势力区域"""
        # 简化版：只绘制城市周围的区域
        for city in self.cities.values():
            if city.faction and city.faction in FACTION_COLORS:
                color = FACTION_COLORS[city.faction]
                x = int(city.x * self.map_zoom + self.map_offset_x)
                y = int(city.y * self.map_zoom + self.map_offset_y)
                # 绘制势力范围圆圈
                radius = int(50 * self.map_zoom)
                surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (*color, 50), (radius, radius), radius)
                screen.blit(surface, (x - radius, y - radius))

    def _draw_cities(self, screen):
        """绘制城市"""
        for city in self.cities.values():
            x = int(city.x * self.map_zoom + self.map_offset_x)
            y = int(city.y * self.map_zoom + self.map_offset_y)

            # 城市颜色
            if city.faction and city.faction in FACTION_COLORS:
                color = FACTION_COLORS[city.faction]
            else:
                color = COLORS['gray']

            # 绘制城市
            city_size = int(20 * self.map_zoom)

            # 如果选中，绘制选中效果
            if self.selected_city == city:
                pygame.draw.circle(screen, COLORS['gold'], (x, y), city_size + 5, 3)

            # 绘制城市主体（六边形）
            points = []
            for i in range(6):
                angle = math.pi / 3 * i - math.pi / 6
                px = x + city_size * math.cos(angle)
                py = y + city_size * math.sin(angle)
                points.append((px, py))
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, COLORS['white'], points, 2)

            # 绘制城市名称
            font = self.resource_loader.get_font('small')
            name_surface = font.render(city.name, True, COLORS['white'])
            name_rect = name_surface.get_rect(center=(x, y + city_size + 15))
            screen.blit(name_surface, name_rect)

            # 显示兵员数量
            soldiers_text = font.render(f"兵:{city.soldiers}", True, COLORS['yellow'])
            screen.blit(soldiers_text, (x - 20, y - city_size - 20))

    def _draw_ui(self, screen):
        """绘制UI"""
        # 绘制按钮
        for button in self.buttons.values():
            button.render(screen, self.resource_loader)
        self.zoom_in_btn.render(screen, self.resource_loader)
        self.zoom_out_btn.render(screen, self.resource_loader)

        # 绘制信息面板
        if self.selected_city:
            self._draw_city_info(screen)

        # 绘制小地图
        self._draw_minimap(screen)

    def _draw_city_info(self, screen):
        """绘制城市信息"""
        if not self.selected_city:
            return

        city = self.selected_city
        panel_x = 10
        panel_y = WINDOW_HEIGHT - 120
        panel_width = 300
        panel_height = 110

        # 绘制面板背景
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (*COLORS['panel_bg'], 200),
                         (0, 0, panel_width, panel_height), border_radius=5)
        pygame.draw.rect(panel_surface, COLORS['panel_border'],
                         (0, 0, panel_width, panel_height), 2, border_radius=5)
        screen.blit(panel_surface, (panel_x, panel_y))

        # 绘制城市名称
        font = self.resource_loader.get_font('default')
        title = font.render(f"{city.name} ({city.faction})", True, COLORS['gold'])
        screen.blit(title, (panel_x + 10, panel_y + 10))

        # 绘制城市信息
        small_font = self.resource_loader.get_font('small')
        info_lines = [
            f"人口: {city.population:,}",
            f"金钱: {city.gold:,}  粮草: {city.food:,}",
            f"兵员: {city.soldiers:,}",
            f"武将: {len(city.generals)}"
        ]
        for i, line in enumerate(info_lines):
            text = small_font.render(line, True, COLORS['white'])
            screen.blit(text, (panel_x + 10, panel_y + 40 + i * 18))

    def _draw_minimap(self, screen):
        """绘制小地图"""
        minimap_width = 180
        minimap_height = 140
        minimap_x = WINDOW_WIDTH - minimap_width - 10
        minimap_y = WINDOW_HEIGHT - minimap_height - 10

        # 绘制小地图背景
        pygame.draw.rect(screen, COLORS['dark_gray'],
                         (minimap_x, minimap_y, minimap_width, minimap_height))
        pygame.draw.rect(screen, COLORS['white'],
                         (minimap_x, minimap_y, minimap_width, minimap_height), 1)

        # 绘制城市点
        scale_x = minimap_width / 900
        scale_y = minimap_height / 500

        for city in self.cities.values():
            x = minimap_x + int(city.x * scale_x)
            y = minimap_y + int(city.y * scale_y)

            if city.faction and city.faction in FACTION_COLORS:
                color = FACTION_COLORS[city.faction]
            else:
                color = COLORS['gray']

            pygame.draw.circle(screen, color, (x, y), 4)

        # 绘制视野框
        view_x = minimap_x + int(-self.map_offset_x / self.map_zoom * scale_x)
        view_y = minimap_y + int(-self.map_offset_y / self.map_zoom * scale_y)
        view_w = int(WINDOW_WIDTH / self.map_zoom * scale_x)
        view_h = int(WINDOW_HEIGHT / self.map_zoom * scale_y)
        pygame.draw.rect(screen, COLORS['white'], (view_x, view_y, view_w, view_h), 1)