# CS50 AI notes - Harvardx Edx

## Search

  [ Approach ]
    - Start with a frontier that contains the initial state
    - Repeat:
      - if the frontier is empty, then there is no solution
      - else remove a node from the frontier
      - if node contains goal state, return the solution
      - Expand node, add resulting node to the frontier

  [ Algorithms ]
    - Deep-first search: Stack, last in first out
    - Breath-first search: Queue, first in first out
    - Greedy best-first search: heuristics specific to the problem
    - A* Search: expands the lowest value of g(n) + h(n)
    -   g(n): cost to reach the node
    -   h(n): estimated cost to goal
    - Minimax: Deterministic adversarial game decision

  [ Solving ]
    - S0: Initial state
    - Player(s): Return which player to move in state s
    - Acton(s): Return legal moves in state s
    - Result(s, a): Returns state after actions a is taken in state s
    - Terminal(s): Checks if s is a terminal state
    - Utility(s): Final numerical value for state s


## Project0
  [ degrees ]
    Find the degree of relation between actors that have appeared on the same movies
