import ti_graphics
import time
start = time.ticks_ms()
for x in range(320):
    for y in range(240):
        ti_graphics.getPixel(x, y)
print("checking the whole screen took", time.ticks_diff(time.ticks_ms(), start), "ms")

#trial took 17775ms, kinda bad lol
#well, okay for calculator standards