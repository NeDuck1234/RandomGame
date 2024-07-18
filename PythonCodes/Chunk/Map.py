import random
import json
from PythonCodes.Tile import Tree

import copy

class Map:

    def loadData(self,size,mapInfo,creatureInfo,biom):
        self.size = size
        self.mapInfo = mapInfo
        self.creatureInfo = creatureInfo
        self.biom = biom

    def toDic(self):
        mapInfo = copy.deepcopy(self.mapInfo)
        for y in range(self.size):
            for x in range(self.size):
                if type(mapInfo[y][x]) != str:
                    mapInfo[y][x] = mapInfo[y][x].toDic()
        value = {
            "size" : self.size,
            "mapInfo" : mapInfo,
            "creature" : self.creatureInfo[:],
            "biom" : self.biom
        }
        return value

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
        
        self.biom = biom

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
            if self.mapInfo[y][x] in ["|","^","@"] or self.mapInfo[y-1][x] in ["^","@"]:continue
            self.mapInfo[y][x] = Tree.Tree()
            self.mapInfo[y-1][x] = "^"
            count -= 1

    def setTile(self,tileLocs):
        if self.biom == 1:
            for loc in tileLocs:
                self.mapInfo[loc[0]][loc[1]] = random.choice(["_",",",";"])
    
    # printMap
    def printMap(self):
        for row in self.mapInfo:
            for item in row:
                print(item,end=" ")
            print()