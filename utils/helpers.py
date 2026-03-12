"""
工具函数
"""
import math
import random


def distance(x1, y1, x2, y2):
    """计算两点距离"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def normalize(value, min_val, max_val):
    """归一化值到0-1范围"""
    return (value - min_val) / (max_val - min_val)


def clamp(value, min_val, max_val):
    """限制值在范围内"""
    return max(min_val, min(max_val, value))


def lerp(start, end, t):
    """线性插值"""
    return start + (end - start) * t


def random_in_range(min_val, max_val):
    """返回范围内的随机数"""
    return random.randint(min_val, max_val)


def weighted_choice(choices, weights):
    """加权随机选择

    Args:
        choices: 选择列表
        weights: 权重列表

    Returns:
        选中的元素
    """
    total = sum(weights)
    r = random.uniform(0, total)
    cumsum = 0
    for choice, weight in zip(choices, weights):
        cumsum += weight
        if r <= cumsum:
            return choice
    return choices[-1]


def format_number(num):
    """格式化数字显示"""
    if num >= 100000000:
        return f"{num / 100000000:.1f}亿"
    elif num >= 10000:
        return f"{num / 10000:.1f}万"
    else:
        return str(num)


def get_color_blend(color1, color2, t):
    """颜色混合

    Args:
        color1: 颜色1 (r, g, b)
        color2: 颜色2 (r, g, b)
        t: 混合比例 (0-1)

    Returns:
        混合后的颜色
    """
    return tuple(int(lerp(c1, c2, t)) for c1, c2 in zip(color1, color2))