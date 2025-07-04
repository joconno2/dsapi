"""
Requires neat_python==0.92

"""

from gamestate import GameState
import cv2 as cv
import neat
import time
import fitness_function
import key_output

def neat_output(pixel_input, net, action_space):
    # scale input down
    scale = 0.05
    pixel_input = cv.resize(pixel_input, (int(pixel_input.shape[1]*scale), int(pixel_input.shape[0]*scale)))
    
    pixel_input = cv.cvtColor(pixel_input, cv.COLOR_BGR2GRAY)

    network_output = net.activate(pixel_input.flatten())

    max_output = max(network_output)
    max_index = network_output.index(max_output)
    action_keys = list(action_space.keys())
    action_values = list(action_space.values())
    action_key = action_keys[max_index]
    action_value = action_values[max_index]

    return action_key, action_value

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        env = GameState()
        
        pixel_input = env.reset()

        start_time = time.time()
        end_time = time.time()

        terminated = False
        while not terminated:
            # lock onto enemy
            time_diff = 0.5
            if end_time - start_time > time_diff and not fitness_function.get_locked_on(pixel_input):
                env.send_input(key_output.q_char)
                start_time = time.time()
                end_time = time.time()
            end_time = time.time()

            action_key, action_value = neat_output(pixel_input, net, env.action_space)
            pixel_input, terminated = env.step(action_value)
            fitness = fitness_function.get_fitness(pixel_input)
            
            # debug
            print(f"Performing:".ljust(15), action_key)
            print(f"Fitness:".ljust(15), fitness)

        genome.fitness = fitness
        print("Terminated")
        time.sleep(5)

def run_neat(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 10)

if __name__ == "__main__":
    run_neat(config_path='config-feedforward.cfg')