import PythonCodes.Chunk.Map as Map
import copy

class Chunk:

    # 생성
    def __init__(self,chunkLocation,mapLocation,size,mapSize,loadData = None):
        if loadData:
            self.chunk = loadData
            self.loadMap()
        else:
            self.chunk = [[0 for j in range(size+1)] for i in range(size+1)]
            self.locMove(chunkLocation,mapLocation,mapSize)

    def loadMap(self):
        for y,row in enumerate(self.chunk):
            for x,mapInfo in enumerate(row):
                if not mapInfo: continue
                mapObject = Map.Map()
                mapObject.loadData(mapInfo)
                self.chunk[y][x] = mapObject

    def getLocation(self,chunkLocation,mapLocation):
        self.chunkLocation = chunkLocation
        self.mapLocation = mapLocation

    def toDic(self):
        chunk = copy.deepcopy(self.chunk)
        size = len(chunk)
        for y in range(size):
            for x in range(size):
                if chunk[y][x]:
                    chunk[y][x] = chunk[y][x].toDic()
        value = {
            "size" : size,
            "chunk" : chunk,
            "chunkLocation" : self.chunkLocation,
            "mapLocation" : self.mapLocation
        }
        return value

    # 출력 ( 터미널 )
    def printChunk(self):
        for row in self.chunk:
            for item in row:
                print(1 if item else 0,end=" ")
            print()
    
    # 출력 맵 ( 터미널 )
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