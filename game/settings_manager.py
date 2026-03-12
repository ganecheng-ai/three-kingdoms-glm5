"""
设置管理器 - 管理游戏设置的持久化存储
"""
import json
import os
from utils.logger import get_logger

logger = get_logger()


class SettingsManager:
    """设置管理器类"""

    def __init__(self):
        """初始化设置管理器"""
        self.settings_file = 'settings.json'
        self.settings = self._get_default_settings()

    def _get_default_settings(self):
        """获取默认设置"""
        return {
            'master_volume': 1.0,
            'music_volume': 0.7,
            'sfx_volume': 1.0,
            'muted': False,
            'tutorial_completed': False,
        }

    def load_settings(self):
        """从文件加载设置

        Returns:
            设置字典
        """
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    # 合并保存的设置和默认设置（处理新版本新增的设置项）
                    for key, value in saved_settings.items():
                        if key in self.settings:
                            self.settings[key] = value
                    logger.info("设置已从文件加载")
            except Exception as e:
                logger.warning(f"加载设置失败: {e}，使用默认设置")
                self.settings = self._get_default_settings()
        else:
            logger.info("设置文件不存在，使用默认设置")

        return self.settings

    def save_settings(self):
        """保存设置到文件

        Returns:
            是否保存成功
        """
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            logger.info("设置已保存到文件")
            return True
        except Exception as e:
            logger.error(f"保存设置失败: {e}")
            return False

    def get_setting(self, key, default=None):
        """获取单个设置项

        Args:
            key: 设置项名称
            default: 默认值

        Returns:
            设置值
        """
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        """设置单个设置项

        Args:
            key: 设置项名称
            value: 设置值
        """
        self.settings[key] = value
        logger.debug(f"设置已更新: {key} = {value}")

    def get_all_settings(self):
        """获取所有设置

        Returns:
            设置字典
        """
        return self.settings.copy()

    def apply_to_sound_manager(self, sound_manager):
        """将设置应用到音效管理器

        Args:
            sound_manager: 音效管理器实例
        """
        if sound_manager:
            sound_manager.master_volume = self.settings.get('master_volume', 1.0)
            sound_manager.music_volume = self.settings.get('music_volume', 0.7)
            sound_manager.sfx_volume = self.settings.get('sfx_volume', 1.0)
            sound_manager.muted = self.settings.get('muted', False)
            logger.info("音量设置已应用到音效管理器")


# 全局设置管理器实例
_settings_manager = None


def get_settings_manager():
    """获取全局设置管理器实例"""
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager