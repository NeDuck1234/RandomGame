from PythonCodes.Item import Wood
from PythonCodes.Item import CraftingTable

import copy

class Inventory:
    def toDic(self):
        inventory = copy.deepcopy(self.inventory)
        for idx,item in enumerate(inventory):
            inventory[idx] = item.toDic()
        value = {
            "inventory" : inventory
        }
        return value

    def __init__(self,loadData=None):
        self.inventory = []
        self.choose = 0
        if loadData:
            self.loadInventory(loadData)
    
    def setChoose(self,choose):
        self.choose = choose

    def getChoose(self):
        return self.choose

    def loadInventory(self,loadData):
        for idx,item in enumerate(loadData["inventory"]):
            itemObject = self.checkItem(item)
            self.inventory.append(itemObject)

    def checkItem(self,itemInfo):
        objectInfo = None
        match itemInfo["tileStr"]:
            case "|":
                objectInfo = Wood.Wood()
                objectInfo.loadData(itemInfo["count"])
            case "#":
                objectInfo = CraftingTable.CraftingTable()
        return objectInfo

    def setItem(self,item):
        self.inventory.append(item)
    
    def removeItem(self,idx):
        self.inventory.pop(idx)
    
    def getInventory(self):
        return self.inventory

    def getItem(self,itemStr):
        for item in self.inventory:
            if item.tileStr == itemStr:
                return item

    def itemExist(self,item):
        items = [itemInfo.tileStr for itemInfo in self.inventory]
        return item in items