import sys

import numpy as np

sys.path.append("./AI/GA_NN/")
import json
from Gameplay import flappy_bird
from AI.GA_NN.ga_nn_ai_handler import GA_NN_Inputter
from Gameplay.flappy_bird_pygame_handler import Renderer

BIRD_COUNT = 40
ITERATOR = 100000
MUTATION_PROBABILITY = 0.25
USE_MODEL = 1
SAVE_MODEL = 1
TRAIN_MOED = 0

game = flappy_bird.Game(bird_count=BIRD_COUNT if TRAIN_MOED else 1, seek=None)

inputer = GA_NN_Inputter(BIRD_COUNT, ITERATOR, MUTATION_PROBABILITY, TRAIN_MOED > 0)
renderer = Renderer(game, "./Resources/", 720 if TRAIN_MOED else 120)

if USE_MODEL or not TRAIN_MOED:
    models = []
    with open("model.json", "r") as f:
        models = json.loads(f.read())
    for i in range(len(models)):
        if i < BIRD_COUNT:
            inputer.bird_models[i].set_model([np.array(item) for item in models[i]])
        else:
            break

game_loop = flappy_bird.GameLooper(game, renderer, inputer)

game_loop.GameLoop()

if SAVE_MODEL:
    models = []
    sorted_pairs = sorted(zip(game.birds, inputer.bird_models), key=lambda pair: pair[0].score, reverse=True)
    for bird, bird_model in sorted_pairs:
        model = bird_model.get_model()
        models.append([item.tolist() for item in model])
    with open("model.json", "w") as f:
        f.write(json.dumps(models))
