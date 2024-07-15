import random
import json

class Map:

    # moveInMapEvent
    def move(self,location,moveWay,beforeLoc=None):
        # w 0 a 1 s 2 d 3
        if moveWay == 0: self.placeBefore([location[0]+1,location[1]])
        elif moveWay == 1: self.placeBefore([location[0],location[1]+1])
        elif moveWay == 2: self.placeBefore([location[0]-1,location[1]])
        elif moveWay == 3: self.placeBefore([location[0],location[1]-1])
        elif moveWay == 4: self.placeBefore([location[0],location[1]])
        else:
            self.placeBefore([beforeLoc[0],beforeLoc[1]-1])
        self.beforeValue = self.mapInfo[location[0]][location[1]]
        if moveWay != None:
            self.mapInfo[location[0]][location[1]] = "@"

    # moveInMap or World Event
    def placeBefore(self,location):
        self.mapInfo[location[0]][location[1]] = self.beforeValue

    # generateMap
    def visit(self,location,size):
        #self.mapInfo = [["_" for j in range(size+1)] for i in range(size+1)]

        self.mapInfo = [["0" for j in range(size+1)] for i in range(size+1)]  # 0
        self.beforeValue = self.mapInfo[location[0]][location[1]]
        self.mapInfo[location[0]][location[1]] = "@"
    
    # printMap
    def printMap(self):
        for row in self.mapInfo:
            for item in row:
                print(item,end=" ")
            print()