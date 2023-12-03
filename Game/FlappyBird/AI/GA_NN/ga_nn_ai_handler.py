import math
import pygame
import numpy as np
import NN
import copy



class GA_NN_Inputter:
    bird_count = 50,
    iterator = 10
    pm = 0.1 #变异的概率
    def __init__(self, bird_count = 50, iterator = 10, pm = 0.1, train_mode = True):
        self.bird_models = []
        self.bird_count = bird_count
        self.iterator = iterator
        self.game_round = 0
        self.train_mode = train_mode
        self.init_bird_model()

    def init_bird_model(self):
        for i in range(self.bird_count):
            nn = NN.NeuralNetwork()
            nn.add_layer(NN.Layer(3, 7), NN.sigmoid, None)
            nn.add_layer(NN.Layer(7, 1), NN.sigmoid, None)
            self.bird_models.append(nn)

    def oninput(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        if game.game_over:
            if not self.train_mode or self.game_round >= self.iterator:
                return True
            else:
                print(game.frame_count)
                self.GA(game)
                game.start_game(self.bird_count)
                self.game_round += 1
        else:
            for i in range(len(game.birds)):
                if not game.birds[i].is_dead:
                    if self.get_bird_input(game, i) <= 0.5:
                        game.birds[i].flap()
        return True

    ## 获取当前鸟的NN输入
    def get_bird_input(self, game, bird_idx):
        input = np.array([min(game.birds[bird_idx].height, game.screen_height * game.land_rate) / game.screen_height / game.land_rate - 0.5,
            next((pipe.x - 80 for pipe in game.pipes if pipe.x > 80), game.screen_width) / game.screen_width - 0.5,
            next((pipe.gap_center - game.birds[bird_idx].height for pipe in game.pipes if pipe.x > 80), 0) / game.screen_height - 0.5])

        output = self.bird_models[bird_idx].forward(input)[0]
        return output

    @staticmethod
    def model_crossover(model1, model2):
        model1 = model1.get_model()
        model2 = model2.get_model()
        model1[0], model2[0] = model2[0], model1[0]
        return [model1, model2]

    def model_mutate(self, weights):
        new_weights = []
        for weight in weights:
            new_weight = copy.deepcopy(weight)
            noise = np.random.uniform(-0.5, 0.5, size=weight.shape)
            prob_matrix = np.random.random(weight.shape)
            new_weight[prob_matrix <= self.pm] += noise[prob_matrix <= self.pm]
            new_weights.append(new_weight)
        return new_weights

    ## 遗传算法
    def GA(self, game):
        bird_num = len(game.birds)
        fitness = np.array([bird.score for bird in game.birds])
        fitness = fitness / np.sum(fitness)
        new_model = []
        for i in range(bird_num // 4):
            parents_indices = np.random.choice(bird_num, 2, p=fitness)

            #复制
            new_model.append(self.bird_models[parents_indices[0]].get_model())
            new_model.append(self.bird_models[parents_indices[1]].get_model())

            #交叉
            child_models = self.model_crossover(
                self.bird_models[parents_indices[0]], self.bird_models[parents_indices[1]])

            #变异
            child_models[0] = self.model_mutate(child_models[0])
            child_models[1] = self.model_mutate(child_models[1])

            new_model.append(child_models[0])
            new_model.append(child_models[1])

        for i in range(len(new_model)):
            self.bird_models[i].set_model(new_model[i])