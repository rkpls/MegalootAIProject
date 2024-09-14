from tensorforce.agents import Agent
from tensorforce.execution import Runner

# Instantiate environment
environment = GameEnv()

# Define agent configuration
agent = Agent.create(
    agent='tensorforce', environment=environment,
    update=64, objective='policy_gradient',
    reward_estimation=dict(horizon=20)
)

# Train the agent
runner = Runner(agent=agent, environment=environment)
runner.run(num_episodes=1000)
runner.close()
