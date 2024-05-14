# TODO:
# Win screen
# restart

import pygame, math, random

def main():
    BOMB_COUNT = 15
    
    BOMB_TILE = 1
    HIDDEN_TILE = 2
    REVEALED_TILE = 0
    FLAGGED_TILE = 1
    
    FPS = 30
    TILE_SIZE = 30
    TILE_GAP = 1
    GRID_SIZE_X = 16
    GRID_SIZE_Y = 10
    BASE_WIDTH = (TILE_SIZE+TILE_GAP)*GRID_SIZE_X+TILE_GAP
    BASE_HEIGHT = (TILE_SIZE+TILE_GAP)*GRID_SIZE_Y+TILE_GAP
    DEBUG = False

    WHITE = [255,255,255]
    BLUE = [0,0,255]
    RED = [255,0,0]
    LIGHT_GRAY = [200]*3
    GRAY = [125,125,125]
    GRAY_RED = [125,100,100]
    GREEN = [0,125,0]

    pygame.init()
    screen = pygame.display.set_mode((BASE_WIDTH,BASE_HEIGHT), pygame.RESIZABLE);
    pygame.display.set_caption("MineSleeper")
    clock = pygame.time.Clock()

    gameOver = False
    victory = False

    def drawGridTile(grid_x,grid_y):
        grid_mouseX, grid_mouseY = mouseToTile()
        is_moused_over = grid_x == grid_mouseX and grid_y == grid_mouseY
        
        is_revealed = isRevealed(grid_x,grid_y)
        is_bomb = isBomb(grid_x,grid_y)
        is_flag = isFlag(grid_x,grid_y)

        # Color logic
        if DEBUG and is_moused_over:
            color = BLUE
        elif is_bomb and (gameOver or is_revealed):
            color = RED
        elif is_revealed:
            color = LIGHT_GRAY
        elif is_flag:
            color = GREEN
        elif DEBUG and is_bomb:
            color = GRAY_RED
        else:
            # Dark grey for unrevealed tiles
            color = GRAY

        draw_x = (TILE_SIZE * grid_x) + (TILE_GAP * (grid_x+1))
        draw_y = (TILE_SIZE * grid_y) + (TILE_GAP * (grid_y+1))
        draw_width = TILE_SIZE
        draw_height = TILE_SIZE

        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        scale_x = screenWidth / BASE_WIDTH
        scale_y = screenHeight / BASE_HEIGHT
        
        draw_x *= scale_x
        draw_y *= scale_y
        draw_width *= scale_x
        draw_height *= scale_y
        
        tile = pygame.Rect(draw_x,draw_y,draw_width,draw_height);
        pygame.draw.rect(screen, color, tile);
        
        if is_revealed or DEBUG:
            drawBombText(grid_x,grid_y);

    def isFlag(grid_x, grid_y):
        return marks_map[grid_y][grid_x] == FLAGGED_TILE

    def drawTiles():
        for y in range(GRID_SIZE_Y):
            for x in range(GRID_SIZE_X):
                drawGridTile(x,y);

    def drawBombText(grid_x,grid_y):
        bombCount = countSurroundingBombs(grid_x,grid_y)
        
        if bombCount > 0 and not isBomb(grid_x,grid_y):
            screenWidth, screenHeight = pygame.display.get_surface().get_size()
            scale_x = screenWidth / BASE_WIDTH
            scale_y = screenHeight / BASE_HEIGHT

            fontSize = int(16*scale_x)
            font = pygame.font.Font('freesansbold.ttf', fontSize)
            text = font.render(f"{bombCount}", True, WHITE)
            textRect = text.get_rect()
            x, y = tileToCoords(grid_x,grid_y)
            x += int(12*scale_x)
            y += int(12*scale_y)
            textRect.center = (x,y)
            
            screen.blit(text, textRect)

    def tileToCoords(grid_x,grid_y):
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        scale_x = screenWidth / BASE_WIDTH
        scale_y = screenHeight / BASE_HEIGHT
        
        x = grid_x*(TILE_SIZE+TILE_GAP)
        y = grid_y*(TILE_SIZE+TILE_GAP)

        x *= scale_x
        y *= scale_y
        
        return x, y
                
    def mouseToTile():
        mouseX, mouseY = pygame.mouse.get_pos()

        tile_x_area = TILE_SIZE+TILE_GAP
        tile_y_area = TILE_SIZE+TILE_GAP

        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        scale_x = screenWidth / BASE_WIDTH
        scale_y = screenHeight / BASE_HEIGHT

        tile_x_area *= scale_x
        tile_y_area *= scale_y
        
        x = math.floor(mouseX/(tile_x_area))
        y = math.floor(mouseY/(tile_y_area))
        
        return x, y

    def validTilePosition(grid_x,grid_y):
        return grid_x >= 0 and grid_x <= GRID_SIZE_X-1 and grid_y >= 0 and grid_y <= GRID_SIZE_Y-1

    def isRevealed(grid_x,grid_y):
        return marks_map[grid_y][grid_x] == REVEALED_TILE

    def countSurroundingBombs(grid_x, grid_y):
        UL, UM, UR, ML, MR, DL, DM, DR = 0, 0, 0, 0, 0, 0, 0, 0
        #why so many ifs XD
        if grid_y > 0:
            if grid_x > 0:
                UL = bomb_map[grid_y-1][grid_x-1]
            UM = bomb_map[grid_y-1][grid_x]
            if grid_x+1 != GRID_SIZE_X:
                UR = bomb_map[grid_y-1][grid_x+1]
        if grid_x > 0:
            ML = bomb_map[grid_y][grid_x-1]
        if grid_x+1 != GRID_SIZE_X:
            MR = bomb_map[grid_y][grid_x+1]
        if grid_y+1 != GRID_SIZE_Y:
            if grid_x > 0:
                DL = bomb_map[grid_y+1][grid_x-1]
            DM = bomb_map[grid_y+1][grid_x]
            if grid_x+1 != GRID_SIZE_X:
                DR = bomb_map[grid_y+1][grid_x+1]

        bombTotal = UL+UM+UR + ML+MR + DL+DM+DR
        #print(bombTotal)
        return bombTotal

    def isHidden(grid_x,grid_y):
        return marks_map[grid_y][grid_x] == HIDDEN_TILE

    def hideTile(grid_x,grid_y):
        marks_map[grid_y][grid_x] = HIDDEN_TILE

    def flagTile(grid_x,grid_y):
        marks_map[grid_y][grid_x] = FLAGGED_TILE
        
    def revealTile(grid_x,grid_y):
        marks_map[grid_y][grid_x] = REVEALED_TILE

    def isZero(grid_x,grid_y):
        return countSurroundingBombs(grid_x,grid_y) == 0

    def revealSurroundingTiles(grid_x, grid_y):
        for y in [-1,0,1]:
            for x in [-1,0,1]:
                neighborX = grid_x+x
                neighborY = grid_y+y
                
                invalidTile = not validTilePosition(neighborX, neighborY)
                if invalidTile:
                    continue
                
                sameTile = x == 0 and y == 0
                alreadyRevealed = isRevealed(neighborX, neighborY)
                
                if sameTile or alreadyRevealed:
                    continue

                revealTile(neighborX,neighborY)
                if isZero(neighborX,neighborY):
                    revealSurroundingTiles(neighborX,neighborY)
                
    def revealMap(grid_x,grid_y):
        revealTile(grid_x,grid_y);

        if isZero(grid_x,grid_y) and not isBomb(grid_x,grid_y):
            revealSurroundingTiles(grid_x,grid_y)
            
    def isBomb(grid_x,grid_y):
        return bomb_map[grid_y][grid_x] == BOMB_TILE

    def toggleFlag(grid_x,grid_y):
        hidden = isHidden(grid_x,grid_y)
        has_flag = isFlag(grid_x,grid_y)
        no_flag = not has_flag
        
        if hidden:
            flagTile(grid_x,grid_y)
        elif has_flag:
            hideTile(grid_x,grid_y)
            
    def printBombMap():
        for y in range(len(bomb_map)):
            print(f"{y}: {bomb_map[y]}")

    def generateBombMap():
        # 2D array
        bombMap = [[0 for x in range(GRID_SIZE_X)] for y in range(GRID_SIZE_Y)]

        bombsLeft = BOMB_COUNT
        while bombsLeft > 0:
            x = random.randrange(GRID_SIZE_X)
            y = random.randrange(GRID_SIZE_Y)

            unoccupiedTile = bombMap[y][x] != BOMB_TILE
            if unoccupiedTile:
                bombMap[y][x] = BOMB_TILE
                bombsLeft -= 1
            
        return bombMap

    def drawText(textString, textX, textY, textSize):
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        scale_x = screenWidth / BASE_WIDTH
        scale_y = screenHeight / BASE_HEIGHT
        
        fontSize = int(textSize*scale_x)
        font = pygame.font.Font('freesansbold.ttf', fontSize)
        text = font.render(textString, True, WHITE)
        textRect = text.get_rect()
        x, y = (textX, textY)
        textRect.center = (x,y)
        screen.blit(text, textRect)

    def generateMarksMap():
        empty_map = [[HIDDEN_TILE for x in range(GRID_SIZE_X)] for y in range(GRID_SIZE_Y)]
        return empty_map

    bomb_map = generateBombMap()
    marks_map = generateMarksMap()

    running = True
    while running:
        clock.tick(FPS)
        if (bomb_map == marks_map):
                    victory = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not (gameOver or victory):
                grid_mx, grid_my = mouseToTile()
                no_flag = not isFlag(grid_mx,grid_my)
                
                if no_flag and event.button == 1:
                    revealMap(grid_mx,grid_my)
                    if isBomb(grid_mx,grid_my):
                        gameOver = True
                elif event.button == 3:
                    toggleFlag(grid_mx,grid_my)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (gameOver or victory):
                    bomb_map = generateBombMap()
                    marks_map = generateMarksMap()
                    gameOver = False
                    victory = False

        screen.fill([0,0,0])

        drawTiles()
        if gameOver:
            screenWidth, screenHeight = pygame.display.get_surface().get_size()
            s = pygame.Surface((screenWidth, screenHeight))
            s.set_alpha(100)
            s.fill((0,0,0))
            screen.blit(s, (0,0))

            drawText("Game Over", screenWidth/2, screenHeight/2, 64)
            drawText("Press R to try again", screenWidth/2, screenHeight*0.75, 24)
        elif victory:
            screenWidth, screenHeight = pygame.display.get_surface().get_size()
            s = pygame.Surface((screenWidth, screenHeight))
            s.set_alpha(100)
            s.fill((0,0,0))
            screen.blit(s, (0,0))

            drawText("You Won!", screenWidth/2, screenHeight/2, 64)
            drawText("Press R to play again", screenWidth/2, screenHeight*0.75, 24)

        pygame.display.flip()

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()
