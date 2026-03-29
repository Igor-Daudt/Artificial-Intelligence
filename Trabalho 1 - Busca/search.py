# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    from collections import deque

    # Variaveis para executar bfs
    added_frontier = set(problem.getStartState())
    # Fila de elemenaddedtos
    frontier = deque(list(i) for i in problem.getSuccessors(problem.getStartState()))
    for i in frontier:
        i.append(list()) # Ira conter lista de movimentos ate resultado

    while frontier:
        state_tuple= frontier.pop()
        current_state, current_move, current_cost, current_path  = state_tuple

        # Verifica se achou o objetivo
        if problem.isGoalState(current_state):
            return current_path + [current_move]

        # Expande AQUI ANTES de vez de no final
        if current_state not in added_frontier:
            added_frontier.add(current_state)

        # Senao continua explorando o caminho
        for v in problem.getSuccessors(current_state):
            if v[0] not in added_frontier:
                new_path = current_path + [current_move]
                new_list = list(v)
                new_list.append(new_path)
                frontier.append(new_list)
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from collections import deque

    # Variaveis para executar bfs
    added_frontier = set(problem.getStartState())
    # Fila de elemenaddedtos
    frontier = deque(list(i) for i in problem.getSuccessors(problem.getStartState()))
    for i in frontier:
        added_frontier.add(i[0])
        i.append(list()) # Ira conter lista de movimentos ate resultado
    
    while True:
        state_tuple= frontier.popleft()
        current_state, current_move, current_cost, current_path  = state_tuple

        # Verifica se achou o objetivo
        if problem.isGoalState(current_state):
            return current_path + [current_move]

        # Senao continua explorando o caminho
        for v in problem.getSuccessors(current_state):
            if v[0] not in added_frontier:
                added_frontier.add(v[0])
                new_path = current_path + [current_move]
                new_list = list(v)
                new_list.append(new_path)
                frontier.append(new_list)
        

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # Variaveis para executar bfs
    visited = set(problem.getStartState())
    # Fila de elementos
    frontier = [list(i) for i in problem.getSuccessors(problem.getStartState())]
    for i in frontier:
        i.append(list()) # Ira conter lista de movimentos ate resultado

    while True:
        selected_index, smaller_cost = 0, frontier[0][2] + problem.getCostOfActions(frontier[0][3])
        for i in range(len(frontier)):
            current_state, current_move, current_cost, current_path  = frontier[i]
            
            current_cost += problem.getCostOfActions(current_path)

            if current_cost < smaller_cost:
                smaller_cost = current_cost
                selected_index = i
        
        state_tuple = frontier.pop(selected_index)
        current_state, current_move, current_cost, current_path  = state_tuple

        # Verifica se achou o objetivo
        if problem.isGoalState(current_state):
            return current_path + [current_move]

        # Senao continua explorando o caminho
        visited.add(current_state)
        for v in problem.getSuccessors(current_state):
            if v[0] not in visited and v[0] not in [i[0] for i in frontier]:
                new_path = current_path + [current_move]
                new_list = list(v)
                new_list.append(new_path)
                frontier.append(new_list)
            #  Se o item ja esta na fronteira, verifica se o caminho atual tem custo menor, se sim, substitui o item da fronteira
            if v[0] in [i[0] for i in frontier]:
                for i in frontier:
                    if v[0] == i[0] and v[2] < i[2]:
                        frontier.remove(i)
                        new_path = current_path + [current_move]
                        new_list = list(v)
                        new_list.append(new_path)
                        frontier.append(new_list)
                        break

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    # Helper function to calculate the priority abstracting the heuristic function
    priority = lambda state, cost: cost + heuristic(state, problem)

    from util import PriorityQueue

    start_state = problem.getStartState()

    # Stores the lowest costs (g) until now
    best_valued = {start_state: 0}

    # Min-heap to pop the closest to 0 priority first
    # total_cost = heur() + cost_from_start()
    frontier = PriorityQueue()
    frontier.push((start_state, [], 0), priority(start_state, 0))

    while not frontier.isEmpty():
        state, path, cost = frontier.pop()

        # Guard to make sure it does not grab worse costs
        if cost > best_valued[state]:
            continue

        # ..... Kinda obvious
        if problem.isGoalState(state):
            return path

        for next, move, step_cost in problem.getSuccessors(state):
            new_cost = cost + step_cost

            # Checks the existance before accessing
            if next not in best_valued or new_cost < best_valued[next]:

                best_valued[next] = new_cost

                # Updates the frontier
                f_item = (next, path + [move], new_cost)
                f_prior = priority(next, new_cost)
                frontier.push(f_item, f_prior)

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
