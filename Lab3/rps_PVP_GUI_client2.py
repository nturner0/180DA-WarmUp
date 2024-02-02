import pygame
import paho.mqtt.client as mqtt

#define MQTT functions

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/test/ahh/server2", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")
                
def on_message(client, userdata, message):
    global my_wins
    global opp_wins
    global result_text
    global sent_move
    sent_move = False

    payload = message.payload.decode()

    if (payload == '0'):
        result_text = "tied!"
    elif (payload == '2'):
        my_wins += 1
        result_text = "won!"
    else:
        opp_wins += 1
        result_text = "lost!"

#create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect_async("mqtt.eclipseprojects.io")
client.loop_start()

pygame.init()

#Define constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

CIRC_RADIUS = 50

#Calculate circle and text center locations
blank = (WINDOW_WIDTH - 6*CIRC_RADIUS) // 4

centers = []
for i in range(1, 4):
    centers.append(((i*blank + (2*i-1)*CIRC_RADIUS), WINDOW_HEIGHT//2))
#Your move text center
centers.append(((1*blank + (1*2-1)*CIRC_RADIUS), WINDOW_HEIGHT//1.2))
centers.append(((2*blank + (2*2-1)*CIRC_RADIUS)*1.1, WINDOW_HEIGHT//1.2))

#Score text
centers.append(((2*blank + (2*2-1)*CIRC_RADIUS), WINDOW_HEIGHT//5))
#Result text
centers.append(((2*blank + (2*2-1)*CIRC_RADIUS), WINDOW_HEIGHT//3))

#Color definitions
GREEN = (61, 168, 89)
PURPLE = (63, 54, 107)
ORANGE = (161, 119, 21)
BLUE = (0, 0, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CIRC_COLORS = [GREEN, PURPLE, ORANGE]

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

#globals
my_wins = 0
opp_wins = 0

sent_move = False
move_input = False
move_text_constant = "You played:"
move_text = ""
result_text = ""
sent_move = False

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if (sent_move):  #already moved, waiting for opponent
                continue
            pos = pygame.mouse.get_pos()
            if (abs(pos[0] - centers[0][0]) < CIRC_RADIUS and abs(pos[1] - centers[0][1]) < CIRC_RADIUS):
                move_text = "Rock"
                sent_move = True
                client.publish("ece180d/test/ahh/client2", '2r', qos=1)
            if (abs(pos[0] - centers[1][0]) < CIRC_RADIUS and abs(pos[1] - centers[1][1]) < CIRC_RADIUS):
                move_text = "Paper"
                sent_move = True
                client.publish("ece180d/test/ahh/client2", '2p', qos=1)
            if (abs(pos[0] - centers[2][0]) < CIRC_RADIUS and abs(pos[1] - centers[2][1]) < CIRC_RADIUS):
                move_text = "Scissors"
                sent_move = True
                client.publish("ece180d/test/ahh/client2", '2s', qos=1)

    # Fill the background with white
    screen.fill(WHITE)

    # Draw input circles
    
    for i in range(3):
        pygame.draw.circle(screen, CIRC_COLORS[i], centers[i], CIRC_RADIUS)

    #fonts
    font = pygame.font.Font('freesansbold.ttf', 20)
    font_big = pygame.font.Font('freesansbold.ttf', 32)

    #Circles
    text_r = font.render('Rock', True, BLACK, GREEN)
    text_p = font.render('Paper', True, BLACK, PURPLE)
    text_s = font.render('Scissors', True, BLACK, ORANGE)
    text_rect_r = text_r.get_rect()
    text_rect_p = text_p.get_rect()
    text_rect_s = text_s.get_rect()
    text_rect_r.center = centers[0]
    text_rect_p.center = centers[1]
    text_rect_s.center = centers[2]
    screen.blit(text_r, text_rect_r)
    screen.blit(text_p, text_rect_p)
    screen.blit(text_s, text_rect_s)

    #Player move info
    text_move_constant = font_big.render(move_text_constant, True, BLACK, WHITE)
    text_move = font_big.render(move_text, True, BLACK, WHITE)
    text_rect_move_constant = text_move_constant.get_rect()
    text_rect_move = text_move.get_rect()
    text_rect_move_constant.center = centers[3]
    text_rect_move.center = centers[4]
    screen.blit(text_move_constant, text_rect_move_constant)
    screen.blit(text_move, text_rect_move)

    #Score info
    text_score = font.render("You " + str(my_wins) + " - " + str(opp_wins) + " Opponent", True, BLACK, WHITE)
    text_result = font.render("You " + result_text, True, BLACK, WHITE)
    text_rect_score = text_score.get_rect()
    text_rect_result = text_result.get_rect()
    text_rect_score.center = centers[5]
    text_rect_result.center = centers[6]
    screen.blit(text_score, text_rect_score)
    screen.blit(text_result, text_rect_result)
    
    
    pygame.display.flip()


#Send a quit message to server
client.publish("ece180d/test/ahh/client2", '2q', qos=1)

#Close everything
pygame.quit()
client.loop_stop()
client.disconnect()