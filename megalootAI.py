from Environment import GameEnv
from stable_baselines3 import DQN
from gymnasium.wrappers import RecordVideo
import gym

env = gym.make("CartPole-v1")
env = GameEnv()
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=500000, log_interval=10, tb_log_name="DQN_logs")
model.save("game_ai_model")
model = DQN.load("game_ai_model")
obs, info = env.reset()
for step in range(10):
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
