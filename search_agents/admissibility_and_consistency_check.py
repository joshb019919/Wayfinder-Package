"""Check the admissibility and consistency of two different heuristic
value sets for a 7-node, directed graph.

USAGE:
python admissibility_and_consistency_check.py

AI USAGE:
I used Copilot (chatGPT 4.1) to verify that I properly implemented the
functions to make the checks.

Graph is as follows:

             A
           /   \\ 
         1/     \\4
         /       \\
        B          C
      3/ \\5   2/  \\2
      /   \\   /    \\
     D       E      F
      \\     |      /
       \\    |     /
       6\\   |1   /3
         \\  |   /
          \\ |  /
             G

No directions are depicted (limitation of ascii art), but all lines 
point downward to their nodes.
"""

from queue import PriorityQueue
import math


class Graph:
    """Represents a graph of nodes in a tree structure."""
    def __init__(self):
        self.h1 = {
            "A": 7,
            "B": 6,
            "C": 3,
            "D": 6,
            "E": 1,
            "F": 3,
            "G": 0
        }

        self.h2 = {
            "A": 10,
            "B": 9,
            "C": 5,
            "D": 8,
            "E": 3,
            "F": 4,
            "G": 0
        }

        self.g = {
            "A": {"B": 1, "C": 4},
            "B": {"D": 3, "E": 5},
            "C": {"E": 2, "F": 2},
            "D": {"G": 6},
            "E": {"G": 1},
            "F": {"G": 3},
            "G": {}
        }

    def get_distance(self, node1, node2):
        """Return the path cost between two nodes."""
        return self.g.get(node1, {}).get(node2, 0)
    
    def get_heuristic(self, node):
        """Return the node's heuristic estimate cost from h1."""
        return self.h1.get(node, 0)
    
    def get_heuristic2(self, node):
        """Return the node's heuristic estimate cost from h2."""
        return self.h2.get(node, 0)
    
    def get_neighbors(self, node):
        """Return the node's neighboring nodes and distances."""
        return self.g.get(node, {})
    

def search(environment, start: str="A", goal: str="G") -> int | float:
    """Perform informed search to find the path from start to goal."""

    # Unpacks everything, checks if currently popped state is goal, and
    # if not, adds it to explore set to avoid cycles, then loops over
    # unexplored neighbors.  Different algorithms will set the priority
    # differently, but otherwise the priority queue holds the same four
    # items: a sorting priority, cumulative path cost, current state,
    # and the path from that state to the start state.  Rinse and repeat
    # until the goal is found.

    e = environment
    fringes = PriorityQueue()
    explored = set()
    states_expanded = 0

    # Priority, cumulative cost, start, path
    fringes.put((e.get_heuristic(start), 0, start, [start]))

    while not fringes.empty():
        priority, cumulative_cost, state, path = fringes.get()

        if state == goal:
            states_expanded += 1
            return cumulative_cost
        
        if state in explored:
            continue
        states_expanded += 1
        explored.add(state)
        for neighbor, distance in e.get_neighbors(state).items():
            if neighbor not in explored:
                new_cost = cumulative_cost + distance
                priority = new_cost + e.get_heuristic(neighbor)
                fringes.put((priority, new_cost, neighbor, path + [neighbor]))

    print("A* Search: No path found")
    return math.inf
    

def check_consistency(graph):
    """Determine if heuristic numbers are consistent.
    
    Consistency is true if the estimated cost from a node to a goal
    state is less than or equal to the actual cost to its child nodes
    plus the estimated cost from the child node to the goal.

    h(n) <= cost(node, child) + h(child)
    """
    
    h1_consistency = True     # Start true, prove false
    h2_consistency = True     # Start true, prove false
    
    # Check each node and its neighbors to compute consistency
    for node in graph.g:
        for neighbor in graph.get_neighbors(node):            
            cost_to_neighbor = graph.get_distance(node, neighbor)
            h1_from_neighbor = graph.get_heuristic(neighbor)
            h2_from_neighbor = graph.get_heuristic2(neighbor)

            if graph.get_heuristic(node) > cost_to_neighbor + h1_from_neighbor:
                h1_consistency = False
                break
            if graph.get_heuristic2(node) > cost_to_neighbor + h2_from_neighbor:
                h2_consistency = False
                break
    
    return h1_consistency, h2_consistency
    

def check_admissibility(graph):
    """Determine if heuristic numbers are admissible.
    
    Admissibility is true if the estimated cost from a node to a goal
    state is less than or equal to the actual cost from the node to the
    goal, else false.

    h(n) <= cost(node, goal)
    """
    
    h1_admissibility = True  # Start true, prove false
    h2_admissibility = True  # Start true, prove false

    # Loop through nodes and compute admissibility
    for node in graph.g:
        node_cost = search(graph, node)

        if graph.get_heuristic(node) > node_cost:
            h1_admissibility = False
        if graph.get_heuristic2(node) > node_cost:
            h2_admissibility = False
    
    return h1_admissibility, h2_admissibility
    

def main():
    graph = Graph()

    # Check heuristic consistencies
    consistencies = check_consistency(graph)
    h1_consistency = consistencies[0]
    h2_consistency = consistencies[1]
    
    # If heuristics are consistent, they're also admissible
    h1_admissibility = True if h1_consistency else check_admissibility(graph)[0]
    h2_admissibility = True if h2_consistency else check_admissibility(graph)[1]

    print(f"h1 is consistent: {h1_consistency}\nh1 is admissible: {h1_admissibility}\n")
    print(f"h2 is consistent: {h2_consistency}\nh2 is admissible: {h2_admissibility}")


if __name__ == "__main__":
    main()
