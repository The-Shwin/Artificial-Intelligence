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

class Position:
    """
        Class for tracking states/positions. Has current state and moves
        to reach that state.
    """
    def __init__(self, state, moves, cost=None):
        self.state = state
        self.moves = moves
        self.cost = cost

    def getState(self):
        return self.state

    def getMoves(self):
        return self.moves

    def getCost(self):
        return self.cost

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def uninformed_search(problem, search_type='dfs'):
    visited_states = set()
    if search_type == 'dfs':
        states_struct = util.Stack()
    elif search_type == 'bfs':
        states_struct = util.Queue()
        visited_states.add(problem.getStartState())

    start_state = Position(problem.getStartState(), [])
    states_struct.push(start_state)

    while not states_struct.isEmpty():
        current_position = states_struct.pop()
        current_state, prior_moves = current_position.getState(), current_position.getMoves()

        if problem.isGoalState(current_state):
            return prior_moves
        else:
            if current_state not in visited_states and search_type =='dfs':
                visited_states.add(current_state)
            successor_list = problem.getSuccessors(current_state)
            for successor in successor_list:
                if successor[0] not in visited_states:
                    post_moves = list(prior_moves)
                    post_moves.append(successor[1])
                    next = Position(successor[0], post_moves)
                    if search_type == 'bfs':
                        visited_states.add(successor[0])
                    states_struct.push(next)
    return []

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    return uninformed_search(problem, 'dfs')
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return uninformed_search(problem, 'bfs')
    #util.raiseNotDefined()

def priority_based_search(problem, use_heuristic=False, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    state_queue = util.PriorityQueue()
    start_state = Position(problem.getStartState(), [], 0)
    visited_states = set()
    state_queue.push(start_state, 0)

    while not state_queue.isEmpty():
        current_position = None
        visited_pos = False
        while not state_queue.isEmpty() and not visited_pos:
            current_position = state_queue.pop()
            if current_position.getState() not in visited_states:
                visited_pos = True

        # Checks if the while loop was entered
        if current_position == None:
            break

        current_state = current_position.getState()
        prior_moves = current_position.getMoves()
        position_cost = current_position.getCost()

        if problem.isGoalState(current_state):
            return prior_moves
        else:
            if current_state not in visited_states:
                visited_states.add(current_state)
            successor_list = problem.getSuccessors(current_state)

            for successor in successor_list:
                if successor[0] not in visited_states:
                    next_moves = list(prior_moves)
                    next_moves.append(successor[1])
                    update_cost = successor[2] + position_cost
                    next_position = Position(successor[0], next_moves, update_cost)
                    if use_heuristic is True and heuristic is not None:
                        update_cost = update_cost + heuristic(successor[0], problem)
                    state_queue.push(next_position, update_cost)
    return []
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    return priority_based_search(problem)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    return priority_based_search(problem, True, heuristic)
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
