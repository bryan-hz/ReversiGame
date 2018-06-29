from graphics import *
from time import sleep
import Tkinter
from tkMessageBox import *
import Board
from random import randint
from math import floor

dim = 8

boardHint = []

win = None
whiteTxt = None
blackTxt = None

cusWhite = color_rgb(240,240,240)
cusBlack = color_rgb(10,10,10)
bgColor = color_rgb(255,255,192)

def initBoard(win):

    boardRec = Rectangle(Point(100.0, 100.0), Point(450, 450))
    boardRec.setFill("White")
    boardRec.draw(win)

    whiteC = Circle(Point(520, 200), 10)
    whiteC.setFill(cusBlack)
    whiteC.draw(win)
    
    blackC = Circle(Point(520, 300), 10)
    blackC.setFill(cusWhite)
    blackC.draw(win)
    
    semiW = Text(Point(540, 200), ":") 
    semiW.setSize(20)
    semiW.draw(win)

    semiB = Text(Point(540, 300), ":") 
    semiB.setSize(20)
    semiB.draw(win)

    for i in xrange(1, dim):
        l = Line(Point(100.0, 100.0+ i * 350.0/dim), Point(450, 100.0 + i * 350.0/dim))
        l.draw(win) 

    for i in xrange(1, dim):
        l = Line(Point(100.0 + i * 350.0/dim, 100.0), Point(100.0 + i * 350.0/dim, 450))
        l.draw(win) 

    whiteC1 = Circle(Point(100.0+((dim-1))*350.0/(2*dim), 100.0+((dim-1))*350.0/(2*dim)), 0.7*350.0/(2*dim))
    whiteC1.setFill(cusWhite)
    whiteC1.draw(win)

    blackC1 = Circle(Point(100.0+((dim-1))*350.0/(2*dim), 100.0+((dim+1))*350.0/(2*dim)), 0.7*350.0/(2*dim))
    blackC1.setFill(cusBlack)
    blackC1.draw(win)

    blackC2 = Circle(Point(100.0+((dim+1))*350.0/(2*dim), 100.0+((dim-1))*350.0/(2*dim)), 0.7*350.0/(2*dim))
    blackC2.setFill(cusBlack)
    blackC2.draw(win)

    whiteC2 = Circle(Point(100.0+((dim+1))*350.0/(2*dim), 100.0+((dim+1))*350.0/(2*dim)), 0.7*350.0/(2*dim))
    whiteC2.setFill(cusWhite)
    whiteC2.draw(win)

    return

def drawHint(win):

    ##print boardHint

    gridLen = 350.0/dim

    trash = []

    for i in xrange(len(boardHint)):
        startPoint = Point(100+gridLen*boardHint[i].y,100+gridLen*boardHint[i].x)
        endPoint = Point(100+gridLen*(1+boardHint[i].y) , 100+gridLen*(1+boardHint[i].x))
        rec = Rectangle(startPoint, endPoint)
        rec.setFill(color_rgb(152, 251, 152))
        rec.draw(win)
        trash.append(rec)
    return trash

def drawMessage(win, message):

    rec = Rectangle(Point(0, 200), Point(720, 320))
    rec.setFill("Black")
    rec.draw(win)

    messageTxt = Text(Point(360, 260), message)
    messageTxt.setStyle("bold italic")
    messageTxt.setSize(30)
    messageTxt.setOutline("White")

    messageTxt.draw(win)

    sleep(1.5)

    messageTxt.undraw()
    rec.undraw()

    return

def drawMove(win, x, y, player):

    sleep(0.1)

    target = cusBlack if(player == 0) else cusWhite

    centerX = 100.0 + 350.0/(2.0*dim) + floor(y) * 350.0/dim
    centerY = 100.0 + 350.0/(2.0*dim) + floor(x) * 350.0/dim

    c = Circle(Point(centerX, centerY), 0.7*350.0/(2.0*dim))
    c.setFill(target)
    c.draw(win)

    if(Board.makeMove(win, player, int(x), int(y)) == False):
        sleep(0.2)
        c.undraw()
        return False

    return True

def computerMakeMove(e):

    def computeRank(p):
        curRank = 0
        if((p.x == 0) or (p.x == 7)):
            curRank += 10
        if((p.y == 0) or (p.y == 7)):
            curRank += 10
        if((p.x == 1) or (p.x == 6)):
            curRank -= 15
        if((p.y == 1) or (p.y == 6)):
            curRank -= 15
        return curRank

    ranks = []

    for i in xrange(len(boardHint)):
        curRank = computeRank(boardHint[i])
        ranks.append(curRank)
    
    maxRank = max(ranks)
    indices = []

    for i in xrange(len(boardHint)):
        if(ranks[i] == maxRank):
            indices.append(i)
    return indices[randint(0, len(indices)-1)]


