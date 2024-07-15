import json

class Player:
    def __init__(self):
        # keyCode
        file = open('./Resource/data/keycodes.json')
        self.keyCodes = json.load(file)
        file.close()

    # moveInMapEvent
    def move(self,event):
        value = None
        if event == self.keyCodes["w"]: value = [0,-1,0] 
        elif event ==  self.keyCodes["a"]: value = [1,-1,1]
        elif event ==  self.keyCodes["s"]: value = [0,1,2]
        elif event ==  self.keyCodes["d"]: value = [1,1,3]
        return value
    
    # moveInWorldEvent
    def moveChunk(self,event):
        value = None
        # w 0 a 1 s 2 d 3

        if event[2] == 0: value = [0,-1]
        elif event[2] == 1: value = [1,-1]
        elif event[2] == 2: value = [0,1]
        elif event[2] == 3: value = [1,1]
        return value
    
    # endGame
    def endGame(self,listeners):
        for listener in listeners:
            try:
                listener.stop()
            except:
                print("error in {listener}")
