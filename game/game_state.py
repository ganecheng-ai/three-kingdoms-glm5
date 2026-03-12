"""
游戏状态管理器 - 管理游戏存档和读档
"""
import json
import os
from datetime import datetime
from config import VERSION
from utils.logger import get_logger

logger = get_logger()


class GameState:
    """游戏状态类"""

    def __init__(self, game_manager):
        """初始化游戏状态管理器

        Args:
            game_manager: 游戏管理器实例
        """
        self.game_manager = game_manager
        self.save_dir = os.path.join(os.path.dirname(__file__), '..', 'saves')
        self.ensure_save_dir()

    def ensure_save_dir(self):
        """确保存档目录存在"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def get_save_path(self, slot):
        """获取存档文件路径

        Args:
            slot: 存档槽位 (1-5)

        Returns:
            存档文件路径
        """
        return os.path.join(self.save_dir, f'save_{slot}.json')

    def save_game(self, slot, game_data):
        """保存游戏

        Args:
            slot: 存档槽位 (1-5)
            game_data: 游戏数据字典

        Returns:
            是否成功
        """
        try:
            # 添加保存时间
            game_data['save_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            game_data['slot'] = slot

            save_path = self.get_save_path(slot)
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"保存游戏失败: {e}")
            return False

    def load_game(self, slot):
        """加载游戏

        Args:
            slot: 存档槽位 (1-5)

        Returns:
            游戏数据字典或None
        """
        try:
            save_path = self.get_save_path(slot)
            if not os.path.exists(save_path):
                return None

            with open(save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 数据完整性校验
            required_fields = ['version', 'player_faction', 'turn', 'factions', 'cities', 'generals']
            for field in required_fields:
                if field not in data:
                    logger.error(f"存档数据不完整，缺少字段: {field}")
                    return None

            # 版本兼容性检查
            save_version = data.get('version', '0.0.0')
            if not self._check_version_compatibility(save_version):
                logger.warning(f"存档版本 {save_version} 与当前版本 {VERSION} 可能不兼容")

            logger.info(f"成功加载存档槽位 {slot}, 版本: {save_version}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"存档文件格式错误: {e}")
            return None
        except Exception as e:
            logger.error(f"加载游戏失败: {e}")
            return None

    def _check_version_compatibility(self, save_version):
        """检查版本兼容性

        Args:
            save_version: 存档版本号

        Returns:
            是否兼容
        """
        try:
            # 解析版本号
            save_parts = [int(x) for x in save_version.split('.')]
            current_parts = [int(x) for x in VERSION.split('.')]

            # 主版本号相同则兼容
            if save_parts[0] == current_parts[0]:
                return True

            return False
        except (ValueError, IndexError):
            return False

    def get_save_info(self, slot):
        """获取存档信息

        Args:
            slot: 存档槽位 (1-5)

        Returns:
            存档信息字典或None
        """
        data = self.load_game(slot)
        if data:
            return {
                'slot': slot,
                'save_time': data.get('save_time', '未知'),
                'player_faction': data.get('player_faction', '未知'),
                'turn': data.get('turn', 0),
                'year': data.get('year', 0),
                'month': data.get('month', 0),
            }
        return None

    def delete_save(self, slot):
        """删除存档

        Args:
            slot: 存档槽位 (1-5)

        Returns:
            是否成功
        """
        try:
            save_path = self.get_save_path(slot)
            if os.path.exists(save_path):
                os.remove(save_path)
            return True
        except Exception as e:
            print(f"删除存档失败: {e}")
            return False

    def list_saves(self):
        """列出所有存档

        Returns:
            存档信息列表
        """
        saves = []
        for slot in range(1, 6):
            info = self.get_save_info(slot)
            saves.append(info)
        return saves

    def export_game_data(self, factions, cities, generals, turn, year, month, player_faction):
        """导出游戏数据

        Args:
            factions: 势力字典
            cities: 城市字典
            generals: 武将字典
            turn: 回合数
            year: 游戏年份
            month: 游戏月份
            player_faction: 玩家势力

        Returns:
            游戏数据字典
        """
        return {
            'version': VERSION,
            'player_faction': player_faction,
            'turn': turn,
            'year': year,
            'month': month,
            'factions': {name: f.to_dict() for name, f in factions.items()},
            'cities': {name: c.to_dict() for name, c in cities.items()},
            'generals': {name: g.to_dict() for name, g in generals.items()},
        }

    def import_game_data(self, data):
        """导入游戏数据

        Args:
            data: 游戏数据字典

        Returns:
            (factions, cities, generals, turn, year, month, player_faction)
        """
        from entities.faction import Faction
        from entities.city import City
        from entities.general import General

        factions = {}
        for name, f_data in data.get('factions', {}).items():
            factions[name] = Faction.from_dict(f_data)

        cities = {}
        for name, c_data in data.get('cities', {}).items():
            cities[name] = City.from_dict(c_data)

        generals = {}
        for name, g_data in data.get('generals', {}).items():
            generals[name] = General.from_dict(g_data)

        turn = data.get('turn', 1)
        year = data.get('year', 190)
        month = data.get('month', 1)
        player_faction = data.get('player_faction', '魏')

        return factions, cities, generals, turn, year, month, player_faction