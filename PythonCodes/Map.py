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
    
    def getTile(self,location):
        return self.mapInfo[location[0]][location[1]]

    # generateMap
    def visit(self,location,size,biom):
        self.mapInfo = [["_" for j in range(size+1)] for i in range(size+1)]  # _

        self.beforeValue = self.mapInfo[location[0]][location[1]]
                
        if biom == 1: self.setPlainEvents(size)

        self.mapInfo[location[0]][location[1]] = "@"

    def returnPercentage(self,value,percent):
        return value*percent//100

    def setPlainEvents(self,size):
        mapSize = size**2

        count = self.returnPercentage(mapSize,90)
        while count > 0:
            x = random.randint(0,size)
            y = random.randint(0,size)
            self.mapInfo[y][x] = ","
            count-=1
        count = self.returnPercentage(mapSize,50)
        while count > 0:
            x = random.randint(0,size)
            y = random.randint(0,size)
            self.mapInfo[y][x] = ";"
            count-=1
        count = self.returnPercentage(mapSize,5)
        while count > 0:
            x = random.randint(1,size-1)
            y = random.randint(1,size-1)
            if self.mapInfo[y][x] in ["|","^","@"] or self.mapInfo[y-1][x] in ["|","^","@"]:continue
            self.mapInfo[y][x] = "|"
            self.mapInfo[y-1][x] = "^"
            count -= 1
    
    # printMap
    def printMap(self):
        for row in self.mapInfo:
            for item in row:
                print(item,end=" ")
            print()