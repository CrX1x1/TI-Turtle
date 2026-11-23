try:
    import ti_graphics
    from TURTLE import Turtle  # your custom TI-84 Plus CE wrapper
    ON_CALC = True
    SCREEN = None
except ImportError:
    import turtle as _stdlib_turtle
    Turtle = _stdlib_turtle.Turtle
    SCREEN = _stdlib_turtle.Screen()
    SCREEN.title("CPython turtle Parity Reference")
    ON_CALC = False


def run_parity_tests():
    if ON_CALC:
        ti_graphics.cls()
    print("I'm alive")
    t = Turtle()
    t.speed(2)
    t.pencolor("black" if not ON_CALC else ti_graphics.Color.BLACK)
    # 1. circle(): native/default vs. segmented arc
    t.penup()
    t.goto(-90, 40)
    t.pendown()
    t.pencolor("blue" if not ON_CALC else ti_graphics.Color.BLUE)
    t.circle(30, 180)

    t.penup()
    t.goto(-10, 40)
    t.pendown()
    t.pencolor("red" if not ON_CALC else ti_graphics.Color.RED)
    t.circle(30, 180, segments=12) if ON_CALC else t.circle(30, 180, steps=12)

    # 2. dot(): custom size & color + fallback to pencolor
    t.penup()
    t.goto(-90, -20)
    t.dot(8, "green" if not ON_CALC else ti_graphics.Color.GREEN)

    t.goto(-50, -20)
    t.pencolor("magenta" if not ON_CALC else ti_graphics.Color.MAGENTA)
    t.dot(5)

    # 3. write(): alignments + move=True marker dots
    t.goto(-90, -60)
    t.pencolor("black" if not ON_CALC else ti_graphics.Color.BLACK)
    t.write("L", move=True, align="left")
    t.dot(3, "red" if not ON_CALC else ti_graphics.Color.RED)

    t.goto(0, -60)
    t.write("C", move=True, align="center")
    t.dot(3, "red" if not ON_CALC else ti_graphics.Color.RED)

    t.goto(80, -60)
    t.write("R", move=False, align="right")
    t.dot(3, "blue" if not ON_CALC else ti_graphics.Color.BLUE)

    pos = t.pos() if hasattr(t, "pos") else (t.x, t.y)
    hdg = t.heading() if callable(getattr(t, "heading", None)) else getattr(t, "_heading", None)
    print("Mode:", "CALC" if ON_CALC else "PC (stdlib turtle)")
    print("End pos:", round(pos[0], 2), round(pos[1], 2), "heading:", hdg)

    if SCREEN is not None:
        SCREEN.mainloop()


run_parity_tests()