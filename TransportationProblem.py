import heapq  # To implement the priority queue for Uniform Cost Search (UCS)
class TransportationProblem:
    def __init__(self, N):
        """Initialize the transportation problem with N states (blocks)."""
        self.N = N  # The target state or destination (N)
    def startState(self):
        """Define the start state (initial position)."""
        return 1  # Starting at position 1
    def isEnd(self, state):
        """Check if the current state is the end state."""
        return state == self.N  # End when state equals N
    def succAndCost(self, state):
        """Return list of (action, newState, cost) triples."""
        result = []
        if state + 1 <= self.N:
            result.append(('walk', state + 1, 1))  # Walking to next block costs 1
        if state * 2 <= self.N:
            result.append(('tram', state * 2, 2))  # Taking a tram costs 2
        return result
# Uniform Cost Search (UCS) Algorithm
def uniformCostSearch(problem):
    """Uniform Cost Search to find the least-cost path to the goal."""
    # Priority queue to keep track of (cost, state, history of actions)
    pq = [(0, problem.startState(), [])]  # (totalCost, currentState, history)
    visited = set()  # To track visited states
    while pq:
        # Pop the state with the lowest total cost
        totalCost, state, history = heapq.heappop(pq)
        # If the state is the goal, return the solution
        if problem.isEnd(state):
            return totalCost, history
        # Skip if the state has already been visited
        if state in visited:
            continue
        visited.add(state)
        # Explore the successors
        for action, newState, cost in problem.succAndCost(state):
            if newState not in visited:
                newCost = totalCost + cost
                heapq.heappush(pq, (newCost, newState, history + [(action, newState)]))
    return None  # If no solution found
# Function to print the solution
def printSolution(solution):
    if solution is None:
        print("No solution found!")
    else:
        totalCost, history = solution
        print("Total Cost: {}".format(totalCost))
        for action, state in history:
            print("Action: {}, New State: {}".format(action, state))
# Example usage
N = 250  # Define the number of blocks or the destination state
problem = TransportationProblem(N)
# Run Uniform Cost Search
solution = uniformCostSearch(problem)
# Print the solution path and cost
printSolution(solution)