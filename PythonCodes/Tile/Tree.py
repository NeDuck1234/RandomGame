import random
from PythonCodes.Item.Wood import Wood

class Tree:

    def loadData(self,HP):
        self.HP = HP

    def toDic(self):
        value = {
            "tileStr" : self.tileStr,
            "HP" : self.HP
        }
        return value

    def __str__(self):
        return self.tileStr
    
    def __init__(self):
        self.HP = 10
        self.tileStr = "|"

    def cuttingAction(self,tileLoc,mapInfo):
        if self.cutting():
            treeLoc = tileLoc[:]
            count = 1
            while mapInfo.mapInfo[treeLoc[0]-count][treeLoc[1]] == "^":
                count += 1
            treeLoc = [treeLoc]
            treeLoc.extend([[tileLoc[0]-count,tileLoc[1]] for count in range(count) ])
            mapInfo.setTile(treeLoc)
            wood = Wood()
            wood.setCount(5+(count-2)*3)
            mapInfo.setItem(tileLoc,wood)
    
    def cutting(self):
        self.HP -= 1
        if not self.HP:
            return True