import pygame
from pygame.locals import *
import PythonCodes.Item.GetItem as GetItem

import PythonCodes.Scene.GenerateScreen as GenerateScreen

class CraftingScreen:
    def __init__(self,screen,images,infos):
        self.screen = screen
        self.GetItem = GetItem.GetItem()

        # 타일 정보 로드
        self.setting = infos[0]
        self.tileInfo = infos[1]
        self.creatureInfo = infos[2]
        self.systemInfo = infos[3]
        self.itemInfo = infos[4]
        self.craftInfo = infos[5]

        # 타일 이미지 로드
        self.tileImages = images[0]
        self.creatureImages = images[1]
        self.systemImage = images[2]
        self.itemImage = images[3]

        self.generateScreen = GenerateScreen.GenerateScreen()

        self.tileSize = self.systemInfo["tileSize"]
        self.craftList = []

        self.playerSelect = 0

        self.inGameSize = (self.setting["mapSize"]+1)*self.tileSize

    def playerSelectChange(self,upDonw):
        if upDonw:  #up
            self.playerSelect -= 1
            if self.playerSelect < 0:
                self.playerSelect = len(self.craftList)-1
        else:
            self.playerSelect += 1
            if self.playerSelect == len(self.craftList):
                self.playerSelect = 0

    def craftSelected(self,inventoryInfo):
        value = None
        inventory = inventoryInfo.getInventory()
        inventoryStr = [str(inv) for inv in inventory]
        needs = self.craftList[self.playerSelect]
        for item,count in needs[1][1]:
            if item in inventoryStr:
                idx = inventoryStr.index(item)
                itemCount = inventory[idx].getCount()
                if count <= itemCount:
                    inventory[idx].setCount(itemCount-count)
                    if inventory[idx].getCount() == 0:
                        inventoryInfo.removeItem(idx)
                    value = self.GetItem.getItem(needs[1][2])
        return value
    
    def showScreen(self,tech):
        self.screen.fill((0, 0, 0))

        tileCount = self.inGameSize//self.tileSize
        self.generateScreen.textShowWidth("CRAFT "+"-"*(tileCount-4),0,0)
        self.generateScreen.textShowWidth("-"*(tileCount+2),0,self.inGameSize)

        self.generateScreen.textShowWidth("NAME",self.tileSize,self.tileSize)
        center = self.tileSize*(tileCount-10)+self.tileSize
        self.generateScreen.textShowWidth("NEED",center,self.tileSize)

        if not self.craftList: self.setCraftList(tech)
        
        for idx,craft in enumerate(self.craftList):
            name = craft[0].upper()
            needs = craft[1][1]
            self.generateScreen.textShowWidth(name,self.tileSize,self.tileSize*(idx+3))
            textLen = 0
            for need in needs:
                item = need[0]
                imageLocation = (
                    self.itemInfo[item][0] * self.tileSize,
                    self.itemInfo[item][1] * self.tileSize,
                    self.tileSize,
                    self.tileSize
                )
                img = self.itemImage.subsurface(pygame.Rect(imageLocation))
                self.screen.blit(img, (textLen * self.tileSize+center, self.tileSize*(idx+3)))
                textLen+=1
                needCount = f"X{need[1]}"
                self.generateScreen.textShowWidth(needCount,textLen * self.tileSize+center,self.tileSize*(idx+3))
                textLen+=len(needCount)

        # 화살표 그리기
        imageLocation = (
            self.systemInfo["arrowRight"][0] * self.tileSize,
            self.systemInfo["arrowRight"][1] * self.tileSize,
            self.tileSize,
            self.tileSize
        )
        img = self.systemImage.subsurface(pygame.Rect(imageLocation))
        self.screen.blit(img, (0, self.tileSize*3 + (self.playerSelect * self.tileSize)))

    def setCraftList(self,tech):
        for craft in self.craftInfo:
            if self.craftInfo[craft][0] <= tech:
                self.craftList.append([craft,self.craftInfo[craft]])

    def clearCraftList(self):
        self.craftList = []