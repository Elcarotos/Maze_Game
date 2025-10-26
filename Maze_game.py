import pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen = pygame.display.set_mode()
clock = pygame.time.Clock()
w, h = screen.get_size()

points = {"A" : (w*0, h*0), "B" : (w, h*0), "C" : (w, h), "D" : (w*0, h),
          "E" : (w*0.05, h*0.05), "F" : (w*0.95, h*0.05), "G" : (w*0.95, h*0.95), "H" : (w*0.05, h*0.95),
          "I" : (w*0.1, h*0.1), "J" : (w*0.9, h*0.1), "K" : (w*0.9, h*0.9), "L" : (w*0.1, h*0.9),
          "M" : (w*0.15, h*0.15), "N" : (w*0.85, h*0.15), "O" : (w*0.85, h*0.85), "P" : (w*0.15, h*0.85),
          "Q" : (w*0.2, h*0.2), "R" : (w*0.80, h*0.2), "S" : (w*0.8, h*0.8), "T" : (w*0.2, h*0.8),
          "U" : (w*0.25, h*0.25), "V" : (w*0.75, h*0.25), "W" : (w*0.75, h*0.75), "X" : (w*0.25, h*0.75),
          "a" : (w*0.3, h*0.3), "b" : (w*0.7, h*0.3), "c" : (w*0.7, h*0.7), "d" : (w*0.3, h*0.7),
          "e" : (w*0.35, h*0.35), "f" : (w*0.65, h*0.35), "g" : (w*0.65, h*0.65), "h" : (w*0.35, h*0.65)}

polygons_front = [[points["A"], points["B"], points["C"], points["D"]],
                 [points["E"], points["F"], points["G"], points["H"]],
                 [points["I"], points["J"], points["K"], points["L"]],
                 [points["M"], points["N"], points["O"], points["P"]],
                 [points["Q"], points["R"], points["S"], points["T"]],
                 [points["U"], points["V"], points["W"], points["X"]],
                 [points["a"], points["b"], points["c"], points["d"]],
                 [points["e"], points["f"], points["g"], points["h"]]]

polygons_left = [[points["A"], points["E"], points["H"], points["D"]],
                [points["E"], points["I"], points["L"], points["H"]],
                [points["I"], points["M"], points["P"], points["L"]],
                [points["M"], points["Q"], points["T"], points["P"]],
                [points["Q"], points["U"], points["X"], points["T"]],
                [points["U"], points["a"], points["d"], points["X"]],
                [points["a"], points["e"], points["h"], points["d"]]]

polygons_right = [[points["B"], points["F"], points["G"], points["C"]],
                 [points["F"], points["J"], points["K"], points["G"]],
                 [points["J"], points["N"], points["O"], points["K"]],
                 [points["N"], points["R"], points["S"], points["O"]],
                 [points["R"], points["V"], points["W"], points["S"]],
                 [points["V"], points["b"], points["c"], points["W"]],
                 [points["b"], points["f"], points["g"], points["c"]]]

size_x, size_y = 16, 16
filepath = "Maps/map_03.txt"

font = pygame.font.Font(None, 40)

main_game = pygame.Surface((w, h))
mini_map = pygame.Surface((size_x*10, size_y*10))
direction_indicator = pygame.Surface((120, 40))

MAP = []
list_tiles = []
player = None
lines_y = 0

# Class for the game
class Tile():
    def __init__(self, state, x, y):
        self.state = state
        self.pos = pygame.Rect(x*size_x, y*size_y, size_x, size_y)

    def affichage(self):
        if self.state == 1:
            pygame.draw.rect(mini_map, "BLUE", self.pos, width=1)
        if self.state == 0:
            pygame.draw.rect(mini_map, "RED", self.pos, width=1)


class View_field():
    def __init__(self, pos):
        self.pos = pos
        self.collision = []


