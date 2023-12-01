import random
import json

class Bird:
    def __init__(self, id):
        self.height = 50  # 初始高度
        self.velocity = 0  # 初始速度
        self.is_dead = False
        self.id = id

    def flap(self):
        # 向上移动时的速度变化
        self.velocity = -8

    def update(self):
        # 模拟重力影响
        self.velocity += 1
        self.height += self.velocity
        self.height = max(0, self.height)  # 防止小鸟掉落地面以下


    def to_object(self):
        return {
            'id': self.id,
            'dead': 1 if self.is_dead else 0,
            'height': self.height,
            'velocity': self.velocity
        }

class Pipe:
    def __init__(self, id, x, gap_center, gap_size):
        self.id = id
        self.x = x
        self.gap_center = gap_center
        self.gap_size = gap_size

    def update(self):
        # 管道向左移动
        self.x -= 2

    def is_off_screen(self):
        # 如果管道完全移出屏幕，则表示可以移除
        return self.x < -50  # 假设管道宽度

    def to_object(self):
        return {
            'id': self.id,
            'x': self.x,
            'gap_center': self.gap_center,
            'gap_size': self.gap_size
        }

class Game:
    screen_height = 450
    screen_width = 640
    pipe_frequency = 90
    pipe_id = 0
    score = 0
    pipes = []
    birds = []
    game_over = False
    frame_count = 0

    def __init__(self, bird_count=1):
        self.start_game(bird_count)

    def start_game(self, bird_count):
        self.pipe_id = 0
        self.score = 0
        self.frame_count = 0
        self.game_over = False
        self.birds = []
        self.pipes = []
        for i in range(max(1, bird_count)):
            self.birds.append(Bird(i + 1))

    def update(self):
        if self.game_over:
            return

        # 更新小鸟的状态
        for bird in self.birds:
            bird.update()

        # 增加新管道
        if self.frame_count % self.pipe_frequency == 0:
            gap_center = random.randint(100, self.screen_height - 30)  # 假设游戏界面高度为480
            new_pipe = Pipe(self.gen_pipe_id(), self.screen_width, gap_center, 100)  # gap_size为管道间隙的大小
            self.pipes.append(new_pipe)

        # 更新所有管道的状态
        for pipe in self.pipes:
            pipe.update()

        # 移除离开屏幕的管道
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

        # 检查是否发生碰撞
        self.check_for_collision()

        # 更新得分和帧数
        self.update_score_and_frames()

    def check_for_collision(self):
        for bird in self.birds:
            if bird.is_dead:
                continue
            # 检查是否飞出上方或下方屏幕
            if bird.height <= 0 or bird.height >= self.screen_height:
                bird.is_dead = True
                continue
            for pipe in self.pipes:
                if pipe.x < 100 < pipe.x + 50:  # 假设小鸟处于屏幕的100的位置，管道宽度是50
                    # 如果在垂直位置与管道的隙缝位置不匹配，则碰撞
                    upper_pipe_bottom = pipe.gap_center - pipe.gap_size / 2
                    lower_pipe_top = pipe.gap_center + pipe.gap_size / 2
                    if not (upper_pipe_bottom < bird.height < lower_pipe_top):
                        bird.is_dead = True

    def update_score_and_frames(self):
        self.game_over = True
        for bird in self.birds:
            if not bird.is_dead:
                self.game_over = False
        if self.game_over:
            print("Game Over!")
            print(f"Final Score: {self.score}")
        else:
            self.frame_count += 1
            # 计算分数：根据通过的管道数量计算分数
            self.score = self.frame_count // self.pipe_frequency

    def gen_pipe_id(self):
        self.pipe_id += 1
        return self.pipe_id

    def to_json(self):
        game_data = {
            'screen_height': self.screen_height,
            'screen_width': self.screen_width,
            'pipe_frequency': self.pipe_frequency,
            'current_score': self.score,
            'game_over': self.game_over,
            'frame_count': self.frame_count,
            'pipes': [pipe.to_object() for pipe in self.pipes],
            'birds': [bird.to_object() for bird in self.birds]
        }
        return json.dumps(game_data, indent=4)