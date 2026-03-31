import pygame
import pgzrun
import random
from pgzero.actor import Actor

FPS = 20
TITLE = "Purpose going to be executed"

mode = "game"
pygame.mouse.set_visible(False)

draw_escape = False

sword = Actor('sword')
count_w = 9
count_h = 10
wall = Actor("brick")
plat = Actor("floor(1)")
player = Actor("hero")
end_white = Actor("end_white")
end_white.top = 8 * wall.height
end_white.left = 6 * wall.width
enemies = []
hearts = []
player.hp = 100
player.attack = 25
enemyHp = [25, 50]

WIDTH = plat.width * count_w
HEIGHT = plat.height * count_h

player.top = 0 * plat.height
player.left = 3 * plat.width

maps = [[1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1]]

for i in range(len(maps)):
    for j in range(len(maps[i])):
        if maps[i][j] == 0:
            if len(enemies) != 4 and (player.top != i * plat.height or player.left != j * plat.width) and random.random() < 0.2:
                e = Actor("skullenemy")
                e.top = i * wall.height
                e.left = j * wall.width
                print(i * wall.height, j * wall.width)
                e.hp = enemyHp[random.randint(0, 1)]
                if i * wall.height == 50 and j * wall.width == 150:
                    continue
                enemies.append(e)

while len(hearts) < 3:
    r_i = random.randint(0, len(maps) - 1)
    r_j = random.randint(0, len(maps[0]) - 1)
    if maps[r_i][r_j] == 0:
        target_top = r_i * plat.height
        target_left = r_j * plat.width
        if player.top == target_top and player.left == target_left:
            continue
        occupied_by_enemy = False
        for e in enemies:
            if e.top == target_top and e.left == target_left:
                occupied_by_enemy = True
                break
        if occupied_by_enemy:
            continue
        occupied_by_heart = False
        for h in hearts:
            if h.top == target_top and h.left == target_left:
                occupied_by_heart = True
                break
        if occupied_by_heart:
            continue
        new_heart = Actor("hp")
        new_heart.top = target_top
        new_heart.left = target_left
        hearts.append(new_heart)

def render_map(maps):
    for i in range(len(maps)):
        for j in range(len(maps[i])):
            if maps[i][j] == 0:
                plat.top = plat.height * i
                plat.left = plat.width * j
                plat.draw()
            elif maps[i][j] == 1:
                wall.top = wall.height * i
                wall.left = wall.width * j
                wall.draw()

def on_mouse_down(pos, button):
    global mode, draw_escape
    if button == mouse.LEFT:
        for e in enemies[:]:
            if e.collidepoint(pos):
                dist_x = abs(player.left - e.left)
                dist_y = abs(player.top - e.top)
                is_near_x = dist_x == plat.width and dist_y == 0
                is_near_y = dist_y == plat.height and dist_x == 0
                if is_near_x or is_near_y:
                    e.hp -= player.attack
                    player.hp -= 25
                    if player.hp <= 0:
                        mode = 'died'
                    if e.hp <= 0:
                        enemies.remove(e)
                        if len(enemies) == 0:
                            print("")
                            draw_escape = True

def on_mouse_move(pos):
    sword.pos = pos

def on_key_down(key):
    old_x, old_y = player.left, player.top
    if key == keys.LEFT:
        player.left -= plat.width
    elif key == keys.RIGHT:
        player.left += plat.width
    elif key == keys.UP:
        player.top -= plat.height
    elif key == keys.DOWN:
        player.top += plat.height
    grid_x = int(player.left / plat.width)
    grid_y = int(player.top / plat.height)
    if (grid_x < 0 or grid_x >= count_w or grid_y < 0 or grid_y >= count_h or maps[grid_y][grid_x] != 0):
        player.left, player.top = old_x, old_y
    for e in enemies:
        if player.colliderect(e):
            player.left, player.top = old_x, old_y
            break
    for h in hearts[:]:
        if player.colliderect(h) and player.hp != 100:
            player.hp += 25
            hearts.remove(h)

def draw():
    global mode, draw_escape, end_white_draw
    if mode == "game":
        screen.clear()
        render_map(maps)
        for e in enemies:
            e.draw()
            screen.draw.text(f"{e.hp}", (e.left, e.top - 15), fontsize=20, color="red")
        for h in hearts:
            h.draw()
        player.draw()
        sword.draw()
        screen.draw.text(f"HP: {player.hp}", (20, HEIGHT - 40), fontsize=40, color="white")
    if mode == "died":
        screen.clear()
        draw_escape = False
        screen.fill((40, 0, 0))
        screen.draw.text(f'Вы проиграли...', center=(WIDTH / 2, HEIGHT / 2), color="red", fontsize=64)
    if mode == "victory":
        screen.clear()
        draw_escape = False
        screen.fill((0, 200, 0))
        screen.draw.text(f'Вы победили!', center=(WIDTH / 2, HEIGHT / 2), color="white", fontsize=64)

    if draw_escape:
        end_white.draw()
        if player.top == 8 * wall.height and player.left == 6 * wall.width:
            mode = "victory"


def update(dt):
    print('')

pgzrun.go()
