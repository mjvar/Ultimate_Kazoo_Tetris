class Game():
    def __init__(self, numRows, numCols):
        self.rows = numRows
        self.cols = numCols
        self.board = Board(self.rows, self.cols)
        
                
class Board():
    def __init__(self, numRows, numCols):
        self.board = []
        for x in range(numRows):
            self.board.append([])
            for y in range(numCols):
                self.board[x].append(0)
        
class Piece():
    def __init__(self):
        self.blocks = []
        
class OPiece():
    def __init__(self, R, G, B):
        self.r = R
        self.g = G
        self.b = B
        self.blocks = []
        
class IPiece():
    def __init__(self, R, G, B):
        self.r = R
        self.g = G
        self.b = B
        self.blocks = []
        
class LPiece():
    def __init__(self, R, G, B):
        self.r = R
        self.g = G
        self.b = B
        self.blocks = []
        
class JPiece():
    def __init__(self, R, G, B):
        self.r = R
        self.g = G
        self.b = B
        self.blocks = []
        
class ZPiece():
    def __init__(self, R, G, B):
        self.r = R
        self.g = G
        self.b = B
        self.blocks = []
        
class SPiece():
    def __init__(self, R, G, B):
        self.r = R
        self.g = G
        self.b = B
        self.blocks = []
        
class TPiece():
    def __init__(self, R, G, B):
        self.r = R
        self.g = G
        self.b = B
        self.blocks = []
        
class Block():
        
        
        
def newGame():
    numRows = 10
    numCols = 20
    game = Game(numRows, numCols)

newGame()

def setup():
    size(800, 800)

def draw():
    background(255)
    
