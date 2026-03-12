"""
军队实体类
"""
import math


class Army:
    """军队类"""

    def __init__(self, faction, general, city_x, city_y):
        """初始化军队

        Args:
            faction: 所属势力
            general: 主将名称
            city_x: 起始X坐标
            city_y: 起始Y坐标
        """
        self.faction = faction
        self.general = general

        # 位置
        self.x = city_x
        self.y = city_y
        self.target_x = city_x
        self.target_y = city_y

        # 兵力
        self.infantry = 0  # 步兵
        self.cavalry = 0  # 骑兵
        self.archer = 0  # 弓兵

        # 状态
        self.morale = 100  # 士气
        self.fatigue = 0  # 疲劳度
        self.is_moving = False
        self.move_speed = 5

    @property
    def total_soldiers(self):
        """总兵力"""
        return self.infantry + self.cavalry + self.archer

    @property
    def combat_power(self):
        """战斗力"""
        # 步兵基础战力较低，骑兵中等，弓兵较高但防御低
        infantry_power = self.infantry * 1.0
        cavalry_power = self.cavalry * 1.5
        archer_power = self.archer * 1.2

        # 士气加成
        morale_bonus = self.morale / 100

        # 疲劳减益
        fatigue_penalty = max(0.5, 1 - self.fatigue / 200)

        return (infantry_power + cavalry_power + archer_power) * morale_bonus * fatigue_penalty

    def set_target(self, x, y):
        """设置移动目标"""
        self.target_x = x
        self.target_y = y
        self.is_moving = True

    def update_position(self):
        """更新位置"""
        if not self.is_moving:
            return

        # 计算方向
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance <= self.move_speed:
            # 到达目标
            self.x = self.target_x
            self.y = self.target_y
            self.is_moving = False
            self.fatigue = min(100, self.fatigue + 10)
        else:
            # 移动
            self.x += (dx / distance) * self.move_speed
            self.y += (dy / distance) * self.move_speed

    def rest(self):
        """休息恢复"""
        self.fatigue = max(0, self.fatigue - 20)
        self.morale = min(100, self.morale + 5)

    def take_damage(self, casualties):
        """受到伤亡"""
        # 按比例分配伤亡
        total = self.total_soldiers
        if total == 0:
            return

        ratio = casualties / total
        self.infantry = max(0, int(self.infantry * (1 - ratio)))
        self.cavalry = max(0, int(self.cavalry * (1 - ratio)))
        self.archer = max(0, int(self.archer * (1 - ratio)))

        # 士气下降
        self.morale = max(0, self.morale - casualties // 100)

    def merge(self, other_army):
        """合并军队"""
        self.infantry += other_army.infantry
        self.cavalry += other_army.cavalry
        self.archer += other_army.archer
        # 平均士气
        total = self.total_soldiers + other_army.total_soldiers
        if total > 0:
            self.morale = int((self.morale * self.total_soldiers +
                               other_army.morale * other_army.total_soldiers) / total)

    def to_dict(self):
        """转换为字典"""
        return {
            'faction': self.faction,
            'general': self.general,
            'x': self.x,
            'y': self.y,
            'infantry': self.infantry,
            'cavalry': self.cavalry,
            'archer': self.archer,
            'morale': self.morale,
            'fatigue': self.fatigue,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建军队"""
        army = cls(data['faction'], data['general'], data['x'], data['y'])
        army.infantry = data.get('infantry', 0)
        army.cavalry = data.get('cavalry', 0)
        army.archer = data.get('archer', 0)
        army.morale = data.get('morale', 100)
        army.fatigue = data.get('fatigue', 0)
        return army