#class creates a dictonary that associates our pieces with their png
import pygame as pGame

#init a dictionary that corresponds a png to our pieces
def loadPNG(pieces_png):
    squareSize = 400/8
    pieces_png = {}
    pieces_png["BB"] = pGame.transform.scale(pGame.image.load("images_pieces/bb.png"),(squareSize,squareSize)) #Black Bishop
    pieces_png["BK"] = pGame.transform.scale(pGame.image.load("images_pieces/bk.png"),(squareSize,squareSize)) #Black King
    pieces_png["BN"] = pGame.transform.scale(pGame.image.load("images_pieces/bn.png"),(squareSize,squareSize)) #Black Knight
    pieces_png["BP"] = pGame.transform.scale(pGame.image.load("images_pieces/bp.png"),(squareSize,squareSize)) #Black Pawn
    pieces_png["BQ"] = pGame.transform.scale(pGame.image.load("images_pieces/bq.png"),(squareSize,squareSize)) #Black Queen
    pieces_png["BR"] = pGame.transform.scale(pGame.image.load("images_pieces/br.png"),(squareSize,squareSize)) #Black Rook

    pieces_png["WB"] = pGame.transform.scale(pGame.image.load("images_pieces/wb.png"),(squareSize,squareSize)) #White Bishop
    pieces_png["WK"] = pGame.transform.scale(pGame.image.load("images_pieces/wk.png"),(squareSize,squareSize)) #White King
    pieces_png["WN"] = pGame.transform.scale(pGame.image.load("images_pieces/wn.png"),(squareSize,squareSize)) #White Knight
    pieces_png["WP"] = pGame.transform.scale(pGame.image.load("images_pieces/wp.png"),(squareSize,squareSize)) #White Pawn
    pieces_png["WQ"] = pGame.transform.scale(pGame.image.load("images_pieces/wq.png"),(squareSize,squareSize)) #White Queen
    pieces_png["WR"] = pGame.transform.scale(pGame.image.load("images_pieces/wr.png"),(squareSize,squareSize)) #White Rook

    pieces_png["pmove"] = pGame.transform.scale(pGame.image.load("images_pieces/pmove.png"),(squareSize,squareSize)) #highlight possible moves
    pieces_png["cmove"] = pGame.transform.scale(pGame.image.load("images_pieces/cmove.png"),(squareSize,squareSize)) #highlight castle move
    pieces_png["check"] = pGame.transform.scale(pGame.image.load("images_pieces/check.png"),(squareSize,squareSize)) #highlight check

    return pieces_png

#returns colors used for the board
def loadColors():
    colors = [pGame.Color("white"), pGame.Color("gray")]
    return colors