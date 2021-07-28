import cv2
import numpy as np


board = cv2.imread('./chess/board.jpg')
cv2.imshow('board',board)
space = cv2.imread('./chess/c5.jpg')
cv2.imshow('space',space)
piece = cv2.imread('./chess/white bishop.jpg')
cv2.imshow('piece',piece)
reverse = cv2.bitwise_not(space)
cv2.imshow('reverse',reverse)
board = cv2.bitwise_and(board,reverse)
cv2.imshow('new board',board)
tile = cv2.bitwise_and(piece,space)
cv2.imshow('tile',tile)
board = cv2.bitwise_or(board,tile)
cv2.imshow('test',board)
cv2.waitKey(0)