import pygame
from pygame.locals import *
import sys
import json

import PythonCodes.Chunk.Chunk as Chunk
import PythonCodes.System.Player as Player
import PythonCodes.Scene.GenerateScreen as GenerateScreen
import PythonCodes.Scene.InGameScene as InGameScene
import PythonCodes.Scene.CraftingScreen as CraftingScreen

import PythonCodes.System.SaveLoad as SaveLoad
import PythonCodes.System.SoundEffect as SoundEffect

import threading

from PythonCodes.Tile.GetTile import GetTile

from PythonCodes.Item.Inventory import Inventory

class SettingAndAction:

    def toDic(self):
        value = {
            "chunkLocation" : self.chunkLocation,
            "mapLocation" : self.mapLocation
        }
        return value

    def __init__(self,screen,loadGame=None):

        # keyCodes 로드
        with open('./Resource/data/keycodes.json') as file:
            self.keyCodes = json.load(file)

        # 소리
        self.SoundEffect = SoundEffect.SoundEffect()

        with open('./setting.json') as file:
            self.setting = json.load(file)

        # 타일 얻기
        self.GetTile = GetTile()
        
        # pygame 설정
        self.generateScreen = GenerateScreen.GenerateScreen()
        images = self.generateScreen.getImages()
        infos = self.generateScreen.getInfos()

        self.itemInfos = infos[4]

        # 0 : 게임화면 , 1 : 크래프팅 화면
        self.screenNumber = 0
        # 게임화면
        self.InGameScene = InGameScene.InGameScene(screen,images,infos)
        self.CraftingScreen = CraftingScreen.CraftingScreen(screen,images,infos)

        # 기술력
        self.tech = 0

        # 플레이어 설정
        self.player = Player.Player()
        
        # 키보드 설정
        self.userEvent = []

        # 초기 위치 설정
        if self.loadGame(loadGame):
            self.mainloop()
            return

        self.MAXMAPSIZE = self.setting["mapSize"]  # 최대 맵 크기
        self.MINCHUNKSIZE = self.setting["chunkSize"]  # 최소 청크 크기

        self.chunkLocation = [self.MINCHUNKSIZE//2, self.MINCHUNKSIZE//2]
        self.mapLocation = [self.MAXMAPSIZE//2, self.MAXMAPSIZE//2]
        
        # 인벤토리 생성
        self.inventory = Inventory()

        # 청크 생성
        self.chunk = Chunk.Chunk(self.chunkLocation, self.mapLocation, self.MINCHUNKSIZE, self.MAXMAPSIZE)

        # pygame main loop 시작
        self.mainloop()
        return
    
    def loadGame(self,datas):
        if not datas: return False

        chunkInfo = datas["chunkInfo"]
        self.chunkLocation = chunkInfo["chunkLocation"]
        self.mapLocation = chunkInfo["mapLocation"]

        self.MAXMAPSIZE = None
        for row in chunkInfo["chunk"]:
            for mapInfo in row:
                if mapInfo: 
                    self.MAXMAPSIZE = mapInfo["size"]
                    break
            if self.MAXMAPSIZE: break
        self.MINCHUNKSIZE = chunkInfo["size"]  # 최소 청크 크기

        self.chunk = Chunk.Chunk(self.chunkLocation, self.mapLocation, self.MINCHUNKSIZE, self.MAXMAPSIZE,chunkInfo["chunk"])
        
        inventoryInfo = datas["inventoryInfo"]
        self.inventory = Inventory(inventoryInfo)

        return True

    # pygame main loop
    def mainloop(self):
        while True:
            for event in pygame.event.get():  
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.userEvent.append(event.key)
                    self.actionSelect()
                elif event.type == KEYUP:
                    if self.keyCodes["shift"] in self.userEvent:
                        self.userEvent = [self.keyCodes["shift"]]
                        if event.key == self.keyCodes["shift"]:
                            self.userEvent = []
                    else:
                        self.userEvent = []

            # 화면 업데이트
            self.showScreen()
            self.updateScreen()
    
    def actionSelect(self):
        match self.screenNumber:
            case 0: self.inGameActionSelect()
            case 1: self.craftingActionSelect()

    def showScreen(self):
        match self.screenNumber:
            case 0: # 게임 화면
                showMapInfo = self.chunk.getMap(self.chunkLocation)
                self.InGameScene.showMap(showMapInfo.mapInfo,showMapInfo.creatureInfo,showMapInfo.itemInfo)
                self.InGameScene.showInventory(self.inventory)
                self.InGameScene.showSystem(self.mapLocation,showMapInfo.itemInfo)
            case 1: # 크래프팅 화면
                self.CraftingScreen.showScreen(self.tech)

    def updateScreen(self):
        self.generateScreen.updateScreen()

    # 액션 선택
    def inGameActionSelect(self):
        keyCode = self.userEvent[-1]
        if keyCode in self.keyCodes["move"]:
            self.moveEvent()
        elif self.userEvent in self.keyCodes["numberShift"]:
            value = self.userEvent[1]-39
            self.inventory.setChoose(value if value > 9 else 18)
            self.userEvent = [self.userEvent[0]]
        elif keyCode in self.keyCodes["number"]:
            value = keyCode - 49
            self.inventory.setChoose(value if value > -1 else 9)
        elif keyCode == self.keyCodes["getItem"]:
            inMap = self.chunk.getMap(self.chunkLocation)
            item = inMap.itemInfo[self.mapLocation[0]][self.mapLocation[1]]
            self.getItem(item)
            inMap.itemInfo[self.mapLocation[0]][self.mapLocation[1]] = "_"
        elif keyCode == self.keyCodes["drop"]:
            self.dropItem()
        elif keyCode == self.keyCodes["setBlock"] and self.userEvent != self.keyCodes["save"]:
            self.setBlock()
        elif keyCode == self.keyCodes["craft"]:
            self.getCraftingTech()
            self.screenNumber = 1
        elif self.userEvent == self.keyCodes["save"]:
            self.saveGame()
            self.userEvent = [self.userEvent[0]]
        elif keyCode == self.keyCodes["esc"]:
            pygame.quit()
            sys.exit()

    # 블록 설치
    def setBlock(self):
        inMap = self.chunk.getMap(self.chunkLocation)
        tileInfo = inMap.mapInfo[self.mapLocation[0]][self.mapLocation[1]]
        itemInfo = inMap.itemInfo[self.mapLocation[0]][self.mapLocation[1]]
        if not self.player.moveAble(tileInfo) or not itemInfo == "_":
            return
        idx = self.inventory.getChoose()
        inventory = self.inventory.getInventory()
        if len(inventory)-1 < idx:
            return
        item = inventory[idx]
        itemStr = item.tileStr
        if not self.itemInfos[itemStr][6]:
            return
        self.inventory.removeItem(idx)
        inMap.mapInfo[self.mapLocation[0]][self.mapLocation[1]] = itemStr
        
    
    # 아이템 떨구기
    def dropItem(self):
        inMap = self.chunk.getMap(self.chunkLocation)
        mapItem = inMap.itemInfo[self.mapLocation[0]][self.mapLocation[1]] 
        idx = self.inventory.getChoose()
        inventory = self.inventory.getInventory()
        if len(inventory)-1 < idx:
            return
        item = inventory[idx]
        if mapItem != "_":
            if type(mapItem) == type(item):
                if mapItem.getCount() == "single":
                    return
                self.inventory.removeItem(idx)
                mapItem.setCount(mapItem.getCount()+item.getCount())
                return
            return
        self.inventory.removeItem(idx)
        inMap.setItem(self.mapLocation,item)

    # 이동 종료
    def moveEnd(self,mapInfo,keyEvent):
        mapInfo.clearCreature()
        mapInfo.creatureMove(self.mapLocation)
        self.userEvent = []

    # 이동
    def moveEvent(self):
        inMap = self.chunk.getMap(self.chunkLocation)
        keyEvent = 0
        for i in range(len(self.userEvent)):
            if self.userEvent in self.keyCodes["move"]:
                keyEvent = i
                break
        moveLoc = self.player.move(self.userEvent[keyEvent])
        if not moveLoc:
            self.moveEnd(inMap,keyEvent)
            return
        movePoint = self.mapLocation[moveLoc[0]] + moveLoc[1]
        if movePoint < 0 or movePoint > self.MAXMAPSIZE:
            moveChunk = self.player.moveChunk(moveLoc)
            chunkPoint = self.chunkLocation[moveChunk[0]] + moveChunk[1]
            if not (chunkPoint < 0 or chunkPoint > self.MINCHUNKSIZE):
                self.chunkLocation[moveChunk[0]] = chunkPoint
                if moveLoc[2] == 0:
                    self.mapLocation[0] = self.MAXMAPSIZE
                elif moveLoc[2] == 1:
                    self.mapLocation[1] = self.MAXMAPSIZE
                elif moveLoc[2] == 2:
                    self.mapLocation[0] = 0
                elif moveLoc[2] == 3:
                    self.mapLocation[1] = 0
                self.chunk.locMove(self.chunkLocation, self.mapLocation, self.MAXMAPSIZE)
        else:
            toMoveLoc = self.mapLocation[:]
            toMoveLoc[moveLoc[0]] = movePoint
            tile = inMap.getTile(toMoveLoc)
            if self.player.moveAble(tile): self.mapLocation[moveLoc[0]] = movePoint
            if type(tile) != str: self.actions(tile,toMoveLoc,inMap)
        self.moveEnd(inMap,keyEvent)
        return

    # 게임 저장
    def saveGame(self):
        print(1)
        self.chunk.getLocation(self.chunkLocation,self.mapLocation)
        save = SaveLoad.SaveLoad()
        save.saveGame(
            self.chunk,
            self.inventory
        )

    # 아이템 획득
    def getItem(self,item):
        if type(item) == str: return
        if self.inventory.itemExist(item.tileStr):
            if item.count == "single":
                self.inventory.setItem(item)
                return True
            inventoryItem = self.inventory.getItem(item.tileStr)
            inventoryItem.count += item.count
        else:
            self.inventory.setItem(item)
        return True

    # 동작
    def actions(self,tile,tileLoc,mapInfo):
        if type(tile) == type(self.GetTile.getTile("|")):
            tile.cuttingAction(tileLoc,mapInfo)
    
    def getCraftingTech(self):
        aroundTile = self.chunk.getMap(self.chunkLocation).arroundFromLocation(self.mapLocation)[0]
        for row in aroundTile:
            for tile in row:
                if tile == "#" and self.tech < 1:
                    self.tech = 1

    # 제작화면 액션
    def craftingActionSelect(self):
        keyCode = self.userEvent[-1]
        if keyCode == self.keyCodes["up"]: 
            self.SoundEffect.playSound("Choose")
            self.CraftingScreen.playerSelectChange(True)
        elif keyCode == self.keyCodes["down"]: 
            self.SoundEffect.playSound("Choose")
            self.CraftingScreen.playerSelectChange(False)
        elif keyCode in [self.keyCodes["enter"],self.keyCodes["right"]]:
            value = self.CraftingScreen.craftSelected(self.inventory)
            if value: self.getItem(value)
            self.SoundEffect.playSound("Select")
            self.craftingEnd()
        elif keyCode == self.keyCodes["craft"]:
            self.screenNumber = 1
        elif keyCode == self.keyCodes["esc"]:
            self.SoundEffect.playSound("Choose")
            self.craftingEnd()

    def craftingEnd(self):
        self.CraftingScreen.clearCraftList()
        self.screenNumber = 0
        self.tech = 0