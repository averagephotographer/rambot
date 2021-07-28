import cv2
import numpy as np

fileRef = ['a','b','c','d','e','f','g','h']
pieceRef = {'wr':'white rook','wn':'white knight','wb':'white bishop','wq':'white queen','wk':'white king','wp':'white pawn',
            'br':'black rook','bn':'black knight','bb':'black bishop','bq':'black queen','bk':'black king','bp':'black pawn'}

def setBoard():
    board = []
    for i in range(8):
        board.append([])
        for x in range(8):
            board[i].append(None)
    board[0][0] = 'wr'
    board[7][0] = 'wr'
    board[1][0] = 'wn'
    board[6][0] = 'wn'
    board[2][0] = 'wb'
    board[5][0] = 'wb'
    board[3][0] = 'wq'
    board[4][0] = "wk"
    for i in range(8): board[i][1] = 'wp'
    board[0][7] = 'br'
    board[7][7] = 'br'
    board[1][7] = 'bn'
    board[6][7] = 'bn'
    board[2][7] = 'bb'
    board[5][7] = 'bb'
    board[3][7] = 'bq'
    board[4][7] = 'bk'
    for i in range(8): board[i][6] = 'bp'
    return board


def boardGen(board):
    boardImage = cv2.imread('./chess/board.jpg')
    for rank in range(8):
        for file in range(8):
            if board[file][rank] == None:
                continue
            space = cv2.imread('./chess/{}{}.jpg'.format(fileRef[file],rank+1))
            piece = cv2.imread('./chess/{}.jpg'.format(pieceRef[board[file][rank]]))
            reverse = cv2.bitwise_not(space)
            boardImage = cv2.bitwise_and(boardImage,reverse)
            tile = cv2.bitwise_and(piece,space)
            boardImage = cv2.bitwise_or(boardImage,tile)
    return boardImage



board = setBoard()
boardCV = boardGen(board)
cv2.imshow('test',boardCV)
cv2.waitKey(0)
board[4][1] = None
board[4][3] = 'wp'
boardCV = boardGen(board)
cv2.imshow('e4',boardCV)
cv2.waitKey(0)
board[3][6] = None
board[3][4] = 'bp'
boardCV = boardGen(board)
cv2.imshow('Scandinavian',boardCV)
cv2.waitKey(0)