#ULTIMATE KAZOO TETRIS: HARD MODE
# A game by Matthew Varona and Shaurya Singh

# Features:
# >Beautiful original soundtrack by world-renowned kazoo virtuoso Matthew Varona
# >Arcade mode: Game punishes you for leaving holes or overhangs in your board
# >Level is determined by score, and speed ramps up based on level
# >More points for line-clearing combos (4, 3, or 2)
# >Bonus points for hard-dropping blocks
# >Player cannot hold multiple blocks in a row 

add_library("minim")
import os
from random import *

#Create audio player for our brilliant original soundtrack
audioPlayer = Minim(this)

myDir = os.getcwd()
 
class Menu():
    def __init__(self):
        self.title = "Ultimate Kazoo Tetris: Hard Mode"
    def printMenu(self):
        #Display menu
        background(10)
        textAlign(CENTER)
        textSize(40)
        fill(255)
        text(self.title, w/2, w/5*1.5)
        rectMode(CENTER)
        rect(w/2, w/5*2.5, 400, 100, 10)
        fill(0)
        text("Classic", w/2, w/5*2.6)
        rectMode(CENTER)
        fill(255)
        rect(w/2, w/5*3.5, 400, 100, 10)
        fill(0)
        text("Arcade", w/2, w/5*3.6)
 
