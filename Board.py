import copy

from math import floor
from graphics import *
from time import sleep

Board = []
xCount = 0
oCount = 0

def printBoard(Board):

    global xCount, oCount

    xCount = 0
    oCount = 0

    #print("\n "),
    for i in xrange(len(Board)):
        pass
        #print(i),
    #print

    for i in xrange(len(Board)):
        #print(i),
        for j in xrange(len(Board)):
            if(Board[i][j] == 'x'):
                xCount += 1
            elif(Board[i][j] == 'o'):
                oCount += 1
            else:
                pass
            #print(Board[i][j]),
        #print
    
    #print("Summary:\nx: " + str(xCount) + "\no: " + str(oCount) + "\n")
    return

def iniBoard(dim):

    global Board

    Board = []
    for x in xrange(dim):
        Board.append([])
        for y in xrange(dim):
            Board[x].append('*')

    Board[dim/2-1][dim/2-1] = 'o'
    Board[dim/2-1][dim/2] = 'x'
    Board[dim/2][dim/2-1] = 'x'
    Board[dim/2][dim/2] = 'o'
    
    printBoard(Board)

    return

def gameOver(player):

    global Board

    unoccupied = 0
    xCount = 0
    oCount = 0

    for i in xrange(len(Board)):
        for j in xrange(len(Board)):
            if(Board[i][j] == 'x'):
                xCount += 1
            elif(Board[i][j] == 'o'):
                oCount += 1
            else:
                unoccupied += 1
    
    if(unoccupied == 0):
        if(xCount > oCount):
            #print("\nCongratulations: " + player[0] + " win\n")
            return "\nCongratulations: " + player[0] + " win\n"
        elif(xCount < oCount):
            #print("\nCongratulations: " + player[1] + " win\n")
            return "\nCongratulations: " + player[1] + " win\n"
        else:
            #print("\nDraw\n")
            return "\nDraw\n"
        return True
    elif(xCount == 0):
        #print("\nCongratulations: " + player[1] + " win\n")
        return "\nCongratulations: " + player[1] + " win\n"
    elif(oCount == 0):
        #print("\nCongratulations: " + player[0] + " win\n")
        return "\nCongratulations: " + player[0] + " win\n"
    else:
        return ""

def checkMove(target, oppo, col, row, coliter, rowiter):

    global Board
    dim = len(Board)

    col += coliter
    row += rowiter

    if((0 <= col < dim) and (0 <= row < dim) and Board[col][row] == oppo):
        while((0 <= col < dim) and (0 <= row < dim)):
            if(Board[col][row] == '*'):
                return False
            elif(Board[col][row] == target):
                return True
            else:
                pass       
            col += coliter
            row += rowiter
    return False

def movability(player):

    #print("\nPossible move(for"),

    global Board

    tempBoard = copy.deepcopy(Board)
    target = 'x' if(player == 0) else 'o'
    oppo = 'o' if(player == 0) else 'x'
    #print(target + "):")

    boardHint = []

    hasMove = False
    for i in xrange(len(tempBoard)):
        for j in xrange(len(tempBoard)):
            if(Board[i][j] == '*'):
                if((checkMove(target, oppo, i, j, 0, 1) == True)
                    or (checkMove(target, oppo, i, j, 0, -1) == True)
                    or (checkMove(target, oppo, i, j, 1, 0) == True)
                    or (checkMove(target, oppo, i, j, -1, 0) == True)
                    or (checkMove(target, oppo, i, j, 1, 1) == True)
                    or (checkMove(target, oppo, i, j, 1, -1) == True)
                    or (checkMove(target, oppo, i, j, -1, 1) == True)
                    or (checkMove(target, oppo, i, j, -1, -1) == True)):
                    tempBoard[i][j] = '_'
                    boardHint.append(Point(i, j))
                    hasMove = True

    if(hasMove == False):
        ##print("\nPlayer " + str(player+1) + " cannot move\n")
        return boardHint
    else:
        printBoard(tempBoard)
        return boardHint

def flop(win, target, col, row, coliter, rowiter):

    global Board
    dim = len(Board)

    cusWhite = color_rgb(240,240,240)
    cusBlack = color_rgb(10,10,10)

    targetColor = cusBlack if(target == 'x') else cusWhite

    col += coliter
    row += rowiter 
    while((0 <= col < dim) and (0 <= row < dim) and (Board[col][row] != target)):
        Board[col][row] = target
        
        centerX = 100.0 + 350.0/(2.0*dim) + floor(row) * 350.0/dim
        centerY = 100.0 + 350.0/(2.0*dim) + floor(col) * 350.0/dim

        c = Circle(Point(centerX, centerY), 0.7*350.0/(2.0*dim))
        c.setFill(targetColor)
        c.draw(win)    

        sleep(0.3)

        col += coliter
        row += rowiter  
    return

def makeMove(win, player, col, row):

    global Board
    
    target = 'x' if(player == 0) else 'o'
    oppo = 'o' if(player == 0) else 'x'
    
    hasMove = False
    for i in xrange(-1, 2):
        for j in xrange(-1, 2):
            if(i == 0 and j == 0):
                continue
            if((Board[col][row] == '*') and (checkMove(target, oppo, col, row, i, j) == True)):
                hasMove = True
                flop(win, target, col, row, i, j)
 
    if(hasMove == True):
        Board[col][row] = target
        printBoard(Board)
        return True
    else:
        return False

def helpMenu():
    #print("\n * enter 'q' to quit")
    #print(" * enter 2 numerical numbers to make move, \n     ex: '2 3' to choose at row 2 col 3\n")
    return

def main():

    iniBoard()

    player = 0

    while(True):
        """"
        if(movability(player) == False):
            player = not player
            continue
        """
        cmd = raw_input(" >> Player " + str(player + 1) + " make move or enter 'help' for help menu:\n$")
         ##print("Confirm command: " + cmd)
        
        x = cmd.split(' ')
        if(len(x) > 2):
            #print("\nToo many arguments, please enter again or enter 'help' for help menu\n")
            continue

        if(x[0] == 'q'):
            return

        if(x[0] == 'help'):
            helpMenu()
            continue
        
        if(len(x) != 2 or x[0].isdigit() == False or x[1].isdigit() == False):
            #print("\nPlease enter 2 numerical number or enter 'help' for help menu\n")
            continue
        """"
        if(makeMove(player, int(x[0]), int(x[1])) == False):
            #print("\nInvalid move, no move is made. Please enter again")
            continue
        """
        if(gameOver() == True):
            return 
        else:
            player = not player

    return

#main()
