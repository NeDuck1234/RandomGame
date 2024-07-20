class Wood:
    def __init__(self):
        self.count = 0
        self.tileStr = "|"

    def toDic(self):
        value = {
            "tileStr" : self.tileStr,
            "count" : self.count
        }
        return value
    
    def loadData(self,count):
        self.count = count
    
    def setCount(self,count):
        self.count = count

    def getCount(self):
        return self.count

    def __str__(self):
        return self.tileStr
    