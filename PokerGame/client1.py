import sys
import  Draw
import pygame
import time
from Network import Network
import requests

def getServerAddress():
    url = "https://poker-address-api.vercel.app/"
    try:
        # Send the GET request
        response = requests.get(url)
        # Check the response status code
        if response.status_code == 200:
            print("GET request successful")
            # Split the response content to extract host and port
            parts = response.text.split(":")
            if len(parts) >= 2:
                host = parts[1][2:].strip()
                port = int(parts[2].strip())
                return [host,port]
            else:
                print("Invalid response format")
                return []
        else:
            print("GET request failed with status code:", response.status_code)
            return []
    except Exception as e:
        print("An error occurred during the GET request:", e)
        return []
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
# Load background image
background_image = pygame.image.load("Images/Table.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

menu_image = pygame.image.load("Images/menu.jpg")
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 32)

# Text field properties
text_color = BLACK

text_field_name = "Name:"
input_rect1 = pygame.Rect(300, 200, 200, 30)
input_rect2 = pygame.Rect(300, 250, 200, 30)
Enter_rect = pygame.Rect(300, 300, 200, 30)

input_color2 = BLACK
input_color1 = BLACK

BUTTON_POSITIONS=(550,500,)
room_id = ""
name = ""
def Waiting(network,host,room_id):
    pygame.display.set_caption("Waiting")
    running = True
    number = (int)(network.sendData(f"get_number"))
    # print(network.sendData(f"get_number"))
    SCREEN.fill((0, 0, 0))
    while running:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicks on the input box, toggle input_active
                if Enter_rect.collidepoint(event.pos):
                    if(number>1 and host):
                        network.sendData("START")

                        Play(network)



        SCREEN.blit(background_image, (0, 0))

        room_circle = pygame.Rect((20, 20, 60, 30))
        pygame.draw.ellipse(SCREEN, ((231, 201, 13)), room_circle)
        room_surface = font.render(f"{room_id}", True, (0, 0, 0))
        room_rect = room_surface.get_rect(center=(room_circle.centerx, room_circle.centery))
        SCREEN.blit(room_surface, room_rect)



        number=(int)(network.sendData(f"get_number"))
        player_money = (int)(network.sendData(f"get_playerMoney"))
        start=(network.sendData(f"can_start")) == "True"

        player_money_surface = font.render(f"{player_money}", True, (255, 255, 255))
        player_money_rect = player_money_surface.get_rect()
        player_money_rect.center = (410, 525)
        SCREEN.blit(player_money_surface, player_money_rect)
        if(start):
            Play(network)

        if(host and number>1):
            name_surface1 = font.render('START', True, BLACK)
            name_rect1 = name_surface1.get_rect(midleft=(Enter_rect.left + 50, Enter_rect.centery))
            pygame.draw.rect(SCREEN, (255,255,255), Enter_rect)
            SCREEN.blit(name_surface1, name_rect1)




        pygame.draw.circle(SCREEN, (255,80,100), (350,450), 50)
        if(number<2):
            name_surface = font.render('Waiting for People', True, (250, 250, 250))
            name_rect = name_surface.get_rect()
            name_rect.center=(400,250)
            SCREEN.blit(name_surface, name_rect)

        pygame.display.update()


