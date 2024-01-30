import pygame
import random

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

move_input = False
move_text_constant = "You played:"
move_text = ""
result_text = ""
player_move = -1
score = [0, 0]

def play_RPS(player_move):
    move_list = [0, 1, 2]
    computer_move = random.choice(move_list)

    if(computer_move == 0):
        return 0 #tie
    elif(computer_move == 1):
        return -1 #loss
    else:
        return 1 #win

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if (abs(pos[0] - centers[0][0]) < CIRC_RADIUS and abs(pos[1] - centers[0][1]) < CIRC_RADIUS):
                move_text = "Rock"
                player_move = 1
            if (abs(pos[0] - centers[1][0]) < CIRC_RADIUS and abs(pos[1] - centers[1][1]) < CIRC_RADIUS):
                move_text = "Paper"
                player_move = 2
            if (abs(pos[0] - centers[2][0]) < CIRC_RADIUS and abs(pos[1] - centers[2][1]) < CIRC_RADIUS):
                move_text = "Scissors"
                player_move = 3
    
    if (player_move != -1):
        result = play_RPS(player_move)
        if (result == -1):
            result_text = "lost!"
            score[1] += 1
        elif (result == 0):
            result_text = "tied!"
        else:
            result_text = "won!"
            score[0] += 1
        player_move = -1

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
    text_score = font.render("You " + str(score[0]) + " - " + str(score[1]) + " Opponent", True, BLACK, WHITE)
    text_result = font.render("You " + result_text, True, BLACK, WHITE)
    text_rect_score = text_score.get_rect()
    text_rect_result = text_result.get_rect()
    text_rect_score.center = centers[5]
    text_rect_result.center = centers[6]
    screen.blit(text_score, text_rect_score)
    screen.blit(text_result, text_rect_result)
    
    

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()