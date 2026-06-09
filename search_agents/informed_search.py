"""Implement the A* search algorithm to find the lowest-cost driving 
route between two cities on the Romania road map. Use the standard 
straight-line distance (SLD) to Bucharest as an admissible and 
consistent heuristic. Compare A* with Uniform-Cost Search and greedy 
search in terms of optimality and search effort (nodes expanded).

INSTRUCTIONS:
python informed_search.py
Specify which algorithm to use with the search function from one of
    a*
    greedy
    uniform-cost

AI USAGE:
Used Copilot (chatGPT 4.1) to give me a scaffolding class and search 
function, which I then corrected and otherwise fleshed out to make it
work.

START: Arad
GOAL: Bucharest

SLDs:
Arad            = 366
Bucharest       =   0
Craiova         = 160
Dobreta         = 242
Eforie          = 161
Fagaras         = 178
Giurgiu         =  77
Hirsova         = 151
Iasi            = 226
Lugoj           = 244
Mehadia         = 241
Neamt           = 234
Oradea          = 380
Pitesti         =  98
Rimnicu Vilcea  = 193
Sibiu           = 253
Timisoara       = 329
Urziceni        =  80
Vaslui          = 199
Zerind          = 374
"""

from queue import PriorityQueue

class Romania:
    """Represents a map of Romania with cities and roads."""

    def __init__(self):
        """Initialize the map with straight-line distances and road connections."""
        self.sld: dict[str, int] = {
            "Arad": 366,
            "Bucharest": 0,
            "Craiova": 160,
            "Dobreta": 242,
            "Eforie": 161,
            "Fagaras": 178,
            "Giurgiu": 77,
            "Hirsova": 151,
            "Iasi": 226,
            "Lugoj": 244,
            "Mehadia": 241,
            "Neamt": 234,
            "Oradea": 380,
            "Pitesti": 98,
            "Rimnicu Vilcea": 193,
            "Sibiu": 253,
            "Timisoara": 329,
            "Urziceni": 80,
            "Vaslui": 199,
            "Zerind": 374
        }

        self.roads: dict[str, dict[str, int]] = {
            "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
            "Bucharest": {"Urziceni": 85, "Giurgiu": 90, "Pitesti": 101, "Fagaras": 211},
            "Craiova": {"Dobreta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
            "Dobreta": {"Mehadia": 75, "Craiova": 120},
            "Eforie": {"Hirsova": 86},
            "Fagaras": {"Sibiu": 99, "Bucharest": 211},
            "Giurgiu": {"Bucharest": 90},
            "Hirsova": {"Urziceni": 98, "Eforie": 86},
            "Iasi": {"Neamt": 87, "Vaslui": 92},
            "Lugoj": {"Timisoara": 111, "Mehadia": 70},
            "Mehadia": {"Lugoj": 70, "Dobreta": 75},
            "Neamt": {"Iasi": 87},
            "Oradea": {"Zerind": 71, "Sibiu": 151},
            "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
            "Rimnicu Vilcea": {"Sibiu": 80, "Craiova": 146, "Pitesti": 97},
            "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
            "Timisoara": {"Arad": 118, "Lugoj": 111},
            "Urziceni": {"Bucharest": 85, "Hirsova": 98, "Vaslui": 142},
            "Vaslui": {"Iasi": 92, "Urziceni": 142},
            "Zerind": {"Arad": 75, "Oradea": 71}
        }
        
    def get_distance(self, city1: str, city2: str) -> int:
        """Return the road distance (path cost) between two cities."""
        return self.roads.get(city1, {}).get(city2, 0)

    def get_heuristic(self, city: str) -> int:
        """Return city's heuristic distance (SLD) to Bucharest."""
        return self.sld.get(city, 0) 

    def get_neighbors(self, city: str) -> dict[str, int]:
        """Return city's neighboring cities and their road distances."""
        return self.roads.get(city, {})


def search(algorithm: str, environment, start: str="Arad", goal: str="Bucharest") -> list:
    """Perform informed search to find the path from start to goal."""

    # Unpacks everything, checks if currently popped state is goal, and
    # if not, adds it to explore set to avoid cycles, then loops over
    # unexplored neighbors.  Different algorithms will set the priority
    # differently, but otherwise the priority queue holds the same four
    # items: a sorting priority, cumulative path cost, current state,
    # and the path from that state to the start state.  Rinse and repeat
    # until the goal is found.

    e = environment()
    fringes = PriorityQueue()
    explored = set()
    states_expanded = 0

    # Priority, cumulative cost, start, path
    fringes.put((e.get_heuristic(start), 0, start, [start]))

    while not fringes.empty():
        priority, cumulative_cost, state, path = fringes.get()

        if state == goal:
            states_expanded += 1
            print(f"{algorithm.capitalize()} Search: Path found: {' -> '.join(path)} "
                  + f"with a path cost of {cumulative_cost} "
                  + f"and {states_expanded} nodes expanded")
            return path
        
        if state in explored:
            continue
        states_expanded += 1
        explored.add(state)
        for neighbor, distance in e.get_neighbors(state).items():
            if neighbor not in explored:
                new_cost = cumulative_cost + distance

                if "uniform-cost" == algorithm.lower():
                    priority = new_cost
                elif "greedy" == algorithm.lower():
                    priority = e.get_heuristic(neighbor)
                elif "a*" == algorithm.lower():
                    priority = new_cost + e.get_heuristic(neighbor)
                
                fringes.put((priority, new_cost, neighbor, path + [neighbor]))

    print("Uniform-Cost Search: No path found")
    return []


def main():
    """Run all three search algorithms and compare results.
    
    Note: Each function prints its own results.
    Can specify other start/goal cities and environments if desired.
    The only required argument is the type of algorithm, which is 
    currently one of
        a*
        greedy
        uniform-cost
    """

    search("a*", Romania)            # Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest (418, 6 nodes)
    search("uniform-cost", Romania)  # Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest (418, 13 nodes)
    search("greedy", Romania)        # Arad -> Sibiu -> Fagaras -> Bucharest (450, 4 nodes)

    print()

    # Reversed start, goal                                  # Interesting how A* searches more nodes in longer graphs
    search("a*", Romania, start="Bucharest", goal="Arad")            # Bucharest -> Pitesti -> Rimnicu Vilcea -> Sibiu -> Arad (418, 17 nodes)
    search("uniform-cost", Romania, start="Bucharest", goal="Arad")  # Same but with 15 nodes
    search("greedy", Romania, start="Bucharest", goal="Arad")        # Same but with 18 nodes


if __name__ == "__main__":
    main()
