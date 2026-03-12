"""
战斗系统
"""
import random


class BattleSystem:
    """战斗系统类"""

    def __init__(self):
        """初始化战斗系统"""
        self.battle_log = []

    def calculate_damage(self, attacker, defender):
        """计算伤害

        Args:
            attacker: 攻击方军队
            defender: 防守方军队

        Returns:
            伤害值
        """
        # 基础伤害 = 攻击方战力 * 随机因子
        base_damage = attacker.combat_power * random.uniform(0.8, 1.2)

        # 防御减伤
        defense_factor = 1 - (defender.combat_power * 0.0001)
        defense_factor = max(0.3, min(0.9, defense_factor))

        # 地形加成（简化）
        terrain_bonus = 1.0

        damage = int(base_damage * defense_factor * terrain_bonus)
        return damage

    def battle_round(self, attacker, defender):
        """进行一回合战斗

        Args:
            attacker: 攻击方军队
            defender: 防守方军队

        Returns:
            战斗结果字典
        """
        # 攻击方攻击
        damage_to_defender = self.calculate_damage(attacker, defender)
        defender.take_damage(damage_to_defender)

        # 防守方反击（如果还有兵力）
        if defender.total_soldiers > 0:
            damage_to_attacker = self.calculate_damage(defender, attacker)
            attacker.take_damage(damage_to_attacker)
        else:
            damage_to_attacker = 0

        return {
            'attacker_damage': damage_to_attacker,
            'defender_damage': damage_to_defender,
            'attacker_remaining': attacker.total_soldiers,
            'defender_remaining': defender.total_soldiers,
        }

    def simulate_battle(self, attacker, defender, max_rounds=100):
        """模拟完整战斗

        Args:
            attacker: 攻击方军队
            defender: 防守方军队
            max_rounds: 最大回合数

        Returns:
            战斗结果
        """
        self.battle_log = []
        round_num = 0

        while round_num < max_rounds:
            round_num += 1

            result = self.battle_round(attacker, defender)
            self.battle_log.append(f"回合 {round_num}: 攻方损失{result['attacker_damage']}, 守方损失{result['defender_damage']}")

            # 检查战斗结束
            if attacker.total_soldiers <= 0:
                return {
                    'winner': 'defender',
                    'rounds': round_num,
                    'log': self.battle_log
                }

            if defender.total_soldiers <= 0:
                return {
                    'winner': 'attacker',
                    'rounds': round_num,
                    'log': self.battle_log
                }

            # 士气检查
            if attacker.morale < 20:
                return {
                    'winner': 'defender',
                    'reason': 'attacker_routed',
                    'rounds': round_num,
                    'log': self.battle_log
                }

            if defender.morale < 20:
                return {
                    'winner': 'attacker',
                    'reason': 'defender_routed',
                    'rounds': round_num,
                    'log': self.battle_log
                }

        # 回合数用尽，判定为平局
        return {
            'winner': 'draw',
            'rounds': max_rounds,
            'log': self.battle_log
        }

    def siege_battle(self, attacker, defender, city):
        """攻城战

        Args:
            attacker: 攻击方军队
            defender: 防守方军队
            city: 城市对象

        Returns:
            战斗结果
        """
        # 城防加成
        defense_bonus = 1 + city.defense / 100

        # 攻城战伤害调整
        damage_to_attacker = self.calculate_damage(defender, attacker) * 1.5
        damage_to_defender = self.calculate_damage(attacker, defender) / defense_bonus

        attacker.take_damage(int(damage_to_attacker))
        defender.take_damage(int(damage_to_defender))

        # 减少城防
        city.defense = max(0, city.defense - attacker.total_soldiers // 100)

        return {
            'attacker_remaining': attacker.total_soldiers,
            'defender_remaining': defender.total_soldiers,
            'city_defense': city.defense,
        }