def setPVEList():

    pList = []

    userInput = Tkinter.Tk()
    userInput.title("Message")

    def readInput(e):
        inputString = inputBox.get()
        if(inputString==""):
            showinfo("Warning", "Player name cannot be 'None'")
            return
        pList.append(inputString)
        userInput.quit()
        return

    inputLabel = Tkinter.Label(userInput, text="Please enter your name: ")
    inputLabel.config(font="times 15 italic")
    inputLabel.pack(side=Tkinter.LEFT)

    inputBox = Tkinter.Entry(userInput,text="something",width=40)
    inputBox.pack(side=Tkinter.LEFT, padx=5)
    inputBox.bind("<Return>", readInput)
    
    confirmButton = Tkinter.Button(userInput, text=u"\u23ce", command = lambda:readInput(0))
    confirmButton.pack(side=Tkinter.RIGHT)
    
    userInput.mainloop()
    userInput.destroy()

    ##print pList

    top = Tkinter.Toplevel()
    #top.geometry("200x320")
    top.title("Message")
    
    def whiteEvent():
        pList.append("Computer")
        top.quit()
        return  

    def blackEvent():
        pList.append("Computer")
        pList.reverse()
        top.quit()
        return

    topMessage = Tkinter.Label(top, text="Do you want to playe Black or White?")
    topMessage.config(font="Times 18 bold italic")
    topMessage.pack(padx=20, pady=30)

    whiteButton = Tkinter.Button(top, text="White", fg="blue", command=blackEvent)
    whiteButton.config()
    whiteButton.pack(side=Tkinter.BOTTOM, pady=10)   

    blackButton = Tkinter.Button(top, text="Black", fg="blue", command=whiteEvent)
    blackButton.config()
    blackButton.pack(side=Tkinter.BOTTOM) 

    top.mainloop()
    top.destroy()

    return pList


def setPVPList():

    pList = ["", ""]

    userInput = Tkinter.Tk()
    userInput.title("Message")

    def readInput(e):
        inputString = inputBox.get()
        if(inputString == ""):
            showinfo("Warning", "Player 1's name cannot be 'None'")
            return
        if(pList[0] == inputString):
            return
        pList.reverse()
        pList.pop()
        pList.append(inputString)
        pList.reverse()
        inputBox.event_generate("<<TraverseOut>>")
        inputBox2.focus()
        inputBox2.event_generate("<<TraverseIn>>")

        return
    
    def readInput2(e):
        inputString = inputBox2.get()        
        if(inputString == ""):
            showinfo("Warning", "Player 2's name cannot be 'None'")
            return 
        if(pList[1] == inputString):
            return
        pList.pop()
        pList.append(inputString)
        
        doneInsert(0)

        return

    def doneInsert(e):
        readInput(0)
        readInput2(0)

        if((pList[0] == "") or (pList[1] == "")):
            return
        
        if(pList[0] == pList[1]):
            showinfo("Warning", "Two players cannot be the same name")
            return      
        userInput.quit()

    confirmButton = Tkinter.Button(userInput, text="Done", width = 5, command = lambda: doneInsert(0))
    confirmButton.bind("<Return>", doneInsert)
    confirmButton.grid(row = 1, column = 2)

    inputLabel = Tkinter.Label(userInput, text="Please enter Player 1's name: ")
    inputLabel.config(font="times 15 italic")
    inputLabel.grid(row=0, column=0)

    inputBox = Tkinter.Entry(userInput,text="something",width=40)
    inputBox.grid(row=0, column=1)
    inputBox.bind("<Return>", readInput)    
    
    inputLabel2 = Tkinter.Label(userInput, text="Please enter Player 2's name: ")
    inputLabel2.config(font="times 15 italic")
    inputLabel2.grid(row=1, column=0)

    inputBox2 = Tkinter.Entry(userInput,text="a",width=40)
    inputBox2.grid(row=1,column=1, padx=5)
    inputBox2.bind("<Return>", readInput2)

    userInput.mainloop()
    userInput.destroy()

    return pList
        
