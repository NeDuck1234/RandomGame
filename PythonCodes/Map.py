import random

class Map:
    def __init__(self):
        self.visited = False
        self.mapInfo = [[random.randint(1,9) for j in range(25)] for i in range(25)]
    
    def visit(self):
        self.visited = True
            
    def printMap(self):
        for row in self.mapInfo:
            for item in row:
                print(item,end=" ")
            print()