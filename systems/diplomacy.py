"""
外交系统
"""


class DiplomacySystem:
    """外交系统类"""

    def __init__(self):
        """初始化外交系统"""
        self.relation_changes = {
            'alliance': 30,
            'trade': 10,
            'gift': 15,
            'war': -50,
            'betrayal': -80,
        }

    def send_gift(self, from_faction, to_faction, gold, food):
        """送礼

        Args:
            from_faction: 送礼势力
            to_faction: 收礼势力
            gold: 金钱数量
            food: 粮草数量

        Returns:
            关系变化
        """
        if from_faction.gold < gold or from_faction.food < food:
            return 0

        # 扣除资源
        from_faction.gold -= gold
        from_faction.food -= food
        to_faction.gold += gold
        to_faction.food += food

        # 计算关系提升
        relation_change = self.relation_changes['gift']
        current_relation = from_faction.get_relation(to_faction.name)
        from_faction.set_relation(to_faction.name, current_relation + relation_change)
        to_faction.set_relation(from_faction.name, current_relation + relation_change)

        return relation_change

    def propose_alliance(self, from_faction, to_faction):
        """提议结盟

        Args:
            from_faction: 提议方
            to_faction: 接受方

        Returns:
            (是否成功, 原因)
        """
        current_relation = from_faction.get_relation(to_faction.name)

        # 关系需要达到一定值才能结盟
        if current_relation < 30:
            return False, "关系不足"

        # 接受概率基于关系值
        accept_chance = min(80, current_relation + 20)

        import random
        if random.randint(0, 100) < accept_chance:
            # 结盟成功
            from_faction.set_relation(to_faction.name, current_relation + self.relation_changes['alliance'])
            to_faction.set_relation(from_faction.name, current_relation + self.relation_changes['alliance'])
            return True, "结盟成功"

        return False, "对方拒绝了结盟请求"

    def break_alliance(self, faction1, faction2):
        """解除同盟

        Args:
            faction1: 势力1
            faction2: 势力2
        """
        current_relation = faction1.get_relation(faction2.name)
        faction1.set_relation(faction2.name, current_relation - 30)
        faction2.set_relation(faction1.name, current_relation - 30)

    def declare_war(self, from_faction, to_faction):
        """宣战

        Args:
            from_faction: 宣战方
            to_faction: 被宣战方
        """
        current_relation = from_faction.get_relation(to_faction.name)
        from_faction.set_relation(to_faction.name, current_relation + self.relation_changes['war'])
        to_faction.set_relation(from_faction.name, current_relation + self.relation_changes['war'])

        # 通知其他势力
        # 这里可以添加外交事件系统

    def make_peace(self, faction1, faction2, tribute=None):
        """议和

        Args:
            faction1: 势力1
            faction2: 势力2
            tribute: 赔款 (金钱, 粮草)

        Returns:
            是否成功
        """
        current_relation = faction1.get_relation(faction2.name)

        # 赔款可以增加接受概率
        accept_chance = 50 + current_relation
        if tribute:
            gold, food = tribute
            accept_chance += gold // 1000 + food // 5000

        import random
        if random.randint(0, 100) < min(90, accept_chance):
            # 议和成功
            new_relation = max(0, current_relation + 20)
            faction1.set_relation(faction2.name, new_relation)
            faction2.set_relation(faction1.name, new_relation)

            if tribute:
                faction1.gold += tribute[0]
                faction1.food += tribute[1]
                faction2.gold -= tribute[0]
                faction2.food -= tribute[1]

            return True

        return False

    def get_diplomatic_status(self, faction1, faction2):
        """获取外交状态

        Args:
            faction1: 势力1
            faction2: 势力2

        Returns:
            状态字符串
        """
        relation = faction1.get_relation(faction2.name)

        if relation >= 50:
            return "同盟"
        elif relation >= 20:
            return "友好"
        elif relation >= -20:
            return "中立"
        elif relation >= -50:
            return "紧张"
        else:
            return "敌对"