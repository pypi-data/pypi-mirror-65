"""Pong, classic arcade game.

Exercises

1. Change the colors.
2. What is the frame rate? Make it faster or slower.
3. Change the speed of the ball.
4. Change the size of the paddles.
5. Change how the ball bounces off walls.
6. How would you add a computer player?
6. Add a second ball.

"""
from random import choice, random
from turtle import *
from freegames import vector
from winsound import PlaySound,SND_FILENAME,SND_ASYNC

SPEED=1.4
def value():
    "Randomly generate value between (-5, -3) or (3, 5)."
    return (3 + random() * 2) * choice([1, -1])

ball = vector(0, 0)
state = {1: 0, 2: 0}
SOUND="sounds\hit.wav"

def move(player, change):
    "Move player position by change."
    state[player] += change

def rectangle(x, y, width, height):
    "Draw rectangle at (x, y) with given width and height."
    up()
    goto(x, y)
    down()
    begin_fill()
    for count in range(2):
        forward(width)
        left(90)
        forward(height)
        left(90)
    end_fill()

def draw():
    "Draw game and move pong ball."
    clear()
    rectangle(-200, state[1], 10, 50)
    rectangle(190, state[2], 10, 50)

    ball.move(aim)
    x = ball.x
    y = ball.y

    up()
    goto(x, y)
    dot(10)
    update()

    if y < -200 or y > 200:
        aim.y = -aim.y

    if x < -185:
        low = state[1]
        high = state[1] + 50

        if low <= y <= high:
            aim.x = -aim.x
            PlaySound(SOUND,SND_FILENAME+SND_ASYNC)
        else:
            return

    if x > 185:
        low = state[2]
        high = state[2] + 50

        if low <= y <= high:
            aim.x = -aim.x
            PlaySound(SOUND,SND_FILENAME+SND_ASYNC)
        else:
            return

    ontimer(draw, 50)

def main(x=None,y=None):
    global aim
    reset()
    aim = vector(value()*SPEED, value()*SPEED)
    scr=getscreen()
    scr.setup(420, 420, 370, 0)
    hideturtle()
    tracer(False)
    scr.listen()
    scr.onkey(lambda: move(1, 20), 'w')
    scr.onkey(lambda: move(1, -20), 's')
    scr.onkey(lambda: move(2, 20), 'i')
    scr.onkey(lambda: move(2, -20), 'k')
    draw()
    done()

if __name__=="__main__":main()
