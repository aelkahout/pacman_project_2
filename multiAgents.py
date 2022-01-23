# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        foodList = newFood.asList()

        if foodList:
            nextFood = min([util.manhattanDistance(newPos, food) for food in foodList])    
        else:
            nextFood = 0.01
        
        return 2/nextFood + childGameState.getScore()
        
def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(currentState,agentIndex, depth = 0):
            
            if  currentState.isWin() or currentState.isLose() or depth == self.depth:
                return [self.evaluationFunction(currentState)]

            numAgent = currentState.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgent
            if nextAgent == 0:
                depth += 1

            allMoves = currentState.getLegalActions(agentIndex)

            if agentIndex == 0:
                maxEval = -99999999999

                for move in allMoves:
                    child = currentState.getNextState(agentIndex, move)
                    eval = minimax(child, nextAgent, depth)[0]
                    maxEval = max(maxEval, eval)
                    
                    if maxEval == eval:
                        bestMove = move

                return maxEval, bestMove

            else:
                minEval = 99999999999999999999

                for move in allMoves:
                    child = currentState.getNextState(agentIndex, move)
                    eval = minimax(child, nextAgent, depth)[0]
                    minEval = min(minEval, eval)

                    if minEval == eval:
                        bestMove = move
                
                return minEval, bestMove
        
        return minimax(gameState, self.index)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(currentState, agentIndex, alpha, beta, depth = 0):
            
            if  currentState.isWin() or currentState.isLose() or depth == self.depth:
                return [self.evaluationFunction(currentState)]

            numAgent = currentState.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgent
            if nextAgent == 0:
                depth += 1

            allMoves = currentState.getLegalActions(agentIndex)
            bestMove = None

            if agentIndex == 0:
                maxEval = -99999999999

                for move in allMoves:
                    child = currentState.getNextState(agentIndex, move)
                    eval = alphabeta(child, nextAgent, alpha, beta, depth)[0]
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, maxEval)
                    
                    if beta < alpha:
                        break

                    if maxEval == eval:
                        bestMove = move

                return maxEval, bestMove

            else:
                minEval = 99999999999999999999
                
                for move in allMoves:

                    child = currentState.getNextState(agentIndex, move)
                    eval = alphabeta(child, nextAgent, alpha, beta, depth)[0]
                    minEval = min(minEval, eval)
                    beta = min(beta, minEval)
                    
                    if beta < alpha:
                        break
                        
                    if minEval == eval:
                        bestMove = move
                
                return minEval, bestMove
        
        return alphabeta(gameState, self.index, -9999999, 9999999)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(currentState,agentIndex, depth = 0):
            
            if  currentState.isWin() or currentState.isLose() or depth == self.depth:
                return [self.evaluationFunction(currentState)]

            numAgent = currentState.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgent
            if nextAgent == 0:
                depth += 1

            allMoves = currentState.getLegalActions(agentIndex)
            numActions = len(allMoves)
            bestMove = None
            if agentIndex == 0:
                maxEval = -99999999999

                for move in allMoves:
                    child = currentState.getNextState(agentIndex, move)
                    eval = expectimax(child, nextAgent, depth)[0]
                    maxEval = max(maxEval, eval)
                    
                    if maxEval == eval:
                        bestMove = move

                return maxEval, bestMove

            else:
                expEval = 0

                for move in allMoves:
                    child = currentState.getNextState(agentIndex, move)
                    eval = expectimax(child, nextAgent, depth)[0]
                    expEval += (1.0/numActions) * eval

                    if expEval == eval:
                        bestMove = move
                
                return expEval, bestMove
        
        return expectimax(gameState, self.index)[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    capsules = currentGameState.getCapsules()
    foodList = currentFood.asList()
    addedScore = 0
    capScore = 200/(len(capsules)+1)
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    hunt = 0
    
    for ghost in newGhostStates:
        ghostPos = ghost.getPosition()
        
        if newScaredTimes[0]:
            dist = util.manhattanDistance(currentPos, ghostPos)
            hunt = 2/dist
        
    if foodList:
        nextFood = min([util.manhattanDistance(currentPos, food) for food in foodList])    
    else:
        nextFood = 0.01

    if capsules:
        nextCapsule = min([util.manhattanDistance(currentPos, capsule) for capsule in capsules])
    else:
        nextCapsule = 0

    if capsules:
        addedScore -= 1000
    else:
        addedScore += 1

    return currentGameState.getScore() + addedScore + 2/nextFood + 1/(0.01+nextCapsule) + capScore + hunt


# Abbreviation
better = betterEvaluationFunction
