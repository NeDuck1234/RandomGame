import pygame
import json
from pygame.locals import *

class InGameScene:
    def __init__(self,screen,images,infos):
        self.screen = screen

        # 타일 정보 로드
        self.setting = infos[0]
        self.tileInfo = infos[1]
        self.creatureInfo = infos[2]
        self.systemInfo = infos[3]

        # 타일 이미지 로드
        self.tileImages = images[0]
        self.creatureImages = images[1]
        self.systemImage = images[2]

        self.tileSize = self.systemInfo["tileSize"]

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