def Play(network):
    pygame.display.set_caption("Play")
    running = True
    SCREEN.fill((0, 0, 0))

    current_value = 0
    max_value = 5000
    slider_x = 550
    thumb_radius = 10
    slider_width = 200
    slider_y = 570
    dragging = False
    winner_flag=False
    min_value=0
    fold_circle = pygame.Rect((BUTTON_POSITIONS[0], BUTTON_POSITIONS[1], 50, 50))
    check_circle = pygame.Rect((BUTTON_POSITIONS[0] + 75, BUTTON_POSITIONS[1], 50, 50))
    rise_circle = pygame.Rect((BUTTON_POSITIONS[0] + 150, BUTTON_POSITIONS[1], 50, 50))
    time_circle = pygame.Rect((270, 320, 50, 50))
    flag_turn=False
    limitTime=10000
    winner_showtime=0
    Pot_rect = pygame.Rect(350, 150, 120, 20)
    while running:
        list_player = (network.GetObs(f"get_players"))
        data = (network.GetObs(f"get_hands"))
        flop = (network.GetObs(f"get_flop"))
        max_value=int(network.sendData(f"get_playerMoney"))
        player_bet = int(network.sendData(f"get_playerBet"))
        min_value= int(network.sendData(f"get_currentBet"))
        pot = int(network.sendData(f"get_pot"))
        turn=(network.sendData(f"get_turn")) == "True"
        winner = (network.sendData(f"get_winner"))





        # current_bet=int(network.sendData(f"get_currentBet"))

        if not data:
            break



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not winner_flag:
                if turn:
                    if check_circle.collidepoint(event.pos):
                        network.sendData("ACTION 1")
                    if fold_circle.collidepoint(event.pos):
                        network.sendData("ACTION 2")
                    if rise_circle.collidepoint(event.pos):
                        print(f"{int(current_value-player_bet)}")
                        network.sendData(f"ACTION 3 {int(current_value-player_bet)}")
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (slider_x - 10 <= mouse_x <= slider_x + slider_width + thumb_radius and
                            slider_y - thumb_radius <= mouse_y <= slider_y + thumb_radius):
                        dragging = True
            elif event.type == pygame.MOUSEBUTTONUP and turn:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging and turn:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                current_value = min(
                    max((mouse_x - slider_x) / slider_width * (max_value - min_value) +min_value, min_value),
                    max_value)


        if (not flag_turn) and turn:
            current_value=min_value
            flag_turn=True
            start_time=pygame.time.get_ticks()
        elif not turn:
            flag_turn=False
        SCREEN.blit(background_image, (0, 0))
        if (winner != "notthing"):
            Draw.drawWinner(winner, SCREEN, font)
            if not winner_flag:
                winner_flag = True
                winner_showtime = pygame.time.get_ticks()
            t = pygame.time.get_ticks() - winner_showtime
            if (t > 5000):
                break



        bet_color = (0, 255, 255)
        if (player_bet == -1):
            bet_color = (242, 33, 23)
            bet_surface = font.render(f"X", True, (0, 0, 0))
        else:
            if (player_bet>0):
                bet_color = (231, 201, 13)
            bet_surface = font.render(f"{player_bet}$", True, (0, 0, 0))
        bet_circle = pygame.Rect((380, 320, 60, 30))
        pygame.draw.ellipse(SCREEN, bet_color, bet_circle)
        bet_rect = bet_surface.get_rect(center=(bet_circle.centerx, bet_circle.centery))
        SCREEN.blit(bet_surface, bet_rect)




        player_money_surface = font.render(f"{max_value} $", True, (255, 255, 255))
        player_money_rect = player_money_surface.get_rect()
        player_money_rect.center = (410, 500)
        SCREEN.blit(player_money_surface, player_money_rect)

        pot_surface = font.render(f'POT : {pot} $', True, BLACK)
        pot_rect = pot_surface.get_rect(midleft=(Pot_rect.left +5, Pot_rect.centery))
        pygame.draw.rect(SCREEN, (255, 255, 255), Pot_rect)
        SCREEN.blit(pot_surface, pot_rect)


        Draw.drawCards(SCREEN,data)
        Draw.drawPlayers(SCREEN,list_player,player_bet,winner_flag)
        Draw.drawflop(SCREEN,flop)

        if turn and not winner_flag:



            timePlay=pygame.time.get_ticks()-start_time
            if (timePlay > limitTime):
                if(min_value<=player_bet):
                    network.sendData("ACTION 1")
                else:
                    network.sendData("ACTION 2")
            pygame.draw.ellipse(SCREEN, (0, 255, 255), time_circle)
            tick_surface = font.render(f"{10-int(timePlay / 1000)}", True, (0, 0, 0))
            tick_rect = tick_surface.get_rect(midleft=(time_circle.centerx, time_circle.centery))
            tick_rect.center=(300,350)
            SCREEN.blit(tick_surface, tick_rect)


            Draw.drawChoiceButton(SCREEN, network, fold_circle, check_circle, rise_circle,min_value)
            pygame.draw.rect(SCREEN, (206, 228, 19), (slider_x, slider_y, slider_width, 10))
            thumb_x = int(slider_x + (current_value - min_value) / (max_value - min_value) * slider_width)
            pygame.draw.circle(SCREEN, (19, 228, 23), (thumb_x, slider_y + 5), thumb_radius)
            current_valueSur = font.render(f'{int(current_value)} $', True, (250, 250, 250))
            current_valueText = current_valueSur.get_rect()
            current_valueText.center = (slider_x - 50, slider_y)
            SCREEN.blit(current_valueSur, current_valueText)

        # name_surface = font.render('Playing', True, (250, 250, 250))
        # name_rect = name_surface.get_rect()
        # name_rect.center = (400, 250)
        # SCREEN.blit(name_surface, name_rect)

        pygame.display.update()
        pygame.display.flip()


