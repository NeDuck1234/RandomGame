import pygame

class TitleScene:
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