class Game():
    #Game class that contains a board
    def __init__(self, numRows, numCols, w):
        self.rows = numRows
        self.cols = numCols
        self.board = Board(self.rows, self.cols, w)
        self.score = 0
        self.level = 1
        self.gameOver = False
        #Only one piece is active at a time; sets to 0 at the beginning of the game
        self.activePiece = 0
        #Key handlers for keyboard input
        self.keyHandler = {LEFT:False, RIGHT:False, UP:False, DOWN:False, 'z':False, 'c':False, ' ':False}
        #The piece descends every self.fps frames
        self.fps = 30
        #Cooldown value for hard drop
        self.dropCooldown = 0
        self.holdCooldown = 0
        self.justHeld = False
        #Array of next pieces; fill and ensure pieces don't come right after each other
        self.nextPieces = []
        while len(self.nextPieces) < 3:
            addedPiece = randint(0, 6)
            if not addedPiece in self.nextPieces:
                self.nextPieces.append(addedPiece)
                
        #Bool to determine extra points for hard drops
        self.droppedHard = False
        #Have values for active piece and held piece. These initialize at 500 to signify that they do not exist yet
        self.currentPieceValue = 500
        self.heldPiece = 500
        
        #Variable to count how many holes there are (for Arcade Mode)
        self.holeCount = 0
        #Bool for activating Arcade Mode
        self.arcade = False
        
        #Initialize a new piece at the start of the game
        self.newPiece()
        
        #Don't start the game unless the menu has been bypassed
        self.start = False
        
        #Beautiful original music
        self.themeSong = audioPlayer.loadFile(myDir + "/assets/tetristheme.mp3")
        self.rowSound = audioPlayer.loadFile(myDir + "/assets/lineclear.mp3")
        self.noHold = audioPlayer.loadFile(myDir + "/assets/cooldown.mp3")
        self.loserSound = audioPlayer.loadFile(myDir + "/assets/losersound.mp3")
                
    def playGame(self):
        #Call all relevant game functions
        background(30)
        self.themeSong.play()
        game.holdPiece()
        game.activePiece.fastDrop()
        if frameCount % game.fps == 0:
            game.fall()
        game.activePiece.movePiece()
        game.activePiece.rotatePiece()
        game.board.printBoard()
        game.activePiece.updatePiece()
        game.activePiece.printPiece()
        game.displayNextBlocks()
        game.increaseLevel()
        game.showScore()
        game.printHeld()
        game.checkGameOver()
        game.activePiece.hardDrop()
    
    def youLost(self):
        #Loss screen
        self.themeSong.pause()
        self.loserSound.play()
        rectMode(CENTER)
        fill(240)
        rect(w/2, w/2, 400, 400, 10)
        textAlign(CENTER)
        textSize(70)
        fill(200, 0, 0)
        text("You Lost!", w/2, w/2) 
        textSize(20)
        text("Click to restart", w/2, w/2 + w/30)
        
    
    def increaseLevel(self):
        #Increase level: levels are determined by 500n + 500(n-1)
        if self.score >= 500*self.level + 500*self.level:
            self.level += 1
        #Adjust game speed in a compounding manner based on level
        self.fps = int(30 / (1 + 0.30*(self.level-1)))
    def newPiece(self):
        #Pop the next piece in the array 
        self.currentPieceValue = self.nextPieces.pop(0)
        if self.currentPieceValue == 0:
            self.activePiece = OPiece(4, 1)
        elif self.currentPieceValue == 1:
            self.activePiece = IPiece(4, 1)
        elif self.currentPieceValue == 2:
            self.activePiece = LPiece(4, 1)
        elif self.currentPieceValue == 3:
            self.activePiece = JPiece(4, 1)
        elif self.currentPieceValue == 4:
            self.activePiece = ZPiece(4, 1)
        elif self.currentPieceValue == 5:
            self.activePiece = SPiece(4, 1)
        elif self.currentPieceValue == 6:
            self.activePiece = TPiece(4, 1)
        while len(self.nextPieces) < 3:
            #Now add a new piece to the array, and ensure that it doesn't already exist in the array
            addedPiece = randint(0, 6)
            if not addedPiece in self.nextPieces:
                self.nextPieces.append(addedPiece)
                
    def newHeldPiece(self, next): 
        #Create a new piece from when the player holds
        #Separate function is necessary because the default newPiece function pulls from the array of next tiles
        self.currentPieceValue = next
        if self.currentPieceValue == 0:
            self.activePiece = OPiece(4, 1)
        elif self.currentPieceValue == 1:
            self.activePiece = IPiece(4, 1)
        elif self.currentPieceValue == 2:
            self.activePiece = LPiece(4, 1)
        elif self.currentPieceValue == 3:
            self.activePiece = JPiece(4, 1)
        elif self.currentPieceValue == 4:
            self.activePiece = ZPiece(4, 1)
        elif self.currentPieceValue == 5:
            self.activePiece = SPiece(4, 1)
        elif self.currentPieceValue == 6:
            self.activePiece = TPiece(4, 1)
        while len(self.nextPieces) < 3:
            #Now add a new piece to the array, and ensure that it doesn't already exist in the array
            addedPiece = randint(0, 6)
            if not addedPiece in self.nextPieces:
                self.nextPieces.append(addedPiece)
    def deleteRows(self):
        #Check if rows are full, and delete them
        rowsDeleted = 0
        #Start from the bottom of the board
        for i in range(19, -1, -1):
            #Don't move up a line unless the line isn't full
            keepChecking = True
            while keepChecking:
                rowCount = 0
                for j in range(10): 
                    if self.board.board[j][i] != 0 and self.board.board[j][i].r != 100:
                        #Only count it as a full row if it's not grey
                        rowCount += 1
                #If the row is full, delete this row and shift the whole board down
                if rowCount == 10:
                    rowsDeleted += 1
                    for m in range(i, 0, -1):
                        for n in range(10):
                            self.board.board[n][m] = self.board.board[n][m-1]
                    #Row clear sound
                    self.rowSound.rewind()
                    self.rowSound.play()
                else:
                    keepChecking = False
                    
        #Award points based on combos
        if rowsDeleted == 4:
            self.score += 800*self.level
        elif rowsDeleted == 3:
            self.score += 500*self.level
        elif rowsDeleted == 2:
            self.score += 300*self.level
        elif rowsDeleted == 1:
            self.score += 100*self.level
        
        #Bonus points for hard-drops
        if self.droppedHard:
            self.score += 50*self.level
        self.droppedHard = False

    def holdPiece(self):
        #Hold a piece
        if self.keyHandler['c'] == True:
            #You can only hold a piece if the cooldown is over AND if you haven't held a piece yet this turn
            if self.holdCooldown <= 0 and not self.justHeld:
                if not self.heldPiece == 500:
                    #If a piece has already been held previously, switch the held piece and the current piece 
                    tempVar = self.currentPieceValue
                    self.newHeldPiece(self.heldPiece)
                    self.heldPiece = tempVar
                else:
                    #If a piece has not been held previously, just hold this one and pull the next piece from the array of next pieces
                    self.heldPiece = self.currentPieceValue
                    self.newPiece()
                self.holdCooldown = 60
                self.justHeld = True
            elif self.holdCooldown < 30:
                #Fixed the loop so the sound plays properly
                self.noHold.rewind()
                self.noHold.play()
        #Reduce move cooldown by 1 every frame
        self.holdCooldown -= 1
                
    def printHeld(self):
        #Print the piece currently held
        pieceToPrint = 0
        if self.heldPiece == 0:
            pieceToPrint = OPiece(4, 1)
        elif self.heldPiece == 1:
            pieceToPrint = IPiece(4, 1)
        elif self.heldPiece == 2:
            pieceToPrint = LPiece(4, 1)
        elif self.heldPiece == 3:
            pieceToPrint = JPiece(4, 1)
        elif self.heldPiece == 4:
            pieceToPrint = ZPiece(4, 1)
        elif self.heldPiece == 5:
            pieceToPrint = SPiece(4, 1)
        elif self.heldPiece == 6:
            pieceToPrint = TPiece(4, 1)
            
        if self.heldPiece != 500:
            tempStep = step*0.69
            for j in pieceToPrint.blocks:
                fill(j.r, j.g, j.b)
                rect(j.x * tempStep + w/60, (j.y + 4)* tempStep + tempStep*2, tempStep, tempStep)
                
