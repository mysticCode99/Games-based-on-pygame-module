#!/usr/bin/python3.8

import pygame


def defineWindow():
    '''Defines default params'''
    pygame.font.init()
    global WIDTH
    WIDTH = 800
    global HEIGHT
    HEIGHT = 1000
    global STATE
    STATE = ['-']*9

    global SCREEN
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

    global PLAYGROUND_HEIGHT
    PLAYGROUND_HEIGHT = 800
    global PLAYGROUND_WIDTH
    PLAYGROUND_WIDTH = 800

    global STATISTIC
    STATISTIC = {
        'X' : 0,
        'O' : 0,
        'draw' : 0,
        'matches' : 0
    }

def drawDash():
    '''
    Drawing dash for game
    '''
    SCREEN.fill((108, 36, 106))
    global SQUARE_LENGTH
    SQUARE_LENGTH = PLAYGROUND_WIDTH//3
    pygame.draw.line(
        surface=SCREEN,
        color='BLACK',
        start_pos=(SQUARE_LENGTH, 0),
        end_pos=(SQUARE_LENGTH, PLAYGROUND_HEIGHT),
        width=5
    )
    pygame.draw.line(
        surface=SCREEN,
        color='BLACK',
        start_pos=(2*SQUARE_LENGTH, 0),
        end_pos=(2*SQUARE_LENGTH, PLAYGROUND_HEIGHT),
        width=5
    )

    global SQUARE_HEIGHT
    SQUARE_HEIGHT = PLAYGROUND_HEIGHT//3
    pygame.draw.line(
        surface=SCREEN,
        color='BLACK',
        start_pos=(0, SQUARE_HEIGHT),
        end_pos=(PLAYGROUND_WIDTH, SQUARE_HEIGHT),
        width=5
    )
    pygame.draw.line(
        surface=SCREEN,
        color='BLACK',
        start_pos=(0, 2*SQUARE_HEIGHT),
        end_pos=(WIDTH, 2*SQUARE_HEIGHT),
        width=5
    )

    pygame.draw.lines(
        surface=SCREEN,
        color='BLACK',
        closed=True,
        points=(
                (0, 0),
                (0, PLAYGROUND_HEIGHT),
                (PLAYGROUND_WIDTH, PLAYGROUND_HEIGHT),
                (PLAYGROUND_WIDTH, 0)
            ),
        width=5
    )
    global XBORDER
    XBORDER = SQUARE_LENGTH*3-1
    global YBORDER
    YBORDER = SQUARE_HEIGHT*3-1

    printInfo()
    STATISTIC['matches'] += 1

def printInfo():
    '''Prints information in window'''
    txt_box = (
        (0, PLAYGROUND_HEIGHT),
        (WIDTH, PLAYGROUND_HEIGHT),
        (WIDTH, PLAYGROUND_HEIGHT+100),
        (0, PLAYGROUND_HEIGHT+100),
        (WIDTH, PLAYGROUND_HEIGHT+100),
        (WIDTH, HEIGHT),
        (0, HEIGHT)
    )
    
    pygame.draw.lines(
        surface=SCREEN,
        color='BLACK',
        points=txt_box,
        closed=True,
        width=5
    )

    fontName = pygame.font.get_default_font()
    fontSize = (HEIGHT - PLAYGROUND_HEIGHT)//4  # 50
    font = pygame.font.SysFont(fontName, fontSize)
    text_1 = f"X : {STATISTIC['X']} | O : {STATISTIC['O']}"
    text_2 = f"Matches : {STATISTIC['matches']} | Draw count : {STATISTIC['draw']} | for restart press R"
    i = 0
    area_height = (HEIGHT - PLAYGROUND_HEIGHT)/2
    for text in (text_1, text_2):
        txt = font.render(text, True, (0, 0, 0))
        txt_x = (WIDTH - txt.get_width())/2
        txt_y = PLAYGROUND_HEIGHT + (area_height-txt.get_height())/2 + i*area_height
        i += 1
        SCREEN.blit(txt, (txt_x, txt_y))

