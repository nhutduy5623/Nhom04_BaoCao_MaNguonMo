import pygame
import time
POSITIONS=[(120,150),(60,270),(400,150),(400,250)]
POSITIONS_BETCIRCLE=[(200,150),(120,270),(320,150),(320,250)]



def drawCards(screen,cards):
    if cards:
        for ind,card in enumerate(cards):
            card_game=pygame.image.load(f"IMGCards/{card}.png")
            card_image = pygame.transform.scale(card_game, (75, 100))
            screen.blit(card_image, (350+55*ind, 360))


def drawflop(screen,flop):
    if flop:
        for ind,card in enumerate(flop):
            card_game=pygame.image.load(f"IMGCards/{card}.png")
            card_image = pygame.transform.scale(card_game, (75, 100))
            screen.blit(card_image, (200+80*ind, 200))
def drawWinner(winner,screen,font):
    color =(231, 201, 13)
    Winner_rect = pygame.Rect(150, 30, 500, 30)
    name_surface1 = font.render(f'{winner}', True, (0,0,0))
    name_rect1 = name_surface1.get_rect(midleft=(Winner_rect.left + 50, Winner_rect.centery))
    pygame.draw.rect(screen, color, Winner_rect)
    screen.blit(name_surface1, name_rect1)

def drawPlayers(screen,players,player_bet,winner_flag):
    if players:
        font = pygame.font.SysFont(None, 24)

        for ind,player in enumerate(players):
            pygame.draw.circle(screen, (255, 80, 100), POSITIONS[ind], 30)
            name_surface = font.render(player[0], True, (250, 250, 250))
            name_rect = name_surface.get_rect()
            name_rect.center = (POSITIONS[ind][0],POSITIONS[ind][1]-60)
            screen.blit(name_surface, name_rect)

            player_money_surface = font.render(f"{player[2]}$", True, (255, 255, 255))
            player_money_rect = player_money_surface.get_rect()
            player_money_rect.center = (POSITIONS[ind][0],POSITIONS[ind][1]+30)
            screen.blit(player_money_surface, player_money_rect)

            if winner_flag:
                for index, card in enumerate(player[3]):
                    card_game = pygame.image.load(f"IMGCards/{card}.png")
                    card_image = pygame.transform.scale(card_game, (45, 60))
                    screen.blit(card_image, (POSITIONS[ind][0] + 30 * index, POSITIONS[ind][1]))
            color=(0, 255, 255)
            if(int(player[1])==-1):
                color = (242, 33, 23)
                name_surface = font.render(f"X", True, (0, 0, 0))
            else:
                if (int(player[1]) > player_bet):
                    color = (231, 201, 13)
                name_surface = font.render(f"{player[1]}$", True, (0, 0, 0))

            bet_circle = pygame.Rect((POSITIONS_BETCIRCLE[ind][0],POSITIONS_BETCIRCLE[ind][1], 60, 30))
            pygame.draw.ellipse(screen, color, bet_circle)

            name_rect = name_surface.get_rect(center=(bet_circle.centerx, bet_circle.centery))
            screen.blit(name_surface, name_rect)


def drawChoiceButton(screen,network,fold_circle, check_circle,rise_circle,current_bet):
        check_color=(0, 255, 255)
        rise_color=(231, 201, 13)
        fold_color=(242, 33, 23)

        font = pygame.font.SysFont(None, 16)
        call_or_check="check"
        if(current_bet>0):
            call_or_check="call"

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if fold_circle.collidepoint(mouse_x, mouse_y ):
                fold_color = (147, 8, 8)
        elif check_circle.collidepoint(mouse_x, mouse_y ):
                check_color = (37, 150, 190)
        elif rise_circle.collidepoint(mouse_x, mouse_y ):
                rise_color = (119, 108, 18)

        pygame.draw.ellipse(screen, fold_color, fold_circle)
        name_surface = font.render("Fold", True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(fold_circle.centerx, fold_circle.centery))
        screen.blit(name_surface, name_rect)

        pygame.draw.ellipse(screen, check_color, check_circle)
        name_surface = font.render(call_or_check, True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(check_circle.centerx, check_circle.centery))
        screen.blit(name_surface, name_rect)

        pygame.draw.ellipse(screen, rise_color, rise_circle)
        name_surface = font.render("Rise", True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(rise_circle.centerx, rise_circle.centery))
        screen.blit(name_surface, name_rect)




