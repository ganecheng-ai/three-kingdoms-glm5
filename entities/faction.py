"""
势力实体类
"""


class Faction:
    """势力类"""

    def __init__(self, name, leader, capital):
        """初始化势力

        Args:
            name: 势力名称
            leader: 领袖名称
            capital: 首都城市
        """
        self.name = name
        self.leader = leader
        self.capital = capital

        # 势力属性
        self.cities = []  # 所属城市列表
        self.generals = []  # 所属武将列表
        self.prestige = 0  # 声望

        # 外交关系 (势力名: 关系值 -100~100)
        self.relations = {}

        # 资源
        self.gold = 0
        self.food = 0

    def add_city(self, city_name):
        """添加城市"""
        if city_name not in self.cities:
            self.cities.append(city_name)

    def remove_city(self, city_name):
        """移除城市"""
        if city_name in self.cities:
            self.cities.remove(city_name)

    def add_general(self, general_name):
        """添加武将"""
        if general_name not in self.generals:
            self.generals.append(general_name)

    def remove_general(self, general_name):
        """移除武将"""
        if general_name in self.generals:
            self.generals.remove(general_name)

    def set_relation(self, faction_name, value):
        """设置外交关系"""
        self.relations[faction_name] = max(-100, min(100, value))

    def get_relation(self, faction_name):
        """获取外交关系"""
        return self.relations.get(faction_name, 0)

    def is_allied(self, faction_name):
        """是否同盟"""
        return self.get_relation(faction_name) >= 50

    def is_enemy(self, faction_name):
        """是否敌对"""
        return self.get_relation(faction_name) <= -50

    def calculate_power(self):
        """计算势力实力"""
        # 基于城市数量、武将数量、资源等
        city_power = len(self.cities) * 100
        general_power = len(self.generals) * 50
        resource_power = self.gold // 100 + self.food // 1000
        return city_power + general_power + resource_power + self.prestige

    def to_dict(self):
        """转换为字典"""
        return {
            'name': self.name,
            'leader': self.leader,
            'capital': self.capital,
            'cities': self.cities,
            'generals': self.generals,
            'prestige': self.prestige,
            'relations': self.relations,
            'gold': self.gold,
            'food': self.food,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建势力"""
        faction = cls(data['name'], data['leader'], data['capital'])
        faction.cities = data.get('cities', [])
        faction.generals = data.get('generals', [])
        faction.prestige = data.get('prestige', 0)
        faction.relations = data.get('relations', {})
        faction.gold = data.get('gold', 0)
        faction.food = data.get('food', 0)
        return faction