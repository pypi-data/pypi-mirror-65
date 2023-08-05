"""Bounce, a simple animation demo.

Exercises

1. Make the ball speed up and down.
2. Change how the ball bounces when it hits a wall.
3. Make the ball leave a trail.
4. Change the ball color based on position.
   Hint: colormode(255); color(0, 100, 200)

"""

import os
from random import *
from turtle import *
from freegames import vector
from winsound import PlaySound,SND_FILENAME,SND_ASYNC

SOUND="sounds\hit.wav"
def value():
    "Randomly generate value between (-5, -3) or (3, 5)."
    return (3 + random() * 2) * choice([1, -1])

ball = vector(0, 0)
aim = vector(value(), value())

def draw():
    "Move ball and draw game."
    ball.move(aim)

    x = ball.x
    y = ball.y

    if x < -window_width()/2:
        aim.x = abs(aim.x)
        PlaySound(SOUND,SND_FILENAME+SND_ASYNC)
    elif x > window_width()/2:
        aim.x = -abs(aim.x)
        PlaySound(SOUND,SND_FILENAME+SND_ASYNC)

    if y < -window_height()/2:
        aim.y=abs(aim.y)
        PlaySound(SOUND,SND_FILENAME+SND_ASYNC)
    elif y > window_height()/2:
        aim.y = -abs(aim.y)
        PlaySound(SOUND,SND_FILENAME+SND_ASYNC)

    clear()
    goto(x, y)
    dot(10)

    ontimer(draw, 10)

def bind():
    "Bind the ball with key and mouse events."
    def up():
        aim.x=0
        aim.y=10
    def down():
        aim.x=0
        aim.y=-10
    def left():
        aim.x=-10
        aim.y=0
    def right():
        aim.x=10
        aim.y=0
    def _onclick(x,y):
        aim.x=(x-xcor())/20
        aim.y=(y-ycor())/20

    onkey(up,"Up")
    onkey(down,"Down")
    onkey(left,"Left")
    onkey(right,"Right")
    onscreenclick(_onclick)
    listen()

scr=getscreen()
scr.setup(420, 420, 370, 0)
scr._canvas.master["cursor"]="target"
hideturtle()
tracer(False)
up()
bind()
draw()
done()
