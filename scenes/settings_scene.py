"""
设置场景 - 游戏设置界面
"""
import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT
from ui.button import Button
from scenes.base_scene import BaseScene


class SettingsScene(BaseScene):
    """设置场景类"""

    def __init__(self, game_manager):
        """初始化设置场景"""
        super().__init__(game_manager)
        self.sound_manager = game_manager.sound_manager

        # 设置值
        self.master_volume = self.sound_manager.master_volume
        self.music_volume = self.sound_manager.music_volume
        self.sfx_volume = self.sound_manager.sfx_volume

        # 滑块状态
        self.dragging_slider = None

        # 创建UI
        self._create_ui()

    def _create_ui(self):
        """创建UI元素"""
        center_x = WINDOW_WIDTH // 2

        # 返回按钮
        self.back_button = Button(
            center_x - 100, WINDOW_HEIGHT - 80, 200, 45,
            "返回", self._on_back
        )

        # 滑块位置
        slider_x = center_x - 150
        slider_width = 300
        slider_height = 20

        self.sliders = {
            'master': {
                'rect': pygame.Rect(slider_x, 180, slider_width, slider_height),
                'value': self.master_volume,
                'label': '主音量'
            },
            'music': {
                'rect': pygame.Rect(slider_x, 280, slider_width, slider_height),
                'value': self.music_volume,
                'label': '音乐音量'
            },
            'sfx': {
                'rect': pygame.Rect(slider_x, 380, slider_width, slider_height),
                'value': self.sfx_volume,
                'label': '音效音量'
            }
        }

    def _on_back(self):
        """返回按钮回调"""
        self.game_manager.play_sound('cancel')
        # 应用设置
        self._apply_settings()
        # 保存设置到文件
        self.game_manager.save_settings()
        self.game_manager.scene_manager.load_scene('main_menu')

    def _apply_settings(self):
        """应用音量设置"""
        self.sound_manager.set_master_volume(self.sliders['master']['value'])
        self.sound_manager.set_music_volume(self.sliders['music']['value'])
        self.sound_manager.set_sfx_volume(self.sliders['sfx']['value'])
        self.logger.info(f"音量设置已应用 - 主音量: {self.sliders['master']['value']:.2f}, "
                   f"音乐: {self.sliders['music']['value']:.2f}, "
                   f"音效: {self.sliders['sfx']['value']:.2f}")

    def handle_event(self, event):
        """处理事件"""
        self.back_button.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键
                mouse_pos = pygame.mouse.get_pos()
                for name, slider in self.sliders.items():
                    if slider['rect'].collidepoint(mouse_pos):
                        self.dragging_slider = name
                        self._update_slider_value(name, mouse_pos[0])

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging_slider = None

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_slider:
                mouse_pos = pygame.mouse.get_pos()
                self._update_slider_value(self.dragging_slider, mouse_pos[0])

    def _update_slider_value(self, slider_name, mouse_x):
        """更新滑块值"""
        slider = self.sliders[slider_name]
        rect = slider['rect']

        # 计算值（0.0 - 1.0）
        relative_x = mouse_x - rect.x
        value = max(0.0, min(1.0, relative_x / rect.width))
        slider['value'] = value

        # 实时预览音量变化
        if slider_name == 'master':
            self.sound_manager.set_master_volume(value)
        elif slider_name == 'music':
            self.sound_manager.set_music_volume(value)
        elif slider_name == 'sfx':
            self.sound_manager.set_sfx_volume(value)
            # 播放测试音效
            self.game_manager.play_sound('click')

    def update(self):
        """更新场景"""
        self.back_button.update()

    def render(self, screen):
        """渲染场景"""
        # 绘制背景
        self._draw_background(screen)

        # 绘制标题
        title_font = self.resource_loader.get_font('title')
        title_text = title_font.render("游戏设置", True, COLORS['gold'])
        title_rect = title_text.get_rect(centerx=WINDOW_WIDTH // 2, top=80)
        screen.blit(title_text, title_rect)

        # 绘制滑块
        for name, slider in self.sliders.items():
            self._draw_slider(screen, slider)

        # 绘制返回按钮
        self.back_button.render(screen, self.resource_loader)

    def _draw_background(self, screen):
        """绘制背景"""
        self._draw_gradient_background(screen, (20, 30, 60), (50, 45, 80))

    def _draw_slider(self, screen, slider):
        """绘制滑块"""
        font = self.resource_loader.get_font('large')

        # 绘制标签
        label_text = font.render(slider['label'], True, COLORS['white'])
        screen.blit(label_text, (slider['rect'].x, slider['rect'].y - 30))

        # 绘制滑块轨道
        pygame.draw.rect(screen, COLORS['gray'], slider['rect'], border_radius=5)

        # 绘制滑块填充部分
        fill_width = int(slider['rect'].width * slider['value'])
        if fill_width > 0:
            fill_rect = pygame.Rect(
                slider['rect'].x,
                slider['rect'].y,
                fill_width,
                slider['rect'].height
            )
            pygame.draw.rect(screen, COLORS['gold'], fill_rect, border_radius=5)

        # 绘制滑块手柄
        handle_x = slider['rect'].x + fill_width
        handle_rect = pygame.Rect(handle_x - 10, slider['rect'].y - 5, 20, 30)
        pygame.draw.rect(screen, COLORS['white'], handle_rect, border_radius=3)

        # 绘制百分比
        percent_text = font.render(f"{int(slider['value'] * 100)}%", True, COLORS['light_gray'])
        screen.blit(percent_text, (slider['rect'].right + 20, slider['rect'].y))