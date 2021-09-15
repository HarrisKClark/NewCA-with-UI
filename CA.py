import copy
import pygame
import random
import pyperclip as pc

pygame.init()

WIDTH = 1300
SIMWIDTH = WIDTH - 300
HEIGHT = 800
FPS = 60
CELLSIZE = 6

font = pygame.font.Font('freesansbold.ttf',17)
font2 = pygame.font.Font('freesansbold.ttf',32)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test GoL")

class UserInterface:
    def __init__(self, rule_set):
        self.x = WIDTH-300
        self.color1 = (150,150,150)
        self.color2 = (100, 100, 100)

        self.genX, self.genY = WIDTH-290,10
        self.statusX, self.statusY = WIDTH - 290, 40
        self.ruleX, self.ruleY = WIDTH - 290, 70
        self.pauseX, self.pauseY = 0, 0
        self.button_clearX, self.button_clearY = WIDTH - 285, 160
        self.button_new_seedX, self.button_new_seedY = WIDTH - 285, 200
        self.button_copyX, self.button_copyY = WIDTH - 285, 240

        self.ruleset = rule_set

        self.clear = False
        self.random = False
        self.deadGen = 0
        self.checkDead = True
        self.copy = False
        self.button_clear_hover = False

    def draw(self, step, paused, dead):
        pygame.draw.rect(WIN, self.color1, (self.x, 0, 300, HEIGHT))
        pygame.draw.rect(WIN, self.color2, (self.x, 0, 5, HEIGHT))
        pygame.draw.rect(WIN, self.color2, (self.button_clearX-5, self.button_clearY-5, 90, 30))
        pygame.draw.rect(WIN, self.color2, (self.button_new_seedX - 5, self.button_new_seedY - 5, 90, 30))
        pygame.draw.rect(WIN, self.color2, (self.button_copyX - 5, self.button_copyY - 5, 90, 30))

        generation = font.render("generation: " + str(step), True, (0, 0, 0))
        rule = font.render("Ruleset: " + str(self.ruleset), True, (0, 0, 0))
        button_clear = font.render("Clear", True, (0, 0, 0))
        button_new_seed = font.render("New Seed", True, (0, 0, 0))
        button_copy = font.render("Copy", True, (0, 0, 0))

        if dead:
            if self.checkDead:
                self.deadGen = step
                self.checkDead = False
            status = font.render("Status: Dead (gen "+str(self.deadGen)+")", True, (0, 0, 0))
        else:
            self.checkDead = True
            status = font.render("Status: Alive", True, (0, 0, 0))

        if paused:
            pause = font2.render("Paused", True, (75, 75, 200))
        else:
            pause = font2.render("", True, (75, 75, 200))

        WIN.blit(generation, (self.genX, self.genY))
        WIN.blit(status, (self.statusX, self.statusY))
        WIN.blit(rule, (self.ruleX, self.ruleY))
        WIN.blit(pause, (self.pauseX, self.pauseY))
        WIN.blit(button_clear, (self.button_clearX, self.button_clearY))
        WIN.blit(button_new_seed, (self.button_new_seedX, self.button_new_seedY))
        WIN.blit(button_copy, (self.button_copyX, self.button_copyY))

    def buttonPress(self,x,y,click2):
        if (x > self.button_clearX-5) and (x < self.button_clearX+50):
            if (y > self.button_clearY-5) and (y < self.button_clearX+25):
                self.clear = True

        if (x > self.button_new_seedX-5) and (x < self.button_new_seedX+85) and click2:
            if (y > self.button_new_seedY-5) and (y < self.button_new_seedY+25):
                self.random = True

        if (x > self.button_copyX-5) and (x < self.button_copyX+85):
            if (y > self.button_copyY-5) and (y < self.button_copyY+25):
                self.copy = True


def draw_cells(cells):
    color = (250, 250, 250)
    for i in range(len(cells)):
        for j in range(len(cells[0])):
            if cells[i][j] == 1:
                x = i * CELLSIZE
                y = j * CELLSIZE
                pygame.draw.rect(WIN, color, (x, y, CELLSIZE, CELLSIZE))


