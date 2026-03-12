"""
城市实体类
"""


class City:
    """城市类"""

    def __init__(self, name, faction, population, gold, food, soldiers, x, y):
        """初始化城市

        Args:
            name: 城市名称
            faction: 所属势力
            population: 人口
            gold: 金钱
            food: 粮草
            soldiers: 兵员
            x: 地图X坐标
            y: 地图Y坐标
        """
        self.name = name
        self.faction = faction
        self.population = population
        self.gold = gold
        self.food = food
        self.soldiers = soldiers
        self.x = x
        self.y = y

        # 城市属性
        self.defense = 100  # 城防值
        self.order = 100  # 治安值

        # 建筑
        self.buildings = {
            'farm': 1,  # 农田等级
            'market': 1,  # 市场等级
            'barracks': 1,  # 兵营等级
            'wall': 1,  # 城墙等级
        }

        # 武将列表
        self.generals = []

    def add_general(self, general_name):
        """添加武将"""
        if general_name not in self.generals:
            self.generals.append(general_name)

    def remove_general(self, general_name):
        """移除武将"""
        if general_name in self.generals:
            self.generals.remove(general_name)

    def calculate_income(self):
        """计算收入"""
        gold_income = int(self.population * 0.01 * self.buildings['market'])
        food_income = int(self.population * 0.02 * self.buildings['farm'])
        return gold_income, food_income

    def recruit_soldiers(self, count):
        """招募士兵"""
        gold_cost = count * 10
        if self.gold >= gold_cost and self.population >= count:
            self.gold -= gold_cost
            self.population -= count
            self.soldiers += count
            return True
        return False

    def update(self):
        """更新城市状态（每月调用）"""
        # 计算收入
        gold_income, food_income = self.calculate_income()
        self.gold += gold_income
        self.food += food_income

        # 消耗粮草
        food_consume = int(self.soldiers * 0.1)
        self.food -= food_consume

        # 人口增长
        if self.order > 50:
            growth = int(self.population * 0.01)
            self.population += growth

    def to_dict(self):
        """转换为字典"""
        return {
            'name': self.name,
            'faction': self.faction,
            'population': self.population,
            'gold': self.gold,
            'food': self.food,
            'soldiers': self.soldiers,
            'x': self.x,
            'y': self.y,
            'defense': self.defense,
            'order': self.order,
            'buildings': self.buildings,
            'generals': self.generals,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建城市"""
        city = cls(
            data['name'],
            data['faction'],
            data['population'],
            data['gold'],
            data['food'],
            data['soldiers'],
            data['x'],
            data['y']
        )
        city.defense = data.get('defense', 100)
        city.order = data.get('order', 100)
        city.buildings = data.get('buildings', {'farm': 1, 'market': 1, 'barracks': 1, 'wall': 1})
        city.generals = data.get('generals', [])
        return city