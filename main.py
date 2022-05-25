import pygame, random, colorsys

# changable values
START_MIN = 0 # the minumum value for pixels on spawn, 0 to 99
START_MAX = 100 # the maxiumum value for pixels on start, 1 to 100
SPEED = 10 # 1 to 100

pygame.display.set_caption('Heat Life')
rows, cols = [100, 100]
grid = [[random.randint(START_MIN, START_MAX) for i in range(cols)] for j in range(rows)]

def hsv2rgb(h,s,v):
    h /= 100
    return tuple([round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v)])

pygame.init()

screen = pygame.display.set_mode((500,500))

def update():
    global grid
    last = []
    for i in grid: last.append(i)

    for i in range(rows):
        for j in range(cols):
            color = hsv2rgb(last[i][j], 1, 1)
            pygame.draw.rect(screen, color, pygame.Rect(i*5, j*5, 5, 5))
            if value(i,j) > last[i][j]:
                last[i][j] += random.randint(1, 25)
            elif value(i,j) < last[i][j]:
                last[i][j] -= random.randint(1, 25)
            
            if last[i][j] > 100:
                last[i][j] = 100
            elif last[i][j] < 0:
                last[i][j] = 0
    grid = []
    for i in last: grid.append(i)

def value(row, column):
    values = []
    for a in range(-1,2):
        for b in range(-1,2):
            try:
                if (row+a >= 0 and column+b >= 0) and not (a==0 and b==0):
                    values.append(grid[row+a][column+b])
            except:
                pass

    return round(sum(values)/len(values), 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.time.wait(round(100/SPEED * 2))
    update()
    pygame.display.flip()