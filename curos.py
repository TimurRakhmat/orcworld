import pygame
import sys
import os

FPS = 50


def load_image(name, wher='datagame'):
    if wher == 'w':
        fullname = os.path.join('3_ORK', name)
    else:
        fullname = os.path.join(wher, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('back2.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "datagame/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, 'g'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.type = tile_type
        if tile_type == 'lawa':
            self.add(lawagrup)
        self.rect = self.image.get_rect().move(
            totx + tile_width * pos_x, toty + tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites, alife_group)
        self.cur_frame = 0
        self.r = 1
        self.image = pygame.transform.scale(pl_img['noth'][self.cur_frame], (50, 70))
        self.rect = self.image.get_rect().move(pos_x * 50, pos_y * 50)
        self.xvel = 0
        self.yvel = 0
        self.t = 0
        self.onGround = False

    def update(self):
        if left:
            if self.r == 1:
                self.cur_frame = 0
            self.r = 0
            self.xvel = -4
        if right:
            if self.r == 0:
                self.cur_frame = 0
            self.r = 1
            self.xvel = 4
        if not (left or right):
            self.xvel = 0

        if up:
            if self.onGround:
                self.yvel = -9

        if not self.onGround:
            self.yvel += 0.25
        if self.t % 3 == 0:
            self.cur_frame = (self.cur_frame + 1) % 7
            if click1 or click2:
                if self.r:
                    self.image = pygame.transform.scale(pl_img['attack'][self.cur_frame], (50, 70))
                else:
                    self.image = pygame.transform.flip(pygame.transform.scale(pl_img['attack'][self.cur_frame],
                                                                              (50, 70)), 1, 0)
            elif up:
                if self.r:
                    self.image = pygame.transform.scale(pl_img['jump'][self.cur_frame], (50, 70))
                else:
                    self.image = pygame.transform.flip(pygame.transform.scale(pl_img['jump'][self.cur_frame], (50, 70)),
                                                       1, 0)
            elif right:
                self.image = pygame.transform.scale(pl_img['run'][self.cur_frame], (50, 70))
            elif left:
                self.image = pygame.transform.flip(pygame.transform.scale(pl_img['run'][self.cur_frame], (50, 70)), 1,
                                                   0)
            else:
                if self.r:
                    self.image = pygame.transform.scale(pl_img['noth'][self.cur_frame], (50, 70))
                else:
                    self.image = pygame.transform.flip(pygame.transform.scale(pl_img['noth'][self.cur_frame], (50, 70)),
                                                       1, 0)

        self.t += 1
        self.onGround = False
        self.rect.x += self.xvel
        self.collide(self.xvel, 0)
        self.rect.y += self.yvel
        self.die()
        self.collide(0, self.yvel)

    def die(self):
        for li in lawagrup:
            if pygame.sprite.collide_rect(self, li):
                self.kill()
                start_screen()
                terminate()

    def collide(self, xvel, yvel):
        for tile in tiles_group:
            if pygame.sprite.collide_rect(self, tile):
                if xvel > 0:
                    self.rect.right = tile.rect.left
                if xvel < 0:
                    self.rect.left = tile.rect.right
                if yvel > 0:
                    self.rect.bottom = tile.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = tile.rect.bottom
                    self.yvel = 0


class Warior(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(npc_group, all_sprites, alife_group)
        self.cur_frame = 0
        self.r = 1
        self.image = pygame.transform.scale(war_img['noth'][self.cur_frame], (50, 70))
        self.rect = self.image.get_rect().move(pos_x * 50, pos_y * 50)
        self.xvel = 0
        self.yvel = 0
        self.t = 0
        self.bit = False
        self.onGround = False

    def update(self):
        if player.rect.x - self.rect.x > -500 and player.rect.x - self.rect.x < -50:
            if self.r == 1:
                self.cur_frame = 0
            self.r = 0
            self.xvel = -4
        if player.rect.x - self.rect.x < 500 and player.rect.x - self.rect.x > 50:
            if self.r == 0:
                self.cur_frame = 0
            self.r = 1
            self.xvel = 4
        if player.rect.x - self.rect.x < 50 and player.rect.x - self.rect.x > -50:
            self.xvel = 0
            self.bit = True
        else:
            self.bit = False
        if player.rect.x - self.rect.x > 500 or player.rect.x - self.rect.x < -500:
            self.xvel = 0

        if up:
            if self.onGround:
                self.yvel = -9

        if not self.onGround:
            self.yvel += 0.25

        if self.t % 3 == 0:
            self.cur_frame = (self.cur_frame + 1) % 7
            if self.bit:
                if self.r:
                    self.image = pygame.transform.scale(war_img['attack'][self.cur_frame], (50, 70))
                else:
                    self.image = pygame.transform.flip(pygame.transform.scale(war_img['attack'][self.cur_frame],
                                                                              (50, 70)), 1, 0)
            elif self.xvel == 4:
                self.image = pygame.transform.scale(war_img['run'][self.cur_frame], (50, 70))
            elif self.xvel == -4:
                self.image = pygame.transform.flip(pygame.transform.scale(war_img['run'][self.cur_frame], (50, 70)), 1,
                                                   0)
            else:
                if self.r:
                    self.image = pygame.transform.scale(war_img['noth'][self.cur_frame], (50, 70))
                else:
                    self.image = pygame.transform.flip(pygame.transform.scale(war_img['noth'][self.cur_frame], (50, 70)),
                                                       1, 0)

        self.t += 1
        self.onGround = False
        self.rect.x += self.xvel
        self.collide(self.xvel, 0)
        self.rect.y += self.yvel
        self.die()
        self.collide(0, self.yvel)

    def die(self):
        for li in lawagrup:
            if pygame.sprite.collide_rect(self, li):
                self.kill()

    def collide(self, xvel, yvel):
        for tile in tiles_group:
            if pygame.sprite.collide_rect(self, tile):
                if xvel > 0:
                    self.rect.right = tile.rect.left
                if xvel < 0:
                    self.rect.left = tile.rect.right
                if yvel > 0:
                    self.rect.bottom = tile.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = tile.rect.bottom
                    self.yvel = 0


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * height for _ in range(width)]

        self.left = 0
        self.top = 0
        self.cell_size = 50

    def set_view(self, left, top):
        self.left += left
        self.top += top

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mpos):
        x, y = mpos
        if x in range(self.left, self.left + self.width * self.cell_size) and \
                y in range(self.top, self.top + self.height * self.cell_size):
            x1 = (x - self.left) // self.cell_size
            y1 = (y - self.top) // self.cell_size
            return x1, y1
        else:
            return None

    def on_click(self, cell):
        if cell:
            x, y = cell
            if self.board[x][y] and click1:
                self.board[x][y].kill()
                self.board[x][y] = 0
            if self.board[x][y] == 0 and click2:
                self.board[x][y] = Tile('wood', x, y)
                if pygame.sprite.spritecollideany(self.board[x][y], alife_group):
                    self.board[x][y].kill()
                    self.board[x][y] = 0

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (144, 144, 144),\
                                 (self.left + i * self.cell_size, self.top + j * self.cell_size,\
                                  self.cell_size, self.cell_size), 1)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def boardapply(self):
        board.set_view(self.dx, self.dy)

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('dirt', x, y)
            elif level[y][x] == '#':
                Tile('wood', x, y)
            elif level[y][x] == '@':
                 man = Player(x, y)
            elif level[y][x] == '5':
                Tile('lawa', x, y)
            elif level[y][x] == '6':
                Tile('stone', x, y)
            elif level[y][x] == 'g':
                Tile('gas', x, y)
            elif level[y][x] == '$':
                Warior(x, y)
    return man, x + 1, y + 1


