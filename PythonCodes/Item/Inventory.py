from PythonCodes.Item import Wood

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
        if loadData:
            self.loadInventory(loadData)

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
        return objectInfo

    def setItem(self,item):
        self.inventory.append(item)
    
    def getInventory(self):
        return self.inventory

    def getItem(self,itemStr):
        for item in self.inventory:
            if item.tileStr == itemStr:
                return item

    def itemExist(self,item):
        items = [itemInfo.tileStr for itemInfo in self.inventory]
        return item in items