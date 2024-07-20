import pygame
import json

class SoundEffect:
    def __init__(self):
        pygame.mixer.init()
        with open('./Resource/data/soundInfo.json') as file:
            self.soundInfos = json.load(file)

    def playSound(self,soundName):
        soundInfo = self.soundInfos[soundName]
        soundType = soundInfo[0]
        soundLoc = soundInfo[1]

        if soundType == "SE": self.playSE(soundLoc)
        elif soundType == "BGM": self.playBGM(soundLoc)

    def playSE(self,soundLoc):
        seSound = pygame.mixer.Sound(soundLoc)
        seSound.play()

    def playBGM(self,soundLoc):
        bgmSound = pygame.mixer.Sound(soundLoc)
        bgmSound.play(loops=1)
