"""
AI系统 - 管理AI势力的行为决策
"""
import random


class AISystem:
    """AI系统类"""

    def __init__(self):
        """初始化AI系统"""
        self.ai_personalities = {
            'aggressive': {'attack_chance': 0.7, 'recruit_priority': 0.8},
            'defensive': {'attack_chance': 0.3, 'recruit_priority': 0.5},
            'balanced': {'attack_chance': 0.5, 'recruit_priority': 0.6},
            'expansive': {'attack_chance': 0.6, 'recruit_priority': 0.7},
        }

        # 势力性格
        self.faction_personalities = {
            '魏': 'aggressive',
            '蜀': 'balanced',
            '吴': 'defensive',
            '吕布': 'aggressive',
            '袁绍': 'expansive',
            '袁术': 'aggressive',
            '公孙瓒': 'aggressive',
            '马腾': 'expansive',
            '董卓': 'aggressive',
        }

    def get_personality(self, faction_name):
        """获取势力性格"""
        return self.faction_personalities.get(faction_name, 'balanced')

    def process_turn(self, faction_name, faction, cities, generals, player_faction):
        """处理AI势力的回合

        Args:
            faction_name: 势力名称
            faction: 势力对象
            cities: 城市字典
            generals: 武将字典
            player_faction: 玩家势力

        Returns:
            行动日志列表
        """
        logs = []
        personality = self.get_personality(faction_name)
        config = self.ai_personalities.get(personality, self.ai_personalities['balanced'])

        # 处理城市发展
        for city_name in faction.cities:
            if city_name in cities:
                city = cities[city_name]
                logs.extend(self._develop_city(city, config))

        # AI军事决策
        logs.extend(self._military_decisions(faction_name, faction, cities, config, player_faction))

        # AI外交决策
        logs.extend(self._diplomacy_decisions(faction_name, faction, cities))

        return logs

    def _develop_city(self, city, config):
        """城市发展决策"""
        logs = []

        # 招募士兵
        recruit_priority = config.get('recruit_priority', 0.6)
        if random.random() < recruit_priority:
            if city.gold > 1000 and city.population > 2000:
                recruit_count = min(1000, city.population // 5)
                if city.recruit_soldiers(recruit_count):
                    logs.append(f"{city.name}招募了{recruit_count}名士兵")

        # 建筑升级
        if city.gold > 5000 and random.random() < 0.3:
            building = random.choice(['farm', 'market', 'barracks', 'wall'])
            current_level = city.buildings.get(building, 1)
            upgrade_cost = current_level * 2000
            if city.gold >= upgrade_cost:
                city.gold -= upgrade_cost
                city.buildings[building] = current_level + 1
                logs.append(f"{city.name}升级了{building}")

        return logs

    def _military_decisions(self, faction_name, faction, cities, config, player_faction):
        """军事决策"""
        logs = []
        attack_chance = config.get('attack_chance', 0.5)

        # 计算总兵力
        total_soldiers = 0
        for city_name in faction.cities:
            if city_name in cities:
                total_soldiers += cities[city_name].soldiers

        # 如果兵力充足，考虑进攻
        if total_soldiers > 10000 and random.random() < attack_chance:
            # 寻找目标城市
            target = self._find_attack_target(faction_name, faction, cities)
            if target:
                logs.append(f"{faction_name}准备进攻{target}")
                # 这里可以触发战斗事件

        return logs

    def _find_attack_target(self, faction_name, faction, cities):
        """寻找攻击目标"""
        # 获取势力城市列表和兵力最多的城市
        my_cities = []
        strongest_city = None
        max_soldiers = 0

        for city_name in faction.cities:
            if city_name in cities:
                city = cities[city_name]
                my_cities.append(city)
                if city.soldiers > max_soldiers:
                    max_soldiers = city.soldiers
                    strongest_city = city

        if not my_cities or not strongest_city:
            return None

        # 寻找最近的敌方城市（兵力少于己方最强城市）
        best_target = None
        min_distance = float('inf')

        for city_name, city in cities.items():
            if city.faction != faction_name:
                # 使用己方兵力最多的城市作为比较基准
                dist = ((city.x - strongest_city.x) ** 2 + (city.y - strongest_city.y) ** 2) ** 0.5
                if dist < min_distance and city.soldiers < strongest_city.soldiers:
                    min_distance = dist
                    best_target = city_name

        return best_target

    def _diplomacy_decisions(self, faction_name, faction, cities):
        """外交决策"""
        logs = []

        # 根据势力情况决定外交策略
        total_power = sum(cities[cn].soldiers for cn in faction.cities if cn in cities)

        # 弱小势力可能寻求结盟
        if total_power < 5000 and random.random() < 0.3:
            logs.append(f"{faction_name}寻求结盟")

        return logs

    def evaluate_threat(self, faction_name, cities):
        """评估威胁等级"""
        threat_level = 0

        for city_name, city in cities.items():
            if city.faction != faction_name:
                # 根据敌方城市兵力评估威胁
                threat_level += city.soldiers * 0.01

        return threat_level

    def decide_defense(self, city, threat_level):
        """决定防御策略"""
        if threat_level > city.soldiers:
            return 'reinforce'  # 需要增援
        elif threat_level > city.soldiers * 0.5:
            return 'alert'  # 保持警惕
        else:
            return 'normal'  # 正常状态


# 全局AI系统实例
_ai_system = None


def get_ai_system():
    """获取全局AI系统实例"""
    global _ai_system
    if _ai_system is None:
        _ai_system = AISystem()
    return _ai_system