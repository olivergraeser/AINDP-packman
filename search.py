# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
from game import Directions


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

from copy import copy

def depthFirstSearch(problem):
    def recursiveSearch(problem, curr_state, visited_list, move_sequence, total_cost):
        if problem.isGoalState(curr_state):
            return move_sequence, total_cost
        else:
            successor_states = problem.getSuccessors(curr_state)
            for successor, move, cost in successor_states:
                if successor not in visited_list:
                    now_visited_list = copy(visited_list)
                    now_visited_list.add(curr_state)
                    now_move_sequence = copy(move_sequence)
                    now_move_sequence.append(move)
                    total_cost += cost
                    result, total_cost = recursiveSearch(problem, successor, now_visited_list, now_move_sequence, total_cost)
                    if result:
                        return result, total_cost
            return [], float('inf')
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    moves, total_cost = recursiveSearch(problem, problem.getStartState(), set(), list(), 0)
    return moves

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    frontier = [(problem.getStartState(), [])]
    visited = {problem.getStartState()}
    i = 0
    while True:
        new_frontier = list()
        for state, movelist in frontier:
            i += 1
            successor_list = problem.getSuccessors(state)
            for successor, move, cost in successor_list:
                if successor not in visited:
                    if problem.isGoalState(successor):
                        return movelist + [move]
                    else:
                        new_movelist = copy(movelist)
                        new_frontier.append((successor, new_movelist + [move]))
                        visited.add(successor)
        frontier = new_frontier
    return


def uniformCostSearch(problem):

    frontier = util.PriorityQueue()
    visited = set(problem.getStartState())
    frontier.push((problem.getStartState(),0, []),0)
    solution_found = False
    while not solution_found:
        expand_element, previous_cost, movelist = frontier.pop()
        if problem.isGoalState(expand_element):
            return movelist
        else:
            successors = problem.getSuccessors(expand_element)
            for successor_state, action, cost in successors:
                if successor_state not in visited:
                    visited.add(successor_state)
                    frontier.push((successor_state, previous_cost + cost, movelist + [action]), previous_cost + cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    frontier = util.PriorityQueueWithFunction(lambda x: x[1]+heuristic(x[0], problem))
    visited = set(problem.getStartState())
    frontier.push((problem.getStartState(),0, []))
    solution_found = False
    while not solution_found:
        expand_element, previous_cost, movelist = frontier.pop()
        if problem.isGoalState(expand_element):
            return movelist
        else:
            successors = problem.getSuccessors(expand_element)
            for successor_state, action, cost in successors:
                if successor_state not in visited:
                    visited.add(successor_state)
                    frontier.push((successor_state, previous_cost + cost, movelist + [action]))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
