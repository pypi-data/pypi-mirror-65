import numpy as np
from collections import namedtuple


def q_learning(env, learning_rate=0.1, gamma=0.95, epsilon=1.0, max_epsilon=1.0, min_epsilon=0.5, decay_rate=0.0001,
               total_episodes=10_000, max_steps_per_episode=2000, decay=True):
    # From https://python-data-science.readthedocs.io/en/latest/reinforcement.html
    action_size = env.action_space.n
    state_size = env.observation_space.n

    qtable = np.zeros((state_size, action_size))

    EpisodeStats = namedtuple(
        "Stats", ["episode_lengths", "episode_rewards", "episode_deltas"])

    stats = EpisodeStats(
        episode_lengths=np.zeros(total_episodes),
        episode_deltas=np.zeros(total_episodes),
        episode_rewards=np.zeros(total_episodes))

    for episode in range(total_episodes):
        state = env.reset()
        total_rewards = 0

        for step in range(max_steps_per_episode):
            exp_exp_tradeoff = np.random.uniform(0, 1)
            action = None
            # If this number > greater than epsilon --> exploitation (taking the biggest Q value for this state)
            if exp_exp_tradeoff > epsilon:
                action = np.argmax(qtable[state, :])
            # Else doing a random choice --> exploration
            else:
                action = env.action_space.sample()

            # Take the action (a) and observe the outcome state(s') and reward (r)
            new_state, reward, done, _ = env.step(action)
            # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
            # qtable[new_state,:] : all the actions we can take from new state
            delta = (reward + (gamma *
                               np.max(qtable[new_state, :])) - qtable[state, action])

            qtable[state, action] += learning_rate * delta
            total_rewards += reward
            state = new_state

            if done == True:
                stats.episode_deltas[episode] = delta
                stats.episode_rewards[episode] += total_rewards
                stats.episode_lengths[episode] = step
                break

        if decay:
            epsilon = min_epsilon + \
                (max_epsilon - min_epsilon) * \
                np.exp(-decay_rate*episode)

    V = np.reshape(np.max(qtable, axis=1), env.desc.shape)
    policy = np.reshape(np.argmax(qtable, axis=1), env.desc.shape)

    return qtable, policy, V, stats
