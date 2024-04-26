#user input, game state
import pygame as pGame #use pygame as GUI for our project
import random
import game_state, images, driver

#AI VARIABLES:
ALPHA = float("inf")
BETA = float("-inf")
DEPTH = 2

pieces_png = {}
pieces_png = images.loadPNG(pieces_png) #loads images dictonary with our pngs
board_color = images.loadColors()

def main():
    pGame.init() #start pygame

    #Game Variables:
    game_clock = pGame.time.Clock()
    current_state = game_state.gState()
    game_active = True
    current_state.depth = DEPTH

    #Board Display
    state_display = pGame.display.set_mode((400,400)) #400 pixels by 400 pixels resolution
    state_display.fill(pGame.Color("white")) #fills board with white

    #Main Game loop
    gameLoop(current_state,state_display,game_active,game_clock)
    
def gameLoop(current_state,state_display,game_active,game_clock):
    mValidMoves = [] #list of possible moves
    mPieceIndex = "" #index our user selected
    mPiece = "" #piece at our index. eg "BP"
    cPiece = "" #captured piece
    mCount = 0 #number of clicks

    while game_active and current_state.checkmate == False:
        for event in pGame.event.get(): #event handling
            if event.type == pGame.QUIT: #quit
                game_active = False
            elif event.type == pGame.KEYDOWN:
                if event.key == pGame.K_1: #if user presses 1, undos recent move
                    current_state.undoMove()
                if event.key == pGame.K_2: #if user presses 2, switches on/off AI
                    current_state.AI=not current_state.AI
                    print("AI active:",current_state.AI)
            elif event.type == pGame.MOUSEBUTTONDOWN: #user clicks

                if current_state.turn == "W" or current_state.AI == False:

                    mPos = pGame.mouse.get_pos()
                    squareSize = 400/8
                    y = mPos[0]//squareSize
                    x = mPos[1]//squareSize

                    print("Clicked: ", current_state.state[int(x)][int(y)], " at: ", int(x),int(y))

                    if mCount == 1:
                        #use method to determine our possible moves
                        #for every possible move, if our cursor matches a possible move index, then move there.
                        for move in mValidMoves:
                            #print(move[0])
                            if int(x) == move[0] and int(y) == move[1]:
                                current_state.makeMove(int(x),int(y),move,mPiece,mPieceIndex,cPiece)
                                break
                        mPieceIndex = ""
                        mPiece = ""
                        mCount = 0
                        cPiece = "" 
                        mValidMoves=[]        
                    else:
                        if mPieceIndex == (x,y): #check if user click same pos twice, reset selected piece and click count
                            mPieceIndex = ""
                            mPiece = ""
                            mCount = 0
                            mValidMoves=[]
                        else: #first click
                            mPieceIndex = (x,y)
                            mPiece = current_state.state[int(x)][int(y)]
                            if mPiece != "--": #if we didnt first select an empty square, 
                                if isProperSide(mPiece,current_state.turn): #check if piece is our side
                                    mCount+=1
                                    print("Selected: ", current_state.state[int(x)][int(y)], " at: ", int(x),int(y))
                                    mValidMoves=current_state.validMoves(mPiece,mPieceIndex)
                                    #for move in mValidMoves:
                                        #print(move)
                                else:
                                    mPieceIndex = ""
                                    mPiece = ""
                                    mCount = 0
                                    mValidMoves=[]
                            else: #if we selected an empty square first, or a piece that isnt ours then reset clicks
                                mPieceIndex = ""
                                mPiece = ""
                                mCount = 0
                                mValidMoves=[]

        #ai turn
        if current_state.turn == "B" and current_state.AI == True:
            
            moves = current_state.generateValidMoves()

            if len(moves) > 0: #check for a stalemate

                #generate a random starting move for the AI:
                x=random.randint(0,len(moves)-1)

                current_state.nextMove = current_state.alpha_beta_search(moves,DEPTH,200,-200,False,moves[x])[1]
                move = current_state.nextMove
                current_state.makeMove(move[0],move[1],move,current_state.state[move[5]][move[6]],(move[5],move[6]),"")

                #print(fmove)
                #current_state.makeMove(fmove[0],fmove[1],fmove,current_state.state[fmove[5]][fmove[6]],(fmove[5],fmove[6]),cPiece)
                #current_state.undoMove()

        game_clock.tick(15) #used for animation
        pGame.display.flip()
        drawState(state_display, current_state, mPieceIndex, mValidMoves)
        pGame.display.update()

#return "W" or "B" based on what piece was clicked at mPos
def isProperSide(mPiece,side):
    if mPiece[0] == side:
        return True
    return False

#paints tiles onto pygame display
def drawState(state_display, gState, mPieceIndex, mValidMoves):
    squareSize = 400/8
    for x in range(8): 
        for y in range(8):

            drawRectangle = pGame.Rect(y*squareSize,x*squareSize,squareSize,squareSize)
            paint = (y+x)%2 #chooses to paint a white or gray square every even or odd tile. 

            #draw tiles
            if paint == 0:
                #paint white
                pGame.draw.rect(state_display,board_color[0],drawRectangle)
            else:
                #paint gray
                pGame.draw.rect(state_display,board_color[1],drawRectangle)

            #draw highlighted square if any
            if mPieceIndex !="":
                if int(mPieceIndex[0]) == x and int(mPieceIndex[1] == y):
                    pGame.draw.rect(state_display,"red",drawRectangle)

            #draw possible moves onto squares
            if len(mValidMoves) > 0:
                for move in mValidMoves:
                    drawMove = pGame.Rect(move[1]*squareSize,move[0]*squareSize,squareSize,squareSize)
                    if move[2][0] == 'c':
                        state_display.blit(pieces_png["cmove"],drawMove) 
                    else:
                        state_display.blit(pieces_png["pmove"],drawMove)

            #draw check
            if gState.check == 'W':
                drawCheck = pGame.Rect(gState.kingPosW[1]*squareSize,gState.kingPosW[0]*squareSize,squareSize,squareSize)
                state_display.blit(pieces_png["check"],drawCheck)
            elif gState.check == "B":
                drawCheck = pGame.Rect(gState.kingPosB[1]*squareSize,gState.kingPosB[0]*squareSize,squareSize,squareSize)
                state_display.blit(pieces_png["check"],drawCheck)

            #draw images of pieces, avoiding empty squares "--"
            p = gState.state[x][y]
            if p != "--":
                state_display.blit(pieces_png[p],drawRectangle) #draws a rectangle and displays png of associated piece with it

            

main()