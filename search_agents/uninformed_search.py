"""
CSC640 Intro to AI
Assignment 1a: Missionaries and Cannibals Problem (DFS & BFS)
Author: Josh Borthick jlb8976s@missouristate.edu
Date: 2025-09-07

DFS:
The DFS algorithm uses a stack to explore nodes (right first since 
popping from end of neighbors), and a set to track visited nodes.  This
finds an optimal path, such as it is.

BFS:
The BFS algorithm uses a queue to explore nodes level by level, and a 
set to track visited nodes.  Proceeds left to right.

The graph is represented as an adjacency list in a dictionary.
The graph structure is as follows:

start   A
      / | \\
     B  C  D
     \\   /
        E
       / \\
      F   G
          |
          H
          |
          I
          |
          J
          |
          K
          |
          L
          |
          M
         / \\
        N   O
        \\ /
goal      P

Output format:

"Node
L: xM yC B(?)
R: xM yC B(?)"

Where x is the number of missionaries, y is the number of cannibals, 
and B indicates the boat's presence on that side.
"""

class Environment:
    # Constants for boat positions
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    """Defines the environment for the Missionaries and Cannibals problem."""
    def __init__(self, start_state):
        self.start_state = start_state
        self.state_id = "A"  # Starting state ID

    def get_factors(self, state):
        """Returns the number and locations of missionaries, cannibals, and the boat."""
        left_m, left_c, boat = state
        right_m = 3 - left_m
        right_c = 3 - left_c
        return left_m, left_c, right_m, right_c, boat

    def is_valid(self, state):
        """Makes sure the no missionaries get eaten and keep within bounds."""
        left_m, left_c, right_m, right_c, boat = self.get_factors(state)

        if ((left_m > 0 and left_m < left_c) or (right_m > 0 and right_m < right_c) or 
            not (0 <= left_m <= 3) or not (0 <= left_c <= 3) or
            not (0 <= right_m <= 3) or not (0 <= right_c <= 3)):
            return False
        return True

    def is_goal(self, state):
        """Checks if the state is the goal state."""
        return state == (0, 0, self.RIGHT)

    def get_valid_states(self, state):
        """Finds all valid next states from the current state."""
        left_m, left_c, right_m, right_c, boat = self.get_factors(state)
        next_states = []

        possible_moves = [
            (2, 0), (0, 2), (1, 1), (1, 0), (0, 1)
        ]

        for missionaries, cannibals in possible_moves:
            new_left_m = left_m - missionaries if boat == self.LEFT else left_m + missionaries
            new_left_c = left_c - cannibals if boat == self.LEFT else left_c + cannibals
            new_right_m = right_m + missionaries if boat == self.LEFT else right_m - missionaries
            new_right_c = right_c + cannibals if boat == self.LEFT else right_c - cannibals
            new_boat = self.RIGHT if boat == self.LEFT else self.LEFT

            new_state = (new_left_m, new_left_c, new_boat)

            if self.is_valid(new_state):
                next_states.append(new_state)

        return next_states
        

def run_dfs():
    """Uses DFS to find a path from start to goal in the graph."""
    environment = Environment((3, 3, Environment.LEFT))
    stack = []
    path = []
    visited = set()

    def dfs():
        """Tries each state in a depth-first manner to find the goal state."""

        # Begin with the start state
        # If stack is empty after looping over all states, no solution
            # Get the next state to explore and process unvisited nodes
                # Add state to path and mark as visited (to avoid cycles)
                # Found the goal state, return the path
                # Get valid next states
                # If no valid next states or all have been visited, backtrack
                # Otherwise, find more states to explore

        stack.append(environment.start_state)
        while stack:
            state = stack.pop()
            if state in visited:
                continue
            path.append((environment.state_id, state))
            visited.add(state)
            if environment.is_goal(state):
                return path
            next_states = environment.get_valid_states(state)
            if not next_states or all(s in visited for s in next_states):
                path.pop()
            for next_state in environment.get_valid_states(state):
                if next_state not in visited:
                    environment.state_id = chr(ord(environment.state_id) + 1)
                    stack.append(next_state)
        return None
    return dfs()

def run_bfs():
    """Uses BFS to find a path from start to goal in the graph."""
    environment = Environment((3, 3, Environment.LEFT))
    queue = []
    visited = set()

    def bfs():
        """Tries each state in a breadth-first manner to find the goal state."""

        # Begin with the start state
        # If queue is empty after looping over all states, no solution
            # Get the next state to explore from front of queue and process unvisited nodes
                # Mark state as visited (to avoid cycles)
                # If found the goal state, return the path
                # Get valid next states
                # If no valid next states or all have been visited, backtrack
                # Otherwise, find more states to explore

        queue.append((environment.start_state, [(environment.state_id, environment.start_state)]))
        while queue:
            (state, path) = queue.pop(0)
            if state in visited:
                continue
            visited.add(state)
            if environment.is_goal(state):
                return path
            next_states = environment.get_valid_states(state)
            if not next_states or all(s in visited for s in next_states):
                path.pop()
            for next_state in next_states:
                if next_state not in visited:
                    environment.state_id = chr(ord(environment.state_id) + 1)
                    queue.append((next_state, path + [(environment.state_id, next_state)]))
        return None
    return bfs()


def main():
    """Print the solutions found by DFS and BFS."""
    print("Missionaries and Cannibals Problem Solutions\n============================================\n")
    print("e.g., '<state_id>: (<left_m>, <left_c>, <boat_side>)'\n")

    print("DFS SOLUTION:\n-------------")
    for state_id, state in run_dfs():
        print(f"{state_id}: {state}")

    print("\n")

    print("BFS SOLUTION:\n-------------")
    for state_id, state in run_bfs():
        print(f"{state_id}: {state}")


if __name__ == "__main__":
    main()
