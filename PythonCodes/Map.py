import random

class Map:

    def move(self,location,moveWay):
        if moveWay == 0: self.mapInfo[location[0]+1][location[1]] = self.beforeValue
        elif moveWay == 1: self.mapInfo[location[0]][location[1]+1] = self.beforeValue
        elif moveWay == 2: self.mapInfo[location[0]-1][location[1]] = self.beforeValue
        elif moveWay == 3: self.mapInfo[location[0]][location[1]-1] = self.beforeValue

        self.beforeValue = self.mapInfo[location[0]][location[1]]
        self.mapInfo[location[0]][location[1]] = "@"

    def visit(self,location):
        self.mapInfo = [[random.randint(1,9) for j in range(26)] for i in range(26)]
        self.beforeValue = self.mapInfo[location[0]][location[1]]
        self.mapInfo[location[0]][location[1]] = "@"
            
    def printMap(self):
        for row in self.mapInfo:
            for item in row:
                print(item,end=" ")
            print()