class Board():
    #Board class that conceptualizes the screen as a grid where pieces are stored
    def __init__(self, numRows, numCols, w):
        self.board = []
        self.numRows = numRows
        self.numCols = numCols
        #step is the width of each block, made global so it can be used anywhere
        global step 
        step = w/20 - w/200
        #Create a 2d list to represent the board
        for x in range(numRows):
            self.board.append([])
            for y in range(numCols):
                #Empty spaces contain a 0, which can be used for different kinds of checks later on.
                #When a space is occupied, it will contain the block object itself.
                self.board[x].append(0)
    def printBoard(self):
        for x in range(self.numRows):
            for y in range(self.numCols):
                #If the cell contains a block, print that block
                if self.board[x][y] != 0:
                    fill(self.board[x][y].r, self.board[x][y].g, self.board[x][y].b)
                    stroke(0);
                    #Making sure the board is centered
                    rect(x * step + (w/4 + w/40),  y * step + step*1.5, step, step)
                else:
                    fill(0)
                    stroke(50)
                    #If the cell is empty, just fill out the grid in the background
                    rect(x * step + (w/4 + w/40),  y * step + step*1.5, step, step)
                    
    def updateBoard(self):
        #Store the blocks of the active piece into the board
        game.justHeld = False
        for j in range(4):
            self.board[game.activePiece.blocks[j].x][game.activePiece.blocks[j].y] = game.activePiece.blocks[j]

class Piece():
    def __init__(self, R, G, B, x, y):
        #Initiating a piece: every piece has color and a list of blocks
        self.r = R
        self.g = G
        self.b = B
        self.x = x
        self.y = y
        self.blocks = []
        #Coords is the list of 4 coordinates used to draw the shape
        self.coords = []
        self.moveCooldown = 0
        self.rotCooldown = 0
        
    def updatePiece(self):
        #When updating the piece, wipe the list of blocks then rewrite them using the coords
        self.blocks = []
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, self.x + i[0], self.y + i[1]))
            
    def printPiece(self):
        #Print the piece at its current position using its block array
        fill(self.r, self.g, self.b)
        stroke(0)
        for i in self.blocks:
            rect(i.x * step + (w/4 + w/40), i.y * step + step*1.5, step, step)
        
    def movePiece(self):
        #Moving the piece left or right based on key presses
        if self.moveCooldown == 0:
            if game.keyHandler[LEFT] == True:
                canMove = True
                for i in self.blocks:
                    #Ensure the block can't move offscreen by checking every block in its array
                    if i.x == 0 or game.board.board[i.x - 1][i.y] != 0:
                        canMove = False
                if canMove:
                    self.x -= 1
                    self.moveCooldown = 5
            elif game.keyHandler[RIGHT] == True:
                canMove = True
                for i in self.blocks:
                    #Ensure the block can't move offscreen by checking every block in its array
                    if i.x == 9 or game.board.board[i.x + 1][i.y] != 0:
                        canMove = False
                if canMove:
                    self.x += 1
                    self.moveCooldown = 5
        else:
            self.moveCooldown -= 1
                
    def fastDrop(self):
        #Speeding up the block's descent based on input
        if game.keyHandler[DOWN] == True:
            game.fps = int(game.fps/5)


class OPiece(Piece):
    def __init__(self, x, y):
        #Specific piece types have xy-coordinates, as well as
        #instructions for how to build the shape stored in self.coord.
        Piece.__init__(self, 247, 171, 30, x, y)
        #Centerpiece: top left corner
        self.coords = [[0, 0], [0, -1], [1, 0], [1, -1]] 
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))
    
    def rot(self, dir):
        self.r = self.r

        
