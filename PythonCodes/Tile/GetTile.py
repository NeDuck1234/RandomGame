import PythonCodes.Tile.Tree as Tree

class GetTile:
    def __init__(self):
        self.tiles = {
            "|":Tree.Tree()
        }
    
    def getTile(self,string):
        return self.tiles[string]

    def getTree(self):
        return Tree.Tree()