import PythonCodes.Item.Wood as Wood
import PythonCodes.Item.CraftingTable as CraftingTable

class GetItem:
    def __init__(self):
        self.items = {
            "|":Wood.Wood(),
            "#":CraftingTable.CraftingTable()
        }
    
    def getItem(self,string):
        return self.items[string]
    
    def getWood(self):
        return Wood.Wood()

    def getCraftingTable(self):
        return CraftingTable.CraftingTable()