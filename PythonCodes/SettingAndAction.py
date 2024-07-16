import pygame
import sys
import json
from pygame.locals import *

import PythonCodes.Chunk as Chunk
import PythonCodes.Player as Player
import PythonCodes.ScreenEvent as ScreenEvent
import threading

class SettingAndAction:
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
        self.screenEvent = ScreenEvent.ScreenEvent(self.MAXMAPSIZE)
        self.screen = self.screenEvent.getScreen()

        # 플레이어 설정
        self.player = Player.Player()

        # 초기 위치 설정
        self.chunkLocation = [self.MINCHUNKSIZE//2, self.MINCHUNKSIZE//2]
        self.mapLocation = [self.MAXMAPSIZE//2, self.MAXMAPSIZE//2]
        self.chunk = Chunk.Chunk(self.chunkLocation, self.mapLocation, self.MINCHUNKSIZE, self.MAXMAPSIZE)

        self.userEvent = None

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
                    self.userEvent = event
                    self.actionSelect()
                    self.setKeyboardInfo(self.userEvent)

            # 화면 업데이트
            showMapInfo = self.chunk.getMap(self.chunkLocation)
            self.screenEvent.showMap(showMapInfo.mapInfo,showMapInfo.creatureInfo)
            pygame.display.update()

    # 액션 선택
    def actionSelect(self):
        if self.userEvent.key in self.keyCodes["move"]:
            self.action("move")
        elif self.userEvent.key == self.keyCodes["esc"]:
            self.action("end")

    # 액션 수행
    def action(self, event):
        if event == "move":
            inMap = self.chunk.getMap(self.chunkLocation)
            moveLoc = self.player.move(self.userEvent.key)
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
                if self.player.moveAble(inMap.getTile(toMoveLoc)):
                    self.mapLocation[moveLoc[0]] = movePoint
            inMap.clearCreature()
            inMap.creatureMove(self.mapLocation)
        if event == "end":
            self.player.endGame((self.keyBoardListener,))
    # 키보드 정보 설정
    def setKeyboardInfo(self, event):
        self.userEvent = None
