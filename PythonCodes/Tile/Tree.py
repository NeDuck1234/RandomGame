import random
class Tree:

    def loadData(self,tileStr,HP):
        self.tileStr = tileStr
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
    
    def cutting(self):
        self.HP -= 1
        if not self.HP:
            return True