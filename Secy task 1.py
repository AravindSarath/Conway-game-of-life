import pygame
import random
#initialising the module
pygame.init()
#setting the colours to be used
black = (0, 0, 0)
grey = (128, 128, 128)
yellow = (255, 255, 0)
#entering parameters of the grid
width=int(input("Enter width of the grid: "))
height=int(input("Enter height of the grid: "))
cellsize=int(input("Enter size of the each cell: "))
gridwidth=width//cellsize
gridheight=height//cellsize
FPS = 100

screen = pygame.display.set_mode((width,height))

clock = pygame.time.Clock()
#function to generate random patterns
def gen(num):
    return set([(random.randrange(0, gridheight), random.randrange(0, gridwidth)) for _ in range(num)])
#drawing the grid and live cells
def drawgrid(positions):
    for position in positions:
        col, row = position
        topleft = (col * cellsize, row * cellsize)
        pygame.draw.rect(screen, yellow, (*topleft, cellsize, cellsize))

    for row in range(gridheight):#horizontal grid lines
        pygame.draw.line(screen,black, (0, row * cellsize), (width, row * cellsize))

    for col in range(gridwidth):#vertical grid lines
        pygame.draw.line(screen, black, (col * cellsize, 0), (col * cellsize, height))
#updating the grid according to rules of the game
def adjustgrid(positions):
    allneighbors = set()
    newpositions = set()

    for position in positions:
        neighbors = getneighbors(position)
        allneighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            newpositions.add(position)
    
    for position in allneighbors:
        neighbors = getneighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            newpositions.add(position)
    
    return newpositions
#function to get all the neighbouring cells at a given time
def getneighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > gridwidth:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > gridheight:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))
    
    return neighbors
#function to run the game loop
def main():
    running = True
    playing = False
    count = 0
    updatefreq = 120

    positions = set()#storing positions of live cells
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        
        if count >= updatefreq:
            count = 0
            positions = adjustgrid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #adding live/dead cells by clicking mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // cellsize
                row = y // cellsize
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:#to pause or play using space bar
                    playing = not playing
                
                if event.key == pygame.K_c:#to clear the screen using letter 'c'
                    positions = set()
                    playing = False
                    count = 0
                
                if event.key == pygame.K_g:#to generate random distribution using letter 'g'
                    positions = gen(random.randrange(4, 10) * gridwidth)

                if event.key == pygame.K_n:#to go the next step using letter 'n' 
                    positions = adjustgrid(positions)
                
    
        screen.fill(grey)#make the screen grey
        drawgrid(positions)#draw grid and the live positions
        pygame.display.update()#updating the display


    pygame.quit()
#to run the main function if this script is executed
if __name__ == "__main__":
    main()
