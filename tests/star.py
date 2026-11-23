try:
    from TURTLE import Turtle
except ImportError:
    from turtle import Turtle

t = Turtle()
legs = int(input("How many sides? "))
t.begin_fill()
for i in range(legs):
    t.forward(100)
    t.right(180-(360 / (2*legs)))
t.end_fill()
#t.redraw()
input()