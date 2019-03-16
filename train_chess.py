import numpy as np
from dynamic_programming import policy_iteration

states = np.load('rook_final.npy').item()

def get_deterministic_policy(states):
    pi = {}
    for state, value in states.items():
        pi[state] = list(value.keys())[0]
    return pi

def deterministic_policy_eval_step(states_actions, V, pi):
    # Evaluation in place (in contrast with evaluation with 2 arrays).
    # Needs less memory and converges too
    # pi is a dict and pi[s] is the best action for that state. (The most probable action)
    delta = 0
    for state, actions in states_actions.items():
        action = pi[state]
        next_node = actions[action]['next_state']
        reward = actions[action]['status']
        V_updated = 0
        if next_node in V:
            V_updated = -(reward + V[next_node])
        else:
            V_updated = -reward
        delta = max(delta, np.abs(V_updated - V[state]))
        V[state] = V_updated
    return V, delta

def policy_improve(V, states_actions):
    pi = {}
    print(sum(abs(np.array(list(V.values())))))
    for state, actions in states_actions.items():
        actions_list = [] # list(actions.keys())
        expected_rewards = [] #np.zeros(len(actions))
        for i, (action, data) in enumerate(actions.items()):
            actions_list.append(action)
            next_state = data['next_state']
            reward = data['status']
            if next_state in V:
                expected_rewards.append(-(reward + V[next_state]))
            else:
                expected_rewards.append(-reward)

        pi[state] = actions_list[np.argmax(expected_rewards)]
    return pi

pi = get_deterministic_policy(states)
# pi = get_deterministic_policy_uniform(states)
pi, V = policy_iteration(states, 
                         pi, 
                         deterministic_policy_eval_step = deterministic_policy_eval_step, 
                         policy_improve=policy_improve, 
                         verbose = 1)