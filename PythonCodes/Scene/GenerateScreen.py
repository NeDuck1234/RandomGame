import json
import pygame

class GenerateScreen:
    def __init__(self):

        with open('./setting.json') as file:
            self.setting = json.load(file)
        with open('./Resource/data/tileInfo.json') as file:
            self.tileInfo = json.load(file)
        with open('./Resource/data/creatureInfo.json') as file:
            self.creatureInfo = json.load(file)
        with open('./Resource/data/systemInfo.json') as file:
            self.systemInfo = json.load(file)

        self.tileSize = self.systemInfo["tileSize"]
        mapSize = self.setting["mapSize"]

        # 캔버스 크기 계산
        #                   기본 화면                      + 인벤토리
        screenWidth = (self.tileSize+1) * mapSize + self.tileSize*2
        screenHeight = (self.tileSize+1) * mapSize

        # pygame 설정
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption("Game")

        self.tileImages = pygame.image.load("./Resource/images/tileImage.png")
        self.creatureImages = pygame.image.load("./Resource/images/creatureImage.png")
        self.systemImage = pygame.image.load("./Resource/images/systemImage.png")
    
    def getScreen(self):
        return self.screen

    def updateScreen(self):
        pygame.display.update()

    def getImages(self):
        return [self.tileImages,self.creatureImages,self.systemImage]

    def getInfos(self):
        return [self.setting,self.tileInfo,self.creatureInfo,self.systemInfo]

    def textShowWidth(self,showText,startX,startY):
        for x, text in enumerate(showText):
            imageLocation = (
                self.systemInfo[text][0] * self.tileSize,
                self.systemInfo[text][1] * self.tileSize,
                self.tileSize,
                self.tileSize
            )
            img = self.systemImage.subsurface(pygame.Rect(imageLocation))
            self.screen.blit(img, (x * self.tileSize + startX, startY))