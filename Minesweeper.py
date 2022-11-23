"""
Command-line MineSweeper project 

Author: Aidan Boase
"""
import os
import random

class Board:
    def __init__(self, size, numBombs):
        self.size = size
        self.numBombs = numBombs
        self.flags = []
        self.gameBoard = []

        # Get mines
        self.mineCoords = self.setMineCoords()

        # Create solution board with mines inserted
        self.solutionBoard = self.generateBoard()

        # Determines number of bombs around each tile
        self.assignNumbers()

        # Keeps track of dug spots
        self.dug = set()

    def addFlag(self, row, col):
        return self.flags.append([[row, col]])

    def removeFlag(self, row, col):
        return self.flags.remove([row, col])
        
    def getFlags(self):
        return self.flags

    def generateBoard(self):
        # Create dummy board
        board = [["X" for x in range(self.size)] for y in range(self.size)]

        # Insert mines to board
        for i in range(len(self.mineCoords)):
            xcoord = self.mineCoords[i][0]
            ycoord = self.mineCoords[i][1]
            board[ycoord][xcoord] = "*"

        return board

    def setMineCoords(self):
        # Generate mines as list of numbers
        mineList = [random.randint(0, (self.size*10)-1) for x in range(self.size)]
        
        # Transfer mine list into list of coordinates as tuples
        mineCoords = []
        for i in range(len(mineList)):
            if mineList[i] < 10:
                mineCoords.append((mineList[i], 0))
            else:
                mineCoords.append((int(str(mineList[i])[:1]),int(str(mineList[i])[1:])))
        
        return mineCoords

    def assignNumbers(self):
        # Determines number of bombs around each tile
        for x in range(self.size):
            for y in range(self.size):
                if self.solutionBoard[x][y] == "*":
                    continue # Don't want to replace bomb, no need to calculate anything
                self.solutionBoard[x][y] = self.getNeighbouringBombs(x, y)
        return self.solutionBoard

    def getNeighbouringBombs(self, row, col):
        numNeighbouringBombs = 0
        for x in range(max(0, row-1), min(self.size-1, row+1)+1):
            for y in range(max(0, col-1), min(self.size-1, col+1)+1):
                if x == row and y == col:
                    # original location, don't check
                    continue
                if self.solutionBoard[x][y] == "*":
                    numNeighbouringBombs += 1
        return numNeighbouringBombs

    def digdug(self, row, col):
        self.dug.add((row, col))

        if self.solutionBoard[row][col] == "*":
            # Bomb Found!
            return False
        elif self.solutionBoard[row][col] > 0:
            return True

        for x in range(max(0, row-1), min(self.size-1, row+1)+1):
            for y in range(max(0, col-1), min(self.size-1, col+1)+1):
                if (x, y) in self.dug:
                    continue # Don't dig already dug spots
                self.digdug(x,y) # Recursion!

        # Successfully dug 
        return True

    def __repr__(self):
        self.gameBoard = [[None for x in range(self.size)] for y in range(self.size)]
        for x in range(self.size):
            for y in range(self.size):
                if (x, y) in self.dug:
                    self.gameBoard[x][y] = str(self.solutionBoard[x][y])
                elif ([[x, y]]) in self.flags:
                    self.gameBoard[x][y] = "F"
                else:
                    self.gameBoard[x][y] = "X"

        sp = "   "
        for i in range(self.size):
            sp = sp + "     " + str(i)
        print(sp)

        for r in range(self.size):
            sp = "     "
            
            # Print horizontal lines only on top and bottom, 
            # not inbetween rows
            if r == 0:
                for c in range(self.size):
                    sp = sp + "------"
                print(sp)

            # With horizontal lines between each row
            #for c in range(self.size):
            #    sp = sp + "------"
            #print(sp)
            
            # Print first row of vertical lines
            sp = "     "
            for c in range(self.size):
                sp = sp + "|     "
            print(sp + "|")

            # Print second row of vertical lines and board value
            sp = "  " + str(r) + "  "
            for c in range(self.size):
                sp = sp + "|  " + str(self.gameBoard[r][c]) + "  "   
            print(sp + "|")	

        # Print final row of underscores columns    
        sp = "     "
        for c in range(self.size):
            sp = sp + "|_____"
        
        return sp + '|'

def play(size = 10, numBombs = 10):
    # 1: Create Board and plant bombs
    # 2: Show the user the board and ask where they want to dig
    # 3a: If location is a bomb, show game over message
    # 3b: If location is not a bomb, repeat step 2
    # 4: If no more possible dig spots other than mines, VICTORY 

    # Clear the screen to begin - will fail on linux
    # os.system('cls')

    # Welcome!
    print("\t\tWelcome to MineSweeper! Bonne chance!\n")

    # Create game board with mines inserted
    board = Board(size, numBombs)
    
    print("\nPlease enter coordinates separated by a space. Ex: 1 2") 
    print("Add an F if you'd like to flag that location. Ex: 1 2 F\n")

    # Flag variable for continuing game execution
    safe = True
    
    # Game Loop
    while len(board.dug) < ((board.size ** 2) - numBombs):
        print("\n")
        print(board)
        userGuess = input("\nWhere would you like to dig? ").split() #Ex: 5 4 F

        if len(userGuess) == 3 or len(userGuess) == 2:
            # Ensures we have numeric coordinates
            try:
                coords = list(map(int, userGuess[:2]))
            except ValueError:
                print("Invalid Input! Please try again.\n")
                continue
            
            # Check numeric values added within range of board size
            if coords[0] > size or coords[0] < 0 or coords[1] > size or coords[1] < 0:
                print("Invalid Input! Please enter a value within the game board.\n")
                continue

            # Extract coordinates
            x = coords[0]
            y = coords[1]

            if len(userGuess) == 3:
                if userGuess[2] != "F" and userGuess[2] != "f":
                    print("Invalid Input! if you'd like to Flag, simply add an F or f after your coordinates.\n")
                    continue

                # Flag already been set
                if coords in board.flags:
                    print("Flag already set.\n") #Removing.\n")
                    board.removeFlag(y, x)
                    continue

                # Trying to flag somewhere with an already assigned number
                if board.gameBoard[y][x] != "X":
                    if len(board.dug) == 0:
                        print("You must select an empty space before you can flag a tile.\n")
                        continue
                    print("You already know the value of this tile. Flag not placed.\n")
                    continue
                
                if len(board.flags) < numBombs:
                    print("Set flag to (" + str(x) + ", " + str(y) + ")\n")

                    # Add flags to list of flags and show board
                    board.addFlag(y, x)
                    continue
                else:
                    print("Flags done\n")
        else:
            print("Invalid Input! Please try again.\n")
            continue

        # Start digging
        safe = board.digdug(y, x)
        if not safe:
            # Gameover, you dug a bomb
            print("\nGAME OVER!! You've dug a bomb :(\n")
            break
        print("Successfully dug at (" + str(x) + ", " + str(y) + ")\n")
    
    if safe:
        print(board)
        print("Congrats! You beat Minesweeper!")
        

if __name__ == "__main__":
    # Lets get down to business
    play()
