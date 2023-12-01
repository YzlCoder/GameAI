"""
Flappy bird游戏的主流程负责渲染和输入
"""
import pygame
import flappy_bird

# 初始化pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game中的一些方法可能需要微调，这里暂时只提供game_input和game_render的实现

def game_input(game):
    # 处理游戏输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # 退出游戏
            return False
        elif event.type == pygame.KEYDOWN:
            if not game.game_over:
                if event.key == pygame.K_SPACE:
                    for bird in game.birds:
                        bird.flap()
            else:
                if event.key == pygame.K_RETURN:
                    game.start_game(1)
                else:
                    pygame.quit()  # 退出游戏
                    return False
    return True

def game_render(game):
    # 渲染游戏界面
    screen.fill(WHITE)  # 填充背景色

    # 绘制小鸟
    for bird in game.birds:
        pygame.draw.circle(screen, RED, (100, int(bird.height)), 10)

    # 绘制管道
    for pipe in game.pipes:
        upper_rect = pygame.Rect(pipe.x, 0, 50, int(pipe.gap_center - pipe.gap_size / 2))
        lower_rect = pygame.Rect(pipe.x, int(pipe.gap_center + pipe.gap_size / 2), 50, game.screen_height)
        pygame.draw.rect(screen, GREEN, upper_rect)
        pygame.draw.rect(screen, GREEN, lower_rect)

    # 显示得分
    score_surface = font.render('Score: ' + str(game.score), True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

    # 更新屏幕
    pygame.display.flip()

# 创建Game实例
g = flappy_bird.Game(bird_count=1)

# 设置屏幕大小
size = (g.screen_width, g.screen_height)
screen = pygame.display.set_mode(size)

# 设置字体和标题
pygame.display.set_caption("Flappy Bird")
font = pygame.font.SysFont(None, 36)


# 设置帧率
clock = pygame.time.Clock()

while True:
    # 处理输入
    if not game_input(g):
        break;
    if not g.game_over:
        g.update()  # 更新游戏状态

    game_render(g)  # 渲染游戏
    clock.tick(30)  # 帧率控制: 30 FPS

pygame.quit()  # 关闭游戏