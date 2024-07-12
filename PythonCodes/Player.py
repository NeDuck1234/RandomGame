class Player:
    
    def move(self,event):
        value = [0,0]
        if event == 13: value = [0,-1,0] 
        elif event == 0: value = [1,-1,1]
        elif event == 1: value = [0,1,2]
        elif event == 2: value = [1,1,3]
        return value
    
    def endGame(self,listener):
        listener.stop()
