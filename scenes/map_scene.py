"""
地图场景 - 游戏主地图界面
"""
import pygame
import math
import json
import os
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, MAP_SCROLL_SPEED, MAP_ZOOM_MIN, MAP_ZOOM_MAX, MAP_ZOOM_STEP, FACTION_COLORS, DATA_DIR
from ui.button import Button
from ui.dialog import Dialog
from entities.city import City
from entities.general import General
from entities.faction import Faction
from systems.battle import BattleSystem
from systems.economy import EconomySystem
from systems.ai_system import get_ai_system
from game.game_state import GameState
from game.tutorial import TutorialSystem
from scenes.base_scene import BaseScene


class MapScene(BaseScene):
    """地图场景类"""

    def __init__(self, game_manager, new_game=True, save_data=None):
        """初始化地图场景

        Args:
            game_manager: 游戏管理器
            new_game: 是否为新游戏
            save_data: 存档数据（如果不是新游戏）
        """
        super().__init__(game_manager)
        self.game_state = GameState(game_manager)
        self.economy_system = EconomySystem()
        self.battle_system = BattleSystem()

        # 教程系统
        self.tutorial = TutorialSystem(game_manager)

        # 游戏时间
        self.turn = 1
        self.year = 190
        self.month = 1
        self.player_faction = '魏'

        # 地图状态
        self.map_offset_x = 200
        self.map_offset_y = 50
        self.map_zoom = 1.0
        self.dragging = False
        self.drag_start = (0, 0)

        # 选中的实体
        self.selected_city = None
        self.selected_army = None

        # 游戏数据
        self.factions = {}
        self.cities = {}
        self.generals = {}
        self.armies = []

        # 消息日志
        self.messages = []
        self.message_timer = 0

        # 对话框
        self.dialog = None
        self.show_save_menu = False

        # 动画
        self.animation_time = 0

        # 初始化游戏数据
        if save_data:
            self._load_from_save(save_data)
        else:
            self._init_game_data()

        # 创建UI
        self._create_ui()
        self.logger.info("地图场景初始化完成")

        # 处理战斗结果（从战斗场景返回时）
        self._process_battle_result()

    def _init_game_data(self):
        """初始化游戏数据"""
        self.logger.info("初始化新游戏数据")
        # 从JSON文件加载数据
        self._load_cities_from_json()
        self._load_generals_from_json()

        # 创建势力
        faction_data = [
            ('魏', '曹操', '许昌'),
            ('蜀', '刘备', '成都'),
            ('吴', '孙权', '建业'),
            ('吕布', '吕布', '下邳'),
            ('袁绍', '袁绍', '南皮'),
            ('袁术', '袁术', '寿春'),
            ('公孙瓒', '公孙瓒', '北平'),
            ('马腾', '马腾', '西凉'),
        ]

        for name, leader, capital in faction_data:
            self.factions[name] = Faction(name, leader, capital)

        # 将城市分配给势力
        for city in self.cities.values():
            if city.faction in self.factions:
                self.factions[city.faction].add_city(city.name)

        # 将武将分配给势力
        for general in self.generals.values():
            if general.faction in self.factions:
                self.factions[general.faction].add_general(general.name)

        self._add_message("游戏开始！选择魏国作为玩家势力。")
        self.logger.info(f"游戏开始，玩家势力: {self.player_faction}")

    def _load_cities_from_json(self):
        """从JSON文件加载城市数据"""
        cities_path = os.path.join(DATA_DIR, 'cities.json')
        try:
            with open(cities_path, 'r', encoding='utf-8') as f:
                cities_data = json.load(f)
                for city_data in cities_data:
                    city = City(
                        city_data['name'],
                        city_data.get('faction', ''),
                        city_data['population'],
                        city_data['gold'],
                        city_data['food'],
                        city_data['soldiers'],
                        city_data['x'],
                        city_data['y']
                    )
                    city.defense = city_data.get('defense', 100)
                    city.order = city_data.get('order', 100)
                    self.cities[city.name] = city
        except FileNotFoundError:
            # 使用默认数据
            self._init_default_cities()

    def _load_generals_from_json(self):
        """从JSON文件加载武将数据"""
        generals_path = os.path.join(DATA_DIR, 'generals.json')
        try:
            with open(generals_path, 'r', encoding='utf-8') as f:
                generals_data = json.load(f)
                for gen_data in generals_data:
                    general = General(
                        gen_data['name'],
                        gen_data['faction'],
                        gen_data['force'],
                        gen_data['intelligence'],
                        gen_data['command'],
                        gen_data['politics'],
                        gen_data['city']
                    )
                    general.skills = gen_data.get('skills', [])
                    self.generals[general.name] = general

                    # 将武将添加到城市
                    if general.city in self.cities:
                        self.cities[general.city].add_general(general.name)
        except FileNotFoundError:
            self._init_default_generals()

    def _init_default_cities(self):
        """初始化默认城市数据"""
        city_data = [
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
            self.cities[name] = City(name, faction, pop, gold, food, soldiers, x, y)

    def _init_default_generals(self):
        """初始化默认武将数据"""
        general_data = [
            ('曹操', '魏', 72, 91, 96, 94, '许昌'),
            ('夏侯惇', '魏', 85, 55, 78, 45, '洛阳'),
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
        ]
        for data in general_data:
            name, faction, force, intel, command, politics, city = data
            self.generals[name] = General(name, faction, force, intel, command, politics, city)
            if city in self.cities:
                self.cities[city].add_general(name)

    def _load_from_save(self, save_data):
        """从存档加载数据"""
        from game.game_state import GameState
        gs = GameState(self.game_manager)
        self.factions, self.cities, self.generals, self.turn, self.year, self.month, self.player_faction = \
            gs.import_game_data(save_data)
        self._add_message(f"已读取存档 - 第{self.turn}回合")

    def _create_ui(self):
        """创建UI元素"""
        # 顶部信息栏按钮
        self.top_buttons = {
            'diplomacy': Button(WINDOW_WIDTH - 400, 10, 90, 35, "外交", self._on_diplomacy),
            'save': Button(WINDOW_WIDTH - 300, 10, 90, 35, "存档", self._on_save),
            'menu': Button(WINDOW_WIDTH - 200, 10, 90, 35, "菜单", self._on_menu),
            'end_turn': Button(WINDOW_WIDTH - 100, 10, 90, 35, "回合结束", self._on_end_turn),
        }

        # 缩放按钮
        self.zoom_in_btn = Button(WINDOW_WIDTH - 210, WINDOW_HEIGHT - 160, 90, 35, "放大", self._on_zoom_in)
        self.zoom_out_btn = Button(WINDOW_WIDTH - 110, WINDOW_HEIGHT - 160, 90, 35, "缩小", self._on_zoom_out)

        # 存档选择按钮
        center_x = WINDOW_WIDTH // 2
        self.save_slots = {}
        for i in range(5):
            self.save_slots[i + 1] = Button(
                center_x - 150, 200 + i * 60, 300, 50,
                f"存档 {i + 1} - 空", lambda slot=i + 1: self._on_save_to_slot(slot)
            )
        self.cancel_save_btn = Button(center_x - 100, WINDOW_HEIGHT - 100, 200, 40, "取消", self._on_cancel_save)

    def _add_message(self, text):
        """添加消息"""
        self.messages.append({'text': text, 'time': 180})  # 显示3秒
        if len(self.messages) > 5:
            self.messages.pop(0)

    def _on_save(self):
        """保存游戏"""
        self.game_manager.play_sound('click')
        self.show_save_menu = True
        saves = self.game_state.list_saves()
        for i, save_info in enumerate(saves):
            slot = i + 1
            if save_info:
                self.save_slots[slot].text = f"存档 {slot}: {save_info['player_faction']} - 第{save_info['turn']}回合"
            else:
                self.save_slots[slot].text = f"存档 {slot} - 空"

    def _on_save_to_slot(self, slot):
        """保存到指定槽位"""
        game_data = self.game_state.export_game_data(
            self.factions, self.cities, self.generals,
            self.turn, self.year, self.month, self.player_faction
        )
        if self.game_state.save_game(slot, game_data):
            self.game_manager.play_sound('save')
            self._add_message(f"游戏已保存到存档 {slot}")
            self.logger.info(f"游戏已保存到存档 {slot}")
        self.show_save_menu = False

    def _on_cancel_save(self):
        """取消保存"""
        self.game_manager.play_sound('cancel')
        self.show_save_menu = False

    def _on_diplomacy(self):
        """外交按钮回调"""
        self.game_manager.play_sound('click')
        # 设置共享数据
        self.game_manager.set_shared_data('factions', self.factions)
        self.game_manager.set_shared_data('player_faction', self.player_faction)
        self.game_manager.scene_manager.load_scene('diplomacy')

    def _on_menu(self):
        """菜单按钮回调"""
        self.game_manager.play_sound('click')
        self.game_manager.scene_manager.load_scene('main_menu')

    def _on_end_turn(self):
        """回合结束"""
        self.game_manager.play_sound('turn_end')
        self._process_turn()
        self._add_message(f"第{self.turn}回合 - {self.year}年{self.month}月")

    def _process_turn(self):
        """处理回合"""
        # 更新时间
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.turn += 1

        # 处理经济
        self.economy_system.process_turn(self.cities)

        # 更新城市
        for city in self.cities.values():
            city.update()

        # 更新军队位置
        for army in self.armies:
            army.update_position()

        # AI行动（简化）
        self._ai_action()

    def _ai_action(self):
        """AI行动"""
        ai_system = get_ai_system()
        for faction_name, faction in self.factions.items():
            if faction_name == self.player_faction:
                continue

            # 使用AI系统处理回合
            logs = ai_system.process_turn(
                faction_name, faction,
                self.cities, self.generals,
                self.player_faction
            )

            # 显示AI行动日志
            for log in logs[:3]:  # 限制显示的日志数量
                self._add_message(log)

    def _on_zoom_in(self):
        """放大地图"""
        self.map_zoom = min(MAP_ZOOM_MAX, self.map_zoom + MAP_ZOOM_STEP)

    def _on_zoom_out(self):
        """缩小地图"""
        self.map_zoom = max(MAP_ZOOM_MIN, self.map_zoom - MAP_ZOOM_STEP)

    def _on_city_detail(self):
        """查看城市详情"""
        if self.selected_city:
            self.game_manager.play_sound('click')
            # 设置共享数据，传递给城市场景
            self.game_manager.set_shared_data('selected_city', self.selected_city)
            # 获取城市中的武将
            generals_in_city = [self.generals[name] for name in self.selected_city.generals if name in self.generals]
            self.game_manager.set_shared_data('generals_in_city', generals_in_city)
            self.game_manager.scene_manager.load_scene('city', city_name=self.selected_city.name)

    def _on_attack(self):
        """发起攻击"""
        if self.selected_city:
            self.game_manager.play_sound('battle_start')
            self.game_manager.scene_manager.load_scene('battle', attacker=self.player_faction, city=self.selected_city)

    def handle_event(self, event):
        """处理事件"""
        # 处理教程事件
        if self.tutorial.visible:
            if self.tutorial.handle_event(event):
                return

        # 如果显示存档菜单
        if self.show_save_menu:
            for btn in self.save_slots.values():
                btn.handle_event(event)
            self.cancel_save_btn.handle_event(event)
            return

        # 如果有对话框
        if self.dialog:
            self.dialog.handle_event(event)
            return

        # 处理顶部按钮
        for button in self.top_buttons.values():
            button.handle_event(event)
        self.zoom_in_btn.handle_event(event)
        self.zoom_out_btn.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键
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
            if event.y > 0:
                self._on_zoom_in()
            else:
                self._on_zoom_out()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._on_menu()

    def _check_city_click(self, pos):
        """检查是否点击了城市"""
        for city in self.cities.values():
            city_x = city.x * self.map_zoom + self.map_offset_x
            city_y = city.y * self.map_zoom + self.map_offset_y
            distance = math.sqrt((pos[0] - city_x) ** 2 + (pos[1] - city_y) ** 2)
            if distance < 30:
                self.selected_city = city
                self._add_message(f"选中城市: {city.name}")
                return

    def update(self):
        """更新场景"""
        # 更新教程
        self.tutorial.update()

        self.animation_time += 1

        # 更新消息
        for msg in self.messages[:]:
            msg['time'] -= 1
            if msg['time'] <= 0:
                self.messages.remove(msg)

        # 更新按钮
        for button in self.top_buttons.values():
            button.update()
        self.zoom_in_btn.update()
        self.zoom_out_btn.update()

        if self.show_save_menu:
            for btn in self.save_slots.values():
                btn.update()
            self.cancel_save_btn.update()

    def render(self, screen):
        """渲染场景"""
        # 绘制地图背景
        self._draw_map_background(screen)

        # 绘制城市
        self._draw_cities(screen)

        # 绘制UI
        self._draw_ui(screen)

        # 绘制消息
        self._draw_messages(screen)

        # 绘制存档菜单
        if self.show_save_menu:
            self._draw_save_menu(screen)

        # 绘制对话框
        if self.dialog:
            self.dialog.render(screen, self.resource_loader)

        # 绘制教程
        self.tutorial.render(screen)

    def _draw_map_background(self, screen):
        """绘制地图背景"""
        # 使用基类的渐变背景方法（绿色调）
        self._draw_gradient_background(screen, (34, 85, 51), (44, 100, 61))

        # 绘制河流
        self._draw_rivers(screen)

        # 绘制势力区域
        self._draw_territories(screen)

    def _draw_rivers(self, screen):
        """绘制河流"""
        # 黄河
        yellow_river = [(100, 200), (200, 180), (350, 200), (500, 170), (650, 200), (750, 180), (850, 200)]
        # 长江
        yangtze_river = [(50, 350), (150, 370), (280, 350), (400, 370), (550, 360), (700, 380), (850, 350)]

        def transform(points):
            return [(int(p[0] * self.map_zoom + self.map_offset_x),
                     int(p[1] * self.map_zoom + self.map_offset_y)) for p in points]

        # 绘制黄河
        pygame.draw.lines(screen, (100, 150, 200), False, transform(yellow_river), 4)
        # 绘制长江
        pygame.draw.lines(screen, (80, 130, 180), False, transform(yangtze_river), 5)

    def _draw_territories(self, screen):
        """绘制势力区域"""
        for city in self.cities.values():
            if city.faction and city.faction in FACTION_COLORS:
                color = FACTION_COLORS[city.faction]
                x = int(city.x * self.map_zoom + self.map_offset_x)
                y = int(city.y * self.map_zoom + self.map_offset_y)
                radius = int(60 * self.map_zoom)

                # 创建半透明表面
                surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (*color, 40), (radius, radius), radius)
                screen.blit(surface, (x - radius, y - radius))

    def _draw_cities(self, screen):
        """绘制城市"""
        for city in self.cities.values():
            x = int(city.x * self.map_zoom + self.map_offset_x)
            y = int(city.y * self.map_zoom + self.map_offset_y)
            city_size = int(22 * self.map_zoom)

            # 城市颜色
            if city.faction and city.faction in FACTION_COLORS:
                color = FACTION_COLORS[city.faction]
            else:
                color = COLORS['gray']

            # 选中效果
            if self.selected_city == city:
                # 脉动效果
                pulse = int(5 + 3 * math.sin(self.animation_time * 0.1))
                pygame.draw.circle(screen, COLORS['gold'], (x, y), city_size + pulse, 3)

            # 绘制城市（六边形）
            points = []
            for i in range(6):
                angle = math.pi / 3 * i - math.pi / 6
                px = x + city_size * math.cos(angle)
                py = y + city_size * math.sin(angle)
                points.append((px, py))
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, COLORS['white'], points, 2)

            # 城市名称
            font = self.resource_loader.get_font('small')
            name_surface = font.render(city.name, True, COLORS['white'])
            name_rect = name_surface.get_rect(center=(x, y + city_size + 15))
            screen.blit(name_surface, name_rect)

            # 兵员数量
            soldiers_text = font.render(f"兵:{city.soldiers//1000}K", True, COLORS['yellow'])
            screen.blit(soldiers_text, (x - 20, y - city_size - 20))

    def _draw_ui(self, screen):
        """绘制UI"""
        # 顶部信息栏
        self._draw_top_bar(screen)

        # 绘制按钮
        for button in self.top_buttons.values():
            button.render(screen, self.resource_loader)
        self.zoom_in_btn.render(screen, self.resource_loader)
        self.zoom_out_btn.render(screen, self.resource_loader)

        # 城市信息面板
        if self.selected_city:
            self._draw_city_info(screen)

        # 小地图
        self._draw_minimap(screen)

    def _draw_top_bar(self, screen):
        """绘制顶部信息栏"""
        # 背景
        bar_height = 50
        pygame.draw.rect(screen, (*COLORS['panel_bg'], 200), (0, 0, WINDOW_WIDTH, bar_height))

        # 时间信息
        font = self.resource_loader.get_font('default')
        time_text = font.render(f"{self.year}年{self.month}月 - 第{self.turn}回合", True, COLORS['gold'])
        screen.blit(time_text, (20, 15))

        # 玩家势力信息
        if self.player_faction in self.factions:
            faction = self.factions[self.player_faction]
            faction_text = font.render(f"势力: {self.player_faction}  城市: {len(faction.cities)}", True, COLORS['white'])
            screen.blit(faction_text, (250, 15))

    def _draw_city_info(self, screen):
        """绘制城市信息面板"""
        if not self.selected_city:
            return

        city = self.selected_city
        panel_x = 10
        panel_y = 60
        panel_width = 320
        panel_height = 180

        # 面板背景
        surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (*COLORS['panel_bg'], 220), (0, 0, panel_width, panel_height), border_radius=8)
        pygame.draw.rect(surface, COLORS['panel_border'], (0, 0, panel_width, panel_height), 2, border_radius=8)
        screen.blit(surface, (panel_x, panel_y))

        # 城市名称
        font = self.resource_loader.get_font('large')
        title = font.render(f"{city.name}", True, COLORS['gold'])
        screen.blit(title, (panel_x + 15, panel_y + 10))

        # 势力
        faction_text = font.render(f"({city.faction})", True, FACTION_COLORS.get(city.faction, COLORS['white']))
        screen.blit(faction_text, (panel_x + 15 + title.get_width() + 10, panel_y + 10))

        # 详细信息
        small_font = self.resource_loader.get_font('default')
        info_lines = [
            f"人口: {city.population:,}  治安: {city.order}",
            f"金钱: {city.gold:,}  粮草: {city.food:,}",
            f"兵员: {city.soldiers:,}  城防: {city.defense}",
            f"武将: {len(city.generals)} 人",
        ]
        for i, line in enumerate(info_lines):
            text = small_font.render(line, True, COLORS['white'])
            screen.blit(text, (panel_x + 15, panel_y + 45 + i * 25))

        # 操作按钮
        btn_y = panel_y + 145
        self.detail_btn = Button(panel_x + 10, btn_y, 90, 30, "详情", self._on_city_detail)
        self.attack_btn = Button(panel_x + 110, btn_y, 90, 30, "出兵", self._on_attack)
        self.detail_btn.render(screen, self.resource_loader)
        self.attack_btn.render(screen, self.resource_loader)

    def _draw_minimap(self, screen):
        """绘制小地图"""
        minimap_width = 180
        minimap_height = 140
        minimap_x = WINDOW_WIDTH - minimap_width - 10
        minimap_y = WINDOW_HEIGHT - minimap_height - 10

        # 背景
        pygame.draw.rect(screen, COLORS['dark_gray'], (minimap_x - 2, minimap_y - 2, minimap_width + 4, minimap_height + 4), border_radius=5)
        pygame.draw.rect(screen, (40, 60, 40), (minimap_x, minimap_y, minimap_width, minimap_height))
        pygame.draw.rect(screen, COLORS['gold'], (minimap_x - 2, minimap_y - 2, minimap_width + 4, minimap_height + 4), 2, border_radius=5)

        # 城市点
        scale_x = minimap_width / 900
        scale_y = minimap_height / 500

        for city in self.cities.values():
            x = minimap_x + int(city.x * scale_x)
            y = minimap_y + int(city.y * scale_y)
            color = FACTION_COLORS.get(city.faction, COLORS['gray'])
            pygame.draw.circle(screen, color, (x, y), 4)

        # 视野框
        view_x = minimap_x + int(-self.map_offset_x / self.map_zoom * scale_x)
        view_y = minimap_y + int(-self.map_offset_y / self.map_zoom * scale_y)
        view_w = int(WINDOW_WIDTH / self.map_zoom * scale_x)
        view_h = int(WINDOW_HEIGHT / self.map_zoom * scale_y)
        pygame.draw.rect(screen, COLORS['white'], (view_x, view_y, view_w, view_h), 1)

    def _draw_messages(self, screen):
        """绘制消息"""
        font = self.resource_loader.get_font('small')
        for i, msg in enumerate(self.messages):
            alpha = min(255, msg['time'] * 3)
            text = font.render(msg['text'], True, COLORS['white'])
            text.set_alpha(alpha)
            screen.blit(text, (10, WINDOW_HEIGHT - 180 - i * 25))

    def _draw_save_menu(self, screen):
        """绘制存档菜单"""
        # 遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # 标题
        font = self.resource_loader.get_font('title')
        title = font.render("选择存档位置", True, COLORS['gold'])
        title_rect = title.get_rect(centerx=WINDOW_WIDTH // 2, top=100)
        screen.blit(title, title_rect)

        # 存档按钮
        for btn in self.save_slots.values():
            btn.render(screen, self.resource_loader)
        self.cancel_save_btn.render(screen, self.resource_loader)

    def _process_battle_result(self):
        """处理战斗结果，更新势力城市列表"""
        battle_result = self.game_manager.get_shared_data('battle_result')
        if not battle_result:
            return

        # 清除已处理的战斗结果
        self.game_manager.set_shared_data('battle_result', None)

        winner = battle_result.get('winner')
        city_name = battle_result.get('city_name')

        if winner == 'attacker' and city_name:
            new_faction = battle_result.get('new_faction')
            old_faction = battle_result.get('old_faction')

            if new_faction and old_faction:
                # 更新势力的城市列表
                if old_faction in self.factions:
                    self.factions[old_faction].remove_city(city_name)
                    self.logger.info(f"{old_faction} 失去城市 {city_name}")

                if new_faction in self.factions:
                    self.factions[new_faction].add_city(city_name)
                    self.logger.info(f"{new_faction} 获得城市 {city_name}")

                # 更新城市的武将归属
                if city_name in self.cities:
                    city = self.cities[city_name]
                    for general_name in city.generals[:]:
                        if general_name in self.generals:
                            general = self.generals[general_name]
                            # 将武将从旧势力移除
                            if old_faction in self.factions:
                                self.factions[old_faction].remove_general(general_name)
                            # 将武将添加到新势力
                            if new_faction in self.factions:
                                self.factions[new_faction].add_general(general_name)
                            general.faction = new_faction

                self._add_message(f"战斗胜利！{city_name} 已归属 {new_faction}！")

        elif winner == 'defender' and city_name:
            self._add_message(f"战斗失败，{city_name} 仍在敌方手中")