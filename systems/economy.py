"""
经济系统
"""


class EconomySystem:
    """经济系统类"""

    def __init__(self):
        """初始化经济系统"""
        self.tax_rate = 0.1  # 默认税率 10%
        self.inflation = 1.0  # 通货膨胀率

    def calculate_city_income(self, city):
        """计算城市收入

        Args:
            city: 城市对象

        Returns:
            (金钱收入, 粮草收入)
        """
        # 基础收入
        base_gold = city.population * self.tax_rate
        base_food = city.population * 0.02

        # 建筑加成
        market_bonus = 1 + city.buildings.get('market', 1) * 0.2
        farm_bonus = 1 + city.buildings.get('farm', 1) * 0.2

        gold_income = int(base_gold * market_bonus)
        food_income = int(base_food * farm_bonus)

        # 治安影响
        order_factor = city.order / 100

        return int(gold_income * order_factor), int(food_income * order_factor)

    def calculate_upkeep(self, city):
        """计算维护费用

        Args:
            city: 城市对象

        Returns:
            (金钱维护, 粮草消耗)
        """
        # 军队维护
        gold_upkeep = city.soldiers * 0.5  # 每士兵0.5金钱
        food_consumption = city.soldiers * 0.1  # 每士兵0.1粮草

        # 武将俸禄
        general_salary = len(city.generals) * 100

        return int(gold_upkeep + general_salary), int(food_consumption)

    def process_turn(self, cities):
        """处理回合经济

        Args:
            cities: 城市字典
        """
        for city in cities.values():
            # 收入
            gold_income, food_income = self.calculate_city_income(city)
            city.gold += gold_income
            city.food += food_income

            # 支出
            gold_upkeep, food_consumption = self.calculate_upkeep(city)
            city.gold -= gold_upkeep
            city.food -= food_consumption

            # 资源下限为0
            city.gold = max(0, city.gold)
            city.food = max(0, city.food)

            # 人口变化
            if city.food > 0 and city.order > 50:
                growth_rate = 0.01 * (city.order / 100)
                city.population += int(city.population * growth_rate)

            # 如果粮草不足，人口下降，士气下降
            if city.food <= 0:
                city.population = int(city.population * 0.95)
                city.order = max(0, city.order - 5)

    def collect_tax(self, city, rate):
        """征收特别税

        Args:
            city: 城市对象
            rate: 税率

        Returns:
            征收金额
        """
        amount = int(city.population * rate)
        city.gold += amount
        city.order = max(0, city.order - int(rate * 100))
        return amount

    def recruit_soldiers(self, city, count):
        """招募士兵

        Args:
            city: 城市对象
            count: 招募数量

        Returns:
            是否成功
        """
        cost = count * 10  # 每士兵10金钱
        if city.gold >= cost and city.population >= count:
            city.gold -= cost
            city.population -= count
            city.soldiers += count
            return True
        return False