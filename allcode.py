from collections import deque, namedtuple
import random
import pygame
from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w

from random import randint

import pygame

from numpy import sqrt
from scoreFenetre import *
import os


BOARD_LENGTH = 32
OFFSET = 16
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)

DIRECTIONS = namedtuple('DIRECTIONS',
                        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)


def rand_color():
    return (random.randrange(254) | 64, random.randrange(254) | 64, random.randrange(254) | 64)


class Snake(object):
    def __init__(self, direction=DIRECTIONS.Right,
                 point=(0, 0, rand_color()), color=None):
        self.tailmax = 1
        self.direction = direction
        self.deque = deque()
        self.deque.append(point)
        self.color = color
        self.nextDir = deque()

    def get_color(self):
        if self.color is None:
            return rand_color()
        else:
            return self.color

    def populate_nextDir(self, events, identifier):
        if (identifier == "arrows"):
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.nextDir.appendleft(DIRECTIONS.Up)
                    elif event.key == pygame.K_DOWN:
                        self.nextDir.appendleft(DIRECTIONS.Down)
                    elif event.key == pygame.K_RIGHT:
                        self.nextDir.appendleft(DIRECTIONS.Right)
                    elif event.key == pygame.K_LEFT:
                        self.nextDir.appendleft(DIRECTIONS.Left)
        if (identifier == "wasd"):
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.nextDir.appendleft(DIRECTIONS.Up)
                    elif event.key == pygame.K_s:
                        self.nextDir.appendleft(DIRECTIONS.Down)
                    elif event.key == pygame.K_d:
                        self.nextDir.appendleft(DIRECTIONS.Right)
                    elif event.key == pygame.K_a:
                        self.nextDir.appendleft(DIRECTIONS.Left)


def find_food(spots):
    while True:
        food = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
        if (not (spots[food[0]][food[1]] == 1 or
                 spots[food[0]][food[1]] == 2)):
            break
    return food


def end_condition(board, coord):
    if (coord[0] < 0 or coord[0] >= BOARD_LENGTH or coord[1] < 0 or
            coord[1] >= BOARD_LENGTH):
        return True
    if (board[coord[0]][coord[1]] == 1):
        return True
    return False


def make_board():
    spots = [[] for i in range(BOARD_LENGTH)]
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
    return spots


def update_board(screen, snakes, food):
    rect = pygame.Rect(0, 0, OFFSET, OFFSET)

    spots = [[] for i in range(BOARD_LENGTH)]
    num1 = 0
    num2 = 0
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
            temprect = rect.move(num1 * OFFSET, num2 * OFFSET)
            pygame.draw.rect(screen, BLACK, temprect)
            num2 += 1
        num1 += 1
    spots[food[0]][food[1]] = 2
    temprect = rect.move(food[1] * OFFSET, food[0] * OFFSET)
    pygame.draw.rect(screen, RED, temprect)
    for snake in snakes:
        for coord in snake.deque:
            spots[coord[0]][coord[1]] = 1
            temprect = rect.move(coord[1] * OFFSET, coord[0] * OFFSET)
            pygame.draw.rect(screen, coord[2], temprect)
    return spots


def get_color(s):
    if s == "bk":
        return BLACK
    elif s == "wh":
        return WHITE
    elif s == "rd":
        return RED
    elif s == "bl":
        return BLUE
    elif s == "fo":
        return rand_color()
    else:
        print("WHAT", s)
        return BLUE


def update_board_delta(screen, deltas):
    # accepts a queue of deltas in the form
    # [("d", 13, 30), ("a", 4, 6, "rd")]
    # valid colors: re, wh, bk, bl
    rect = pygame.Rect(0, 0, OFFSET, OFFSET)
    change_list = []
    delqueue = deque()
    addqueue = deque()
    while len(deltas) != 0:
        d = deltas.pop()
        change_list.append(pygame.Rect(d[1], d[2], OFFSET, OFFSET))
        if d[0] == "d":
            delqueue.append((d[1], d[2]))
        elif d[0] == "a":
            addqueue.append((d[1], d[2], get_color(d[3])))

    for d_coord in delqueue:
        temprect = rect.move(d_coord[1] * OFFSET, d_coord[0] * OFFSET)
        # TODO generalize background color
        pygame.draw.rect(screen, BLACK, temprect)

    for a_coord in addqueue:
        temprect = rect.move(a_coord[1] * OFFSET, a_coord[0] * OFFSET)
        pygame.draw.rect(screen, a_coord[2], temprect)

    return change_list


