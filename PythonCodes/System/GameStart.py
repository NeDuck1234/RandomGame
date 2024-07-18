import PythonCodes.Scene.GenerateScreen as GenerateScreen
import PythonCodes.Scene.TitleScene as TitleScene

class GameStart:
    def __init__(self):
        generateScreen = GenerateScreen.GenerateScreen()
        screen = generateScreen.getScreen()
        images = generateScreen.getImages()
        infos = generateScreen.getInfos()
        titleScene = TitleScene.TitleScene(screen,images,infos)