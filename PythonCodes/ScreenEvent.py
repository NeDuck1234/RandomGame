import pygame
import json
from pygame.locals import *

class ScreenEvent:
    def __init__(self, mapSize):
        self.tileSize = 16
        self.tileInfo = None
        self.tileImages = None

        # 타일 정보 로드
        with open('./Resource/data/tileInfo.json') as file:
            self.tileInfo = json.load(file)
        with open('./Resource/data/creatureInfo.json') as file:
            self.creatureInfo = json.load(file)

        # 타일 이미지 로드
        self.tileImages = pygame.image.load("./Resource/images/tileImage.png")
        self.creatureImages = pygame.image.load("./Resource/images/creatureImage.png")

        # 캔버스 크기 계산
        self.canvas_width = (self.tileSize + 1) * mapSize
        self.canvas_height = (self.tileSize + 1) * mapSize

        # pygame 설정
        self.screen = pygame.display.set_mode((self.canvas_width, self.canvas_height))
        pygame.display.set_caption("Game")

    def getScreen(self):
        return self.screen

    def showMap(self, mapInfo, creatureLocInfo):
        # 화면 지우기
        self.screen.fill((0, 0, 0))

        # 각 타일 로드 및 그리기
        for y in range(len(mapInfo)):
            for x in range(len(mapInfo[0])):
                tile = mapInfo[y][x]
                imageLocation = (
                    self.tileInfo[tile][0] * self.tileSize,
                    self.tileInfo[tile][1] * self.tileSize,
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