# Return 0 to exit the program, 1 for a one-player game
def menu(screen):
    font = pygame.font.Font(None, 30)
    menu_message1 = font.render("Press enter for one-player, t for two-player", True, WHITE)
    menu_message2 = font.render("Red is first player, blue is second player", True, WHITE)
    menu_message3 = font.render("Press b for AI BOT TO PLAY THE GAME FOR YOU ", True, WHITE)
    screen.fill(BLACK)
    screen.blit(menu_message1, (32, 32))
    screen.blit(menu_message2, (32, 64))
    screen.blit(menu_message3, (32, 96))
    pygame.display.update()
    while True:
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 1
                if event.key == pygame.K_t:
                    return 2
                if event.key == pygame.K_b:
                    return 3
                if event.key == pygame.K_n:
                    return 4
        if done:
            break
    if done:
        pygame.quit()
        return 0


def quit(screen):
    return False


def move(snake):
    if len(snake.nextDir) != 0:
        next_dir = snake.nextDir.pop()
    else:
        next_dir = snake.direction
    head = snake.deque.pop()
    snake.deque.append(head)
    next_move = head
    if (next_dir == DIRECTIONS.Up):
        if snake.direction != DIRECTIONS.Down:
            next_move = (head[0] - 1, head[1], snake.get_color())
            snake.direction = next_dir
        else:
            next_move = (head[0] + 1, head[1], snake.get_color())
    elif (next_dir == DIRECTIONS.Down):
        if snake.direction != DIRECTIONS.Up:
            next_move = (head[0] + 1, head[1], snake.get_color())
            snake.direction = next_dir
        else:
            next_move = (head[0] - 1, head[1], snake.get_color())
    elif (next_dir == DIRECTIONS.Left):
        if snake.direction != DIRECTIONS.Right:
            next_move = (head[0], head[1] - 1, snake.get_color())
            snake.direction = next_dir
        else:
            next_move = (head[0], head[1] + 1, snake.get_color())
    elif (next_dir == DIRECTIONS.Right):
        if snake.direction != DIRECTIONS.Left:
            next_move = (head[0], head[1] + 1, snake.get_color())
            snake.direction = next_dir
        else:
            next_move = (head[0], head[1] - 1, snake.get_color())
    return next_move


def is_food(board, point):
    return board[point[0]][point[1]] == 2


# Return false to quit program, true to go to
# gameover screen
def one_player(screen):
    clock = pygame.time.Clock()
    spots = make_board()

    snake = Snake()
    # Board set up
    spots[0][0] = 1
    food = find_food(spots)

    while True:
        clock.tick(15)
        # Event processing

        done = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                print("Quit given")
                done = True
                break
        if done:
            return False

        snake.populate_nextDir(events, "arrows")

        # Game logic
        next_head = move(snake)
        if (end_condition(spots, next_head)):
            return snake.tailmax

        if is_food(spots, next_head):
            snake.tailmax += 1
            food = find_food(spots)

        snake.deque.append(next_head)

        if len(snake.deque) > snake.tailmax:
            snake.deque.popleft()

        # Draw code
        screen.fill(BLACK)  # makes screen black

        spots = update_board(screen, [snake], food)

        pygame.display.update()


def two_player(screen):
    clock = pygame.time.Clock()
    spots = make_board()

    snakes = [Snake(DIRECTIONS.Right, (0, 0, RED), RED), Snake(DIRECTIONS.Right, (5, 5, BLUE), BLUE)]
    for snake in snakes:
        point = snake.deque.pop()
        spots[point[0]][point[1]] = 1
        snake.deque.append(point)
    food = find_food(spots)

    while True:
        clock.tick(15)
        done = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True
                break
        if done:
            return False
        snakes[0].populate_nextDir(events, "arrows")
        snakes[1].populate_nextDir(events, "wasd")

        for snake in snakes:
            next_head = move(snake)
            if (end_condition(spots, next_head)):
                return snake.tailmax

            if is_food(spots, next_head):
                snake.tailmax += 1
                food = find_food(spots)

            snake.deque.append(next_head)

            if len(snake.deque) > snake.tailmax:
                snake.deque.popleft()

        screen.fill(BLACK)

        spots = update_board(screen, snakes, food)

        pygame.display.update()



def game_over(screen, eaten):
    message1 = "You ate %d foods" % eaten
    app = QApplication(sys.argv)
    w = scoreFenetre("%d"% eaten)
    pygame.quit()
    sys.exit(app.exec_())

