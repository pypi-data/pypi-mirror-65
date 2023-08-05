"""Cannon, hitting targets with projectiles.

Exercises

1. Keep score by counting target hits.
2. Vary the effect of gravity.
3. Apply gravity to the targets.
4. Change the speed of the ball.

"""
import os
from random import randrange
from turtle import *
from freegames import vector, get_data, set_data, save
from winsound import PlaySound,SND_FILENAME,SND_ASYNC

ball = vector(-200, -200)
speed = vector(0, 0)
targets = []
state={"score": 0, "record": get_data("cannon", 0)}

def tap(x, y):
    "Respond to screen tap."
    if not inside(ball):
        ball.x = -199
        ball.y = -199
        speed.x = (x + 200) / 25
        speed.y = (y + 200) / 25

def inside(xy):
    "Return True if xy within screen."
    return -200 < xy.x < 200 and -200 < xy.y < 200

def draw():
    "Draw ball, targets and score."
    clear()

    for target in targets:
        goto(target.x, target.y)
        dot(20, 'blue')

    if inside(ball):
        goto(ball.x, ball.y)
        dot(6, 'red')

    goto(window_width()//2-90,window_height()//2-35)
    write("Score: %s\nRecord: %s" % (state["score"], state["record"]),
          font = (None,12))
    update()

def move():
    "Move ball and targets."
    if randrange(40) == 0:
        y = randrange(-150, 150)
        target = vector(200, y)
        targets.append(target)

    for target in targets:
        target.x -= 0.5

    if inside(ball):
        speed.y -= 0.35
        ball.move(speed)

    dupe = targets.copy()
    targets.clear()

    for target in dupe:
        if abs(target - ball) > 13:
            targets.append(target)
        else:
            state["score"]+=1
            if state["record"] < state["score"]:
                state["record"] = state["score"]
                set_data("cannon", state["record"])
                save()

            PlaySound("sounds\\bomb.wav",SND_FILENAME+SND_ASYNC)
    draw()

    for target in targets:
        if not inside(target):
            targets.remove(target)

    ontimer(move, 50)

scr = Screen()
scr.setup(420, 420, 370, 0)
scr._canvas.master["cursor"] = "target"
hideturtle()
up()
tracer(False)
onscreenclick(tap)
move()
done()