def tiles():
    for tile in tiles_group:
        x, y = tile.x, tile.y
        board.board[x][y] = tile


pygame.init()
pygame.mixer.init()
left = right = up = down = click1 = click2 = False
totx = toty = 0
camera = Camera()

width, height = 500, 500

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
start_screen()

tile_images = {
    'wood': load_image('wood.png'),
    'dirt': load_image('dirt.png'),
    'lawa': load_image('lawa.jpg'),
    'gas': load_image('gas.jpg'),
    #'water': load_image('water.png'),
    'stone': load_image('stone.jpg')
    }
pl_img = {
    'run': [load_image('RUN_000.png'), load_image('RUN_001.png'), load_image('RUN_002.png'),
            load_image('RUN_003.png'),load_image('RUN_004.png'), load_image('RUN_005.png'),
            load_image('RUN_006.png')],
    'attack': [load_image('ATTAK_000.png'), load_image('ATTAK_001.png'), load_image('ATTAK_002.png'),
               load_image('ATTAK_003.png'), load_image('ATTAK_004.png'), load_image('ATTAK_005.png'),
               load_image('ATTAK_006.png')],
    'jump': [load_image('JUMP_000.png'), load_image('JUMP_001.png'), load_image('JUMP_002.png'),
               load_image('JUMP_003.png'), load_image('JUMP_004.png'), load_image('JUMP_005.png'),
               load_image('JUMP_006.png')],
    'noth': [load_image('IDLE_000.png'), load_image('IDLE_001.png'), load_image('IDLE_002.png'),
               load_image('IDLE_003.png'), load_image('IDLE_004.png'), load_image('IDLE_005.png'),
               load_image('IDLE_006.png')],
    }
