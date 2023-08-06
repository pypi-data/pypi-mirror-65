import numpy as np


def policy_eval(policy, env, discount_factor=0.9, theta=0.0001):
    """
    Evaluate a policy given an environment and a full description of the environment's dynamics.

    Args:
        policy: [S, A] shaped matrix representing the policy.
        env: OpenAI env. env.P represents the transition probabilities of the environment.
            env.P[s][a] is a list of transition tuples (prob, next_state, reward, done).
            env.nS is a number of states in the environment.
            env.nA is a number of actions in the environment.
        theta: We stop evaluation once our value function change is less than theta for all states.
        discount_factor: Gamma discount factor.

    Returns:
        Vector of length env.nS representing the value function.
    """
    # Start with a random (all 0) value function
    V = np.zeros(env.env.nS)
    while True:
        delta = 0  # delta = change in value of state from one iteration to next

        for state in range(env.env.nS):  # for all states
            val = 0  # initiate value as 0

            # for all actions/action probabilities
            for action, act_prob in enumerate(policy[state]):
                # transition probabilities,state,rewards of each action
                for prob, next_state, reward, _ in env.env.P[state][action]:
                    val += act_prob * prob * \
                        (reward + discount_factor *
                         V[next_state])  # eqn to calculate
            delta = max(delta, np.abs(val-V[state]))
            V[state] = val
        # break if the change in value is less than the threshold (theta)
        if delta < theta:
            break
    return np.array(V)


def policy_iteration(env, discount_factor=0.9):
    """
    Policy Improvement Algorithm. Iteratively evaluates and improves a policy
    until an optimal policy is found.

    Args:
        env: The OpenAI envrionment.
        policy_eval_fn: Policy Evaluation function that takes 3 arguments:
            policy, env, discount_factor.
        discount_factor: gamma discount factor.

    Returns:
        A tuple (policy, V).
        policy is the optimal policy, a matrix of shape [S, A] where each state s
        contains a valid probability distribution over actions.
        V is the value function for the optimal policy.

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
        for a in range(env.env.nA):
            for prob, next_state, reward, _ in env.env.P[state][a]:
                A[a] += prob * (reward + discount_factor * V[next_state])
        return A
    # Start with a random policy
    policy = np.ones([env.env.nS, env.env.nA]) / env.env.nA

    iterations = 1

    while True:
        curr_pol_val = policy_eval(
            policy, env, discount_factor)  # eval current policy

        policy_stable = True
        for state in range(env.env.nS):  # for each states
            # best action (Highest prob) under current policy
            chosen_act = np.argmax(policy[state])
            # use one step lookahead to find action values
            act_values = one_step_lookahead(state, curr_pol_val)
            best_act = np.argmax(act_values)  # find best action
            if chosen_act != best_act:
                policy_stable = False  # Greedily find best action
            policy[state] = np.eye(env.env.nA)[best_act]  # update
        if policy_stable:
            return policy, curr_pol_val, iterations

        iterations += 1

    return policy, np.zeros(env.env.nS), iterations
