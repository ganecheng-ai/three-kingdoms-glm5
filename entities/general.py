"""
武将实体类
"""


class General:
    """武将类"""

    def __init__(self, name, faction, force, intelligence, command, politics, city):
        """初始化武将

        Args:
            name: 武将名称
            faction: 所属势力
            force: 武力值 (1-100)
            intelligence: 智力值 (1-100)
            command: 统率值 (1-100)
            politics: 政治值 (1-100)
            city: 所在城市
        """
        self.name = name
        self.faction = faction
        self.force = force
        self.intelligence = intelligence
        self.command = command
        self.politics = politics
        self.city = city

        # 状态
        self.hp = 100  # 生命值
        self.mp = 100  # 技力值
        self.morale = 100  # 士气
        self.fatigue = 0  # 疲劳度

        # 技能
        self.skills = []
        self.equipment = {}

    @property
    def total_power(self):
        """计算武将综合战力"""
        return (self.force * 1.2 + self.intelligence * 0.8 +
                self.command * 1.0 + self.politics * 0.5)

    def add_skill(self, skill_name):
        """添加技能"""
        if skill_name not in self.skills:
            self.skills.append(skill_name)

    def rest(self):
        """休息恢复"""
        self.fatigue = max(0, self.fatigue - 20)
        self.hp = min(100, self.hp + 10)
        self.mp = min(100, self.mp + 10)

    def to_dict(self):
        """转换为字典"""
        return {
            'name': self.name,
            'faction': self.faction,
            'force': self.force,
            'intelligence': self.intelligence,
            'command': self.command,
            'politics': self.politics,
            'city': self.city,
            'skills': self.skills,
            'equipment': self.equipment,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建武将"""
        general = cls(
            data['name'],
            data['faction'],
            data['force'],
            data['intelligence'],
            data['command'],
            data['politics'],
            data['city']
        )
        general.skills = data.get('skills', [])
        general.equipment = data.get('equipment', {})
        return general