import random
import json

PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
LAND_RATE = 0.79
class Bird:
    def __init__(self, id):
        self.height = 50
        self.velocity = 0
        self.angle = 0
        self.is_dead = False
        self.id = id
        self.score = 0

    def flap(self):
        self.velocity = - 4

    def update(self):
        self.velocity += 9.8 / 60
        #self.velocity = min(10, self.velocity)
        self.height = self.height + self.velocity
        self.angle = self.angle + (- self.velocity * 3 - self.angle) * 0.3

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
    def __init__(self, bird_count=1, screen_height=512, screen_width=288, move_speed=2, bird_size=(34, 24), seek = 0):
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.pipe_frequency = 300
        self.pipe_width = 50
        self.move_speed = move_speed
        self.bird_size = bird_size
        self.seek = seek
        self.land_rate = LAND_RATE
        self.start_game(bird_count)

    def start_game(self, bird_count):
        self.birds = [Bird(i + 1) for i in range(max(1, bird_count))]
        self.pipes = []
        self.game_over = False
        self.score = 0
        self.frame_count = 0
        self.world_pos = 0
        self.last_world_pos = 0
        self.pipe_id = 0
        self.rng = random.Random(self.seek)

    def update(self):
        if self.game_over:
            return
        # 更新小鸟的状态
        for bird in self.birds:
            if not bird.is_dead:
                bird.update()
                bird.score = self.frame_count

        # 更新管道的状态，移除屏幕外的管道
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]
        for pipe in self.pipes:
            pipe.move(self.move_speed)
        self.last_world_pos = self.world_pos
        self.world_pos -= self.move_speed

        # 增加新管道
        if abs(int(self.world_pos)) % self.pipe_frequency < abs(int(self.last_world_pos)) % self.pipe_frequency:
            gap_center = self.rng.randrange(int(self.screen_height * LAND_RATE * 0.2),
                                          int(self.screen_height * LAND_RATE * 0.8 - PIPEGAPSIZE / 2))
            self.pipes.append(
                Pipe(self.pipe_id, self.screen_width, gap_center,  PIPEGAPSIZE, self.pipe_width))
            self.pipe_id += 1

        # 检查小鸟是否撞到管道或飞出屏幕范围
        self.check_for_collision()

        # 更新得分和帧数
        if len(self.pipes) > 0 and self.pipes[0].x < 100:
            self.score = self.pipes[0].id + 1
        self.frame_count += 1
        self.game_over = all(bird.is_dead for bird in self.birds)

    def check_for_collision(self):
        for bird in self.birds:
            if bird.is_dead:
                continue
            # 检查小鸟是否飞出上方或者下方屏幕
            if bird.height <= 0 or bird.height >= self.screen_height * self.land_rate:
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
                    break

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
        while True:
            self.game.update()  # 更新游戏状态
            if self.renderer:
                self.renderer.renderer(self.game)  # 渲染游戏
            if not self.inputter.oninput(self.game):
                if self.renderer:
                    self.renderer.quit()
                return



