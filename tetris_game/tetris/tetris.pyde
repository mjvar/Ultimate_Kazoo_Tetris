class Game():
    #Game class that contains a board, and will contain more functionality in the future
    def __init__(self, numRows, numCols):
        self.rows = numRows
        self.cols = numCols
        self.board = Board(self.rows, self.cols)
        
                
class Board():
    #Board class that conceptualizes the screen as a grid where pieces are stored
    def __init__(self, numRows, numCols):
        self.board = []
        #Create a 2d list to represent the board
        for x in range(numRows):
            self.board.append([])
            for y in range(numCols):
                #Empty spaces contain a 0, which can be used for different kinds of checks later on.
                #When a space is occupied, it will contain the block object itself.
                self.board[x].append(0)
        
class Piece():
    def __init__(self):
        #Initiating a piece: every piece has color and a list of blocks
        self.r = R
        self.g = G
        self.b = B
        self.blocks = []
        
class OPiece():
    def __init__(self, R, G, B, x, y):
        #Specific piece types have xy-coordinates, as well as
        #instructions for how to build the shape stored in self.coord.
        Piece.__init__(self, R, G, B)
        self.x = x
        self.y = y
        self.coords = [[0, 0], [0, 1], [1, 0], [1, 1]] 
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))
        
class IPiece():
    def __init__(self, R, G, B, x, y):
        Piece.__init__(self, R, G, B)
        self.x = x
        self.y = y
        self.coords = [[0, 0], [0, -1], [0, -2], [0, -3]] 
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))

        
class LPiece():
    def __init__(self, R, G, B, x, y):
        Piece.__init__(self, R, G, B)
        self.x = x
        self.y = y
        self.coords = [[0, 0], [0, -1], [0, -2], [1, -2]] 
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))

        
class JPiece():
    def __init__(self, R, G, B, x, y):
        Piece.__init__(self, R, G, B)
        self.x = x
        self.y = y
        self.coords = [[0, 0], [0, -1], [0, -2], [-1, -2]] 
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))
        
class ZPiece():
    def __init__(self, R, G, B, x, y):
        Piece.__init__(self, R, G, B)
        self.x = x
        self.y = y
        self.coords = [[0, 0], [-1, 0], [1, 1], [0, 1]] 
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))

        
class SPiece():
    def __init__(self, R, G, B, x, y):
        Piece.__init__(self, R, G, B)
        self.x = x
        self.y = y
        self.coords = [[0, 0], [1, 0], [0, 1], [-1, 1]] 
        for i in self.coords:
            self.blocks.append(Block(self.r, self.g, self.b, x + i[0], y + i[1]))

        
class TPiece():
    def __init__(self, R, G, B, x, y):
        Piece.__init__(self, R, G, B)
        self.x = x
        self.y = y
        self.coords = [[0, 0], [-1, 0], [1, 0], [0, -1]] 
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
    #Function to start a new game. May be useful for restarting when the game is over
    numRows = 10
    numCols = 20
    game = Game(numRows, numCols)

newGame()

def setup():
    size(800, 800)

def draw():
    background(255)
    
