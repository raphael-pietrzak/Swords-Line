import os, socket, json, pygame, sys, time
from classes.settings import *
# from network.ping import *


counter = 0
start_time = time.time()

def ping():
    global counter, start_time
    counter += 1
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time >= 1.0:
        rps = counter / elapsed_time
        print(f"Réceptions par seconde : {rps:.2f}")
        counter = 0
        start_time = current_time


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, PORT))

pygame.init()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SERVER CONSOLE")

while True:

    data, addr = server_socket.recvfrom(BUFFER_SIZE)
    received_data = json.loads(data.decode())
    # print(f"{received_data['players'][0]['position']}, {received_data['players'][1]['position']}")
    ping()  


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    display_surface.fill('aquamarine')

    pygame.draw.circle(display_surface, RED_PLAYER, received_data['players'][0]['position'], 10)
    pygame.draw.circle(display_surface, BLUE_PLAYER, received_data['players'][1]['position'], 10)

    pygame.display.update()
