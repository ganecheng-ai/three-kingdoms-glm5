"""
城市场景 - 城市管理界面
"""
import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, FACTION_COLORS
from ui.button import Button
from ui.panel import Panel
from systems.economy import EconomySystem


class CityScene:
    """城市场景类"""

    def __init__(self, game_manager, city_name=None):
        """初始化城市场景"""
        self.game_manager = game_manager
        self.resource_loader = game_manager.resource_loader
        self.city_name = city_name
        self.economy = EconomySystem()

        # 获取城市数据
        self.city = None
        self.generals_in_city = []

        # 当前选中的标签页
        self.current_tab = 'overview'

        # 选中的武将
        self.selected_general = None

        # 操作结果消息
        self.message = None
        self.message_timer = 0

        # 创建UI
        self._create_ui()

    def _create_ui(self):
        """创建UI元素"""
        # 返回按钮
        self.buttons = {
            'back': Button(10, 10, 100, 40, "返回地图", self._on_back),
        }

        # 标签页按钮
        tab_y = 70
        self.tab_buttons = {
            'overview': Button(100, tab_y, 120, 40, "概览", lambda: self._switch_tab('overview')),
            'generals': Button(230, tab_y, 120, 40, "武将", lambda: self._switch_tab('generals')),
            'army': Button(360, tab_y, 120, 40, "军队", lambda: self._switch_tab('army')),
            'buildings': Button(490, tab_y, 120, 40, "建筑", lambda: self._switch_tab('buildings')),
        }

        # 操作按钮
        self.action_buttons = {
            'recruit': Button(800, 300, 120, 45, "招募士兵", self._on_recruit),
            'train': Button(800, 360, 120, 45, "训练军队", self._on_train),
            'upgrade': Button(800, 420, 120, 45, "升级建筑", self._on_upgrade),
        }

    def _on_back(self):
        """返回地图"""
        self.game_manager.play_sound('cancel')
        self.game_manager.scene_manager.load_scene('map')

    def _switch_tab(self, tab_name):
        """切换标签页"""
        self.game_manager.play_sound('click')
        self.current_tab = tab_name
        self.selected_general = None

    def _on_recruit(self):
        """招募士兵"""
        if self.city:
            if self.city.gold >= 1000 and self.city.population >= 1000:
                self.city.gold -= 1000
                self.city.population -= 1000
                self.city.soldiers += 1000
                self.game_manager.play_sound('recruit')
                self._show_message("成功招募1000名士兵！")
            else:
                self.game_manager.play_sound('cancel')
                self._show_message("资源不足！需要金钱1000，人口1000")

    def _on_train(self):
        """训练军队"""
        if self.city:
            if self.city.gold >= 500:
                self.city.gold -= 500
                self.game_manager.play_sound('gold')
                self._show_message("军队训练完成，士气提升！")
            else:
                self.game_manager.play_sound('cancel')
                self._show_message("金钱不足！需要500金钱")

    def _on_upgrade(self):
        """升级建筑"""
        if self.city:
            upgrade_cost = self.city.buildings.get('farm', 1) * 2000
            if self.city.gold >= upgrade_cost:
                self.city.gold -= upgrade_cost
                self.city.buildings['farm'] = self.city.buildings.get('farm', 1) + 1
                self.game_manager.play_sound('build')
                self._show_message(f"农田升级到 Lv.{self.city.buildings['farm']}！")
            else:
                self.game_manager.play_sound('cancel')
                self._show_message(f"金钱不足！需要{upgrade_cost}金钱")

    def _show_message(self, text):
        """显示消息"""
        self.message = text
        self.message_timer = 120

    def handle_event(self, event):
        """处理事件"""
        for button in self.buttons.values():
            button.handle_event(event)
        for button in self.tab_buttons.values():
            button.handle_event(event)
        for button in self.action_buttons.values():
            button.handle_event(event)

    def update(self):
        """更新场景"""
        for button in self.buttons.values():
            button.update()
        for button in self.tab_buttons.values():
            button.update()
        for button in self.action_buttons.values():
            button.update()

        # 更新消息
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.message = None

    def render(self, screen):
        """渲染场景"""
        # 绘制背景
        self._draw_background(screen)

        # 绘制城市标题
        self._draw_title(screen)

        # 绘制返回按钮
        for button in self.buttons.values():
            button.render(screen, self.resource_loader)

        # 绘制标签页
        for name, button in self.tab_buttons.items():
            if name == self.current_tab:
                button.color = COLORS['gold']
            else:
                button.color = COLORS['button_normal']
            button.render(screen, self.resource_loader)

        # 绘制内容区域
        self._draw_content_area(screen)

        # 根据标签页绘制内容
        if self.current_tab == 'overview':
            self._render_overview(screen)
        elif self.current_tab == 'generals':
            self._render_generals(screen)
        elif self.current_tab == 'army':
            self._render_army(screen)
        elif self.current_tab == 'buildings':
            self._render_buildings(screen)

        # 绘制操作按钮
        for button in self.action_buttons.values():
            button.render(screen, self.resource_loader)

        # 绘制消息
        if self.message:
            self._draw_message(screen)

    def _draw_background(self, screen):
        """绘制背景"""
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(30 + ratio * 15)
            g = int(35 + ratio * 20)
            b = int(45 + ratio * 25)
            pygame.draw.line(screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

    def _draw_title(self, screen):
        """绘制标题"""
        font = self.resource_loader.get_font('title')
        city_name = self.city_name if self.city_name else "城市管理"

        # 势力颜色
        if self.city and self.city.faction in FACTION_COLORS:
            color = FACTION_COLORS[self.city.faction]
        else:
            color = COLORS['gold']

        title = font.render(city_name, True, color)
        title_rect = title.get_rect(centerx=WINDOW_WIDTH // 2, top=15)
        screen.blit(title, title_rect)

        # 势力标签
        if self.city:
            small_font = self.resource_loader.get_font('default')
            faction_text = small_font.render(f"势力: {self.city.faction}", True, COLORS['white'])
            screen.blit(faction_text, (WINDOW_WIDTH // 2 + title.get_width() // 2 + 20, 25))

    def _draw_content_area(self, screen):
        """绘制内容区域"""
        # 主内容面板
        panel_x = 50
        panel_y = 130
        panel_width = 700
        panel_height = WINDOW_HEIGHT - 160

        # 绘制面板背景
        surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (*COLORS['panel_bg'], 200), (0, 0, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(surface, COLORS['panel_border'], (0, 0, panel_width, panel_height), 2, border_radius=10)
        screen.blit(surface, (panel_x, panel_y))

        # 右侧操作面板
        right_panel_x = 780
        right_panel_width = 200
        surface2 = pygame.Surface((right_panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(surface2, (*COLORS['panel_bg'], 200), (0, 0, right_panel_width, panel_height), border_radius=10)
        pygame.draw.rect(surface2, COLORS['panel_border'], (0, 0, right_panel_width, panel_height), 2, border_radius=10)
        screen.blit(surface2, (right_panel_x, panel_y))

        # 操作面板标题
        font = self.resource_loader.get_font('default')
        title = font.render("操作", True, COLORS['gold'])
        screen.blit(title, (right_panel_x + 80, panel_y + 10))

    def _render_overview(self, screen):
        """渲染概览页面"""
        font = self.resource_loader.get_font('large')
        small_font = self.resource_loader.get_font('default')

        y_start = 160
        x_start = 80

        # 标题
        title = font.render("城市概览", True, COLORS['gold'])
        screen.blit(title, (x_start, y_start))

        if self.city:
            info_items = [
                ("人口", f"{self.city.population:,}"),
                ("金钱", f"{self.city.gold:,}"),
                ("粮草", f"{self.city.food:,}"),
                ("兵员", f"{self.city.soldiers:,}"),
                ("城防", f"{self.city.defense}"),
                ("治安", f"{self.city.order}"),
                ("武将", f"{len(self.city.generals)} 人"),
            ]

            y = y_start + 50
            for label, value in info_items:
                # 标签
                label_text = small_font.render(f"{label}:", True, COLORS['light_gray'])
                screen.blit(label_text, (x_start, y))
                # 值
                value_text = small_font.render(value, True, COLORS['white'])
                screen.blit(value_text, (x_start + 100, y))
                y += 35

            # 收入预测
            gold_income, food_income = self.economy.calculate_city_income(self.city)
            y += 20
            income_title = font.render("预计收入", True, COLORS['gold'])
            screen.blit(income_title, (x_start, y))
            y += 40
            gold_text = small_font.render(f"金钱: +{gold_income}/月", True, COLORS['yellow'])
            food_text = small_font.render(f"粮草: +{food_income}/月", True, COLORS['green'])
            screen.blit(gold_text, (x_start, y))
            screen.blit(food_text, (x_start + 150, y))

            # 消耗
            gold_cost, food_cost = self.economy.calculate_upkeep(self.city)
            y += 35
            cost_text = small_font.render(f"维护: -{gold_cost}金钱  -{food_cost}粮草/月", True, COLORS['red'])
            screen.blit(cost_text, (x_start, y))
        else:
            no_data = small_font.render("未选择城市", True, COLORS['gray'])
            screen.blit(no_data, (x_start, y_start + 50))

    def _render_generals(self, screen):
        """渲染武将页面"""
        font = self.resource_loader.get_font('large')
        small_font = self.resource_loader.get_font('default')

        y_start = 160
        x_start = 80

        # 标题
        title = font.render("武将列表", True, COLORS['gold'])
        screen.blit(title, (x_start, y_start))

        if self.city and self.city.generals:
            y = y_start + 50
            for i, general_name in enumerate(self.city.generals[:8]):
                # 武将名
                name_text = small_font.render(f"• {general_name}", True, COLORS['white'])
                screen.blit(name_text, (x_start, y))

                # 属性（简化显示）
                attrs = small_font.render("武:90 智:80 统:85", True, COLORS['light_gray'])
                screen.blit(attrs, (x_start + 120, y))
                y += 35
        else:
            no_data = small_font.render("该城市暂无武将", True, COLORS['gray'])
            screen.blit(no_data, (x_start, y_start + 50))

    def _render_army(self, screen):
        """渲染军队页面"""
        font = self.resource_loader.get_font('large')
        small_font = self.resource_loader.get_font('default')

        y_start = 160
        x_start = 80

        # 标题
        title = font.render("军队管理", True, COLORS['gold'])
        screen.blit(title, (x_start, y_start))

        if self.city:
            # 兵力分布（简化）
            infantry = self.city.soldiers * 60 // 100
            cavalry = self.city.soldiers * 25 // 100
            archer = self.city.soldiers - infantry - cavalry

            info_items = [
                ("步兵", f"{infantry:,}", "主力部队"),
                ("骑兵", f"{cavalry:,}", "机动作战"),
                ("弓兵", f"{archer:,}", "远程支援"),
                ("总兵力", f"{self.city.soldiers:,}", ""),
            ]

            y = y_start + 50
            for label, value, desc in info_items:
                label_text = small_font.render(f"{label}:", True, COLORS['light_gray'])
                screen.blit(label_text, (x_start, y))
                value_text = small_font.render(value, True, COLORS['white'])
                screen.blit(value_text, (x_start + 80, y))
                if desc:
                    desc_text = small_font.render(f"({desc})", True, COLORS['gray'])
                    screen.blit(desc_text, (x_start + 180, y))
                y += 35

            # 军队状态
            y += 20
            status_title = font.render("军队状态", True, COLORS['gold'])
            screen.blit(status_title, (x_start, y))
            y += 40
            morale = small_font.render("士气: 良好", True, COLORS['green'])
            training = small_font.render("训练度: 中等", True, COLORS['yellow'])
            screen.blit(morale, (x_start, y))
            screen.blit(training, (x_start + 150, y))

    def _render_buildings(self, screen):
        """渲染建筑页面"""
        font = self.resource_loader.get_font('large')
        small_font = self.resource_loader.get_font('default')

        y_start = 160
        x_start = 80

        # 标题
        title = font.render("建筑管理", True, COLORS['gold'])
        screen.blit(title, (x_start, y_start))

        if self.city:
            buildings_info = [
                ("农田", "farm", "增加粮草产量"),
                ("市场", "market", "增加金钱收入"),
                ("兵营", "barracks", "提高招募效率"),
                ("城墙", "wall", "增强城市防御"),
            ]

            y = y_start + 50
            for name, key, desc in buildings_info:
                level = self.city.buildings.get(key, 1)
                # 建筑名和等级
                name_text = small_font.render(f"{name} Lv.{level}", True, COLORS['white'])
                screen.blit(name_text, (x_start, y))
                # 描述
                desc_text = small_font.render(f"({desc})", True, COLORS['gray'])
                screen.blit(desc_text, (x_start + 120, y))
                # 升级费用
                cost = level * 2000
                cost_text = small_font.render(f"升级: {cost}金", True, COLORS['yellow'])
                screen.blit(cost_text, (x_start + 350, y))
                y += 40

            # 建筑效果说明
            y += 20
            effect_title = font.render("建筑效果", True, COLORS['gold'])
            screen.blit(effect_title, (x_start, y))
            y += 40
            effects = [
                f"粮草产量: +{self.city.buildings.get('farm', 1) * 10}%",
                f"金钱收入: +{self.city.buildings.get('market', 1) * 10}%",
                f"招募效率: +{self.city.buildings.get('barracks', 1) * 5}%",
                f"城防加成: +{self.city.buildings.get('wall', 1) * 10}%",
            ]
            for effect in effects:
                effect_text = small_font.render(effect, True, COLORS['white'])
                screen.blit(effect_text, (x_start, y))
                y += 30

    def _draw_message(self, screen):
        """绘制消息"""
        if self.message:
            font = self.resource_loader.get_font('default')

            # 消息框
            msg_width = font.size(self.message)[0] + 40
            msg_height = 50
            msg_x = (WINDOW_WIDTH - msg_width) // 2
            msg_y = WINDOW_HEIGHT - 100

            surface = pygame.Surface((msg_width, msg_height), pygame.SRCALPHA)
            pygame.draw.rect(surface, (*COLORS['panel_bg'], 230), (0, 0, msg_width, msg_height), border_radius=8)
            pygame.draw.rect(surface, COLORS['gold'], (0, 0, msg_width, msg_height), 2, border_radius=8)
            screen.blit(surface, (msg_x, msg_y))

            text = font.render(self.message, True, COLORS['white'])
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, msg_y + 25))
            screen.blit(text, text_rect)