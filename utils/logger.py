"""
日志系统 - 提供游戏运行日志记录功能
"""
import logging
import os
from datetime import datetime
from config import BASE_DIR


class GameLogger:
    """游戏日志管理器"""

    _instance = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """初始化日志系统"""
        if self._initialized:
            return

        self._initialized = True
        self.log_dir = os.path.join(BASE_DIR, 'logs')

        # 确保日志目录存在
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # 创建日志记录器
        self.logger = logging.getLogger('ThreeKingdoms')
        self.logger.setLevel(logging.DEBUG)

        # 避免重复添加处理器
        if not self.logger.handlers:
            # 文件处理器 - 按日期命名
            log_filename = os.path.join(
                self.log_dir,
                f'game_{datetime.now().strftime("%Y%m%d")}.log'
            )
            file_handler = logging.FileHandler(
                log_filename,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)

            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # 格式化器
            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # 添加处理器
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        self.info("日志系统初始化完成")

    def debug(self, message):
        """记录调试信息"""
        self.logger.debug(message)

    def info(self, message):
        """记录一般信息"""
        self.logger.info(message)

    def warning(self, message):
        """记录警告信息"""
        self.logger.warning(message)

    def error(self, message):
        """记录错误信息"""
        self.logger.error(message)

    def critical(self, message):
        """记录严重错误"""
        self.logger.critical(message)

    def game_event(self, event_type, details):
        """记录游戏事件

        Args:
            event_type: 事件类型 (battle, diplomacy, economy, etc.)
            details: 事件详情
        """
        self.info(f"[{event_type.upper()}] {details}")

    def battle_log(self, attacker, defender, result):
        """记录战斗日志"""
        self.game_event('battle', f"{attacker} vs {defender}: {result}")

    def economy_log(self, city, action, amount):
        """记录经济日志"""
        self.game_event('economy', f"{city} - {action}: {amount}")

    def diplomacy_log(self, faction1, faction2, action):
        """记录外交日志"""
        self.game_event('diplomacy', f"{faction1} <-> {faction2}: {action}")


def get_logger():
    """获取日志管理器实例"""
    return GameLogger()