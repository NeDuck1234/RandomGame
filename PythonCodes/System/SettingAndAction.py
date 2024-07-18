import pygame
import sys
import json
from pygame.locals import *

import PythonCodes.Chunk.Chunk as Chunk
import PythonCodes.System.Player as Player
import PythonCodes.Scene.GenerateScreen as GenerateScreen
import PythonCodes.Scene.InGameScene as InGameScene

import PythonCodes.System.SaveLoad as SaveLoad

import threading

from PythonCodes.Tile.Tree import Tree

class SettingAndAction:

    def toDic(self):
        value = {
            "chunkLocation" : self.chunkLocation,
            "mapLocation" : self.mapLocation
        }
        return value

    def __init__(self):
        pygame.init()

        # keyCodes 로드
        with open('./Resource/data/keycodes.json') as file:
            self.keyCodes = json.load(file)

        # 맵 설정

        with open('./setting.json') as file:
            self.setting = json.load(file)

        self.MAXMAPSIZE = self.setting["mapSize"]  # 최대 맵 크기
        self.MINCHUNKSIZE = self.setting["chunkSize"]  # 최소 청크 크기

        # pygame 설정
        generateScreen = GenerateScreen.GenerateScreen()
        screen = generateScreen.getScreen()
        images = generateScreen.getImages()
        infos = generateScreen.getInfos()
        self.InGameScene = InGameScene.InGameScene(self.MAXMAPSIZE,screen,images,infos)

        # 플레이어 설정
        self.player = Player.Player()

        # 초기 위치 설정
        self.chunkLocation = [self.MINCHUNKSIZE//2, self.MINCHUNKSIZE//2]
        self.mapLocation = [self.MAXMAPSIZE//2, self.MAXMAPSIZE//2]
        self.chunk = Chunk.Chunk(self.chunkLocation, self.mapLocation, self.MINCHUNKSIZE, self.MAXMAPSIZE)

        self.userEvent = []

        # pygame main loop 시작
        self.mainloop()

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
                    self.userEvent = []

            # 화면 업데이트
            showMapInfo = self.chunk.getMap(self.chunkLocation)
            self.InGameScene.showMap(showMapInfo.mapInfo,showMapInfo.creatureInfo)
            pygame.display.update()

    # 액션 선택
    def actionSelect(self):
        if self.userEvent[-1] in self.keyCodes["move"]:
            self.action("move")
        elif self.userEvent == self.keyCodes["save"]:
            self.action("save")
        elif self.userEvent[-1] == self.keyCodes["esc"]:
            self.action("end")

    # 이동 종료
    def moveEnd(self,mapInfo,keyEvent):
        mapInfo.clearCreature()
        mapInfo.creatureMove(self.mapLocation)
        self.userEvent = []

    # 액션 수행
    def action(self, event):
        if event == "move":
            self.moveEvent(event)
            return
        if event == "save":
            self.saveGame()
            return
        if event == "end":
            self.player.endGame((self.keyBoardListener,))
            return

    # 이동
    def moveEvent(self,event):
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
        self.chunk.getLocation(self.chunkLocation,self.mapLocation)
        save = SaveLoad.SaveLoad()
        save.saveGame(
            self.chunk
        )

    # 동작
    def actions(self,tile,tileLoc,mapInfo):
        if type(tile) == Tree:
            if tile.cutting():
                treeLoc = tileLoc[:]
                count = 1
                while mapInfo.mapInfo[treeLoc[0]-count][treeLoc[1]] == "^":
                    count += 1
                treeLoc = [treeLoc]
                treeLoc.extend([[tileLoc[0]-count,tileLoc[1]] for count in range(count) ])
                mapInfo.setTile(treeLoc)
