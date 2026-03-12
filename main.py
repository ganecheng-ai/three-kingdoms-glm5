"""
三国霸业游戏主入口
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS, COLORS
from game.game_manager import GameManager


def main():
    """游戏主函数"""
    # 初始化 Pygame
    pygame.init()
    pygame.font.init()

    # 创建窗口
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    # 创建时钟
    clock = pygame.time.Clock()

    # 创建游戏管理器
    game_manager = GameManager(screen)

    # 游戏主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game_manager.handle_event(event)

        # 更新游戏状态
        game_manager.update()

        # 渲染
        screen.fill(COLORS['background'])
        game_manager.render()
        pygame.display.flip()

        # 控制帧率
        clock.tick(FPS)

    # 清理资源
    game_manager.cleanup()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()