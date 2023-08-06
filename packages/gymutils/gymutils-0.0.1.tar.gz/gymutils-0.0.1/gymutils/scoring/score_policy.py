import numpy as np


def get_score(env, policy, terminal_reward=1, episodes=1000, max_steps=10_000):
    # From https://medium.com/analytics-vidhya/solving-the-frozenlake-environment-from-openai-gym-using-value-iteration-5a078dffe438
    misses = 0
    steps_list = []
    for _ in range(episodes):
        observation = env.reset()
        steps = 0
        while steps < max_steps:
            action = policy[observation]
            observation, reward, done, _ = env.step(action)
            steps += 1
            if done and reward == terminal_reward:
                steps_list.append(steps)
                break
            elif done and reward == 0:
                misses += 1
                break

    return np.mean(steps_list), (1 - (misses/episodes))
