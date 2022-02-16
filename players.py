from copy import deepcopy
import random
import sys
import time
import pygame
import math

class connect4Player(object):
    def __init__(self, position, seed=0):
        self.position = position
        self.opponent = None
        self.seed = seed
        random.seed(seed)

    def play(self, env, move):
        move = [-1]

class human(connect4Player):

    def play(self, env, move):
        move[:] = [int(input('Select next move: '))]
        while True:
            if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
                break
            move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

    def play(self, env, move):
        done = False
        while(not done):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.position == 1:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                    else: 
                        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
                    move[:] = [col]
                    done = True

class randomAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        if 3 in indices:
            move[:] = [3]
        elif 2 in indices:
            move[:] = [2]
        elif 1 in indices:
            move[:] = [1]
        elif 5 in indices:
            move[:] = [5]
        elif 6 in indices:
            move[:] = [6]
        else:
            move[:] = [0]

class minimaxAI(connect4Player):
    
    

    def play(self, env, move):
        if env.turnPlayer.position == 1:
            MaxPlayer = True
        else:
            MaxPlayer = False
            
        current_state = deepcopy(env)
        move[:]=[self.minimax(current_state,1,MaxPlayer)]
        
        
        
        
    def winning_move(self,env, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if env.board[r][c] == piece and env.board[r][c+1] == piece and env.board[r][c+2] == piece and env.board[r][c+3] == piece:
                    return True

    # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if env.board[r][c] == piece and env.board[r+1][c] == piece and env.board[r+2][c] == piece and env.board[r+3][c] == piece:
                    return True

    # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if env.board[r][c] == piece and env.board[r+1][c+1] == piece and env.board[r+2][c+2] == piece and env.board[r+3][c+3] == piece:
                    return True

    # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if env.board[r][c] == piece and env.board[r-1][c+1] == piece and env.board[r-2][c+2] == piece and env.board[r-3][c+3] == piece:
                    return True
                
                
                
        
    def minimax(self,env,depth,maximizingPlayer):
        playerID = env.turnPlayer.position
        playerhistory = env.history[0]
        if len(playerhistory) != 0:
         if depth == 0 or env.gameOver(env.history[0][-1],playerID): 
                if depth == 0:
                    evaluation = self.eval(env,env.turnPlayer)-self.eval(env,env.turnPlayer.opponent)
                    return evaluation
                else:
                    if self.winning_move(env,env.turnPlayer.position):
                        return 100000000000000
                    elif self.winning_move(env,env.turnPlayer.opponent.position):
                        return -100000000000000
                    else:
                        return 0
        print("done")
                    
        if maximizingPlayer == True:
            value = -math.inf
            best_move= random.choice(self.valid_locations(env))
            
            for col in self.valid_locations(env): # valid_locations returns the indices of the possible columns
                
                board_copy = deepcopy(env) # double check this one
                
                self.simulateMove(board_copy,col, env.turnPlayer.position)
                
                child_val = self.minimax(board_copy,depth-1,False)
                if child_val > value:
                    value = child_val
                    best_move = col # best_move = child_move
                   
            return best_move
        else: # minimizing player
            value = math.inf
            best_move= random.choice(self.valid_locations(env))
            
            for col in self.valid_locations(env):
                
                board_copy = deepcopy(env) # double check this one
                
                self.simulateMove(board_copy,col, env.turnPlayer.opponent.position)
                child_val = self.minimax(board_copy,depth-1,True)
                
               
                if child_val < value:
                    value = child_val
                    best_move = col # best_move = child_move
            
            return best_move
        
    
    
    
    def simulateMove(self, env, move, player):
       
        env.board[env.topPosition[move]][move] = player
        
        env.topPosition[move] -= 1
        env.history[0].append(move) 
  
  
    def eval(self,env,piece):
        score = 0
    #middle column  
        middle_array = [int(i) for i in list(env.board[:,COLUMN_COUNT//2])]
        
        middle_count = middle_array.count(piece.position)
        score += middle_count * 3
        
        
    #Score horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(env.board[r,:])]
            for c in range(COLUMN_COUNT-3):
                token_list= row_array[c:c+4]
                score+=self.eval_score_method(token_list,piece.position)
                
      
    #Score vertical 
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(env.board[:,c])]
            for r in range(ROW_COUNT-3): # max of four columns
                token_list = col_array[r:r+4]
                score+=self.eval_score_method(token_list,piece.position)
       
           
    # score positive slope diagonal 
        for r in range(ROW_COUNT-3):
             for c in range(COLUMN_COUNT-3):
                token_list=[env.board[r+i][c+i] for i in range(4)]
                score+=self.eval_score_method(token_list,piece.position)
            
    # negative slope score diagonal 
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                token_list=[env.board[r+3-i][c+i] for i in range(4)]
                score+=self.eval_score_method(token_list,piece.position)
                
        
        return score
        
        
#helper functions and eval functions
# need for yourself and for the opponent
    def valid_locations(self,env):
        # arrange them which is the best move first. for alpha beta pruning. 
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        return indices

    def eval_score_method(self,token_list,piece):
        score = 0
        if token_list.count(piece) == 4:
            score += 100 
        elif token_list.count(piece) == 3 and token_list.count(0) == 1: # if there are three in a row tokens
            score += 5 
        elif token_list.count(piece) == 2 and token_list.count(0) == 2: # if there are two in a row tokens
            score += 2
        return score








class alphaBetaAI(connect4Player):

    def play(self, env, move):
        if env.turnPlayer.position == 1:
            MaxPlayer = True
        else:
            MaxPlayer = False
            
        current_state = deepcopy(env)
        move[:]=[self.alphabeta(current_state,1,-math.inf,math.inf,MaxPlayer)]

    def winning_move(self,env, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if env.board[r][c] == piece and env.board[r][c+1] == piece and env.board[r][c+2] == piece and env.board[r][c+3] == piece:
                    return True

    # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if env.board[r][c] == piece and env.board[r+1][c] == piece and env.board[r+2][c] == piece and env.board[r+3][c] == piece:
                    return True

    # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if env.board[r][c] == piece and env.board[r+1][c+1] == piece and env.board[r+2][c+2] == piece and env.board[r+3][c+3] == piece:
                    return True

    # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if env.board[r][c] == piece and env.board[r-1][c+1] == piece and env.board[r-2][c+2] == piece and env.board[r-3][c+3] == piece:
                    return True

    def alphabeta(self,env,depth,alpha,beta,maximizingPlayer):
        playerID = env.turnPlayer.position
        playerhistory = env.history[0]
        if len(playerhistory) != 0:
         if depth == 0 or env.gameOver(env.history[0][-1],playerID): 
             
                if depth == 0:
                    evaluation = self.eval(env,env.turnPlayer)-self.eval(env,env.turnPlayer.opponent)
                    return evaluation 
                      
                else:
                    if self.winning_move(env,env.turnPlayer.position):
                        return math.inf
                    elif self.winning_move(env,env.turnPlayer.opponent.position):
                        return -math.inf
                    else:
                        return 0
                    
        print("done") 
                
                    
        if maximizingPlayer == True:
          
            value = -math.inf
            best_move= random.choice(self.valid_locations(env))
            
            for col in self.valid_locations(env): # valid_locations returns the indices of the possible columns
                
                board_copy = deepcopy(env) # double check this one
                
                self.simulateMove(board_copy,col, env.turnPlayer.position)
                # print("Max:")
                # print("at depth ",depth)
                child_val = self.alphabeta(board_copy,depth-1,alpha,beta,False)
                # print("child val is ",child_val)
                if child_val > value:
                    value = child_val
                    best_move = col 

                if value >= beta:
                    break
                alpha=max(alpha,value)
            return best_move
        else: # minimizing player
            value = math.inf
            best_move= random.choice(self.valid_locations(env))
            
            for col in self.valid_locations(env):
                
                board_copy = deepcopy(env) # double check this one
                
                self.simulateMove(board_copy,col, env.turnPlayer.opponent.position)
                # print("Min:")
                # print("at depth ",depth)
                child_val = self.alphabeta(board_copy,depth-1,alpha,beta,True)
                # print("child val is ",child_val)
                if child_val < value:
                    value = child_val
                    best_move = col # best_move = child_move
                if value <= alpha:
                    break
                beta=min(beta,value)

            return best_move
        
    
    
    
    def simulateMove(self, env, move, player):
       
        env.board[env.topPosition[move]][move] = player
        
        env.topPosition[move] -= 1
        env.history[0].append(move) 
  
  
    def eval(self,env,piece):
        score = 0
    #middle column  
        middle_array = [int(i) for i in list(env.board[:,COLUMN_COUNT//2])]
        
        middle_count = middle_array.count(piece.position)
        score += middle_count * 3
        
    #Score horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(env.board[r,:])]
            for c in range(COLUMN_COUNT-3):
                token_list= row_array[c:c+4]
                score+=self.eval_score_method(token_list,piece.position)
                
      
    #Score vertical 
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(env.board[:,c])]
            for r in range(ROW_COUNT-3): # max of four columns
                token_list = col_array[r:r+4]
                score+=self.eval_score_method(token_list,piece.position)
       
           
    # score positive slope diagonal 
        for r in range(ROW_COUNT-3):
             for c in range(COLUMN_COUNT-3):
                token_list=[env.board[r+i][c+i] for i in range(4)]
                score+=self.eval_score_method(token_list,piece.position)
            
    # negative slope score diagonal 
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                token_list=[env.board[r+3-i][c+i] for i in range(4)]
                score+=self.eval_score_method(token_list,piece.position)
                
                
        return score
        
        
#helper functions and eval functions
# need for yourself and for the opponent
#sucessor function
    def valid_locations(self,env):
        # arrange them which is the best move first. for alpha beta pruning. 
        possible = env.topPosition >= 0
        indices = []
        order =[3,2,4,1,5,0,6]
        possible =[possible[i] for i in order]
        for i, p in enumerate(possible):
            if p: indices.append(i)
        return indices

    def eval_score_method(self,token_list,piece):
        score = 0
        if token_list.count(piece) == 4:
            score += 100
        elif token_list.count(piece) == 3 and token_list.count(0) == 1: # if there are three in a row tokens
            score += 5 
        elif token_list.count(piece) == 2 and token_list.count(0) == 2: # if there are two in a row tokens
            score += 2
        return score


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)