def SnakeAstar(screen ):

    done = False

    BLACK = (0, 0, 0)

    WHITE = (255, 255, 255)

    BLUE = (0, 0, 255)

    GREEN = (0, 255, 0)

    RED = (255, 0, 0)

    cols = 25

    rows = 25

    width = 500

    height = 500

    wr = width / cols

    hr = height / rows

    direction = 1
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = display.set_mode([width, height])

    display.set_caption("Snake Game")

    clock = time.Clock()

    def getpath(food1, snake1):

        food1.camefrom = []

        for s in snake1:
            s.camefrom = []

        openset = [snake1[-1]]

        closedset = []

        dir_array1 = []

        while 1:

            done = False
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print("Quit given")
                    done = True
                    break
            if done:
                return False

            current1 = min(openset, key=lambda x: x.f)

            openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]

            closedset.append(current1)

            for neighbor in current1.neighbors:

                if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:

                    tempg = neighbor.g + 1

                    if neighbor in openset:

                        if tempg < neighbor.g:
                            neighbor.g = tempg

                    else:

                        neighbor.g = tempg

                        openset.append(neighbor)


                    neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)

                    neighbor.f = neighbor.g + neighbor.h

                    neighbor.camefrom = current1

            if current1 == food1:
                break

        while current1.camefrom:

            if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:

                dir_array1.append(2)

            elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:

                dir_array1.append(0)

            elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:

                dir_array1.append(3)

            elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:

                dir_array1.append(1)

            current1 = current1.camefrom

        # print(dir_array1)

        for i in range(rows):

            for j in range(cols):
                grid[i][j].camefrom = []

                grid[i][j].f = 0

                grid[i][j].h = 0

                grid[i][j].g = 0

        return dir_array1

    class Spot:

        def __init__(self, x, y):

            self.x = x

            self.y = y

            self.f = 0

            self.g = 0

            self.h = 0

            self.neighbors = []

            self.camefrom = []

            self.obstrucle = False

            if randint(1, 101) < 3:
                self.obstrucle = True

        def show(self, color):

            draw.rect(screen, color, [self.x * hr + 2, self.y * wr + 2, hr - 4, wr - 4])

        def add_neighbors(self):

            if self.x > 0:
                self.neighbors.append(grid[self.x - 1][self.y])

            if self.y > 0:
                self.neighbors.append(grid[self.x][self.y - 1])

            if self.x < rows - 1:
                self.neighbors.append(grid[self.x + 1][self.y])

            if self.y < cols - 1:
                self.neighbors.append(grid[self.x][self.y + 1])

    grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]

    for i in range(rows):

        for j in range(cols):
            grid[i][j].add_neighbors()

    snake = [grid[round(rows / 2)][round(cols / 2)]]

    food = grid[randint(0, rows - 1)][randint(0, cols - 1)]

    current = snake[-1]

    dir_array = getpath(food, snake)


    food_array = [food]

    while not done:

        clock.tick(12)

        screen.fill(BLACK)

        direction = dir_array.pop(-1)

        if direction == 0:  # down

            snake.append(grid[current.x][current.y + 1])

        elif direction == 1:  # right

            snake.append(grid[current.x + 1][current.y])

        elif direction == 2:  # up

            snake.append(grid[current.x][current.y - 1])

        elif direction == 3:  # left

            snake.append(grid[current.x - 1][current.y])

        current = snake[-1]

        if current.x == food.x and current.y == food.y:

            while 1:

                food = grid[randint(0, rows - 1)][randint(0, cols - 1)]

                if not (food.obstrucle or food in snake):
                    break

            food_array.append(food)

            dir_array = getpath(food, snake)
            print('snake {0}'.format(dir_array))

        else:

            snake.pop(0)

        for spot in snake:
            spot.show(WHITE)

        for i in range(rows):

            for j in range(cols):

                if grid[i][j].obstrucle:
                    grid[i][j].show(RED)

        food.show(GREEN)

        snake[-1].show(BLUE)

        display.flip()

        for event in pygame.event.get():

            if event.type == QUIT:

                done = True

            elif event.type == KEYDOWN:

                if event.key == K_w and not direction == 0:

                    direction = 2

                elif event.key == K_a and not direction == 1:

                    direction = 3

                elif event.key == K_s and not direction == 2:

                    direction = 0

                elif event.key == K_d and not direction == 3:

                    direction = 1


def main():

    pygame.init()
    swidth, sheight = pygame.display.Info().current_w, pygame.display.Info().current_h
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (swidth/2-255, sheight/2-270)
    print(swidth,sheight)

    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET,
                                      BOARD_LENGTH * OFFSET])
    pygame.display.set_caption("Snake Game ")
    thing = pygame.Rect(10, 10, 50, 50)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255, 255), pygame.Rect(50, 50, 10, 10))
    first = True
    playing = True
    while playing:
        if first or pick == 3:


            #pick = menu(screen)
            pick=int(sys.argv[1])

        options = {0: quit,
                   1: one_player,#### PRESS ENTER
                   2: two_player,#### PRESS T
                   3: SnakeAstar,#### PRESS B

                   }
        now = options[pick](screen)
        if now == False:
            break
        elif pick == 1 or pick == 2:
            eaten = now-1 #/ 4 - 1
            playing = game_over(screen, eaten)
            first = False

    pygame.quit()


if __name__ == "__main__":
    main()