import pickle,os
from turtle import TPen
from turtle import *

__all__=["load","get_data","set_data","load_turtle","save_turtle","save"]
_data={}
FILENAME="data.pickle"

def load():
    try:
        f=open(FILENAME,'rb')
        _data.update(pickle.load(f))
    except:pass

def get_data(key,default={}):
    return _data.get(key,default)

def set_data(key,value):
    _data[key]=value


def _redo(turtle,action,data):
    # Does the main part of the work for redo()
    if action == "rot":
        angle, degPAU = data
        turtle.setheading(angle*degPAU/turtle._degreesPerAU)
    elif action == "go":
        old, new, go_modes, coodata = data
        drawing, pc, ps, filling = go_modes
        turtle.pen(pendown=drawing, pencolor=pc,
                   fillcolor=pc, pensize=ps)
        turtle._goto(new)
    elif action == "dofill":
        turtle.end_fill()
    elif action == "beginfill":
        turtle.begin_fill()
    elif action == "pen":
        turtle.pen(data[0])

def redo(turtle,undobuffer):
    if undobuffer is None:
        return
    for item in undobuffer:
        if item == [None]:continue
        action = item[0]
        data = item[1:]
        _redo(turtle,action, data)

def load_turtle(key):
    data=get_data(key,{})
    turtle = Turtle()
    turtle.__dict__.update(data)
    tracer(False)
    redo(turtle, turtle.undobuffer.buffer.copy())
    tracer(True)
    return turtle

def save_turtle(key,turtle):
    data = turtle.__dict__.copy()
    del data["screen"]
    del data["turtle"]
    set_data(key, data)

def save():
    with open(FILENAME,'wb') as f:
        pickle.dump(_data,f)
