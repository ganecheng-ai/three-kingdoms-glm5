"""
教程系统 - 新手引导功能
"""
import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT


class TutorialStep:
    """教程步骤"""

    def __init__(self, title, description, highlight_area=None, action_hint=None):
        """初始化教程步骤

        Args:
            title: 步骤标题
            description: 步骤描述
            highlight_area: 高亮区域 (x, y, width, height)，可选
            action_hint: 操作提示，可选
        """
        self.title = title
        self.description = description
        self.highlight_area = highlight_area
        self.action_hint = action_hint
        self.completed = False


class TutorialSystem:
    """教程引导系统"""

    def __init__(self, game_manager):
        """初始化教程系统

        Args:
            game_manager: 游戏管理器实例
        """
        self.game_manager = game_manager
        self.resource_loader = game_manager.resource_loader

        # 教程状态
        self.enabled = True  # 是否启用教程
        self.current_step = 0
        self.visible = False
        self.tutorial_started = False

        # 教程步骤定义
        self.steps = self._create_tutorial_steps()

        # 动画
        self.animation_time = 0

    def _create_tutorial_steps(self):
        """创建教程步骤"""
        return [
            TutorialStep(
                title="欢迎来到三国霸业",
                description="这是一款经典的三国策略游戏。在这个游戏中，\n"
                           "您将扮演一方诸侯，征战天下，最终统一三国。",
                action_hint="点击任意位置继续"
            ),
            TutorialStep(
                title="游戏目标",
                description="您的目标是消灭所有敌对势力，统一天下。\n"
                           "通过发展经济、招募武将、攻城略地来实现霸业。",
                action_hint="点击继续"
            ),
            TutorialStep(
                title="地图操作",
                description="• 鼠标左键：选择城市\n"
                           "• 鼠标右键拖拽：移动地图\n"
                           "• 鼠标滚轮：缩放地图",
                highlight_area=(WINDOW_WIDTH - 220, WINDOW_HEIGHT - 200, 200, 80),
                action_hint="尝试拖拽或缩放地图"
            ),
            TutorialStep(
                title="城市信息",
                description="每个城市显示以下信息：\n"
                           "• 势力颜色标识\n"
                           "• 城市名称\n"
                           "• 兵员数量",
                action_hint="点击城市查看详情"
            ),
            TutorialStep(
                title="城市管理",
                description="点击城市后可以：\n"
                           "• 查看[详情]：进入城市管理界面\n"
                           "• 点击[出兵]：发起战斗",
                highlight_area=(10, 60, 320, 180),
                action_hint="选择一个己方城市"
            ),
            TutorialStep(
                title="回合制游戏",
                description="游戏采用回合制：\n"
                           "• 每回合代表一个月\n"
                           "• 点击[回合结束]推进游戏\n"
                           "• AI势力会在每回合行动",
                highlight_area=(WINDOW_WIDTH - 100, 10, 90, 35),
                action_hint="准备好后点击回合结束"
            ),
            TutorialStep(
                title="存档功能",
                description="点击[存档]按钮可以保存游戏进度。\n"
                           "游戏提供5个存档槽位，随时可以保存和读取。",
                highlight_area=(WINDOW_WIDTH - 300, 10, 90, 35),
                action_hint="记得经常保存游戏"
            ),
            TutorialStep(
                title="武将系统",
                description="武将是游戏的核心：\n"
                           "• 武力：影响战斗伤害\n"
                           "• 智力：影响计策成功率\n"
                           "• 统率：影响军队战斗力\n"
                           "• 政治：影响城市发展",
                action_hint="点击继续"
            ),
            TutorialStep(
                title="战斗系统",
                description="发起战斗时：\n"
                           "• 选择出兵城市和目标城市\n"
                           "• 选择参战武将\n"
                           "• 战斗自动进行\n"
                           "• 可以选择自动战斗或手动指挥",
                action_hint="点击继续"
            ),
            TutorialStep(
                title="祝您游戏愉快！",
                description="教程到此结束。\n"
                           "如有疑问，可随时查看操作说明。\n\n"
                           "祝您早日统一三国，成就霸业！",
                action_hint="点击开始游戏"
            ),
        ]

    def start_tutorial(self):
        """开始教程"""
        if self.enabled:
            self.visible = True
            self.tutorial_started = True
            self.current_step = 0
            from utils.logger import get_logger
            get_logger().info("教程开始")

    def skip_tutorial(self):
        """跳过教程"""
        self.visible = False
        self.tutorial_started = True
        self.enabled = False
        from utils.logger import get_logger
        get_logger().info("教程已跳过")

    def next_step(self):
        """下一步"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
        else:
            self.complete_tutorial()

    def prev_step(self):
        """上一步"""
        if self.current_step > 0:
            self.current_step -= 1

    def complete_tutorial(self):
        """完成教程"""
        self.visible = False
        self.tutorial_started = True
        from utils.logger import get_logger
        get_logger().info("教程完成")

    def handle_event(self, event):
        """处理事件"""
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键
                # 检查跳过按钮
                skip_rect = pygame.Rect(WINDOW_WIDTH - 120, WINDOW_HEIGHT - 60, 100, 35)
                if skip_rect.collidepoint(event.pos):
                    self.skip_tutorial()
                    return True

                # 检查上一步按钮
                prev_rect = pygame.Rect(WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT - 60, 100, 35)
                if prev_rect.collidepoint(event.pos) and self.current_step > 0:
                    self.prev_step()
                    return True

                # 检查下一步按钮
                next_rect = pygame.Rect(WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT - 60, 100, 35)
                if next_rect.collidepoint(event.pos):
                    self.next_step()
                    return True

                # 点击其他区域也进入下一步
                self.next_step()
                return True

        return True  # 阻止事件传递

    def update(self):
        """更新教程状态"""
        self.animation_time += 1

    def render(self, screen):
        """渲染教程界面"""
        if not self.visible:
            return

        step = self.steps[self.current_step]

        # 创建半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # 高亮区域（如果有）
        if step.highlight_area:
            x, y, w, h = step.highlight_area
            # 闪烁效果
            alpha = int(100 + 50 * abs(pygame.math.Vector2(1, 0).rotate(self.animation_time * 3).x))
            highlight_surface = pygame.Surface((w + 10, h + 10), pygame.SRCALPHA)
            pygame.draw.rect(highlight_surface, (*COLORS['gold'], alpha), (0, 0, w + 10, h + 10), 3, border_radius=5)
            screen.blit(highlight_surface, (x - 5, y - 5))

        # 教程面板
        panel_width = 500
        panel_height = 280
        panel_x = (WINDOW_WIDTH - panel_width) // 2
        panel_y = (WINDOW_HEIGHT - panel_height) // 2

        # 面板背景
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (*COLORS['panel_bg'], 240),
                        (0, 0, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(panel_surface, COLORS['gold'],
                        (0, 0, panel_width, panel_height), 3, border_radius=10)
        screen.blit(panel_surface, (panel_x, panel_y))

        # 步骤指示器
        indicator_y = panel_y + 15
        total_steps = len(self.steps)
        indicator_width = 200
        indicator_x = panel_x + (panel_width - indicator_width) // 2

        for i in range(total_steps):
            dot_x = indicator_x + (indicator_width // total_steps) * i + (indicator_width // total_steps) // 2
            color = COLORS['gold'] if i == self.current_step else COLORS['gray']
            pygame.draw.circle(screen, color, (dot_x, indicator_y), 6)

        # 标题
        title_font = self.resource_loader.get_font('large')
        title_text = title_font.render(step.title, True, COLORS['gold'])
        title_rect = title_text.get_rect(centerx=panel_x + panel_width // 2, top=panel_y + 40)
        screen.blit(title_text, title_rect)

        # 描述
        desc_font = self.resource_loader.get_font('default')
        lines = step.description.split('\n')
        for i, line in enumerate(lines):
            text = desc_font.render(line, True, COLORS['white'])
            text_rect = text.get_rect(centerx=panel_x + panel_width // 2, top=panel_y + 85 + i * 28)
            screen.blit(text, text_rect)

        # 操作提示
        if step.action_hint:
            hint_font = self.resource_loader.get_font('small')
            hint_text = hint_font.render(step.action_hint, True, COLORS['yellow'])
            hint_rect = hint_text.get_rect(centerx=panel_x + panel_width // 2, top=panel_y + 180)
            screen.blit(hint_text, hint_rect)

        # 导航按钮
        button_font = self.resource_loader.get_font('default')
        button_y = panel_y + panel_height - 50

        # 上一步按钮
        if self.current_step > 0:
            prev_rect = pygame.Rect(panel_x + 70, button_y, 100, 35)
            pygame.draw.rect(screen, COLORS['button_normal'], prev_rect, border_radius=5)
            pygame.draw.rect(screen, COLORS['panel_border'], prev_rect, 2, border_radius=5)
            prev_text = button_font.render("上一步", True, COLORS['white'])
            prev_text_rect = prev_text.get_rect(center=prev_rect.center)
            screen.blit(prev_text, prev_text_rect)

        # 下一步/完成按钮
        next_text = "完成" if self.current_step == len(self.steps) - 1 else "下一步"
        next_rect = pygame.Rect(panel_x + panel_width - 170, button_y, 100, 35)
        pygame.draw.rect(screen, COLORS['button_normal'], next_rect, border_radius=5)
        pygame.draw.rect(screen, COLORS['gold'], next_rect, 2, border_radius=5)
        next_btn_text = button_font.render(next_text, True, COLORS['white'])
        next_btn_rect = next_btn_text.get_rect(center=next_rect.center)
        screen.blit(next_btn_text, next_btn_rect)

        # 跳过按钮
        skip_font = self.resource_loader.get_font('small')
        skip_text = skip_font.render("跳过教程", True, COLORS['light_gray'])
        skip_rect = skip_text.get_rect(right=panel_x + panel_width - 20, top=panel_y + panel_height - 30)
        screen.blit(skip_text, skip_rect)

    def should_show(self):
        """是否应该显示教程"""
        return self.enabled and not self.tutorial_started

    def save_state(self):
        """保存教程状态"""
        return {
            'enabled': self.enabled,
            'tutorial_started': self.tutorial_started,
            'current_step': self.current_step
        }

    def load_state(self, state):
        """加载教程状态"""
        if state:
            self.enabled = state.get('enabled', True)
            self.tutorial_started = state.get('tutorial_started', False)
            self.current_step = state.get('current_step', 0)