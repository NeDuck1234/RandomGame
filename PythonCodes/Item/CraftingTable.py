class CraftingTable:

    def toDic(self):
        return {
            "tileStr" : "#"
        }

    def __init__(self):
        self.count = "single"
        self.tileStr = "#"

    def __str__(self):
        return self.tileStr
    
    def getCount(self):
        return "single"