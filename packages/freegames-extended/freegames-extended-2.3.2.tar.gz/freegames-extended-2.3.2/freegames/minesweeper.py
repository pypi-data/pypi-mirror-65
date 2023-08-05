"""Minesweeper

Exercises

1. What does the `seed(0)` function call do?
2. Change the number of bombs on the grid.
3. Change the size of the grid.

"""
import os,time
from random import randrange, seed
from turtle import *
from freegames import floor, square
from winsound import PlaySound,SND_FILENAME,SND_ASYNC
from freegames.button import Button

try:os.chdir(os.path.split(__file__)[0])
except:pass

bombs = {}
shown = {}
counts = {}

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
bomb=Turtle()
bomb.hideturtle()
bomb.penup()
bomb.shape("turtle")
bomb.shapesize(1.2)
bomb.color("red")

def initialize(x=None,y=None):
    "Initialize `bombs`, `counts`, and `shown` grids."
    clear()
    bomb.clearstamps()
    for x in range(-250, 250, 50):
        for y in range(-250, 250, 50):
            bombs[x, y] = False
            shown[x, y] = False
            counts[x, y] = -1

    for count in range(8):
        x = randrange(-200, 200, 50)
        y = randrange(-200, 200, 50)
        bombs[x, y] = True

    for x in range(-200, 200, 50):
        for y in range(-200, 200, 50):
            total = 0
            for i in (-50, 0, 50):
                for j in (-50, 0, 50):
                    total += bombs[x + i, y + j]
            counts[x, y] = total
    draw()
    onscreenclick(tap)


def stamp(x, y, text,_color="black",backcolor="alice blue"):
    "Display `text` at coordinates `x` and `y`."
    square(x, y, 50, backcolor)
    color(_color)
    write(text, font=('Arial', 25, 'normal'))

def message(text,pos=(-190,-120),color="black"):
    penup()
    pencolor(color)
    goto(pos)
    write(text,font=("Courier",18,"bold"))

def draw():
    "Draw the initial board grid."
    for x in range(-200, 200, 50):
        for y in range(-200, 200, 50):
            goto(x,y+50)
            Button(50,50,color1="LightSkyBlue1",
                   color2="LightSkyblue2")
            update()
    fillcolor("black")

def draw_bomb(x,y):
    bomb.goto(x+25,y+25)
    bomb.setheading(randrange(0,360))
    bomb.stamp()

def end(color="red",delay=0):
    "Draw the bombs on the grid."
    for x in range(-200, 200, 50):
        for y in range(-200, 200, 50):
            if bombs[x, y]:
                draw_bomb(x,y)
                update()
                time.sleep(delay)
    onscreenclick(initialize)

def win():
    for x in range(-200, 200, 50):
        for y in range(-200, 200, 50):
            if bombs[x, y]==shown[x ,y]:
                return False
    return True
            

def tap(x, y):
    "Respond to screen click at `x` and `y` coordinates."
    x = floor(x, 50)
    y = floor(y, 50)

    if bombs[x, y]:
        PlaySound("sounds\\bomb.wav",SND_FILENAME+SND_ASYNC)
        end()
        message("""You lost the game.
Press screen to play again.""",color="red")
        return

    pairs = [(x, y)]
    if not shown[(x, y)]:
        PlaySound("sounds\\tile.wav",SND_FILENAME+SND_ASYNC)

    while pairs:
        x, y = pairs.pop()
        stamp(x, y, (counts[x, y] if counts[x, y] != -1 else ''))
        shown[x, y] = True

        if counts[x, y] == 0:
            for i in (-50, 0, 50):
                for j in (-50, 0, 50):
                    pair = x + i, y + j
                    if not shown[pair]:
                        pairs.append(pair)
    if win():
        PlaySound("sounds\\win.wav",SND_FILENAME+SND_ASYNC)
        end(color="blue",delay=0.27)
        message("""Congratulations!You win the game.
Press screen to play again.""",pos=(-200,-120),color="blue")

penup()
initialize()
done()
