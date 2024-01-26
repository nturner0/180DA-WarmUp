# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

#Define constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

CIRC_RADIUS = 50

#Color definitions
BLUE = (0, 0, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if (abs(pos[0] - centers[0][0]) < CIRC_RADIUS and abs(pos[1] - centers[0][1]) < CIRC_RADIUS):
                print("Rock")
            if (abs(pos[0] - centers[1][0]) < CIRC_RADIUS and abs(pos[1] - centers[1][1]) < CIRC_RADIUS):
                print("Paper")
            if (abs(pos[0] - centers[2][0]) < CIRC_RADIUS and abs(pos[1] - centers[2][1]) < CIRC_RADIUS):
                print("Scissors")

    # Fill the background with white
    screen.fill(WHITE)

    # Draw input circles

    blank = (WINDOW_WIDTH - 6*CIRC_RADIUS) // 4

    centers = []
    for i in range(1, 4):
        centers.append(((i*blank + (2*i-1)*CIRC_RADIUS), WINDOW_HEIGHT//2))
    
    for i in range(3):
        pygame.draw.circle(screen, BLUE, centers[i], CIRC_RADIUS)

    font = pygame.font.Font('freesansbold.ttf', 20)

    text_r = font.render('Rock', True, BLACK, BLUE)
    text_p = font.render('Paper', True, BLACK, BLUE)
    text_s = font.render('Scissors', True, BLACK, BLUE)

    text_rect_r = text_r.get_rect()
    text_rect_p = text_p.get_rect()
    text_rect_s = text_s.get_rect()
    
    text_rect_r.center = centers[0]
    text_rect_p.center = centers[1]
    text_rect_s.center = centers[2]

    screen.blit(text_r, text_rect_r)
    screen.blit(text_p, text_rect_p)
    screen.blit(text_s, text_rect_s)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()