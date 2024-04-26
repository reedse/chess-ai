#store info about current game state
#determine valid moves at current state

class gState():

    def __init__(self): #constructor for our game state
        #use a 2D array to represent our game state

        #2D array board looks like:

        #---- is a space
            #Black Side

            #col0 #col1 #col2 #col3 #col4 #col5 #col6 #col7

    #row0   #rook,knight,bishop,queen,king,bishop,knight,rook
    #row1   #pawn, pawn, pawn, pawn, pawn, pawn, pawn, pawn
    #row2   #----, -----, ----, ----, ----, ----, ----, ----
    #row3   #----, -----, ----, ----, ----, ----, ----, ----
    #row4   #----, -----, ----, ----, ----, ----, ----, ----
    #row5   #----, -----, ----, ----, ----, ----, ----, ----
    #row6   #pawn, pawn, pawn, pawn, pawn, pawn, pawn, pawn
    #row7   #rook,knight,bishop,queen,king,bishop,knight,rook

            #white Side

        #first char indicates black "B" and white "W"
        #second char indicates piece, eg pawn is "P". knight is "N" and king is "K"
        #"--" indicates a space
        self.state = [
            ["BR","BN","BB","BQ","BK","BB","BN","BR"],
            ["BP","BP","BP","BP","BP","BP","BP","BP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["WP","WP","WP","WP","WP","WP","WP","WP"],
            ["WR","WN","WB","WQ","WK","WB","WN","WR"]
        ]
        #make sure to change where king is for both sides when modifying state. if no king, then leave tuples empty
        self.kingPosB=(0,4)
        self.kingPosW=(7,4)

        self.log = [] #stores moves into this log to be printed out into a file "log.txt" at end of game
        self.turn = "W" #"W" indicates white's turn, "B" indicates black's turn
        self.scores=[0,0] #[0] is white, [1] is black scores. based on pieces captured
        self.board_evaluation=[0,0] #[0] is white, [1] is black. is a sum of all board evaluation functions to determine which side is favorable
        self.castle=[0,0] #[0] is white, [1] is black. if =1 then side has castled already
        self.check="" #returns a side that is in check either "W" or "B" or ""
        self.checkmate=False
        self.stalemate=False
        self.depth = 2
        self.nextMove = None
        self.AI = False

    def inCheck(self):
        #determine if king is under attack
        for x in range(8):
            for y in range(8):
                pxy = (x,y)
                for move in self.validMoves(self.state[x][y],pxy): 
                    if move[3] == "true":
                         if move[4][1] == 'K': #if there is an attack on B king
                            if move[4][0] == "B":
                                self.check = "B"
                                return "B"
                            elif move[4][0] == "W":
                                self.check = "W"
                                return "W" 
        self.check = ""
        return ""
 
    #updates board_evaluation score for each side
    def evaluate_Board(self):

        white_sum = 0
        black_sum = 0

        #take into account player scores
        white_sum+= self.scores[0] - self.scores[1] #take difference in scores
        black_sum+= self.scores[1] - self.scores[0]

        #factor pieces that have lines of attack
        white_sum+=self.evaluate_Attack("W")
        black_sum+=self.evaluate_Attack("B")

        #factor number of pieces each side has
        boardCountW=0
        boardCountB=0
        for x in range(8):
            for y in range(8):
                if self.state[x][y] != "--":
                    if self.state[x][y][0] == "W":
                        boardCountW+=self.getPieceScore(self.state[x][y])
                    else:
                        boardCountB+=self.getPieceScore(self.state[x][y])
        white_sum+=(boardCountW-boardCountB)
        black_sum+=(boardCountB-boardCountW)

        #update board evaluations
        self.board_evaluation[0] = white_sum
        self.board_evaluation[1] = black_sum

        #print("White board eval:",self.board_evaluation[0])
        #print("Black board eval:",self.board_evaluation[1])

    #returns a score for a side based on how many pieces have a line of attack
    def evaluate_Attack(self,side):
        score = 0
        for x in range(8):
            for y in range(8):
                if self.state[x][y][0] == side:
                    #search all possible moves and if there is a capture, then add to score
                    pxy = (x,y)
                    for move in self.validMoves(self.state[x][y],pxy): 
                        if move[3] == "true":
                            #print(move[4])
                            score+=self.getPieceScore(move[4])
                    
        #print("side:",side,"attack score: ",score)

        return score

    def getPieceScore(self,cPiece):
        if len(cPiece) <= 0:
            return 0
        score = 0
        if cPiece[1] == "P":
            score = 1
        elif cPiece[1] == "N":
            score = 3
        elif cPiece[1] == "B":
            score = 3
        elif cPiece[1] == "R":
            score = 5
        elif cPiece[1] == "Q": 
            score = 9
        elif cPiece[1] == "K":
            score = 50
        return score

    def get_state(self):
        return self.state

    #alpha beta search, since our AI starts as black, we will have it be the minimizing player
    def alpha_beta_search(self,moves,depth,alpha,beta,max_player,b_move):

        if depth == 0 or self.checkmate:
            self.evaluate_Board()
            return (self.board_evaluation[1],b_move)

        b_score = 100

        for move in moves:
            #make a move and search result state
            self.makeMove(move[0],move[1],move,self.state[move[5]][move[6]],(move[5],move[6]),"")
            newMoves=self.generateValidMoves()
            score = self.alpha_beta_search(newMoves,depth-1,beta,alpha,max_player,move)

            if score[0] < b_score:
                b_score = score[0]
                if depth == self.depth:
                    b_move = move
            self.undoMove()

            if b_score < beta:
                beta = b_score

            if alpha <= beta:
                break

        return (b_score,b_move)


    #generates all possible moves
    def generateMoves(self,side):
        allMoves=[]
        for x in range(8):
            for y in range(8):
                piece=self.state[x][y]
                if piece != "--":
                    if side != "" and piece[0] == side:
                        for move in self.validMoves(piece,(x,y)):
                            allMoves.append(move)
        return allMoves

    #generate only valid moves taking account for checks
    def generateValidMoves(self):
        allMoves=self.generateMoves(self.turn) #generate our moves
        #print(allMoves)
        #for a in range(len(allMoves)-1,-1,-1): #start at end of list and decrement by 1
            #have us make a move, if we are still in check, then remove the move from list
        return allMoves

    def undoMove(self):

        if len(self.log) > 0:
            #print("Printed Log:")
            #for move in self.log:
                #print(move)
            #undo last move
            last_move = self.log.pop() #most recent move
            
            #print(last_move)

            #check if we captured a piece
            side=last_move[1]
 
            cur_x = last_move[4][0]
            cur_y = last_move[4][1]
            prev_x = last_move[5][0]
            prev_y = last_move[5][1]
            if (last_move[4][3] == "true"):
                #check for promotion
                cPiece=last_move[4][4]
                if len(last_move) > 6:
                    self.state[prev_x][prev_y] = last_move[6][1]
                    self.state[cur_x][cur_y] = cPiece
                else:
                    #print(self.state[prev_x][prev_y])
                    #print(self.state[cur_x][cur_y])
                    #print(cPiece)
                    self.state[prev_x][prev_y] = last_move[3]
                    self.state[cur_x][cur_y] = cPiece
                if side == "W":
                    self.scores[0] -= self.getPieceScore(cPiece)
                else:
                    self.scores[1] -= self.getPieceScore(cPiece)
            else:
                temp=self.state[prev_x][prev_y]

                if self.state[cur_x][cur_y] == "WK":
                    self.kingPosW = (prev_x,prev_y)
                elif self.state[cur_x][cur_y] == "BK":
                    self.kingPosB = (prev_x,prev_y)

                self.state[prev_x][prev_y] = self.state[cur_x][cur_y]
                self.state[cur_x][cur_y] = temp
            #captured a piece

            #set turn back to previous
            if (last_move[1] == 'W'):
                self.turn = "W"
            if (last_move[1] == 'B'):
                self.turn = "B"

    def makeMove(self,x,y,move,mPiece,mPieceIndex,cPiece):
        #print("Moved",mPiece,"to: ", move[0], move[1], move[2])

        #update log
        log_str=["turn:",self.turn,"piece:",mPiece,move]

        #update state or board
        offset_x = int(mPieceIndex[0]) - move[0]
        offset_y = int(mPieceIndex[1]) - move[1]

        oTile = self.state[move[0]][move[1]]
        cPiece = move[4]

        self.state[move[0]][move[1]] = mPiece #update new tile with moved piece
        self.state[int(x)+offset_x][int(y)+offset_y] = "--" #update previous location with empty
        store_old=(int(x)+offset_x,int(y)+offset_y)
        log_str.append(store_old)
        #print("old pos: ",oTile, int(x)+offset_x, int(y)+offset_y)
        #print("new pos: ",current_state.state[move[0]][move[1]], move[0], move[1] )

        #check for castle
        if move[2][0] == 'c':
            #print("clicked castle move")
            #swap rook position with king old position
            if self.turn == "W":
                if move[2][4] == 'l': #castled left
                    self.state[int(x)+offset_x][int(y)+offset_y-1] = self.state[7][0] #move rook beside king
                    self.state[7][0] = "--" #replace rook spot with empty
                    log_str=log_str,"castled-l-w:","WK"
                elif move[2][4] == 'r': #castled right
                    self.state[int(x)+offset_x][int(y)+offset_y+1] = self.state[7][7]
                    self.state[7][7] = "--"
                    log_str=log_str,"castled-r-w:","WK"
                self.castle[0] = 1
            else:
                if move[2][4] == 'l': #castled left
                    self.state[int(x)+offset_x][int(y)+offset_y-1] = self.state[0][0]
                    self.state[0][0] = "--"
                    log_str=log_str,"castled-l-b:","BK"
                elif move[2][4] == 'r': #castled right
                    self.state[int(x)+offset_x][int(y)+offset_y+1] = self.state[0][7]
                    self.state[0][7] = "--"
                    log_str=log_str,"castled-r-b:","BK"
                self.castle[1] = 1

        #if move[3] == "true":
            #log_str=log_str,"captured:",oTile

        #update turn and check if it was a capture 

        #self.generateValidMoves()

        if (self.turn == "W"):

            #check if pawn was promoted
            if mPiece[1] == "P" and x==0: #if we reached end as a pawn
                log_str.append(("promotion:",self.state[move[0]][move[1]]))
                self.state[move[0]][move[1]] = "WQ" #update board state
                mPiece = "WQ" 
                print("Promoted: ", mPiece, "at", move[0], move[1])

            #check if king or rook moved for castle
            if self.castle[0] == 0:
                if mPiece[1] == "R" or mPiece[1] == "K":
                    self.castle[0] = 1
                    #print("White K or R moved, cant castle")

            if mPiece[1] == "K":
                self.kingPosW = (move[0],move[1])

            #update scores 
            self.scores[0] += self.getPieceScore(cPiece)

            #if oTile == "BK":
                #self.checkmate = True

            self.turn = "B"

        elif (self.turn == "B"):

            #check if pawn was promoted
            if mPiece[1] == "P" and move[0] == 7: #if we reached end as a pawn
                log_str.append(("promotion:",self.state[move[0]][move[1]]))
                self.state[move[0]][move[1]] = "BQ" #update board state
                mPiece = "BQ" 
                #print("Promoted: ", mPiece, "at", move[0], move[1])

            #check if king or rook moved for castle
            if self.castle[1] == 0:
                if mPiece[1] == "R" or mPiece[1] == "K":
                    self.castle[1] = 1
                    #print("Black K or R moved, cant castle")

            if mPiece[1] == "K":
                self.kingPosB = (move[0],move[1])

            #update scores 
            self.scores[1] += self.getPieceScore(cPiece)

            #if oTile == "WK":
                #self.checkmate = True

            self.turn = "W"

        #evaluate board
        #print("in check: ",self.inCheck())
        self.inCheck()
        self.evaluate_Board()

        self.log.append(log_str)
        #print(log_str)

    #method that takes a piece, and returns a list of possible indexes it can move to. only valid moves
    def validMoves(self,mPiece,mPiece_xy):
        possibleMoves=[]

        mPiece_x = int(mPiece_xy[0])
        mPiece_y = int(mPiece_xy[1])

        #print(mPiece)
        #print(mPiece_xy)

        #make sure to check if there is something in the way. 

        #possibleMove = ( piece_x, mPiece_y, "direction", "capture a piece?" )

        if mPiece[1] == "R": #Rook can move any tiles up, down, or side to side. check for 4 directions
            possibleMoves.extend(self.checkUp(mPiece,mPiece_x,mPiece_y,True,7))
            possibleMoves.extend(self.checkDown(mPiece,mPiece_x,mPiece_y,True,7))
            possibleMoves.extend(self.checkLeft(mPiece,mPiece_x,mPiece_y,True,7))
            possibleMoves.extend(self.checkRight(mPiece,mPiece_x,mPiece_y,True,7))
        elif mPiece[1] == "P": #Pawn can move only up once, twice at beginning. or diagonal if there is a capturable piece.
            if mPiece[0] == "W":
                possibleMoves.extend(self.checkUp(mPiece,mPiece_x,mPiece_y,False,1))
                possibleMoves.extend(self.checkUpRight(mPiece,mPiece_x,mPiece_y,True,1))
                possibleMoves.extend(self.checkUpLeft(mPiece,mPiece_x,mPiece_y,True,1))
            elif mPiece[0] == "B":
                possibleMoves.extend(self.checkDown(mPiece,mPiece_x,mPiece_y,False,1))   
                possibleMoves.extend(self.checkDownRight(mPiece,mPiece_x,mPiece_y,True,1))     
                possibleMoves.extend(self.checkDownLeft(mPiece,mPiece_x,mPiece_y,True,1)) 
        elif mPiece[1] == "N": #knight can skip over pieces too.
            possibleMoves.extend(self.checkNMoves(mPiece,mPiece_x,mPiece_y,True,"up_right"))
            possibleMoves.extend(self.checkNMoves(mPiece,mPiece_x,mPiece_y,True,"up_left"))
            possibleMoves.extend(self.checkNMoves(mPiece,mPiece_x,mPiece_y,True,"right_down"))
            possibleMoves.extend(self.checkNMoves(mPiece,mPiece_x,mPiece_y,True,"left_down"))
            possibleMoves.extend(self.checkNMoves(mPiece,mPiece_x,mPiece_y,True,"right_up"))
            possibleMoves.extend(self.checkNMoves(mPiece,mPiece_x,mPiece_y,True,"left_up"))
            possibleMoves.extend(self.checkNMoves(mPiece,mPiece_x,mPiece_y,True,"down_right"))
            possibleMoves.extend(self.checkNMoves(mPiece,mPiece_x,mPiece_y,True,"down_left"))
        elif mPiece[1] == "B":
            possibleMoves.extend(self.checkUpRight(mPiece,mPiece_x,mPiece_y,True,7))
            possibleMoves.extend(self.checkUpLeft(mPiece,mPiece_x,mPiece_y,True,7))
            possibleMoves.extend(self.checkDownRight(mPiece,mPiece_x,mPiece_y,True,7))     
            possibleMoves.extend(self.checkDownLeft(mPiece,mPiece_x,mPiece_y,True,7)) 
        elif mPiece[1] == "Q":
            possibleMoves.extend(self.checkUp(mPiece,mPiece_x,mPiece_y,True,7))
            possibleMoves.extend(self.checkDown(mPiece,mPiece_x,mPiece_y,True,7))
            possibleMoves.extend(self.checkLeft(mPiece,mPiece_x,mPiece_y,True,7))
            possibleMoves.extend(self.checkRight(mPiece,mPiece_x,mPiece_y,True,7))
            possibleMoves.extend(self.checkUpRight(mPiece,mPiece_x,mPiece_y,True,7))
            possibleMoves.extend(self.checkUpLeft(mPiece,mPiece_x,mPiece_y,True,7))
            possibleMoves.extend(self.checkDownRight(mPiece,mPiece_x,mPiece_y,True,7))     
            possibleMoves.extend(self.checkDownLeft(mPiece,mPiece_x,mPiece_y,True,7)) 
        elif mPiece[1] == "K":
            possibleMoves.extend(self.checkUp(mPiece,mPiece_x,mPiece_y,True,1))
            possibleMoves.extend(self.checkDown(mPiece,mPiece_x,mPiece_y,True,1))
            possibleMoves.extend(self.checkLeft(mPiece,mPiece_x,mPiece_y,True,1))
            possibleMoves.extend(self.checkRight(mPiece,mPiece_x,mPiece_y,True,1))
            possibleMoves.extend(self.checkUpRight(mPiece,mPiece_x,mPiece_y,True,1))
            possibleMoves.extend(self.checkUpLeft(mPiece,mPiece_x,mPiece_y,True,1))
            possibleMoves.extend(self.checkDownRight(mPiece,mPiece_x,mPiece_y,True,1))     
            possibleMoves.extend(self.checkDownLeft(mPiece,mPiece_x,mPiece_y,True,1))

        return possibleMoves

    #checks all knight directions
    def checkNMoves(self,mPiece,mPiece_x,mPiece_y,capture,dir):
        possibleMoves = []
        
        offset_x = 0
        offset_y = 0

        if dir == "up_right":
            offset_x = -2
            offset_y = 1
        if dir == "up_left":
            offset_x = -2
            offset_y = -1
        if dir == "right_down":
            offset_x = 1
            offset_y = 2
        if dir == "left_down":
            offset_x = 1
            offset_y = -2
        if dir == "right_up":
            offset_x = -1
            offset_y = 2
        if dir == "left_up":
            offset_x = -1
            offset_y = -2
        if dir == "down_right":
            offset_x = 2
            offset_y = 1
        if dir == "down_left":
            offset_x = 2
            offset_y = -1

        if (mPiece_x+offset_x) > -1 and (mPiece_x+offset_x) < 8 and (mPiece_y+offset_y) > -1 and (mPiece_y+offset_y) < 8:
            #print("x",mPiece_x,offset_x," ",mPiece_y,offset_y,"new: ",mPiece_x+offset_x,mPiece_y+offset_y)
            #print((mPiece_x+offset_x) <= 8)
            current_tile = self.state[mPiece_x+offset_x][mPiece_y+offset_y]
            if current_tile != "--": #check if piece in our way
                if current_tile[0] != mPiece[0] and capture == True: #if the tile we're on is other color
                    possibleMove = ( (mPiece_x+offset_x), (mPiece_y+offset_y), dir, "true", current_tile, mPiece_x, mPiece_y ) #add a possible move, that says we can capture
                    possibleMoves.append(possibleMove)
            else:
                possibleMove = ( (mPiece_x+offset_x), (mPiece_y+offset_y), dir, "false", "", mPiece_x, mPiece_y ) #add a possible move
                possibleMoves.append(possibleMove)
        return possibleMoves

    #checks up right, diagonal right.
    def checkUpRight(self,mPiece,mPiece_x,mPiece_y,capture,dist):
        possibleMoves = []
        for dir in range(1,dist+1):
            if (mPiece_x-dir) <= -1 or (mPiece_y+dir) >= 8:
                break
            current_tile = self.state[mPiece_x-dir][mPiece_y+dir]
            if current_tile != "--": #check if piece in our way
                if current_tile[0] != mPiece[0] and capture == True: #if the tile we're on is other color
                    possibleMove = ( (mPiece_x-dir), (mPiece_y+dir), "up-right", "true", current_tile, mPiece_x, mPiece_y ) #add a possible move, that says we can capture
                    possibleMoves.append(possibleMove)
                    break; #can't capture more than one piece
                else: #if tile we're on is our color
                    break; #can't move onto our own tile
            else:
                if mPiece[1] != "P":
                    possibleMove = ( (mPiece_x-dir), (mPiece_y+dir), "up-right", "false", "", mPiece_x, mPiece_y ) #add a possible move
                    possibleMoves.append(possibleMove)
        return possibleMoves

    #checks up left, diagonal left upwards.
    def checkUpLeft(self,mPiece,mPiece_x,mPiece_y,capture,dist):
        possibleMoves = []
        for dir in range(1,dist+1):
            if (mPiece_x-dir) <= -1 or (mPiece_y-dir) <= -1:
                break
            current_tile = self.state[mPiece_x-dir][mPiece_y-dir]
            if current_tile != "--": #check if piece in our way
                if current_tile[0] != mPiece[0] and capture == True: #if the tile we're on is other color
                    possibleMove = ( (mPiece_x-dir), (mPiece_y-dir), "up-left", "true", current_tile, mPiece_x, mPiece_y ) #add a possible move, that says we can capture
                    possibleMoves.append(possibleMove)
                    break; #can't capture more than one piece
                else: #if tile we're on is our color
                    break; #can't move onto our own tile
            else:
                if mPiece[1] != "P":
                    possibleMove = ( (mPiece_x-dir), (mPiece_y-dir), "up-left", "false", "", mPiece_x, mPiece_y ) #add a possible move
                    possibleMoves.append(possibleMove)
        return possibleMoves

    #checks down right, diagonal right downwards.
    def checkDownRight(self,mPiece,mPiece_x,mPiece_y,capture,dist):
        possibleMoves = []
        for dir in range(1,dist+1):
            if (mPiece_x+dir) >= 8 or (mPiece_y+dir) >= 8:
                break
            current_tile = self.state[mPiece_x+dir][mPiece_y+dir]
            if current_tile != "--": #check if piece in our way
                if current_tile[0] != mPiece[0] and capture == True: #if the tile we're on is other color
                    possibleMove = ( (mPiece_x+dir), (mPiece_y+dir), "down-right", "true", current_tile, mPiece_x, mPiece_y ) #add a possible move, that says we can capture
                    possibleMoves.append(possibleMove)
                    break; #can't capture more than one piece
                else: #if tile we're on is our color
                    break; #can't move onto our own tile
            else:
                if mPiece[1] != "P":
                    possibleMove = ( (mPiece_x+dir), (mPiece_y+dir), "down-right", "false", "", mPiece_x, mPiece_y ) #add a possible move
                    possibleMoves.append(possibleMove)
        return possibleMoves

    #checks down left, diagonal left downwards.
    def checkDownLeft(self,mPiece,mPiece_x,mPiece_y,capture,dist):
        possibleMoves = []
        for dir in range(1,dist+1):
            if (mPiece_x+dir) >= 8 or (mPiece_y-dir) <= -1:
                break
            current_tile = self.state[mPiece_x+dir][mPiece_y-dir]
            if current_tile != "--": #check if piece in our way
                if current_tile[0] != mPiece[0] and capture == True: #if the tile we're on is other color
                    possibleMove = ( (mPiece_x+dir), (mPiece_y-dir), "down-left", "true", current_tile, mPiece_x, mPiece_y ) #add a possible move, that says we can capture
                    possibleMoves.append(possibleMove)
                    break; #can't capture more than one piece
                else: #if tile we're on is our color
                    break; #can't move onto our own tile
            else:
                if mPiece[1] != "P":
                    possibleMove = ( (mPiece_x+dir), (mPiece_y-dir), "down-left", "false", "", mPiece_x, mPiece_y ) #add a possible move
                    possibleMoves.append(possibleMove)
        return possibleMoves

    #Checks tiles up, and returns a list of possible moves upwards.
    #capture is a bool if we can capture
    #dist is # of tiles piece can move
    def checkUp(self,mPiece,mPiece_x,mPiece_y,capture,dist):
        possibleMoves = []

        if mPiece[1] == "P": #if pawn is in its starting position, can move upwards 2
            if (mPiece[0] == "W" and mPiece_x == 6) or (mPiece[0] == "B" and mPiece_x == 1):
                dist=dist+1

        for dir in range(1,dist+1):
            if (mPiece_x-dir) <= -1:
                break
            current_tile = self.state[mPiece_x-dir][mPiece_y]
            if current_tile != "--": #check if piece in our way
                if current_tile[0] != mPiece[0] and capture == True: #if the tile we're on is other color
                    possibleMove = ( (mPiece_x-dir), mPiece_y, "up", "true", current_tile, mPiece_x, mPiece_y ) #add a possible move, that says we can capture
                    possibleMoves.append(possibleMove)
                    break; #can't capture more than one piece
                else: #if tile we're on is our color
                    break; #can't move onto our own tile
            else:
                possibleMove = ( (mPiece_x-dir), mPiece_y, "up", "false", "", mPiece_x, mPiece_y ) #add a possible move
                possibleMoves.append(possibleMove)
        return possibleMoves

    #Checks tiles down, and returns a list of possible moves down.
    def checkDown(self,mPiece,mPiece_x,mPiece_y,capture,dist):
        possibleMoves = []

        if mPiece[1] == "P": #if pawn is in its starting position, can move upwards 2
            if (mPiece[0] == "W" and mPiece_x == 6) or (mPiece[0] == "B" and mPiece_x == 1):
                dist=dist+1

        for dir in range(1,dist+1):
            if (mPiece_x+dir) >= 8:
                break
            current_tile = self.state[mPiece_x+dir][mPiece_y]
            if current_tile != "--": #check if piece in our way
                if current_tile[0] != mPiece[0] and capture == True: #if the tile we're on is other color
                    possibleMove = ( (mPiece_x+dir), mPiece_y, "down", "true", current_tile, mPiece_x, mPiece_y ) #add a possible move, that says we can capture
                    possibleMoves.append(possibleMove)
                    break; #can't capture more than one piece
                else: #if tile we're on is our color
                    break; #can't move onto our own tile
            else:
                possibleMove = ( (mPiece_x+dir), mPiece_y, "down", "false", "", mPiece_x, mPiece_y ) #add a possible move
                possibleMoves.append(possibleMove)
        return possibleMoves

    #Checks tiles left, and returns a list of possible moves.
    def checkLeft(self,mPiece,mPiece_x,mPiece_y,capture,dist):
        possibleMoves = []
        for dir in range(1,dist+1):
            if (mPiece_y-dir) <= -1:
                break
            current_tile = self.state[mPiece_x][mPiece_y-dir]
            if current_tile != "--": #check if piece in our way
                if current_tile[0] != mPiece[0] and capture == True: #if the tile we're on is other color
                    possibleMove = ( mPiece_x, (mPiece_y-dir), "left", "true", current_tile, mPiece_x, mPiece_y ) #add a possible move, that says we can capture
                    possibleMoves.append(possibleMove)
                    break; #can't capture more than one piece
                else: #if tile we're on is our color
                    break; #can't move onto our own tile
            else:
                #check for  castle
                if mPiece[1] == "K":
                    #print(self.check,self.turn,"left")
                    if self.turn == "W" and mPiece[0] == self.turn and self.castle[0] == 0 and self.check != "W": #check white side castle
                        if self.state[7][0] == "WR": #check if rook still there
                            for c in range(1,5): #check for clear path to rook
                                current_tile = self.state[mPiece_x][mPiece_y-c]
                                #print("Cur tile:",current_tile,"at",mPiece_x,mPiece_y-c)
                                if current_tile != "--":
                                    break
                            #if there is clear path, then return a possible castle move.
                            if current_tile == "WR":
                                #print("reached rook, add castle move")
                                possibleMove = ( mPiece_x, (mPiece_y-2), "c-w-left", "false", "", mPiece_x, mPiece_y ) #add castle move
                                possibleMoves.append(possibleMove)
                    elif self.turn == "B" and mPiece[0] == self.turn and self.castle[1] == 0 and self.check != "B": #check black side castle
                        if self.state[0][0] == "BR": #check if rook still there
                            for c in range(1,5): #check for clear path to rook
                                current_tile = self.state[mPiece_x][mPiece_y-c]
                                #print("Cur tile:",current_tile,"at",mPiece_x,mPiece_y-c)
                                if current_tile != "--":
                                    break
                            #if there is clear path, then return a possible castle move.
                            if current_tile == "BR":
                                possibleMove = ( mPiece_x, (mPiece_y-2), "c-b-left", "false", "", mPiece_x, mPiece_y ) #add castle move
                                possibleMoves.append(possibleMove)
                
                possibleMove = ( mPiece_x, (mPiece_y-dir), "left", "false", "", mPiece_x, mPiece_y ) #add a possible move
                possibleMoves.append(possibleMove)
        return possibleMoves

    #Checks tiles right, and returns a list of possible moves.
    def checkRight(self,mPiece,mPiece_x,mPiece_y,capture,dist):
        possibleMoves = []
        for dir in range(1,dist+1):
            if (mPiece_y+dir) >= 8:
                break
            current_tile = self.state[mPiece_x][mPiece_y+dir]
            if current_tile != "--": #check if piece in our way
                if current_tile[0] != mPiece[0] and capture == True: #if the tile we're on is other color
                    possibleMove = ( mPiece_x, (mPiece_y+dir), "right", "true", current_tile, mPiece_x, mPiece_y ) #add a possible move, that says we can capture
                    possibleMoves.append(possibleMove)
                    break; #can't capture more than one piece
                else: #if tile we're on is our color
                    break; #can't move onto our own tile
            else:
                #check for  castle
                if mPiece[1] == "K":
                    #print(self.check,self.turn,"right")
                    if self.turn == "W" and mPiece[0] == self.turn and self.castle[0] == 0 and self.check != "W": #check white side castle
                        #print("castle: ",self.castle[0])
                        if self.state[7][7] == "WR": #check if rook still there
                            for c in range(1,5): #check for clear path to rook
                                current_tile = self.state[mPiece_x][mPiece_y+c]
                                #print("Cur tile:",current_tile,"at",mPiece_x,mPiece_y-c)
                                if current_tile != "--":
                                    break
                            #if there is clear path, then return a possible castle move.
                            if current_tile == "WR":
                                #print("reached rook, add castle move")
                                possibleMove = ( mPiece_x, (mPiece_y+2), "c-w-right", "false", "", mPiece_x, mPiece_y ) #add castle move
                                possibleMoves.append(possibleMove)
                    elif self.turn == "B" and mPiece[0] == self.turn and self.castle[1] == 0 and self.check != "B": #check black side castle
                        #print("castle: ",self.castle[1])
                        if self.state[0][7] == "BR": #check if rook still there
                            for c in range(1,5): #check for clear path to rook
                                current_tile = self.state[mPiece_x][mPiece_y+c]
                                #print("Cur tile:",current_tile,"at",mPiece_x,mPiece_y-c)
                                if current_tile != "--":
                                    break
                            #if there is clear path, then return a possible castle move.
                            if current_tile == "BR":
                                possibleMove = ( mPiece_x, (mPiece_y+2), "c-b-right", "false", "", mPiece_x, mPiece_y ) #add castle move
                                possibleMoves.append(possibleMove)

                possibleMove = ( mPiece_x, (mPiece_y+dir), "right", "false", "", mPiece_x, mPiece_y ) #add a possible move
                possibleMoves.append(possibleMove)
        return possibleMoves
