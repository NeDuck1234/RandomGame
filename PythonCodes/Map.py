import random
import json

class Map:

    def clearCreature(self):
        self.creatureInfo = [["_" for j in range(self.size+1)] for i in range(self.size+1)]

    def creatureMove(self,player):
        self.creatureInfo[player[0]][player[1]] = "@"
    
    # getTile
    def getTile(self,location):
        return self.mapInfo[location[0]][location[1]]

    # generateMap
    def visit(self,location,biom):
        with open('./setting.json') as file:
            setting = json.load(file)
        self.size = setting["mapSize"]
        self.mapInfo = [["_" for j in range(self.size+1)] for i in range(self.size+1)]  # tileInfo
        self.creatureInfo = [["_" for j in range(self.size+1)] for i in range(self.size+1)]  # creatureInfo
                
        self.mapInfo[location[0]][location[1]] = "@"

        if biom == 1: self.setPlainEvents()

        self.creatureInfo[location[0]][location[1]] = "@"
        if self.mapInfo[location[0]][location[1]] == "@":
            self.mapInfo[location[0]][location[1]] = "_"

    def returnPercentage(self,value,percent):
        return value*percent//100

    def setPlainEvents(self):
        mapSize = self.size**2

        count = self.returnPercentage(mapSize,90)
        while count > 0:
            x = random.randint(0,self.size)
            y = random.randint(0,self.size)
            self.mapInfo[y][x] = ","
            count-=1
        count = self.returnPercentage(mapSize,50)
        while count > 0:
            x = random.randint(0,self.size)
            y = random.randint(0,self.size)
            self.mapInfo[y][x] = ";"
            count-=1
        count = self.returnPercentage(mapSize,5)
        while count > 0:
            x = random.randint(1,self.size-1)
            y = random.randint(1,self.size-1)
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