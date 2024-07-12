import PythonCodes.Map as Map

class Chunk:
    def __init__(self,chunkLocation,mapLocation):
        self.chunk = [[0 for j in range(51)] for i in range(51)]
        self.locMove(chunkLocation,mapLocation)


    def printChunk(self):
        for row in self.chunk:
            for item in row:
                print(1 if item else 0,end=" ")
            print()
    
    def locPrint(self,location):
        self.chunk[location[0]][location[1]].printMap()
    
    def getMap(self,location):
        return self.chunk[location[0]][location[1]]
    
    def locMove(self,chunkLocation,mapLocation):
        self.chunk[chunkLocation[0]][chunkLocation[1]] = Map.Map()
        self.chunk[chunkLocation[0]][chunkLocation[1]].visit(mapLocation)