class Player():
    DIRECTIONS = ["NORTH", "WEST", "SOUTH", "EAST"]

    def __init__(self, joystick):
        self.joystick = joystick
        self.pos = None
        self.view_field = {}
        self.dir = "NORTH"
        self.couldown_move_x = False
        self.couldown_move_y = False

    def set_pos(self, x, y):
        self.pos = pygame.Rect(x*size_x, y*size_y, size_x, size_y)

    def set_view_field(self):
        self.view_field["view_front"] = View_field(pygame.Rect(self.pos))
        self.view_field["view_left"] = View_field(pygame.Rect(self.pos))
        self.view_field["view_right"] = View_field(pygame.Rect(self.pos))

    def set_couldown_move_x(self, state):
        self.couldown_move_x = state
    def set_couldown_move_y(self, state):
        self.couldown_move_y = state

    def rotate(self, direction):
        index = Player.DIRECTIONS.index(self.dir)
        size_list = len(Player.DIRECTIONS)
        if direction < 0:
            self.dir = Player.DIRECTIONS[(index+1) % size_list]
        if direction > 0:
            self.dir = Player.DIRECTIONS[(index-1) % size_list]

    def move(self):
        if self.dir == "NORTH":
            self.pos.y -= size_y
            [view_field[1].pos.y - size_y for view_field in self.view_field.items()]
        if self.dir == "WEST":
            self.pos.x -= size_x
            [view_field[1].pos.x - size_x for view_field in self.view_field.items()]
        if self.dir == "SOUTH":
            self.pos.y += size_y
            [view_field[1].pos.y + size_y for view_field in self.view_field.items()]
        if self.dir == "EAST":
            self.pos.x += size_x
            [view_field[1].pos.x + size_x for view_field in self.view_field.items()]

    def collision(self):
        for tile in list_tiles:
            if self.pos == tile.pos and tile.state == 1:
                if self.dir == "NORTH":
                    self.pos.y += size_y
                    [view_field[1].pos.y + size_y for view_field in self.view_field.items()]
                if self.dir == "WEST":
                    self.pos.x += size_x
                    [view_field[1].pos.x + size_x for view_field in self.view_field.items()]
                if self.dir == "SOUTH":
                    self.pos.y -= size_y
                    [view_field[1].pos.y - size_y for view_field in self.view_field.items()]
                if self.dir == "EAST":
                    self.pos.x -= size_x
                    [view_field[1].pos.x - size_x for view_field in self.view_field.items()]


    def view_update(self):
        if self.dir == "NORTH":
            self.view_field["view_front"].pos = pygame.Rect((self.pos.x, self.pos.y-abs(self.pos.y)), (size_x, abs(self.pos.y)))
            self.view_field["view_left"].pos = pygame.Rect((self.pos.x-size_x, self.pos.y-abs(self.pos.y)), (size_x, abs(self.pos.y)))
            self.view_field["view_right"].pos = pygame.Rect((self.pos.x+size_x, self.pos.y-abs(self.pos.y)), (size_x, abs(self.pos.y)))

        if self.dir == "WEST":
            self.view_field["view_front"].pos = pygame.Rect((self.pos.x-abs(self.pos.x), self.pos.y), (abs(self.pos.x), size_y))
            self.view_field["view_left"].pos = pygame.Rect((self.pos.x-abs(self.pos.x), self.pos.y+size_y), (abs(self.pos.x), size_y))
            self.view_field["view_right"].pos = pygame.Rect((self.pos.x-abs(self.pos.x), self.pos.y-size_y), (abs(self.pos.x), size_y))

        if self.dir == "SOUTH":
            self.view_field["view_front"].pos = pygame.Rect((self.pos.x, self.pos.y+size_y), (size_x, abs(self.pos.y+size_y-len(MAP[-1]*size_y))))
            self.view_field["view_left"].pos = pygame.Rect((self.pos.x+size_x, self.pos.y+size_y), (size_x, abs(self.pos.y+size_y-len(MAP[-1]*size_y))))
            self.view_field["view_right"].pos = pygame.Rect((self.pos.x-size_x, self.pos.y+size_y), (size_x, abs(self.pos.y+size_y-len(MAP[-1]*size_y))))

        if self.dir == "EAST":
            self.view_field["view_front"].pos = pygame.Rect((self.pos.x+size_x, self.pos.y), (abs(self.pos.x+size_x-len(MAP[-1]*size_x)), size_y))
            self.view_field["view_left"].pos = pygame.Rect((self.pos.x+size_x, self.pos.y-size_y), (abs(self.pos.x+size_x-len(MAP[-1]*size_x)), size_y))
            self.view_field["view_right"].pos = pygame.Rect((self.pos.x+size_x, self.pos.y+size_y), (abs(self.pos.x+size_x-len(MAP[-1]*size_x)), size_y))


#----------------------------------------------------------------------------------
    def view_collide(self):
        list_tiles_wall = [tile.pos for tile in list_tiles if tile.state == 1]
        
        collide_front = self.view_field["view_front"].pos.collidelistall(list_tiles_wall)
        collide_left = self.view_field["view_left"].pos.collidelistall([tile.pos for tile in list_tiles])
        collide_right = self.view_field["view_right"].pos.collidelistall([tile.pos for tile in list_tiles])

        if self.dir == "NORTH":
            collide_front.reverse()
            collide_left.reverse()
            collide_right.reverse()

        if self.dir == "WEST":
            collide_front.reverse()
            collide_left.reverse()
            collide_right.reverse()

        self.view_field["view_left"].collision = collide_left
        self.view_field["view_right"].collision = collide_right


        rect = list_tiles_wall[collide_front[0]]
        
        pos_x = abs(self.pos.x - rect.x)
        pos_y = abs(self.pos.y - rect.y)
        distance = pos_x / size_x + pos_y / size_y

        self.view_field["view_front"].collision = distance


    def affichage(self):
        pygame.draw.rect(mini_map, "GREEN", self.pos, width=2)
#----------------------------------------------------------------------------------
# Init VFD effet
def create_scanlines_surface():
    scanlines = pygame.Surface((w, h), pygame.SRCALPHA)
    for y in range(0, h, 4):
        pygame.draw.line(scanlines, (0, 20, 0, 100), (0, y), (w, y), 3)
    return scanlines
