import PythonCodes.Chunk as Chunk
import keyboard

class Main:

    def __init__(self):
        keyboard.hook(self.readKey)
        self.location = [25,25]
        self.chunk = Chunk.Chunk(self.location)
        self.userEvent = None
        self.main()

    def wait(self,event):
        return False if event else True

    def readKey(self,event):
        self.userEvent = event

    def main(self):
        while True:
            self.chunk.printChunk()
            print("_"*100)
            self.chunk.locPrint(self.location)
            while self.wait(self.userEvent): pass
            self.userEvent = None


if __name__ == "__main__":
    Main()