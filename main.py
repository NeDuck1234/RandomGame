import PythonCodes.Chunk as Chunk
import PythonCodes.Player as Player
from pynput import keyboard
import os
import sys

class Main:
    def __init__(self):
        self.player = Player.Player()
        self.setting()

        self.chunkLocation = [25, 25]
        self.mapLocation = [13,13]
        self.chunk = Chunk.Chunk(self.chunkLocation,self.mapLocation)
        self.chunk.locPrint(self.chunkLocation)
        self.userEvent = None

        self.listener = keyboard.Listener(on_press=self.readKey)
        self.threadingKeyinput()
    
    def setting(self):
        self.moveAction = [0,1,2,13]
        self.endAction = 53

    def exitHandler(self):
        self.keyInputThread.join()

    def threadingKeyinput(self):
        with self.listener as listener:
            listener.join()

    def readKey(self, key):
        try:
            if hasattr(key, 'vk'):
                self.userEvent = key.vk
            else:
                self.userEvent = key.value.vk
        except AttributeError:
            self.userEvent = None
        
        if self.userEvent != None: self.actionSelect()

    def actionSelect(self):
        if self.userEvent in self.moveAction: self.action("move")
        elif self.userEvent == self.endAction: self.action("end")

    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def action(self,event):
        self.clearScreen()

        if event == "move":
            moveLoc = self.player.move(self.userEvent)
            self.mapLocation[moveLoc[0]] += moveLoc[1]
            inMap = self.chunk.getMap(self.chunkLocation)
            inMap.move(self.mapLocation,moveLoc[2])
        if event == "end":
            self.player.endGame(self.listener)

        self.chunk.locPrint(self.chunkLocation)

        self.userEvent = None


if __name__ == "__main__":
    Main()
