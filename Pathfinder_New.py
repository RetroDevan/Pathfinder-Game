import pygame
from heapq import *
from collections import deque

pygame.init()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
text_font = pygame.font.SysFont("Arial",22)


window_size = 800
window = pygame.display.set_mode((window_size,window_size))
grid_size = 20

pygame.display.set_caption("Pathfinder")

window.fill(WHITE)
gap = window_size//grid_size
blocksize = gap

class block:
    def __init__(self,row,col) :
        self.row = row
        self.col = col
        self.xcor = row*gap
        self.ycor = col*gap
        self.color = WHITE
        self.neighbours = []
    
    def makeblock(self):
        pygame.draw.rect(window,self.color,(self.xcor,self.ycor,gap,gap))
    
    def assign_neighbours(self,grid):
        if(self.row>0 and grid[self.row-1][self.col].color != WHITE):
            self.neighbors.append(grid[self.row-1][self.col])
        if(self.row<grid_size-1 and grid[self.row+1][self.col].color != WHITE):
            self.neighbors.append(grid[self.row+1][self.col])
        if(self.col>0 and grid[self.row][self.col-1].color!=WHITE):
            self.neighbors.append(grid[self.row][self.col-1])
        if(self.col<grid_size-1 and grid[self.row][self.col+1].color!= WHITE):
            self.neighbors.append(grid[self.row][self.col+1])

def draw_text(text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    window.blit(img,(x,y))



def gridlines():
    x = 0
    y = 0
    for i in range(grid_size):
        x += window_size//grid_size
        y += window_size//grid_size
        pygame.draw.line(window,BLACK,(x,window_size//grid_size),(x,window_size))
        pygame.draw.line(window,BLACK,(0,y),(window_size,y))

def draw(grid):
    
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid[i][j].makeblock()
    
    gridlines()


def manhattan(a,b):
    return abs(a.xcor-b.xcor)+abs(a.ycor-b.ycor)


def Astar(draw,grid,st,end):
    trackpath = {}
    h = []
    cnt = 0
    f = {}
    g = {}
    for i in range(grid_size):
        for j in range(grid_size):
            f[grid[i][j]] = 10**9
            g[grid[i][j]] = 10**9

    g[st] = 0
    f[st] = g[st]+ manhattan(st,end)
    heappush(h,(f[st],cnt,st))
    while(len(h) != 0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = heappop(h)[2]

        if(curr == end):
            while(curr in trackpath):
                curr = trackpath[curr]
                curr.color = RED
                draw()
            return

        for i in curr.neighbors:
            if(g[i] > g[curr]+1):
                trackpath[i] = curr
                g[i] = g[curr]+1
                f[i] = g[i] + manhattan(i,end)
                cnt+=1
                i.color = GREEN
                heappush(h,(f[i],cnt,i))

        draw()
        if(curr != st):
            curr.color = ORANGE

    return


def eucledean(a,b):
    return ((a.xcor-b.xcor)**2 + (a.ycor-b.ycor)**2)**(0.5)

def bestfirstsearch(draw,grid,st,end):
    vis = {}
    val = {}
    for i in range(grid_size):
        for j in range(grid_size):
            vis[grid[i][j]] = False
            val[grid[i][j]] = eucledean(grid[i][j],end)
    trackpath = {}
    have = []
    cnt = 0
    vis[st] = True
    heappush(have,(val[st],cnt,st))
    while(len(have)!=0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = heappop(have)[2]
        if(curr == end):
            while(curr in trackpath):
                curr = trackpath[curr]
                curr.color = RED
                draw()
            return

        for i in curr.neighbors:
            if(not vis[i]):
                i.color = GREEN
                trackpath[i] = curr
                vis[i] = True
                cnt+=1
                heappush(have,(eucledean(i,end),cnt,i))
        draw()
        if(curr != st):
            curr.color = ORANGE
    return




def main():
    grid = []
    for i in range(grid_size):
        temp = []
        for j in range(grid_size):
            temp.append(block(i,j))
        grid.append(temp)
    
    st = False
    end = False
    ob = False
    running = True
    while(running):
        draw(grid)
        if(not st):
            draw_text("CLICK ON THE START POINT", text_font, BLACK,5,5)
        elif(not end):
            draw_text("CLICK ON THE FINISH POINT, RIGHT CLICK TO REMOVE START POINT", text_font, BLACK,5,5)
        elif(not ob):
            draw_text("DRAW OBSTRUCTIONS, THEN PRESS ENTER. OR RIGHT CLICK TO REMOVE", text_font, BLACK,5,5)
        else:
            draw_text("PRESS 1-ASTAR, 2-BFS, 3-DJIKSTRA, BACKSPACE TO GO BACK",text_font, BLACK,5,5)
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False
                
            if(pygame.mouse.get_pressed()[0]): #leftclick
                x,y= pygame.mouse.get_pos()
                i = x//gap
                j = y//gap

                if(not st and grid[i][j] != end):
                    st = grid[i][j]
                    grid[i][j].color = YELLOW

                elif(not end and grid[i][j] != st):
                    end = grid[i][j]
                    grid[i][j].color = PURPLE

                elif(grid[i][j] != st and grid[i][j]!=end):
                    grid[i][j].color = BLACK


            elif(pygame.mouse.get_pressed()[2]): #rightclick
                x,y = pygame.mouse.get_pos()
                i = x//gap
                j = y//gap

                if(grid[i][j] == st):
                    st = False
                    grid[i][j].color = WHITE
                elif(grid[i][j] == end):
                    end = False
                    grid[i][j].color = WHITE
                else:
                    ob = False
                    grid[i][j].color = WHITE

            elif(event.type==pygame.KEYDOWN and not ob):
                if event.key==pygame.K_RETURN:
                    ob = True
                
            elif(event.type==pygame.KEYDOWN and ob):
                
                if event.key==pygame.K_BACKSPACE:
                    ob = False
                elif(event.key == pygame.K_2): 
                    djkistra(lambda:draw(grid),grid,st,end)
                elif(event.key == pygame.K_a): 
                    Astar(lambda:draw(grid),grid,st,end)
                if(event.key == pygame.K_3): #best first seach
                    bestfirstsearch(lambda :draw(grid),grid,st,end)
                    

        pygame.display.update()


main() 