war_img = {
    'attack': [load_image('ATTAK_000.png', 'w'), load_image('ATTAK_001.png', 'w'), load_image('ATTAK_002.png', 'w'),
               load_image('ATTAK_003.png', 'w'), load_image('ATTAK_004.png', 'w'), load_image('ATTAK_005.png', 'w'),
               load_image('ATTAK_006.png', 'w')],
    'jump': [load_image('JUMP_000.png', 'w'), load_image('JUMP_001.png', 'w'), load_image('JUMP_002.png', 'w'),
               load_image('JUMP_003.png', 'w'), load_image('JUMP_004.png', 'w'), load_image('JUMP_005.png', 'w'),
               load_image('JUMP_006.png', 'w')],
    'run': [load_image('RUN_000.png', 'w'), load_image('RUN_001.png', 'w'), load_image('RUN_002.png', 'w'),
            load_image('RUN_003.png', 'w'),load_image('RUN_004.png', 'w'), load_image('RUN_005.png', 'w'),
            load_image('RUN_006.png', 'w')],
    'noth': [load_image('IDLE_000.png', 'w'), load_image('IDLE_001.png', 'w'), load_image('IDLE_002.png', 'w'),
               load_image('IDLE_003.png', 'w'), load_image('IDLE_004.png', 'w'), load_image('IDLE_005.png', 'w'),
               load_image('IDLE_006.png', 'w')],
    }
tile_width = tile_height = 50
player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
lawagrup = pygame.sprite.Group()
npc_group = pygame.sprite.Group()
alife_group = pygame.sprite.Group()

player, x1, y1 = generate_level(load_level('1.txt'))
orc2 = Warior(800, -70)
board = Board(x1, y1)
tiles()
width, height = 1200, 800
fon = pygame.transform.scale(load_image('back2.jpg'), (width, height))
screen = pygame.display.set_mode((width, height))
running = True
muza = pygame.mixer.Sound(os.path.join('datagame', 'day.ogg'))
muza.play(-1)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        if event.type == pygame.KEYDOWN:
            f = pygame.key.get_pressed()
            if f[pygame.K_w]:
                up = True
            if f[pygame.K_a]:
                left = True
            if f[pygame.K_d]:
                right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                up = False
            elif event.key == pygame.K_a:
                left = False
            elif event.key == pygame.K_d:
                right = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click1 = True
                board.get_click(event.pos)
            elif event.button == 3:
                click2 = True
                board.get_click(event.pos)

        if event.type == pygame.MOUSEMOTION:
            if click1 or click2:
                board.get_click(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            click1 = False
            click2 = False

    screen.fill((255, 255, 255))
    screen.blit(fon, (0, 0))
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    totx += camera.dx
    toty += camera.dy
    npc_group.update()
    player.update()
    tiles_group.draw(screen)
    npc_group.draw(screen)
    player_group.draw(screen)
    camera.boardapply()
    board.render()
    pygame.display.flip()
    clock.tick(620)
