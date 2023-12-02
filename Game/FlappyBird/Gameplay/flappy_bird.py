import random
import json

class Bird:
    def __init__(self, id):
        self.height = 50
        self.velocity = 0
        self.angle = 0
        self.is_dead = False
        self.id = id

    def flap(self):
        self.velocity = -4

    def update(self, delta):
        self.velocity += 9.8 * delta
        #self.velocity = min(10, self.velocity)
        self.height = self.height + self.velocity
        self.angle = self.angle + (-self.velocity * 2 - self.angle) * 0.3

class Pipe:
    def __init__(self, id, x, gap_center, gap_size, width):
        self.id = id
        self.x = x
        self.width = width
        self.gap_center = gap_center
        self.gap_size = gap_size

    def move(self, speed):
        self.x -= speed

    def is_off_screen(self):
        return self.x < - self.width

class Game:
    def __init__(self, bird_count=1, screen_height=450, screen_width=640, move_speed=2, bird_size=(34, 24)):
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.pipe_frequency = 180
        self.pipe_width = 50
        self.move_speed = move_speed
        self.bird_size = bird_size
        self.start_game(bird_count)

    def start_game(self, bird_count):
        self.birds = [Bird(i + 1) for i in range(max(1, bird_count))]
        self.pipes = []
        self.game_over = False
        self.score = 0
        self.frame_count = 0
        self.world_pos = 0
        self.pipe_id = 0

    def update(self, delta):
        if not self.game_over:
            # 更新小鸟的状态
            for bird in self.birds:
                bird.update(delta)

            # 更新管道的状态，移除屏幕外的管道
            self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]
            for pipe in self.pipes:
                pipe.move(self.move_speed)
            self.world_pos -= self.move_speed

            # 增加新管道
            if abs(self.world_pos) % self.pipe_frequency == 0:
                gap_center = random.randint(100, self.screen_height - 100)
                self.pipes.append(
                    Pipe(self.pipe_id,
                         self.screen_width,
                         gap_center,
                         100,
                         self.pipe_width))
                self.pipe_id += 1

        # 检查小鸟是否撞到管道或飞出屏幕范围
        self.check_for_collision()

        # 更新得分和帧数
        self.score = self.frame_count // self.pipe_frequency
        self.frame_count += 1
        self.game_over = all(bird.is_dead for bird in self.birds)

    def check_for_collision(self):
        for bird in self.birds:
            # 检查小鸟是否飞出上方或者下方屏幕
            if bird.height <= 0 or bird.height >= self.screen_height:
                bird.is_dead = True
                continue

            bird_rect = (
                100,
                bird.height,
                self.bird_size[0],
                self.bird_size[1]
            )
            for pipe in self.pipes:
                # 定义上下管道的矩形范围
                pipe_upper_rect = (
                    pipe.x, 0,
                    pipe.width,
                    pipe.gap_center - pipe.gap_size // 2
                )
                pipe_lower_rect = (
                    pipe.x,
                    pipe.gap_center + pipe.gap_size // 2,
                    pipe.width,
                    self.screen_height - pipe.gap_center - pipe.gap_size // 2
                )
                # 检测小鸟是否碰撞上部或下部管道
                if self.rects_collide(bird_rect, pipe_upper_rect) or self.rects_collide(bird_rect, pipe_lower_rect):
                    bird.is_dead = True

    @staticmethod
    def rects_collide(rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)

class GameLooper:

    def __init__(self, game, renderer, inputter):
        self.game = game
        self.renderer = renderer
        self.inputter = inputter


    def GameLoop(self):
        delta_time = 0
        while True:
            if not self.inputter.oninput(self.game):
                self.renderer.quit()
                return
            self.game.update(delta_time)  # 更新游戏状态
            delta_time = self.renderer.renderer(self.game)  # 渲染游戏

