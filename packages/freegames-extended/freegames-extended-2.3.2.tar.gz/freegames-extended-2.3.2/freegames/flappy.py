"""Flappy, game inspired by Flappy Bird.

Exercises

1. Keep score.
2. Vary the speed.
3. Vary the size of the balls.
4. Allow the bird to move forward and back.

"""
import os
from random import *
from turtle import *
from freegames import vector, get_data, set_data, save
from winsound import PlaySound,SND_FILENAME,SND_ASYNC

bird = vector(0, 0)
balls = []
state={"alive":True, "distance":0, "record":get_data("flappy", 0)}

def tap(x, y):
    "Move bird up in response to screen tap."
    if state["alive"]:
        PlaySound("sounds\\click.wav",SND_FILENAME+SND_ASYNC)
    up = vector(0, 30)
    bird.move(up)

def inside(point):
    "Return True if point on screen."
    return -210 < point.x < 210 and -210 < point.y < 210

def draw(alive):
    "Draw screen objects and show score."
    state["alive"] = alive
    if not alive:
        PlaySound("sounds\\lose.wav",SND_FILENAME+SND_ASYNC)
    clear()

    goto(bird.x, bird.y)

    if alive:
        dot(10, 'green')
    else:
        dot(10, 'red')

    for ball in balls:
        goto(ball.x, ball.y)
        dot(20, 'black')

    goto(34,178)
    write("Flying distance:{:.1f} m\nRecord:{:.1f} m".format(
        state["distance"], state["record"]), font=(None,10))
    
    update()

def move():
    "Update object positions."
    bird.y -= 5
    state["distance"]+=0.1
    if state["record"]<state["distance"]:
        state["record"]=state["distance"]

    for ball in balls:
        ball.x -= 3

    if randrange(10) == 0:
        y = randrange(-199, 199)
        ball = vector(199, y)
        balls.append(ball)

    while len(balls) > 0 and not inside(balls[0]):
        balls.pop(0)

    if not inside(bird):
        draw(False)
        return

    for ball in balls:
        if abs(ball - bird) < 15:
            draw(False)
            return

    draw(True)
    ontimer(move, 50)

def quit():
    try:
        set_data("flappy", state["record"])
        save()
    finally:
        bye()

scr=Screen()
scr.setup(420, 420, 370, 0)
scr._canvas.master["cursor"]="sb_up_arrow"
scr._canvas.master.wm_protocol("WM_DELETE_WINDOW",quit)

hideturtle()
up()
tracer(False)
onscreenclick(tap)
move()
done()
