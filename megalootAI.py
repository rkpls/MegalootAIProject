from Environment import GameEnv
from stable_baselines3 import DQN
from gymnasium.wrappers import RecordVideo
import gym

env = gym.make("CartPole-v1")
env = RecordVideo(env, video_folder="./videos")

# Initialize your environment
env = GameEnv()

# Initialize the model
model = DQN("MlpPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=50000)

# Save the trained model
model.save("game_ai_model")

# Load the trained model
model = DQN.load("game_ai_model")

# Run the model in your environment
obs, info = env.reset()  # Now reset returns (observation, info)
for step in range(1000):
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)  # step returns additional values now
    
    # Check if the episode is over
    if terminated or truncated:
        obs, info = env.reset()  # Reset the environment after episode ends