scanlines_surface = create_scanlines_surface()

# Init timer for update animation
def create_timer_animation():
    timer = pygame.time.set_timer(pygame.USEREVENT, 5)

# Init map functions
def load_map_from_file():
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            MAP.append([caracter for caracter in line if caracter != '\n'])
    return MAP
def create_list_tiles():
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if MAP[y][x] == '0':
                list_tiles.append(Tile(0, x, y))
            if MAP[y][x] == '1':
                list_tiles.append(Tile(1, x, y))
    return list_tiles

# Init player functions
def create_joystick():
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        player = Player(joystick)
        return player
    else:
        destroy()
def create_player():
    x, y = 2, 3
    player.set_pos(x, y)
def create_view_field():
    player.set_view_field()

# Init
def general_init():
    create_timer_animation()
def maze_init():
    MAP = load_map_from_file()
    list_tiles = create_list_tiles()
def player_init():
    global player
    player = create_joystick()
    create_player()
    create_view_field()


# Animation affichage
def scanline_refresh_affichage():
    global lines_y
    pygame.draw.line(scanlines_surface, (0, 20, 0, 100), (0, lines_y), (w, lines_y), 3)
    lines_y += 4
    if lines_y == h:
        lines_y = 0
    else:
        pygame.draw.line(scanlines_surface, (100, 120, 100, 100), (0, lines_y), (w, lines_y), 3)
        pygame.draw.line(scanlines_surface, (100, 120, 100, 100), (0, lines_y+4), (w, lines_y+4), 3)
        pygame.draw.line(scanlines_surface, (100, 120, 100, 100), (0, lines_y+8), (w, lines_y+8), 3)

# Game affichage
def background_game():
    main_game.fill("BLACK")
def front_wall_affichage():
    pygame.draw.polygon(main_game, "GREEN", polygons_front[int(player.view_field["view_front"].collision)-1])
    pygame.draw.polygon(main_game, (100, 100, 100), polygons_front[int(player.view_field["view_front"].collision)-1], width=8)
def left_wall_affichage():
    for wall in range(0, int(player.view_field["view_front"].collision-1)):
        if list_tiles[player.view_field["view_left"].collision[wall]].state == 1:
            pygame.draw.polygon(main_game, "GREEN", polygons_left[wall])
            pygame.draw.polygon(main_game, (100, 100, 100), polygons_left[wall], width=8)
def right_wall_affichage():
    for wall in range(0, int(player.view_field["view_front"].collision-1)):
        if list_tiles[player.view_field["view_right"].collision[wall]].state == 1:
            pygame.draw.polygon(main_game, "GREEN", polygons_right[wall])
            pygame.draw.polygon(main_game, (100, 100, 100), polygons_right[wall], width=8)
def scanlines_affichage():
    main_game.blit(scanlines_surface, (0, 0))
def main_game_affichage():
    screen.blit(main_game, (0, 0))

# Map affichage
def background_map():
    mini_map.fill("BLACK")
def tiles_affichage():
    for tile in list_tiles:
        tile.affichage()
def player_affichage():
    player.affichage()
def mini_map_affichage():
    screen.blit(mini_map, (w-160, 0))

# Direction affichage
def background_direction():
    direction_indicator.fill("BLACK")
def edges_affichage():
    pygame.draw.rect(direction_indicator, "BLUE", (0, 0, 120, 40), width=4)
def text_affichage():
    text = str(player.dir)
    direction_indicator.blit(font.render(text, True, "BLUE"), (9, 8))
def direction_indicator_affichage():
    screen.blit(direction_indicator, (0, 0))


# Update
def animation_affichage():
    scanline_refresh_affichage()
def game_affichage():
    background_game()
    front_wall_affichage()
    left_wall_affichage()
    right_wall_affichage()
    scanlines_affichage()
    main_game_affichage()
def map_affichage():
    background_map()
    tiles_affichage()
    player_affichage()
    mini_map_affichage()
def direction_affichage():
    background_direction()
    edges_affichage()
    text_affichage()
    direction_indicator_affichage()

def controller():
    axis_x = player.joystick.get_axis(0)
    axis_y = player.joystick.get_axis(1)
    if abs(axis_x) > 0.8 and not player.couldown_move_x:
        player.rotate(axis_x)
        player.set_couldown_move_x(True)
    if abs(axis_x) < 0.6 and player.couldown_move_x:
        player.set_couldown_move_x(False)
    if axis_y < -0.9 and not player.couldown_move_y:
        player.move()
        player.set_couldown_move_y(True)
    if axis_y > -0.6 and player.couldown_move_y:
        player.set_couldown_move_y(False)

def update():
    player.collision()
    player.view_update()
    player.view_collide()


# Close the game
def destroy():
    pygame.quit()
    exit()


general_init()
maze_init()
player_init()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            destroy()
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                destroy()

        if event.type == pygame.USEREVENT:
            animation_affichage()

    clock.tick(30)

    controller()
    update()

    game_affichage()
    map_affichage()
    direction_affichage()

    pygame.display.flip()
