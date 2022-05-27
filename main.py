import pygame, random, colorsys

START_MIN = 0 # the minumum value for pixels on spawn, 0 to 99
START_MAX = 100 # the maxiumum value for pixels on start, 1 to 100
SPEED = 1000 # 1 to 1000
RANDOMNESS = 15 # 1 to 100

rows, cols = [100, 100]
grid = [[random.randint(START_MIN, START_MAX) for i in range(cols)] for j in range(rows)]

def hsv2rgb(h,s,v):
    h /= 100
    return tuple([round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v)])

pygame.init()

#initialising assets
screen = pygame.display.set_mode((550,540))

hsv_image = pygame.image.load("hue.jpeg")
hsv_image = pygame.transform.scale(hsv_image, (20, 500))

pygame.font.init()
font = pygame.font.SysFont('Helvetica', 20)

def update():
    global grid
    last = [[j for j in i] for i in grid]

    for i in range(rows):
        for j in range(cols):
            color = hsv2rgb(grid[i][j], 1, 1) # heatmap
            # color = (last[i][j]/100*255, last[i][j]/100*255, last[i][j]/100*255) # grayscale
            pygame.draw.rect(screen, color, pygame.Rect(j*5+10, i*5+10, 5, 5))
            if value(i,j, grid) > grid[i][j]:
                last[i][j] += random.randint(1, RANDOMNESS)
            elif value(i,j, grid) < grid[i][j]:
                last[i][j] -= random.randint(1, RANDOMNESS)

    if last[i][j] > 100:
        last[i][j] = 0
    if last[i][j] < 0:
        last[i][j] = 100
    grid = [[j for j in i] for i in last]

def value(row, column, grid):
    values = []
    for a in range(-1,2):
        for b in range(-1,2):
            try:
                if (row+a >= 0 and column+b >= 0) and not (a==0 and b==0):
                    values.append(grid[row+a][column+b])
            except:
                pass

    return round(sum(values)/len(values), 2)

gen = 0
running = True

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0,0,0))

    screen.blit(hsv_image, (520, 10))
    gen += 1
    gen_label = font.render('Generation ' + str(gen), False, (255, 255, 255))
    screen.blit(gen_label, (10, 515))
    update()
    max_list = [max(i) for i in grid]
    pygame.draw.line(screen, (255,255,255), (520, 10 + max(max_list) * 5), (540, 10 + max(max_list) * 5), width=5)
    min_list = [min(i) for i in grid]
    pygame.draw.line(screen, (255,255,255), (520, 10 + min(min_list) * 5), (540, 10 + min(min_list) * 5), width=5)
    pygame.display.flip()

    pygame.time.wait(round(1000/SPEED))