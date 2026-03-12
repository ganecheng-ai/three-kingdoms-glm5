"""
外交场景 - 外交管理界面
"""
import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, FACTION_COLORS
from ui.button import Button
from systems.diplomacy import DiplomacySystem
from scenes.base_scene import BaseScene


class DiplomacyScene(BaseScene):
    """外交场景类"""

    def __init__(self, game_manager):
        """初始化外交场景"""
        super().__init__(game_manager)
        self.diplomacy_system = DiplomacySystem()

        # 从共享数据获取游戏数据
        self.factions = game_manager.get_shared_data('factions', {})
        self.player_faction = game_manager.get_shared_data('player_faction', '魏')
        self.player_faction_obj = self.factions.get(self.player_faction)

        # 选中的势力
        self.selected_faction = None

        # 创建UI
        self._create_ui()
        self.logger.info("外交场景初始化完成")

    def _create_ui(self):
        """创建UI元素"""
        center_x = WINDOW_WIDTH // 2

        # 返回按钮
        self.back_button = Button(
            center_x - 100, WINDOW_HEIGHT - 60, 200, 40,
            "返回地图", self._on_back
        )

        # 势力按钮（在左侧显示）
        self.faction_buttons = {}
        btn_y = 120
        for faction_name in self.factions:
            if faction_name != self.player_faction:
                self.faction_buttons[faction_name] = Button(
                    50, btn_y, 180, 40,
                    faction_name, lambda fn=faction_name: self._on_select_faction(fn)
                )
                btn_y += 50

        # 外交操作按钮
        self.action_buttons = {
            'gift': Button(400, 200, 120, 40, "送礼", self._on_gift),
            'alliance': Button(540, 200, 120, 40, "结盟", self._on_alliance),
            'peace': Button(400, 260, 120, 40, "议和", self._on_peace),
            'war': Button(540, 260, 120, 40, "宣战", self._on_war),
        }

    def _on_back(self):
        """返回地图"""
        self.game_manager.play_sound('cancel')
        self.game_manager.scene_manager.load_scene('map')

    def _on_select_faction(self, faction_name):
        """选中势力"""
        self.game_manager.play_sound('click')
        self.selected_faction = faction_name

    def _on_gift(self):
        """送礼"""
        if not self.selected_faction or not self.player_faction_obj:
            return

        target_faction = self.factions.get(self.selected_faction)
        if not target_faction:
            return

        # 检查资源
        gift_gold = 1000
        gift_food = 2000

        if self.player_faction_obj.gold < gift_gold or self.player_faction_obj.food < gift_food:
            self.game_manager.play_sound('cancel')
            return

        # 送礼
        self.game_manager.play_sound('gold')
        change = self.diplomacy_system.send_gift(
            self.player_faction_obj, target_faction,
            gift_gold, gift_food
        )
        self._add_message(f"向{self.selected_faction}送礼，关系+{change}")

    def _on_alliance(self):
        """结盟"""
        if not self.selected_faction or not self.player_faction_obj:
            return

        target_faction = self.factions.get(self.selected_faction)
        if not target_faction:
            return

        success, reason = self.diplomacy_system.propose_alliance(
            self.player_faction_obj, target_faction
        )

        if success:
            self.game_manager.play_sound('confirm')
            self._add_message(f"与{self.selected_faction}结盟成功！")
        else:
            self.game_manager.play_sound('cancel')
            self._add_message(f"结盟失败: {reason}")

    def _on_peace(self):
        """议和"""
        if not self.selected_faction or not self.player_faction_obj:
            return

        target_faction = self.factions.get(self.selected_faction)
        if not target_faction:
            return

        success = self.diplomacy_system.make_peace(
            self.player_faction_obj, target_faction
        )

        if success:
            self.game_manager.play_sound('confirm')
            self._add_message(f"与{self.selected_faction}议和成功")
        else:
            self.game_manager.play_sound('cancel')
            self._add_message("议和失败")

    def _on_war(self):
        """宣战"""
        if not self.selected_faction or not self.player_faction_obj:
            return

        target_faction = self.factions.get(self.selected_faction)
        if not target_faction:
            return

        self.diplomacy_system.declare_war(
            self.player_faction_obj, target_faction
        )
        self.game_manager.play_sound('battle_start')
        self._add_message(f"向{self.selected_faction}宣战！")

    def _add_message(self, text):
        """添加消息到共享数据"""
        messages = self.game_manager.get_shared_data('diplomacy_messages', [])
        messages.append(text)
        self.game_manager.set_shared_data('diplomacy_messages', messages[-5:])

    def handle_event(self, event):
        """处理事件"""
        self.back_button.handle_event(event)

        for btn in self.faction_buttons.values():
            btn.handle_event(event)

        if self.selected_faction:
            for btn in self.action_buttons.values():
                btn.handle_event(event)

    def update(self):
        """更新场景"""
        self.back_button.update()

        for btn in self.faction_buttons.values():
            btn.update()

        for btn in self.action_buttons.values():
            btn.update()

    def render(self, screen):
        """渲染场景"""
        # 绘制背景
        self._draw_background(screen)

        # 绘制标题
        title_font = self.resource_loader.get_font('title')
        title_text = title_font.render("外交管理", True, COLORS['gold'])
        title_rect = title_text.get_rect(centerx=WINDOW_WIDTH // 2, top=30)
        screen.blit(title_text, title_rect)

        # 绘制势力列表
        self._draw_faction_list(screen)

        # 绘制选中势力的信息
        if self.selected_faction:
            self._draw_faction_info(screen)

        # 绘制返回按钮
        self.back_button.render(screen, self.resource_loader)

    def _draw_background(self, screen):
        """绘制背景"""
        self._draw_gradient_background(screen, (20, 30, 60), (50, 45, 80))

    def _draw_faction_list(self, screen):
        """绘制势力列表"""
        font = self.resource_loader.get_font('large')
        label = font.render("势力列表", True, COLORS['gold'])
        screen.blit(label, (50, 80))

        for btn in self.faction_buttons.values():
            btn.render(screen, self.resource_loader)

    def _draw_faction_info(self, screen):
        """绘制选中势力信息"""
        faction = self.factions.get(self.selected_faction)
        if not faction:
            return

        # 信息面板
        panel_x = 380
        panel_y = 80
        panel_width = 350
        panel_height = 150

        surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (*COLORS['panel_bg'], 220), (0, 0, panel_width, panel_height), border_radius=8)
        pygame.draw.rect(surface, COLORS['panel_border'], (0, 0, panel_width, panel_height), 2, border_radius=8)
        screen.blit(surface, (panel_x, panel_y))

        font = self.resource_loader.get_font('large')
        small_font = self.resource_loader.get_font('default')

        # 势力名称
        faction_color = FACTION_COLORS.get(self.selected_faction, COLORS['white'])
        name_text = font.render(self.selected_faction, True, faction_color)
        screen.blit(name_text, (panel_x + 15, panel_y + 15))

        # 势力信息
        relation = self.player_faction_obj.get_relation(self.selected_faction) if self.player_faction_obj else 0
        status = self.diplomacy_system.get_diplomatic_status(
            self.player_faction_obj, faction
        ) if self.player_faction_obj else "未知"

        info_lines = [
            f"领袖: {faction.leader}",
            f"城市: {len(faction.cities)}",
            f"武将: {len(faction.generals)}",
            f"关系: {relation}",
            f"状态: {status}",
        ]

        for i, line in enumerate(info_lines):
            text = small_font.render(line, True, COLORS['white'])
            screen.blit(text, (panel_x + 15, panel_y + 50 + i * 20))

        # 绘制操作按钮
        for btn in self.action_buttons.values():
            btn.render(screen, self.resource_loader)