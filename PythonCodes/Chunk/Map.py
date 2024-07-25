import random
import json

from PythonCodes.Tile.GetTile import GetTile
from PythonCodes.Item.GetItem import GetItem

import copy

class Map:

    def __init__(self):
        self.GetTile = GetTile()
        self.GetItem = GetItem()

    def loadData(self,mapInfo):
        self.size = mapInfo["size"]
        self.mapInfo = mapInfo["mapInfo"]
        self.creatureInfo = mapInfo["creature"]
        self.itemInfo = mapInfo["itemInfo"]
        self.biom = mapInfo["biom"]
        self.loadTile()

    def loadTile(self):
        for y,row in enumerate(self.mapInfo):
            for x,tileInfo in enumerate(row):
                if type(tileInfo) == str: continue
                tileObject = self.checkTile(tileInfo)
                self.mapInfo[y][x] = tileObject

        for y,row in enumerate(self.itemInfo):
            for x,itemInfo in enumerate(row):
                if type(itemInfo) == str: continue
                tileObject = self.checkItem(itemInfo)
                self.itemInfo[y][x] = tileObject


    def checkTile(self,tileInfo):
        objectInfo = None
        match tileInfo["tileStr"]:
            case "|":
                objectInfo = self.GetTile.getTree()
                objectInfo.loadData(tileInfo["HP"])
        return objectInfo

    def checkItem(self,itemInfo):
        objectInfo = None
        match itemInfo["tileStr"]:
            case "|":
                objectInfo = self.GetItem.getWood()
                objectInfo.loadData(itemInfo["count"])
        return objectInfo

    def toDic(self):
        mapInfo = copy.deepcopy(self.mapInfo)
        for y in range(self.size):
            for x in range(self.size):
                if type(mapInfo[y][x]) != str:
                    mapInfo[y][x] = mapInfo[y][x].toDic()

        itemInfo = copy.deepcopy(self.itemInfo)
        for y in range(self.size):
            for x in range(self.size):
                if type(itemInfo[y][x]) != str:
                    itemInfo[y][x] = itemInfo[y][x].toDic()

        value = {
            "size" : self.size,
            "mapInfo" : mapInfo,
            "creature" : self.creatureInfo[:],
            "itemInfo" : itemInfo,
            "biom" : self.biom
        }
        return value
    
    def arroundFromLocation(self,loc):
        tile,creature,item = [[],[],[]],[[],[],[]],[[],[],[]]
        width = [loc[1]-1,loc[1],loc[1]+1]
        height = [loc[0]-1,loc[0],loc[0]+1]
        for idxY,y in enumerate(height):
            for x in width:
                if x in range(0,self.size+1) or y in range(0,self.size+1):
                    tile[idxY].append(self.mapInfo[y][x])
                    creature[idxY].append(self.creatureInfo[y][x])
                    item[idxY].append(self.itemInfo[y][x])
                else:
                    tile[idxY].append(None)
                    creature[idxY].append(None)
                    item[idxY].append(None)
        return (tile,creature,item)

                
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
        self.mapInfo = [["_" for j in range(self.size+1)] for i in range(self.size+1)]
        self.creatureInfo = [["_" for j in range(self.size+1)] for i in range(self.size+1)]
        self.itemInfo = [["_" for j in range(self.size+1)] for i in range(self.size+1)]
        
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
            self.mapInfo[y][x] = self.GetTile.getTree()
            self.mapInfo[y-1][x] = "^"
            count -= 1

    def setTile(self,tileLocs):
        if self.biom == 1:
            for loc in tileLocs:
                self.mapInfo[loc[0]][loc[1]] = random.choice(["_",",",";"])

    def setItem(self,itemLoc,itemInfo):
        self.itemInfo[itemLoc[0]][itemLoc[1]] = itemInfo
    
    # printMap
    def printMap(self):
        for row in self.mapInfo:
            for item in row:
                print(item,end=" ")
            print()