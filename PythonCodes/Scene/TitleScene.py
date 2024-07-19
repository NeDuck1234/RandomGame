import pygame
from pygame.locals import *
import sys
import json

import PythonCodes.Scene.GenerateScreen as GenerateScreen

import PythonCodes.System.SettingAndAction as SettingAndAction
import PythonCodes.System.SaveLoad as SaveLoad

class TitleScene:
    def __init__(self,screen):
        self.screen = screen

        self.generateScreen = GenerateScreen.GenerateScreen()
        images = self.generateScreen.getImages()
        infos = self.generateScreen.getInfos()

        # 타일 정보 로드
        self.setting = infos[0]
        self.tileInfo = infos[1]
        self.creatureInfo = infos[2]
        self.systemInfo = infos[3]

        # keyCodes 로드
        with open('./Resource/data/keycodes.json') as file:
            self.keyCodes = json.load(file)

        # 타일 이미지 로드
        self.tileImages = images[0]
        self.creatureImages = images[1]
        self.systemImage = images[2]

        self.tileSize = self.systemInfo["tileSize"]

        self.selectAction = 0

        self.mainloop()
    
    def mainloop(self):
        while True:
            userEvent = None
            for event in pygame.event.get():  
                if event.type == QUIT:
                    self.exitGame()
                elif event.type == KEYDOWN:
                    userEvent = event.key

            self.titleAction(userEvent)
            self.showTitle()
            self.updateScreen()

    def exitGame(self):
        pygame.quit()
        sys.exit()

    def titleAction(self,event):
        if event == self.keyCodes["up"]:
            self.selectAction -= 1
            if self.selectAction < 0: self.selectAction = 2
        elif event == self.keyCodes["down"]:
            self.selectAction += 1
            if self.selectAction > 2: self.selectAction = 0
        elif event == self.keyCodes["enter"]:
            self.selectActionFunction()
        elif event == self.keyCodes["esc"]:
            self.exitGame()

    def selectActionFunction(self):
        match self.selectAction:
            case 0:
                SettingAndAction.SettingAndAction(self.screen)
            case 1:
                sl = SaveLoad.SaveLoad()
                loadGame = sl.loadGame()
                SettingAndAction.SettingAndAction(self.screen,loadGame=loadGame)
            case 2:
                self.exitGame()

    def updateScreen(self):
        self.generateScreen.updateScreen()

    def showTitle(self):
        # 화면 지우기
        self.screen.fill((0, 0, 0))

        # 텍스트 그리기
        self.generateScreen.textShowWidth("START",80,288)
        self.generateScreen.textShowWidth("LOAD",80,320)
        self.generateScreen.textShowWidth("EXIT",80,352)

        # 화살표 그리기
        imageLocation = (
            self.systemInfo["arrowRight"][0] * self.tileSize,
            self.systemInfo["arrowRight"][1] * self.tileSize,
            self.tileSize,
            self.tileSize
        )
        img = self.systemImage.subsurface(pygame.Rect(imageLocation))
        self.screen.blit(img, (48, 288 + (self.selectAction * self.tileSize * 2)))
        