def main():

    settings = []

    def pvpEvent():
        #showinfo("Message", "Chosen PVP mode")
        settings.append(False)
        menu.quit()
        return

    def pveEvent():
        #showinfo("Message", "Chosen PVE mode")
        settings.append(True)
        menu.quit()
        return

    def doQuit(quitConfirm):
        quitConfirm.destroy()
        menu.quit()
        exit(0)

    def quitEvent(e):
        if askyesno("Message", "Are you sure you want to quit?"):
            menu.quit()
            exit(0)
        return

    menu = Tkinter.Tk()
    menu.bind("<Escape>", quitEvent)
    menu.title("Menu")
    #menu.geometry("250x320")

    menuMessage = Tkinter.Label(menu, text="Please choose playing mode:", pady=50)
    menuMessage.config(font="Times 18 bold italic")
    menuMessage.pack()

    pvpButton = Tkinter.Button(menu, text="Player vs Player", command=pvpEvent, fg="blue")
    pvpButton.config()
    pvpButton.pack()

    pveButton = Tkinter.Button(menu, text="Player vs Computer", command=pveEvent, fg="blue")
    pveButton.config()
    pveButton.pack()

    quitButton = Tkinter.Button(menu, text="Exit", command=lambda:quitEvent(0), fg="blue", width=5)
    quitButton.config()
    quitButton.pack()

    menuMessage = Tkinter.Label(menu, text="", pady=25)
    menuMessage.config()
    menuMessage.pack(side=Tkinter.BOTTOM)

    menu.mainloop()
    menu.destroy()

    auto = settings[0]

    playerList = setPVEList() if(auto==True) else setPVPList()

    ##print playerList
    global win, whiteTxt, blackTxt, boardHint

    if(win == None):
        win = GraphWin("Reversi Game", 720, 540)
        win.setBackground(bgColor)
        win.customBind("<Escape>")

    titleTxt = Text(Point(350.0, 50), "Reversi")
    titleTxt.setStyle("bold italic")
    titleTxt.setSize(50)
    titleTxt.draw(win)

    Board.iniBoard(dim)
    initBoard(win)

    whiteTxt = Text(Point(580, 300), "2")
    whiteTxt.setSize(20)
    whiteTxt.draw(win)

    blackTxt = Text(Point(580, 200), "2")
    blackTxt.setSize(20)
    blackTxt.draw(win)

    consoleRec = Circle(Point(100, 490), 10)
    consoleRec.setFill(bgColor)
    consoleRec.setOutline(bgColor)
    consoleRec.draw(win)

    consoleTxt = Text(Point(250, 490), ">>      Click anywhere to start")
    consoleTxt.setStyle("italic")
    consoleTxt.setSize(15)
    consoleTxt.draw(win)
    
    win.getMouse()
    drawMessage(win, "Game Start")
    player = 0
    cannotMove = 0
    while(True):
        
        boardHint = Board.movability(player)   

        if(len(boardHint) == 0):
            drawMessage(win, playerList[player] + " cannot move")
            player = not player
            cannotMove += 1

            if(cannotMove == 2):
                endMessage = Board.gameOver(playerList)
                consoleRec.setFill(bgColor)
                consoleRec.setOutline(bgColor)
                consoleTxt.setText("")
                sleep(0.2)
                showinfo("Game over", endMessage)
                #drawMessage(win, endMessage)
                consoleTxt.setText(">>      Click anywhere to restart")
                pr = win.getMouse()
                win.close()
                win = None
            else:
                continue

        cannotMove = 0
        trash = drawHint(win)

        ##print("Wait " + playerList[player] + " to make move")        
        hintColor = cusBlack if(player == 0) else cusWhite
        consoleRec.setOutline("Black")
        consoleRec.setFill(hintColor)
        consoleTxt.setText(">>  Wait " + playerList[player] + " to make move")
        
        areaRow = 0
        areaCol = 0

        if(auto == True and playerList[player] == "Computer"):
            sleep(0.5)

            moveIndex = computerMakeMove(boardHint)

            areaCol = boardHint[moveIndex].x
            areaRow = boardHint[moveIndex].y
        else:
            pr = None
            validClick = False
            while(validClick == False):
                pr = win.getMouse()
                areaRow = int((pr.x-100.0) / (350.0/dim))
                areaCol = int((pr.y-100.0) / (350.0/dim))
                ##print(pr)
                if((0 <= areaCol < 8) and (0 <= areaCol < 8)):
                    ##print("Detected click on board")
                    validClick = True  
                  
        for i in xrange(len(trash)):
            trash[i].undraw()
        if(drawMove(win, areaCol, areaRow, player) == True):
            whiteTxt.setText(Board.oCount)
            blackTxt.setText(Board.xCount)
            player = not player

        endMessage = Board.gameOver(playerList)
        if(endMessage != ""):
            consoleRec.setFill(bgColor)
            consoleRec.setOutline(bgColor)
            consoleTxt.setText("")
            sleep(0.2)
            showinfo("Game over", endMessage)
            #drawMessage(win, endMessage)
            consoleTxt.setText(">>      Click anywhere to restart")
            pr = win.getMouse()
            win.close()
            win = None
            break 
        else:
            pass
    main()

main()

exit(0)

from Tkinter import *

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()
   
root = Tk()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
root.mainloop()
