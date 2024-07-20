import pygame
import json
from pygame.locals import *

import PythonCodes.Scene.GenerateScreen as GenerateScreen

class InGameScene:
    def __init__(self,screen,images,infos):
        self.screen = screen

        # 타일 정보 로드
        self.setting = infos[0]
        self.tileInfo = infos[1]
        self.creatureInfo = infos[2]
        self.systemInfo = infos[3]
        self.itemInfo = infos[4]

        # 타일 이미지 로드
        self.tileImages = images[0]
        self.creatureImages = images[1]
        self.systemImage = images[2]
        self.itemImage = images[3]

        self.generateScreen = GenerateScreen.GenerateScreen()

        self.tileSize = self.systemInfo["tileSize"]

        self.inGameSize = (self.setting["mapSize"]+1)*self.tileSize


    def showSystem(self,playerLoc,itemInfo):
        # 시스템 메시지
        systemText = "SYSTEM"
        itemObject = itemInfo[playerLoc[0]][playerLoc[1]]
        item = self.itemInfo[str(itemObject)]
        systemText = item[2].upper()
        if not item[4]:
            systemText += f" X {itemObject.getCount()}"

        self.generateScreen.textShowWidth(systemText,0,self.inGameSize)

    def showInventory(self,inventoryInfo):
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
                self.screen.blit(img, (x * self.tileSize + self.inGameSize, y * self.tileSize))

        # 아이템 표시
        for idx, item in enumerate(inventoryInfo):
            itemInfo = self.itemInfo[item.tileStr]
            imageLocation = (
                itemInfo[0] * self.tileSize,
                itemInfo[1] * self.tileSize,
                self.tileSize,
                self.tileSize
            )
            img = self.itemImage.subsurface(pygame.Rect(imageLocation))
            x = int(idx>9)
            y = idx%10
            self.screen.blit(img, (x * self.tileSize + self.inGameSize, y * self.tileSize))

            # 개수 표시
            count = str(item.getCount())
            unit = len(count)
            for idx,number in enumerate(count):
                text = f"i{number}"
                systemInfo = self.systemInfo[text]
                imageLocation = (
                    systemInfo[0] * self.tileSize,
                    systemInfo[1] * self.tileSize,
                    self.tileSize,
                    self.tileSize
                )
                img = self.systemImage.subsurface(pygame.Rect(imageLocation))
                self.screen.blit(img, (x * self.tileSize + self.inGameSize-3*(unit-idx-1), y * self.tileSize))


    def showMap(self, mapInfo, creatureLocInfo, itemInfo):
        # 화면 지우기
        self.screen.fill((0, 0, 0))

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
                
        # 아이템 그리기
        for y in range(len(itemInfo)):
            for x in range(len(itemInfo[0])):
                item = itemInfo[y][x]
                imageLocation = (
                    self.itemInfo[str(item)][0] * self.tileSize,
                    self.itemInfo[str(item)][1] * self.tileSize,
                    self.tileSize,
                    self.tileSize
                )
                img = self.itemImage.subsurface(pygame.Rect(imageLocation))
                self.screen.blit(img, (x * self.tileSize, y * self.tileSize))

        # 생물 그리기
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