class IPiece(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, 3, 61, 212, x, y)
        #Centerpiece: second block
        self.rotations = [[[-2, 0], [-1, 0], [0, 0], [1, 0]], [[0, -1], [0, 0], [0, 1], [0, 2]], [[-2, 1], [-1, 1], [0, 1], [1, 1]], [[-1, -1], [-1, 0], [-1, 1], [-1, 2]]]
        self.coords = [[-2, 0], [-1, 0], [0, 0], [1, 0]] 
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))
        #State indicates which rotation to use
        self.state = 0
    
    def rot(self, dir):
        #Specialized rotation for I because it's the only different one
        tempState = self.state
        if dir == 'L':
            tempState += 1
        elif dir == 'R':
            tempState -= 1
        tempCoords = self.rotations[self.state%4]
        tempBlocks = []
        for i in tempCoords:
            tempBlocks.append([self.x + i[0], self.y + i[1]])
            
        canRotate = True
        for i in tempBlocks:
            if i[0] < 0 or i[0] > 9 or i[1] > 19:
                canRotate = False
                
        if canRotate:
            for i in tempBlocks:
                if game.board.board[i[0]][i[1]] != 0:
                    canRotate = False
                    
        if canRotate:
            self.state = tempState
            for i in range(len(self.coords)):
                self.coords[i] = tempCoords[i]
        
        
class LPiece(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, 245, 0, 18, x, y)
        #Centerpiece: middle of the L
        self.coords = [[-1, 0], [0, 0], [1, 0], [1, -1]]
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))
    
        
class JPiece(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, 248, 249, 22, x, y)
        #Centerpiece: middle of the J
        self.coords = [[-1, -1], [-1, 0], [0, 0], [1, 0]] 
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))
            
        
class ZPiece(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, 5, 167, 5, x, y)
        #Centerpiece: bottom middle piece
        self.coords = [[-1, -1], [0, -1], [0, 0], [1, 0]]
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))

        
class SPiece(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, 254, 96, 34, x, y)
        #Centerpiece: bottom middle piece
        self.coords = [[-1, 0], [0, 0], [0, -1], [1, -1]]
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))

        
class TPiece(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, 255, 0, 186, x, y)
        #Centerpiece: bottom middle piece
        self.coords = [[-1, 0], [0, 0], [1, 0], [0, -1]] 
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))
            
class Block():
    def __init__(self, R, G, B, x, y):
        #A block is an individual part of a piece
        self.r = R
        self.g = G
        self.b = B
        self.x = x
        self.y = y
        
def newGame():
    #Function to start a new game.
    numRows = 10
    numCols = 20
    global w
    w = 800
    global game
    game = Game(numRows, numCols, w)


newGame()

menu = Menu()

def setup():
    size(w, w)
    rectMode(CENTER)

def draw():
    if not game.gameOver and game.start:
        game.playGame()
    elif not game.gameOver:
        menu.printMenu()
    else:
        game.youLost()
    
    
def keyPressed():
    if keyCode == UP:
        game.keyHandler[UP] = True
    if keyCode == LEFT:
        game.keyHandler[LEFT] = True
    if keyCode == RIGHT:
        game.keyHandler[RIGHT] = True
    if keyCode == DOWN:
        game.keyHandler[DOWN] = True
    if keyCode == ESC:
        game.keyHandler[ESC] = True
    if key == 'z':
        game.keyHandler['z'] = True
    if key == 'c':
        game.keyHandler['c'] = True
    if key == ' ':
        game.keyHandler[' '] = True
        
def keyReleased():
    if keyCode == UP:
        game.keyHandler[UP] = False
    if keyCode == LEFT:
        game.keyHandler[LEFT] = False
    if keyCode == RIGHT:
        game.keyHandler[RIGHT] = False
    if keyCode == DOWN:
        game.keyHandler[DOWN] = False
    if key == 'z':
        game.keyHandler['z'] = False
    if key == 'c':
        game.keyHandler['c'] = False
    if key == ' ':
        game.keyHandler[' '] = False
        
def mousePressed():
    #Click function for restarting the game
    if game.gameOver and mouseX > w/2 - 200 and mouseX < w/2 + 200 and mouseY > w/2 - 200 and mouseY < w/2 + 200:
        game.themeSong.pause()
        game.loserSound.pause()
        newGame()
    #Click function for the initial menu
    elif not game.gameOver and not game.start:
        if mouseX > w/2 - 200 and mouseX < w/2 + 200 and mouseY > w/5*2.5 - 100 and mouseY < w/5*2.5 + 100:
            game.start = True
        elif mouseX > w/2 - 200 and mouseX < w/2 + 200 and mouseY > w/5*3.5 - 100 and mouseY < w/5*3.5 + 100:
            game.start = True
            game.arcade = True
            