def drawO(x, y):
    '''
    Drawing circle
    '''
    center_x = x*SQUARE_LENGTH+SQUARE_LENGTH/2
    center_y = y*SQUARE_HEIGHT+SQUARE_HEIGHT/2
    radius = SQUARE_HEIGHT/2 - 5
    pygame.draw.circle(
        surface=SCREEN, 
        color=(123, 234, 0),
        center=(center_x, center_y), 
        radius=radius, 
        width=5
    )

def drawX(x, y):
    '''
    Drawing X sign
    '''
    color = (255, 0, 0)
    pygame.draw.line(
        surface=SCREEN,
        color=color,
        start_pos=(x*SQUARE_LENGTH+3, y*SQUARE_HEIGHT+3),
        end_pos=((x+1)*SQUARE_LENGTH-3, (y+1)*SQUARE_HEIGHT-3),
        width=5
    )
    pygame.draw.line(
        surface=SCREEN,
        color=color,
        start_pos=(x*SQUARE_LENGTH+3, (y+1)*SQUARE_HEIGHT-3),
        end_pos=((x+1)*SQUARE_LENGTH-3, y*SQUARE_HEIGHT+3),
        width=5
    )

def doStep(turn):
    '''
    Calculating and adding moves in main list
    '''
    global STATE
    x, y = pygame.mouse.get_pos()
    if x > XBORDER:
        x = XBORDER
    if y > YBORDER:
        y = YBORDER

    index = y//SQUARE_HEIGHT*3 + x//SQUARE_LENGTH
    if STATE[index] != '-':
        print('Select another square')
        return turn
    
    if turn % 2 == 1:
        figure = 'X'
        drawX(x//SQUARE_LENGTH, y//SQUARE_HEIGHT)
    else:
        figure = 'O'
        drawO(x//SQUARE_LENGTH, y//SQUARE_HEIGHT)
    STATE[index] = figure

    turn += 1
    return turn

def checkState(turn):
    '''
    Checking state and return winner or draw
    '''
    global STATE
    winner = ''

    # checks rows and colums
    for i in range(0, 3):
        # checks if 
        # horizontal line not used 
        # pass horizontal line
        if STATE[i*3] == '-':
            pass
        # checks horizontal ( rows )
        elif STATE[i*3]==STATE[i*3+1]==STATE[i*3+2]:
            winner = STATE[i*3]
            break
        # checks if 
        # vertical line not used 
        # pass vertical line
        if STATE[i] == '-':
            pass
        # checks vertical ( colums )
        elif STATE[i]==STATE[i+3]==STATE[i+6]:
            winner = STATE[i]
            # + ' vertical wins'
            break
    
    # checks diaganals
    if STATE[4] == '-':
        pass
    elif STATE[0]==STATE[4]==STATE[8]:
        winner = STATE[4]
        # + ' diagnal wins'
    elif STATE[2]==STATE[4]==STATE[6]:
        winner = STATE[4]
        # + '-diagnal wins'
    
    
    # checks if winner found
    # updates playground
    if winner:
        STATISTIC[winner] += 1
        winner = ''
        STATE = ['-']*9
        drawDash()
        return 0
    
    # checks if aren't winner and 
    # all squares are used 
    # updates playground
    if turn >= 9:
        STATISTIC['draw'] += 1
        STATE = ['-']*9
        drawDash()
        return 0
    
    return turn


def gameLoop():
    running = True
    turn = 0
    drawDash()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif pygame.mouse.get_pressed()[0]:
                turn = doStep(turn)
                turn = checkState(turn)
                pygame.event.wait(1000)
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                drawDash()
                global STATE
                STATE = ['-']*9
        pygame.display.update()

def main():
    defineWindow()
    gameLoop()

if __name__ == '__main__':
    main()