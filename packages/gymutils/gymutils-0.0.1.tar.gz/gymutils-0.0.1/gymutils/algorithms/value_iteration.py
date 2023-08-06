import numpy as np


def value_iteration(env, theta=0.0001, discount_factor=0.9):
    """
    Value Iteration Algorithm.

    Args:
        env: OpenAI env. env.P represents the transition probabilities of the environment.
            env.P[s][a] is a list of transition tuples (prob, next_state, reward, done).
            env.nS is a number of states in the environment.
            env.nA is a number of actions in the environment.
        theta: We stop evaluation once our value function change is less than theta for all states.
        discount_factor: Gamma discount factor.

    Returns:
        A tuple (policy, V) of the optimal policy and the optimal value function.
    """

    def one_step_lookahead(state, V):
        """
        Helper function to calculate the value for all action in a given state.

        Args:
            state: The state to consider (int)
            V: The value to use as an estimator, Vector of length env.nS

        Returns:
            A vector of length env.nA containing the expected value of each action.
        """
        A = np.zeros(env.env.nA)
        for act in range(env.env.nA):
            for prob, next_state, reward, _ in env.env.P[state][act]:
                A[act] += prob * (reward + discount_factor * V[next_state])
        return A

    V = np.zeros(env.env.nS)

    iterations = 1
    while True:
        delta = 0  # checker for improvements across states
        for state in range(env.env.nS):
            act_values = one_step_lookahead(state, V)  # lookahead one step
            best_act_value = np.max(act_values)  # get best action value
            # find max delta across all states
            delta = max(delta, np.abs(best_act_value - V[state]))
            V[state] = best_act_value  # update value to best action value
        if delta < theta:  # if max improvement less than threshold
            break

        iterations += 1

    policy = np.zeros([env.env.nS, env.env.nA])

    for state in range(env.env.nS):  # for all states, create deterministic policy
        act_val = one_step_lookahead(state, V)
        best_action = np.argmax(act_val)
        policy[state][best_action] = 1

    return policy, V, iterations
