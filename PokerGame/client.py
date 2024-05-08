import socket
import pygame
import sys
# Server address and port (replace with actual server IP if needed)
HOST = 'localhost'
PORT = 65432

WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Simple Pygame Window")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Load background image
background_image = pygame.image.load("Images/menu.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
def connect_and_join(room_id, name):
    WIDTH, HEIGHT = 800, 600
    WINDOW_SIZE = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Simple Pygame Window")

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Load background image
    background_image = pygame.image.load("Images/menu.jpg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    """Connects to the server, sends room ID, and receives confirmation."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = False
        s.connect((HOST, PORT))
        # Send formatted message (room ID + message)
        message = f"JOIN {room_id} AS {name}"
        s.sendall(message.encode())
        # Receive confirmation message
        data = s.recv(1024).decode()
        print(data)  # Print confirmation message from server


        if data.find("host") != -1:
            host = True
            # message = input("Enter your message (or 'quit' to disconnect): ")
            # if message.lower() == 'quit':
            #     return s
        formatted_message = f"{room_id} {name} START"
        s.sendall(formatted_message.encode())
        print("Waiting for host to start the game...")
        # Game loop to maintain connection and send/receive messages
        while True:
            data = s.recv(1024).decode()
            if not data:
                continue
            print(f"{data}")


            if data.startswith(f"{name} TURN") or data == "Enter the amount" or data.find("host") != -1:
                if data.find("host") != -1:
                    host = True
                message = input("Enter your message (or 'quit' to disconnect): ")
                if message.lower() == 'quit':
                    return s
                # Send formatted message (room ID + sender + message)
                formatted_message = f"ACTION {name} {message}"
                s.sendall(formatted_message.encode())
            if data.find("wins") != -1:
                if host:
                    message = input("Enter your message (or 'quit' to disconnect): ")
                    if message.lower() == 'quit':
                        return s
                    # Send formatted message (room ID + sender + message)
                    formatted_message = f"ACTION {name} {message}"
                    s.sendall(formatted_message.encode())
                else:
                    print("Waiting for host to start the game...")
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 32)

# Text field properties
text_color = BLACK

text_field_name = "Name:"
input_rect1 = pygame.Rect(300, 200, 200, 30)
input_rect2 = pygame.Rect(300, 250, 200, 30)
Enter_rect = pygame.Rect(300, 300, 200, 30)
text_input1 = ""
input_active1 = False
text_input2 = ""
input_active2 = False
hover_Color=(100,100,100)
input_color2 = BLACK
input_color1 = BLACK
if __name__ == '__main__':
    # Get room ID from user\
    running = True
    while running:


        # try:
        #     name = input("Please enter your name: ")
        #     room_id = int(input("Enter room ID to join: "))
        #     break
        # except ValueError:
        #     print("Invalid room ID. Please enter a number.")
        room_id=""
        name=""
        for event in pygame.event.get():
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
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicks on the input box, toggle input_active
                if Enter_rect.collidepoint(event.pos):
                    room_id=text_input2
                    name = text_input1
                    print("Asdsad")
                    break
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
        if (room_id != "" and name != ""):
            break
        screen.blit(background_image, (0, 0))

        pygame.draw.rect(screen, (200,200,200), input_rect1)
        pygame.draw.rect(screen, input_color1, input_rect1, 2)
        text_surface = font.render(text_input1, True, WHITE)
        screen.blit(text_surface, (input_rect1.x + 5, input_rect1.y + 5))

        name_surface = font.render('Name:', True, BLACK)
        name_rect = name_surface.get_rect(midleft=(input_rect1.left - 70, input_rect1.centery))
        screen.blit(name_surface, name_rect)

        pygame.draw.rect(screen,(200,200,200) , input_rect2)
        pygame.draw.rect(screen, input_color2, input_rect2, 2)
        text_surface = font.render(text_input2, True, WHITE)
        screen.blit(text_surface, (input_rect2.x + 5, input_rect2.y + 5))

        name_surface1 = font.render('Id Table:', True, BLACK)
        name_rect1 = name_surface.get_rect(midleft=(input_rect2.left - 95, input_rect2.centery))
        screen.blit(name_surface1, name_rect1)

        name_surface1 = font.render('START', True, BLACK)
        name_rect1 = name_surface.get_rect(midleft=(Enter_rect.left+50 , Enter_rect.centery))
        pygame.draw.rect(screen, hover_Color, Enter_rect)
        screen.blit(name_surface1, name_rect1)
        # Update the display
        pygame.display.flip()
    # Connect and join the room


    pygame.quit()
    if (room_id != "" and name != ""):
        con = connect_and_join(room_id, name)
    con.close()

    # Close the socket when done
