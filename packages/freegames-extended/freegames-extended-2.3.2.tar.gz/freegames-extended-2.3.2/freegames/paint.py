"""Paint, for drawing shapes.

Exercises

1. Add a color.
2. Complete circle.
3. Complete rectangle.
4. Complete triangle.
5. Add width parameter.

"""

import pprint
from turtle import *
from freegames import *

def line(start, end):
    "Draw line from start to end."
    t.up()
    t.goto(start.x, start.y)
    t.down()
    _towards(end)
    t.goto(end.x, end.y)

def polygon(start, end, sides):
    "Draw a polygon from start to end."
    t.up()
    t.goto(start.x, start.y)
    t.down()
    t.begin_fill()
    _towards(end)
    dis=distance(start,end)
    for count in range(sides):
        t.forward(dis)
        t.right(360/sides)

    t.end_fill()

triangle = lambda start,end:polygon(start,end,3)
square = lambda start,end:polygon(start,end,4)
def circle(start, end):
    "Draw circle from start to end."
    pass  # TODO

def rectangle(start, end):
    "Draw rectangle from start to end."
    pass  # TODO

def dot(pos):
    t.penup()
    t.goto(pos)
    t.dot(5)

def text(pos):
    t.penup()
    t.goto(pos)
    t.write(scr.textinput("","Enter text to write:"),font=(None, 12))

def _towards(pos):
    t.speed(0)
    t.setheading(t.towards(pos.x,pos.y))
    t.speed(6)

def tap(x, y):
    "Store starting point or draw shape."
    onscreenclick(None)

    start = state['start']
    shape = state['shape']

    if shape in (dot, text):
        shape(vector(x, y))
        onscreenclick(tap)
        save_turtle("paint", t)
        save()
        return

    if start is None:
        state['start'] = vector(x, y)
        t.penup()
        _towards(state['start'])
        t.goto(x,y)
        t.pendown()
    else:
        end = vector(x, y)
        shape(start, end)
        state['start'] = None

    save_turtle("paint", t)
    save()
    onscreenclick(tap)

def store(key, value):
    "Store value in state at key."
    state[key] = value

state = {'start': None, 'shape': line}

scr=Screen()
scr.setup(420, 420, 370, 0)
scr._canvas.master["cursor"]="crosshair"
scr._canvas.bind_all("<Control-Key-Z>", lambda event:t.undo())
onscreenclick(tap)
onkey(undo, 'u')
onkey(lambda: t.color('black'), 'b')
onkey(lambda: t.color('white'), 'w')
onkey(lambda: t.pencolor('green'), 'g')
onkey(lambda: t.color('blue'), 'b')
onkey(lambda: t.color('purple'), 'p')
onkey(lambda: t.color('red'), 'r')
onkey(lambda: store('shape', line), 'l')
onkey(lambda: store('shape', square), 's')
onkey(lambda: store('shape', circle), 'c')
onkey(lambda: store('shape', rectangle), 'e')
onkey(lambda: store('shape', triangle), 'i')
onkey(lambda: store('shape', text), 't')
onkey(lambda: store('shape', dot), 'd')
def clear_all():
    t.clear()
    t.reset()
    t.shapesize(1.5)
    store('shape', line)
    save_turtle("paint", t)
    save()

onkey(clear_all, 'c')
listen()

t = load_turtle("paint")
#t.shape("triangle")
t.shapesize(1.5)
done()
