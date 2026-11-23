# TI-Turtle

A very very smol(not) `turtle` port built on ti_graphics and ti_system for all TI calculators with Python programming. Built to run on calculator hardware and stuff.

# Features
- Movement and turning: `forward()`, `fd()`; `backward()` etc.
- Angle Modes: `degrees(full_circle==360)` and `radians()`
- Pen and visibility: `penup()`, `pu()`; `pendown()` etc.
- Shapes:
  - `circle(radius, extent, segments)`: uses drawArc by default for speed but can use segments to be slower
  - `dot(size=1, color)`: draws a filled dot at current pos in desired color, fall back to current pen color
  - `write(text, move=False, font=None, align="left"`: writes text horizontally, woah
  - `begin_fill()`, `end_fill()`, `filling()`: record points and then fills polygons from it with fillPolygon from ti_graphics
  - `stamp()`, `clearstamps()`: stamp the turtle

## Notices
### funny calculator quirks that will be useful in development
- module names will be in all caps if not compiled to mpy bytecode
  - if you want to compile the module, I suggest https://tiplanet.org/pb/
- coordinates work differently; increasing y coordinate will go down, that's normal.
- drawing might be clobbered by the turtle, call Turtle.redraw() if that happens.
- undo and redraw might have rough edges, open up an issue or PR to discuss

# Demo
it counts, right?
- [`media/star.mp4`](https://github.com/user-attachments/assets/9a02c0e8-cd09-4c83-8e88-2715d97fe97e): oh, look it is drawing stars
- [`media/random.mp4`](https://github.com/user-attachments/assets/c459653f-2076-45e4-8d28-2a64b507d0c1): random doodles