def draw_grid():

    color = (0, 0, 0)

    for i in range(HEIGHT // CELLSIZE):
        pygame.draw.line(WIN, color, (0, i * CELLSIZE), (SIMWIDTH, i * CELLSIZE))
    for i in range(SIMWIDTH // CELLSIZE):
        pygame.draw.line(WIN, color, (i * CELLSIZE, 0), (i * CELLSIZE, HEIGHT))


def add_cell(x, y, cells, click, right_click):
    try:
        if click and x <= SIMWIDTH:
            cells[x // CELLSIZE][y // CELLSIZE] = 1
        elif right_click and x <= SIMWIDTH:
            cells[x // CELLSIZE][y // CELLSIZE] = 0
    except IndexError:
        pass

    return cells


def count_alive(cells, x, y):
    return cells[x-1][y+1] + cells[x][y+1] + cells[x+1][y+1] + cells[x-1][y] + cells[x+1][y] + cells[x-1][y-1] + cells[x][y-1] + cells[x+1][y-1]
#[0, 1, 2, 3, 2, 3, 2, 2, 2]

def update_cells(cells,rule_set,dead):
    new_cells = copy.deepcopy(cells)
    checked = False

    for i in range(0, len(cells) - 1):
        for j in range(0, len(cells[0]) - 1):
            alive = count_alive(cells, i, j)
            if rule_set[alive] == 1 :
                new_cells[i][j] = 0
                if not checked and (cells[i][j] != 0):
                    dead = False
                    checked = True
            elif rule_set[alive] == 2:
                new_cells[i][j] = 1
                if not checked and (cells[i][j] != 1):
                    dead = False
                    checked = True

    if not checked:
        dead = True

    return new_cells,dead


def update(x, y, cells, click, right_click,rule_set,paused,UI,step,dead,click2):
    if click or right_click:
        cells = add_cell(x, y, cells, click, right_click)
        UI.buttonPress(x,y,click2)

    if UI.clear == True:
        cells = [[0 for j in range(0, (HEIGHT // CELLSIZE))] for i in range(0, (SIMWIDTH // CELLSIZE))]
        UI.clear = False

    if UI.random == True:
        paused = True

        cells = [[0 for j in range(0, (HEIGHT // CELLSIZE))] for i in range(0, (SIMWIDTH // CELLSIZE))]
        rule_set = []
        for i in range(9):
            rule_set.append(random.randint(1, 2))
        UI.ruleset = rule_set
        UI.random = False
        step = 0
        dead = True

    if UI.copy == True:
        pc.copy(str(rule_set))
        UI.copy == False

    if not paused:
        cells, dead = update_cells(cells,rule_set,dead)
        step += 1

    WIN.fill((0, 0, 0))
    draw_cells(cells)

    draw_grid()
    UI.draw(step,paused, dead)

    if dead:
        step = -1

    return cells, step, dead,rule_set,paused


def main():
    clock = pygame.time.Clock()

    run = True
    click = False
    right_click = False
    paused = True
    step = 0
    rule_set = [0]
    dead = False
    waiting = False

    for i in range(9):
        rule_set.append(random.randint(1,2))
    rule_set =[1, 2, 2, 1, 1, 3, 2, 2, 1, 1]
    print(rule_set)

    #[0, 0, 0, 2, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 2, 2, 1, 0, 1, 1, 2, 1, 2, 2, 0, 2, 1, 2, 0, 2, 1]
    #[1, 2, 3, 3, 1, 1, 3, 1, 3, 2]

    cells = [[0 for j in range(0, (HEIGHT // CELLSIZE))] for i in range(0, (SIMWIDTH // CELLSIZE))]

    UI = UserInterface(rule_set)

    while run:
        x, y = pygame.mouse.get_pos()
        clock.tick(FPS)
        pressed = pygame.key.get_pressed()
        click2 = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP) and event.button == 3:
                if right_click:
                    right_click = False
                else:
                    right_click = True
            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP) and event.button == 1:
                if click:
                    click = False
                else:
                    click = True
            if (event.type == pygame.MOUSEBUTTONDOWN) and event.button == 1:
                if not waiting:
                    click2 = True
                    waiting = True
            if (event.type == pygame.MOUSEBUTTONUP) and event.button == 1:
                waiting = False

            if event.type == pygame.KEYUP:
                if pressed[pygame.K_SPACE]:
                    if not paused:
                        paused = True
                    else:
                        paused = False

        cells, step, dead, rule_set, paused = update(x, y, cells, click, right_click,rule_set,paused,UI,step,dead,click2)

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
