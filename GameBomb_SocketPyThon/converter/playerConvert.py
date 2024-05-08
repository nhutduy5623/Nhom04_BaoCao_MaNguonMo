import pygame
from DTO.playerDTO import PlayerDTO
from player import Player
from converter.bombConvert import bombConvert

class playerConvert():
    def toDTO(self, Player):   
        listBombDTO = [] 
        for bomb in Player.listBomb:
            listBombDTO.append(bombConvert().toDTO(bomb))
        return PlayerDTO(Player.flag_StartGame, Player.getCenterx(), Player.getCentery(), Player.getVel(), Player.getMaxBomb(), Player.getStatus(), Player.getRecoverTime(), listBombDTO)
    def toPlayer(playerDTO, playerSurface, bomb):
        pass
