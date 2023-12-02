"""
Flappy bird游戏的pygame渲染器和输入器
"""
import os
import pygame

class Inputter:

    def oninput(self, game):
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
                    if event.key == pygame.K_SPACE:
                        game.start_game(1)
                    else:
                        pygame.quit()  # 退出游戏
                        return False
        return True


class Renderer:
    # 定义资源路径
    BIRD_IMAGE = 'bird.png'
    PIPE_IMAGE_UP = 'pipe_up.png'  # 需要一个朝上的管道图像
    PIPE_IMAGE_DOWN = 'pipe_down.png'  # 需要一个朝下的管道图像
    BG_IMAGE = 'bg.jpg'
    LAND_IMAGE = 'land.png'

    def __init__(self, game, resources_root):
        self.bird_img = pygame.image.load(os.path.join(resources_root, self.BIRD_IMAGE))
        self.bg_img = pygame.image.load(os.path.join(resources_root, self.BG_IMAGE))
        self.land_img = pygame.image.load(os.path.join(resources_root, self.LAND_IMAGE))
        self.pipe_img_up = pygame.image.load(os.path.join(resources_root, self.PIPE_IMAGE_UP))
        self.pipe_img_down = pygame.image.load(os.path.join(resources_root, self.PIPE_IMAGE_DOWN))

        # 初始化pygame
        pygame.init()

        pygame.display.set_caption("Flappy Bird")
        self.font = pygame.font.SysFont(None, 36)

        size = (game.screen_width, game.screen_height)
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()

    def renderer(self, game):
        # 绘制背景图片
        self.screen.blit(self.bg_img, (self.negative_mod(game.world_pos, game.screen_width), 0))
        self.screen.blit(self.bg_img, (self.negative_mod(game.world_pos, game.screen_width) + game.screen_width, 0))

        # 绘制管道
        for pipe in game.pipes:

            # 缩放管道图像以匹配pipe.width
            scaled_pipe_img_down = pygame.transform.scale(self.pipe_img_down,
                                                          (pipe.width, self.pipe_img_down.get_height()))
            scaled_pipe_img_up = pygame.transform.scale(self.pipe_img_up,
                                                        (pipe.width, self.pipe_img_up.get_height()))

            # 计算管道下部分和上部分的Y坐标
            pipe_upper_y = pipe.gap_center - (scaled_pipe_img_down.get_height() + pipe.gap_size // 2)
            pipe_lower_y = pipe.gap_center + pipe.gap_size // 2

            # 绘制管道
            self.screen.blit(scaled_pipe_img_down, (pipe.x, pipe_upper_y))
            self.screen.blit(scaled_pipe_img_up, (pipe.x, pipe_lower_y))



        # 绘制小鸟
        for bird in game.birds:
            bird_img = pygame.transform.scale(self.bird_img, game.bird_size)
            bird_img = pygame.transform.rotate(bird_img, bird.angle)
            self.screen.blit(bird_img, (100, int(bird.height)))

        # 显示得分
        score_surface = self.font.render('Score: ' + str(game.score), True, (0, 0, 0))
        self.screen.blit(score_surface, (10, 10))

        # 更新屏幕
        pygame.display.flip()
        # 帧率控制: 30 FPS
        return self.clock.tick(60) / 1000.0

    def quit(self):
        pygame.quit()

    @staticmethod
    def negative_mod(n, m):
        return n % m if n >= 0 else -(abs(n) % m)

