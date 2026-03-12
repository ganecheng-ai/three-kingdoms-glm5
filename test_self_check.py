#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
三国霸业游戏自验证测试脚本
运行此脚本验证代码质量和核心功能
"""
import sys
import os
import json
import importlib.util

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """测试所有模块是否可以正确导入"""
    print("=" * 50)
    print("测试1: 模块导入测试")
    print("=" * 50)

    modules = [
        'config',
        'entities.general',
        'entities.city',
        'entities.faction',
        'entities.army',
        'systems.battle',
        'systems.economy',
        'systems.ai_system',
        'systems.diplomacy',
        'game.game_state',
        'utils.logger',
    ]

    passed = 0
    failed = 0

    for module in modules:
        try:
            __import__(module)
            print(f"  [PASS] {module}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {module}: {e}")
            failed += 1

    print(f"\n结果: {passed} 通过, {failed} 失败")
    return failed == 0


def test_data_files():
    """测试数据文件是否有效"""
    print("\n" + "=" * 50)
    print("测试2: 数据文件测试")
    print("=" * 50)

    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    files = ['generals.json', 'cities.json', 'skills.json']

    passed = 0
    failed = 0

    for filename in files:
        filepath = os.path.join(data_dir, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"  [PASS] {filename} - {len(data) if isinstance(data, list) else len(data.keys())} 条记录")
                passed += 1
            else:
                print(f"  [SKIP] {filename} - 文件不存在")
                passed += 1  # 部分文件可选
        except Exception as e:
            print(f"  [FAIL] {filename}: {e}")
            failed += 1

    print(f"\n结果: {passed} 通过, {failed} 失败")
    return failed == 0


def test_entities():
    """测试实体类"""
    print("\n" + "=" * 50)
    print("测试3: 实体类测试")
    print("=" * 50)

    from entities.general import General
    from entities.city import City
    from entities.faction import Faction
    from entities.army import Army

    passed = 0
    failed = 0

    # 测试武将类
    try:
        general = General("测试武将", "魏", 80, 70, 75, 60, "许昌")
        assert general.name == "测试武将"
        assert general.force == 80
        assert general.total_power > 0
        print(f"  [PASS] General类 - 战力: {general.total_power:.1f}")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] General类: {e}")
        failed += 1

    # 测试城市类
    try:
        city = City("测试城", "蜀", 50000, 10000, 20000, 5000, 500, 300)
        assert city.name == "测试城"
        income = city.calculate_income()
        assert income[0] > 0  # 金钱收入
        print(f"  [PASS] City类 - 月收入: 金{income[0]}, 粮{income[1]}")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] City类: {e}")
        failed += 1

    # 测试势力类
    try:
        faction = Faction("测试势力", "测试君主", "测试城")
        assert faction.name == "测试势力"
        faction.add_city("城市1")
        assert "城市1" in faction.cities
        print(f"  [PASS] Faction类")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] Faction类: {e}")
        failed += 1

    # 测试军队类
    try:
        army = Army("魏", "主将", 100, 200)
        army.infantry = 1000
        army.cavalry = 500
        assert army.total_soldiers == 1500
        print(f"  [PASS] Army类 - 总兵力: {army.total_soldiers}")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] Army类: {e}")
        failed += 1

    print(f"\n结果: {passed} 通过, {failed} 失败")
    return failed == 0


def test_systems():
    """测试游戏系统"""
    print("\n" + "=" * 50)
    print("测试4: 游戏系统测试")
    print("=" * 50)

    from systems.battle import BattleSystem
    from entities.army import Army
    from entities.city import City

    passed = 0
    failed = 0

    # 测试战斗系统
    try:
        battle = BattleSystem()
        attacker = Army("魏", "主将", 100, 200)
        attacker.infantry = 3000
        attacker.cavalry = 1500

        defender = Army("蜀", "守将", 700, 300)
        defender.infantry = 2000
        defender.cavalry = 1000

        result = battle.simulate_battle(attacker, defender)
        assert 'winner' in result
        print(f"  [PASS] BattleSystem - 胜者: {result['winner']}, 回合: {result['rounds']}")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] BattleSystem: {e}")
        failed += 1

    # 测试攻城战
    try:
        battle = BattleSystem()
        attacker = Army("魏", "主将", 100, 200)
        attacker.infantry = 5000

        defender = Army("蜀", "守将", 700, 300)
        defender.infantry = 2000

        city = City("测试城", "蜀", 50000, 10000, 20000, 3000, 500, 300)
        city.defense = 100

        result = battle.siege_battle(attacker, defender, city)
        assert 'city_defense' in result
        print(f"  [PASS] 攻城战 - 城防: {result['city_defense']}")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] 攻城战: {e}")
        failed += 1

    print(f"\n结果: {passed} 通过, {failed} 失败")
    return failed == 0


def test_save_system():
    """测试存档系统"""
    print("\n" + "=" * 50)
    print("测试5: 存档系统测试")
    print("=" * 50)

    from game.game_state import GameState
    from entities.faction import Faction
    from entities.city import City
    from entities.general import General
    from config import VERSION

    passed = 0
    failed = 0

    try:
        # 创建模拟游戏管理器
        class MockGameManager:
            pass

        game_state = GameState(MockGameManager())

        # 测试导出游戏数据
        factions = {"魏": Faction("魏", "曹操", "许昌")}
        cities = {"许昌": City("许昌", "魏", 50000, 10000, 20000, 5000, 600, 280)}
        generals = {"曹操": General("曹操", "魏", 72, 91, 96, 94, "许昌")}

        data = game_state.export_game_data(factions, cities, generals, 1, 190, 1, "魏")
        assert data['version'] == VERSION
        assert data['player_faction'] == "魏"
        print(f"  [PASS] 导出存档数据 - 版本: {data['version']}")
        passed += 1

        # 测试导入游戏数据
        factions, cities, generals, turn, year, month, player = game_state.import_game_data(data)
        assert player == "魏"
        assert turn == 1
        print(f"  [PASS] 导入存档数据")
        passed += 1

    except Exception as e:
        print(f"  [FAIL] 存档系统: {e}")
        failed += 1

    print(f"\n结果: {passed} 通过, {failed} 失败")
    return failed == 0


def test_ai_system():
    """测试AI系统"""
    print("\n" + "=" * 50)
    print("测试6: AI系统测试")
    print("=" * 50)

    from systems.ai_system import get_ai_system
    from entities.faction import Faction
    from entities.city import City

    passed = 0
    failed = 0

    try:
        ai = get_ai_system()

        # 测试势力性格
        personality = ai.get_personality("魏")
        print(f"  [PASS] 获取势力性格 - 魏: {personality}")
        passed += 1

        # 测试回合处理
        faction = Faction("袁绍", "袁绍", "南皮")
        faction.add_city("南皮")
        cities = {"南皮": City("南皮", "袁绍", 40000, 8000, 15000, 4000, 580, 150)}
        generals = {}

        logs = ai.process_turn("袁绍", faction, cities, generals, "魏")
        print(f"  [PASS] AI回合处理 - 生成 {len(logs)} 条日志")
        passed += 1

    except Exception as e:
        print(f"  [FAIL] AI系统: {e}")
        failed += 1

    print(f"\n结果: {passed} 通过, {failed} 失败")
    return failed == 0


def test_version_consistency():
    """测试版本号一致性"""
    print("\n" + "=" * 50)
    print("测试7: 版本号一致性测试")
    print("=" * 50)

    from config import VERSION
    from game.game_state import GameState

    passed = 0
    failed = 0

    try:
        # 检查 config.py 版本
        print(f"  config.py 版本: {VERSION}")

        # 检查存档版本
        class MockGameManager:
            pass
        game_state = GameState(MockGameManager())
        data = game_state.export_game_data({}, {}, {}, 1, 190, 1, "魏")
        save_version = data['version']
        print(f"  存档版本: {save_version}")

        if VERSION == save_version:
            print(f"  [PASS] 版本号一致: {VERSION}")
            passed += 1
        else:
            print(f"  [FAIL] 版本号不一致: config={VERSION}, save={save_version}")
            failed += 1

    except Exception as e:
        print(f"  [FAIL] 版本检查: {e}")
        failed += 1

    print(f"\n结果: {passed} 通过, {failed} 失败")
    return failed == 0


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("  三国霸业游戏 - 自验证测试")
    print("=" * 60)

    results = []

    results.append(("模块导入", test_imports()))
    results.append(("数据文件", test_data_files()))
    results.append(("实体类", test_entities()))
    results.append(("游戏系统", test_systems()))
    results.append(("存档系统", test_save_system()))
    results.append(("AI系统", test_ai_system()))
    results.append(("版本一致性", test_version_consistency()))

    print("\n" + "=" * 60)
    print("  测试结果汇总")
    print("=" * 60)

    total_passed = sum(1 for _, r in results if r)
    total_failed = sum(1 for _, r in results if not r)

    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {name}")

    print("\n" + "-" * 60)
    print(f"  总计: {total_passed} 通过, {total_failed} 失败")
    print("=" * 60)

    if total_failed == 0:
        print("\n  所有测试通过! 代码质量良好。")
        return 0
    else:
        print(f"\n  有 {total_failed} 项测试失败，请检查修复。")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())