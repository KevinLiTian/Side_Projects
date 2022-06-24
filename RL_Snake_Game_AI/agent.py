import torch
import random
import numpy as np
from collections import deque

from game import SnakeGameAI, Direction, Point, BLOCK_SIZE
from model import Linear_QNet, QTrainer
from plot import plot

USE_TRAINED_MODEL = False

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001 # Learning rate
INPUT_SIZE = 11
HIDDEN_SIZE = 256
OUTPUT_SIZE = 3
GAMMA = 0.9


class Agent():
    """ The Agent of the Snake Game"""
    def __init__(self):
        self.n_games = 0 # number of games
        self.epsilon = 0 # Control randomness
        self.gamma = GAMMA # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # if memory exceeded, then popleft()

        # Learning model
        self.model = Linear_QNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
        if USE_TRAINED_MODEL:
            self.model.load_state_dict(torch.load('model/trained_model2.pth'))
            self.model.eval()

        # Trainer
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        """
        There are 11 booleans to help determine the current state of the game
        They are:
        danger in straight, right or left, 3
        move direction in one of the four directions, 4
        food location relative to the snake in four directions, 4
        """
        # Calculate the tiles neighbouring snake head
        head = game.snake[0]
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)
        
        # Boolean of current direction of the snake
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right (Collision in next clocowise direction)
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left (Collision in previous clocowise direction)
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        # Convert 11 boolean in state to int array
        return np.array(state, dtype=int)
        

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        # If there are enough data, then randomly select 1000 data
        # Otherwise use all the data
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        # Extract each item from mini sample
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        final_move = [0, 0, 0]
        if USE_TRAINED_MODEL:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        else:  
            # Random moves/Model predicted moves
            # Trade of between exploration and exploitation
            self.epsilon = 80 - self.n_games # More games, smaller epsilon

            # Less games -> More random moves
            # More games -> More predicted moves
            if random.randint(0, 200) < self.epsilon:
                move = random.randint(0, 2)
                final_move[move] = 1

            # Predicted Moves using Pytorch tensors
            else:
                state0 = torch.tensor(state, dtype=torch.float)
                prediction = self.model(state0)
                move = torch.argmax(prediction).item()
                final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record =  0
    agent = Agent()
    game = SnakeGameAI()

    # Training loop
    while True:
        # Get old state
        state_old = agent.get_state(game)

        # Get move based on current state
        final_move = agent.get_action(state_old)

        # Perform move and get new state
        reward, game_over, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # Remember all the data
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            # Reset the game, plus number of games by 1
            # Train long memory
            # Plot the result so far
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save('model.pth')

            print('Game', agent.n_games, 'Score', score, 'Record', record)

            # Plot the scores
            plot_scores.append(score)
            total_score += score
            mean_scores = total_score / agent.n_games
            plot_mean_scores.append(mean_scores)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()