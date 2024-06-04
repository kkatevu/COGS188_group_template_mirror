from engine import Game, Player
# setting up pygame
import pygame 

pygame.init()
pygame.font.init()
pygame.display.set_caption('Battleship')
font = pygame.font.SysFont("fresansttf", 100)
# global variables 
SQ_SIZE = 25
H_MARGIN = SQ_SIZE *4
V_MARGIN = SQ_SIZE
WIDTH = SQ_SIZE * 15 * 2 + H_MARGIN
HEIGHT = SQ_SIZE * 15 * 2 + V_MARGIN
INDENT = 5
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
HUMAN1 = True
HUMAN2 = True

#colors
GREY = (40,50,60)
WHITE = (255, 250, 250)
GREEN = (50, 200, 150)
BLUE = (50, 150, 250)
RED = (250, 50, 100)
PINK = (250, 140, 220)
COLORS = {"U": GREY, "M": BLUE, "H": PINK, "S": RED}

# function to draw grid
def draw_grid(player, left = 0, top = 0, search = False):
    for i in range (225):
        x = left + i % 15 * SQ_SIZE
        y = top + i // 15 * SQ_SIZE
        square = pygame.Rect(x,y, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(SCREEN, WHITE, square, width = 3)
        if search:
            x += SQ_SIZE // 2
            y += SQ_SIZE //2
            pygame.draw.circle(SCREEN, COLORS[player.search[i]], (x,y), radius = SQ_SIZE//4)
#function to draw ships onto the postiion grids
def draw_ships(player, left = 0, top = 0):
    for ship in player.ships:
        x = left + ship.col * SQ_SIZE + INDENT
        y = top + ship.row * SQ_SIZE + INDENT
        if ship.orientation == "h":
            width = ship.size *SQ_SIZE -  2*INDENT
            height = SQ_SIZE - 2*INDENT
        else:
            width = SQ_SIZE - 2*INDENT
            height = ship.size * SQ_SIZE - 2*INDENT
        rectangle = pygame.Rect(x,y, width, height)
        pygame.draw.rect(SCREEN, GREEN, rectangle, border_radius = 15)
game = Game(HUMAN1, HUMAN2)
#pygame loop
animating = True 
pausing = False
while animating:
    #track user interaction
    for event in pygame.event.get():
        #user closes the pygame window
        if event.type == pygame.QUIT:
            animating = False
        
        #user cicks on mouse
        if event.type == pygame.MOUSEBUTTONDOWN and not game.over:
            x,y = pygame.mouse.get_pos()
        
            if game.player1_turn and x < SQ_SIZE * 15 and y < SQ_SIZE*15:
                row = y // SQ_SIZE
                col = x // SQ_SIZE
                index = row*15 +col
                game.make_move(index)  
            elif not game.player1_turn and x > WIDTH - SQ_SIZE*15 and y > SQ_SIZE*15 + V_MARGIN:
                row = (y - 400) // SQ_SIZE
                col = (x - (WIDTH - SQ_SIZE *15))//SQ_SIZE
                index = row*15 +col
                game.make_move(index)
                
        #user presses key on keyboard
        if event.type == pygame.KEYDOWN:
            
            #escape key to close the animation
            if event.key == pygame.K_ESCAPE:
                animating = False

            #space bar to pause and unpause the animation
            if event.key == pygame.K_SPACE:
                pausing = not pausing
            
            #return key to restart game
            if event.key == pygame.K_RETURN:
                game = Game(HUMAN1, HUMAN2) 

    #execution
    if not pausing:
        SCREEN.fill(GREY)
        draw_grid(game.player1, search = True)
        draw_grid(game.player2,search = True, left = (WIDTH-H_MARGIN)//2 +H_MARGIN, top = 400)
        
        draw_grid(game.player2, left = (WIDTH-H_MARGIN)//2 +H_MARGIN, top = 0)
        draw_grid(game.player1, left = 0, top = 400)

        #draw ships onto position grids
        draw_ships(game.player1, top = 400)
        draw_ships(game.player2, left = (WIDTH-H_MARGIN)//2 +H_MARGIN,)
        
        #computer moves randombot
        if not game.over and game.computer_turn:
            if game.player1_turn:
                game.q_learning_epsilon()
            else:
                game.q_learning_policy()
        
        #game over message 
        if game.over:
            text = "Player " +str(game.result) + " wins!!"
            textbox = font.render(text, False, GREY, WHITE)
            SCREEN.blit(textbox, (WIDTH//2 -240, HEIGHT//2 -50))
        #update screen
        pygame.time.delay(20)
        pygame.display.flip()
