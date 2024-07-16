import PythonCodes.Map as Map

class Chunk:
    # generateWorld
    def __init__(self,chunkLocation,mapLocation,size,mapSize):
        self.chunk = [[0 for j in range(size+1)] for i in range(size+1)]
        self.locMove(chunkLocation,mapLocation,mapSize)

    # printChunks
    def printChunk(self):
        for row in self.chunk:
            for item in row:
                print(1 if item else 0,end=" ")
            print()
    
    # printMap
    def locPrint(self,location):
        self.chunk[location[0]][location[1]].printMap()
    
    # getMapByLocation
    def getMap(self,location):
        return self.chunk[location[0]][location[1]]
    
    # moveInWorld
    def locMove(self,chunkLocation,mapLocation,size):
        mapInfo = self.chunk[chunkLocation[0]][chunkLocation[1]]
        if mapInfo:
            mapInfo.clearCreature()
            mapInfo.creatureMove(mapLocation)
        else:
            self.chunk[chunkLocation[0]][chunkLocation[1]] = Map.Map()
            self.chunk[chunkLocation[0]][chunkLocation[1]].visit(mapLocation,1) # 바이옴은 아직 구현중