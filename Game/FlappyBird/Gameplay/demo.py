import flappy_bird
import flappy_bird_pygame_handler as handler


game = flappy_bird.Game(bird_count=1)

inputer = handler.Inputter()
renderer = handler.Renderer(game, "./../Resources/")

game_loop = flappy_bird.GameLooper(game, renderer, inputer)

game_loop.GameLoop()
