import pygame
import json
from pygame.locals import *

class ScreenEvent:
    def __init__(self, mapSize):
        self.tileSize = 16
        self.tileInfo = None
        self.tileImages = None

        # 타일 정보 로드
        with open('./setting.json') as file:
            self.setting = json.load(file)
        with open('./Resource/data/tileInfo.json') as file:
            self.tileInfo = json.load(file)
        with open('./Resource/data/creatureInfo.json') as file:
            self.creatureInfo = json.load(file)
        with open('./Resource/data/systemInfo.json') as file:
            self.systemInfo = json.load(file)

        # 타일 이미지 로드
        self.tileImages = pygame.image.load("./Resource/images/tileImage.png")
        self.creatureImages = pygame.image.load("./Resource/images/creatureImage.png")
        self.systemImage = pygame.image.load("./Resource/images/systemImage.png")

        # 캔버스 크기 계산
        #                   기본 화면                      + 인벤토리
        self.screenWidth = (self.tileSize+1) * mapSize + self.tileSize*2
        self.screenHeight = (self.tileSize+1) * mapSize

        # pygame 설정
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Game")

    def getScreen(self):
        return self.screen

    def showMap(self, mapInfo, creatureLocInfo):
        # 화면 지우기
        self.screen.fill((0, 0, 0))

        # 인벤토리 그리기
        for y in range(10):
            for x in range(2):
                inventory = self.systemInfo["inventory"]
                imageLocation = (
                    inventory[0] * self.tileSize,
                    inventory[1] * self.tileSize,
                    self.tileSize,
                    self.tileSize
                )
                img = self.systemImage.subsurface(pygame.Rect(imageLocation))
                self.screen.blit(img, (x * self.tileSize + (self.setting["mapSize"]+1)*self.tileSize, y * self.tileSize))
                

        # 각 타일 로드 및 그리기
        for y in range(len(mapInfo)):
            for x in range(len(mapInfo[0])):
                tile = mapInfo[y][x]
                imageLocation = (
                    self.tileInfo[str(tile)][0] * self.tileSize,
                    self.tileInfo[str(tile)][1] * self.tileSize,
                    self.tileSize,
                    self.tileSize
                )
                img = self.tileImages.subsurface(pygame.Rect(imageLocation))
                self.screen.blit(img, (x * self.tileSize, y * self.tileSize))

        for y in range(len(creatureLocInfo)):
            for x in range(len(creatureLocInfo[0])):
                creature = creatureLocInfo[y][x]
                imageLocation = (
                    self.creatureInfo[creature][0] * self.tileSize,
                    self.creatureInfo[creature][1] * self.tileSize,
                    self.tileSize,
                    self.tileSize
                )
                img = self.creatureImages.subsurface(pygame.Rect(imageLocation))
                self.screen.blit(img, (x * self.tileSize, y * self.tileSize))
