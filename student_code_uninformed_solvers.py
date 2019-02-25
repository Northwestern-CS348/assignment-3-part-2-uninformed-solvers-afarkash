
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        if (self.currentState.state == self.victoryCondition):
            return True

        #If there are already children, visit them!
        if(len(self.currentState.children) > 0):
            for child in self.currentState.children:
                if child not in self.visited:
                    self.visited[child] = True
                    self.gm.makeMove(child.requiredMovable)
                    self.currentState = child
                    if self.currentState.state != self.victoryCondition: 
                        return False
                    else: 
                        return True
            if self.currentState.parent:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return False        
        #if there are no children, create them
        else:
            moves = self.gm.getMovables()
            #if there are no movables, go back
            if(moves == False):
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return False
            #if there are movables, add the resulting states as children
            else:
                for move in moves:
                    childSt8 = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                    self.gm.reverseMove(move)

                    if childSt8 not in self.visited:
                        self.visited[childState] = False
                    childSt8.parent = self.currentState
                    self.currentState.children.append(childSt8)
                return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        return True
