import ti_graphics

for i in range(10):
    ti_graphics.setPen(0, i)
    ti_graphics.drawLine(0, 0, 320, 240)
    input()
    ti_graphics.cls()