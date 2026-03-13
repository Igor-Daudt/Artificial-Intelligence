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
    from game import Directions
    dict_directions = {'North': Directions.NORTH,'West': Directions.WEST, 'South':  Directions.SOUTH , 'East': Directions.EAST}
    
    # Variaveis para executar dfs
    visited = set()
    # Forma listas que contem 1 tupla dentro de cada uma
    stack = [list(i) for i in problem.getSuccessors(problem.getStartState())]
    for i in stack:
        i.append(list()) # Ira conter lista de movimentos ate resultado
    
    while True:
        state_tuple= stack.pop()
        current_state, current_move, current_status, current_path  = state_tuple
        
        # Verifica se achou o objetivo
        if problem.isGoalState(current_state):
            return current_path + [current_move]

        # Senao continua explorando o caminho
        visited.add(current_state)
        for v in problem.getSuccessors(current_state):
            if v[0] not in visited:
                new_path = current_path + [dict_directions[current_move]]
                new_list = list(v)
                new_list.append(new_path)
                stack.append(new_list)
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from collections import deque
    from game import Directions
    dict_directions = {'North': Directions.NORTH,'West': Directions.WEST, 'South':  Directions.SOUTH , 'East': Directions.EAST}

    # Variaveis para executar bfs
    visited = set()
    # Fila de elementos
    frontier = deque(list(i) for i in problem.getSuccessors(problem.getStartState()))
    for i in frontier:
        i.append(list()) # Ira conter lista de movimentos ate resultado
    
    while True:
        state_tuple= frontier.popleft()
        current_state, current_move, current_status, current_path  = state_tuple

        # Verifica se achou o objetivo
        if problem.isGoalState(current_state):
            return current_path + [current_move]

        # Senao continua explorando o caminho
        visited.add(current_state)
        for v in problem.getSuccessors(current_state):
            if v[0] not in visited:
                new_path = current_path + [dict_directions[current_move]]
                new_list = list(v)
                new_list.append(new_path)
                frontier.append(new_list)
        

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from game import Directions
    dict_directions = {'North': Directions.NORTH,'West': Directions.WEST, 'South':  Directions.SOUTH , 'East': Directions.EAST}

    # Variaveis para executar bfs
    visited = set()
    # Fila de elementos
    frontier = [list(i) for i in problem.getSuccessors(problem.getStartState())]
    for i in frontier:
        i.append(list()) # Ira conter lista de movimentos ate resultado
    

    while True:
        selected_index, smaller_cost = frontier[0], 999999
        for i in range(len(frontier)):
            current_state, current_move, current_status, current_path  = frontier[i]
            current_cost = problem.getCostOfActions(current_path + [dict_directions[current_move]])
            if current_cost < smaller_cost:
                smaller_cost = current_cost
                selected_index = i
            
        state_tuple= frontier.pop(selected_index)
        current_state, current_move, current_status, current_path  = state_tuple

        # Verifica se achou o objetivo
        if problem.isGoalState(current_state):
            return current_path + [current_move]

        # Senao continua explorando o caminho
        visited.add(current_state)
        for v in problem.getSuccessors(current_state):
            if v[0] not in visited:
                new_path = current_path + [dict_directions[current_move]]
                new_list = list(v)
                new_list.append(new_path)
                frontier.append(new_list)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from game import Directions
    dict_directions = {'North': Directions.NORTH,'West': Directions.WEST, 'South':  Directions.SOUTH , 'East': Directions.EAST}

    # Variaveis para executar bfs
    visited = set()
    # Fila de elementos
    frontier = [list(i) for i in problem.getSuccessors(problem.getStartState())]
    for i in frontier:
        i.append(list()) # Ira conter lista de movimentos ate resultado
    

    while True:
        selected_index, smaller_cost = frontier[0], 999999
        for i in range(len(frontier)):
            current_state, current_move, current_status, current_path  = frontier[i]
            current_cost = problem.getCostOfActions(current_path + [dict_directions[current_move]]) + heuristic(current_state, problem)
            if current_cost < smaller_cost:
                smaller_cost = current_cost
                selected_index = i
            
        state_tuple= frontier.pop(selected_index)
        current_state, current_move, current_status, current_path  = state_tuple

        # Verifica se achou o objetivo
        if problem.isGoalState(current_state):
            return current_path + [current_move]

        # Senao continua explorando o caminho
        visited.add(current_state)
        for v in problem.getSuccessors(current_state):
            if v[0] not in visited:
                new_path = current_path + [dict_directions[current_move]]
                new_list = list(v)
                new_list.append(new_path)
                frontier.append(new_list)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
