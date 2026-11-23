try:
    import ti_graphics
    from TURTLE import Turtle
    CALC = True
    SCR = None
except ImportError:
    import turtle as _t
    Turtle, SCR, CALC = _t.Turtle, _t.Screen(), False

if CALC:
    ti_graphics.cls()

t = Turtle()
c = (lambda n: getattr(ti_graphics.Color, n)) if CALC else (lambda n: n.lower())
t.speed(2)
# circle: fast vs segmented
t.penup(); t.goto(15, 45); t.pendown()
t.pencolor(c("BLUE")); t.circle(10, 180)

t.penup(); t.goto(45, 45); t.pendown()
t.pencolor(c("RED"))
t.circle(10, 180, segments=12) if CALC else t.circle(10, 180, steps=12)

# dot: explicit color & fallback
t.penup(); t.goto(15, 25); t.dot(6, c("GREEN"))
t.goto(45, 25); t.pencolor(c("MAGENTA")); t.dot(4)

# write: left, center, right + move markers
t.goto(10, 10); t.pencolor(c("BLACK")); t.write("L", move=True, align="left"); t.dot(2, c("RED"))
t.goto(40, 10); t.write("C", move=True, align="center"); t.dot(2, c("RED"))
t.goto(70, 10); t.write("R", move=False, align="right"); t.dot(2, c("BLUE"))

if CALC:
    t.redraw()

input()