def Menu():
    # Get room ID from user\
    pygame.display.set_caption("Simple Pygame Window")
    game_state = "menu"
    hover_Color = (100, 100, 100)

    running = True
    text_input1 = ""
    input_active1 = False
    text_input2 = ""
    input_active2 = False
    address = getServerAddress()
    n=Network("","")
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type ==  pygame.MOUSEMOTION:
                if Enter_rect.collidepoint(event.pos):
                    hover_Color = (100, 100, 50)
                elif input_rect2.collidepoint(event.pos):
                    input_color2=(90,150,190)
                elif input_rect1.collidepoint(event.pos):
                    input_color1 = (90, 150, 190)
                else:
                    hover_Color = (100, 100, 100)
                    input_color1=BLACK
                    input_color2=BLACK

            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicks on the input box, toggle input_active
                if Enter_rect.collidepoint(event.pos):
                    room_id=text_input2
                    name = text_input1
                    if room_id!="" and name !="":
                        game_state = "play"
                if input_rect1.collidepoint(event.pos):
                    input_active1 = True
                    input_active2 = False
                elif input_rect2.collidepoint(event.pos):
                    input_active2 = True
                    input_active1 = False
                else:
                    input_active1 = False
                    input_active2 = False
            if event.type == pygame.KEYDOWN:
                # If input_active is True, handle key presses
                if input_active1:
                    if event.key == pygame.K_BACKSPACE :
                        # If Backspace is pressed, remove the last character from the input
                        text_input1 = text_input1[:-1]
                        # If Backspace is pressed, remove the last character from the input

                    else:
                        # Add the pressed key to the input
                        text_input1 += event.unicode
                if input_active2:
                    if event.key == pygame.K_BACKSPACE  or event.key == pygame.K_BACKSPACE:
                        # If Backspace is pressed, remove the last character from the input
                        text_input2 = text_input2[:-1]
                        # If Backspace is pressed, remove the last character from the input

                    else:
                        # Add the pressed key to the input
                        text_input2 += event.unicode

        if game_state == "menu":
            SCREEN.blit(menu_image, (0, 0))
            pygame.draw.rect(SCREEN, (200, 200, 200), input_rect1)
            pygame.draw.rect(SCREEN, BLACK, input_rect1, 2)
            text_surface = font.render(text_input1, True, WHITE)
            SCREEN.blit(text_surface, (input_rect1.x + 5, input_rect1.y + 5))

            name_surface = font.render('Name:', True, BLACK)
            name_rect = name_surface.get_rect(midleft=(input_rect1.left - 70, input_rect1.centery))
            SCREEN.blit(name_surface, name_rect)

            pygame.draw.rect(SCREEN, (200, 200, 200), input_rect2)
            pygame.draw.rect(SCREEN, BLACK, input_rect2, 2)
            text_surface = font.render(text_input2, True, WHITE)
            SCREEN.blit(text_surface, (input_rect2.x + 5, input_rect2.y + 5))

            name_surface1 = font.render('Id Table:', True, BLACK)
            name_rect1 = name_surface1.get_rect(midleft=(input_rect2.left - 95, input_rect2.centery))
            SCREEN.blit(name_surface1, name_rect1)

            name_surface1 = font.render('START', True, BLACK)
            name_rect1 = name_surface1.get_rect(midleft=(Enter_rect.left + 50, Enter_rect.centery))
            pygame.draw.rect(SCREEN, hover_Color, Enter_rect)
            SCREEN.blit(name_surface1, name_rect1)

        elif game_state == "play":
            host=n.setNAR(room_id,name)
            Waiting(n,host,room_id)
        pygame.display.update()
        pygame.display.flip()

Menu()
pygame.quit()





    # Connect and join the room

