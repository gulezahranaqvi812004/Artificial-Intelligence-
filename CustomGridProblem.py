import numpy as np

n_rows, n_cols = 4, 4
n_states = n_rows * n_cols
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
actions = [UP, DOWN, LEFT, RIGHT]

# Initialize transition and reward matrices
P = np.zeros((n_states, len(actions), n_states))  # Transition matrix
R = np.zeros((n_states, len(actions)))            # Reward matrix

def to_state(row, col):
    """Helper function to convert grid coordinates to state number."""
    return row * n_cols + col

def from_state(state):
    """Helper function to convert state number back to grid coordinates."""
    return divmod(state, n_cols)

# Define rewards
rewards = {
    (2, 1): -50,  # -50 reward at position (2, 1)
    (1, 4): -5,   # -5 reward at position (1, 4)
    (4, 4): 70    # 70 reward at goal position (4, 4)
}

# Define terminal states (END)
terminal_states = [to_state(2, 3), to_state(3, 3)]  # Marked "END" in the grid

# Define transitions
for row in range(n_rows):
    for col in range(n_cols):
        s = to_state(row, col)
        
        if s in terminal_states:
            continue  # No transitions from terminal states

        # Moving up
        if row > 0:
            next_s = to_state(row - 1, col)
        else:
            next_s = s  # If moving out of bounds, stay in the same state
        P[s, UP, next_s] = 1

        # Moving down
        if row < n_rows - 1:
            next_s = to_state(row + 1, col)
        else:
            next_s = s
        P[s, DOWN, next_s] = 1

        # Moving left
        if col > 0:
            next_s = to_state(row, col - 1)
        else:
            next_s = s
        P[s, LEFT, next_s] = 1

        # Moving right
        if col < n_cols - 1:
            next_s = to_state(row, col + 1)
        else:
            next_s = s
        P[s, RIGHT, next_s] = 1

        # Assign rewards
        for a in actions:
            r, c = from_state(s)
            R[s, a] = rewards.get((r + 1, c + 1), 0)  # Default reward is 0 unless specified

# Value Iteration
def value_iteration(P, R, gamma=0.9, theta=0.0001):
    """Value Iteration Algorithm"""
    V = np.zeros(n_states)  # Initialize state values to zero
    policy = np.zeros(n_states, dtype=int)  # Initialize policy to zeros

    while True:
        delta = 0
        for s in range(n_states):
            if s in terminal_states:
                continue

            v = V[s]
            # Update state-value function
            V[s] = max([sum([P[s, a, s_prime] * (R[s, a] + gamma * V[s_prime]) 
                             for s_prime in range(n_states)]) for a in actions])
            delta = max(delta, abs(v - V[s]))

        if delta < theta:  # Stop if the value function converges
            break

    # Derive policy from the value function
    for s in range(n_states):
        if s in terminal_states:
            continue

        action_values = []
        for a in actions:
            action_value = sum([P[s, a, s_prime] * (R[s, a] + gamma * V[s_prime])
                                for s_prime in range(n_states)])
            action_values.append(action_value)
        policy[s] = np.argmax(action_values)

    return policy, V

# Solve MDP
policy, value_function = value_iteration(P, R)

# Display results
def display_policy(policy):
    """Helper function to display the policy on the grid."""
    action_symbols = {UP: '↑', DOWN: '↓', LEFT: '←', RIGHT: '→'}
    grid_policy = []
    for row in range(n_rows):
        grid_row = []
        for col in range(n_cols):
            state = to_state(row, col)
            if state in terminal_states:
                grid_row.append('END')
            else:
                grid_row.append(action_symbols[policy[state]])
        grid_policy.append(grid_row)
    return grid_policy

# Display optimal policy
optimal_policy = display_policy(policy)
for row in optimal_policy:
    print(row)

# Display value function
print("\nState Values:")
value_grid = value_function.reshape((n_rows, n_cols))
print(value_grid)
