import PythonCodes.Map as Map

class Chunk:
    def __init__(self,location):
        self.chunk = [[Map.Map() for j in range(51)] for i in range(51)]
        self.chunk[location[0]][location[1]].visit()

    def printChunk(self):
        for row in self.chunk:
            for item in row:
                print(1 if item.visited else 0,end=" ")
            print()
    
    def locPrint(self,location):
        self.chunk[location[0]][location[1]].printMap()