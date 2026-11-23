import ti_graphics
import ti_system
import math
import time
import gc #hehehehe

#gc.disable() #screw the players over... later

#globals
enemies = []

#math helper(s)
def get_intersection(x, y, dx, dy):
    # Find where the infinite line through (x, y) intersects the screen.
    # The origin and direction may be negative or outside the screen bounds.
    min_x, max_x = 0, 320
    min_y, max_y = 30, 240

    hits = []
    if dx != 0:
        for edge_x in (min_x, max_x):
            t = (edge_x - x) / dx
            y_intersect = y + t * dy
            if min_y <= y_intersect <= max_y:
                hits.append((edge_x, y_intersect))
    if dy != 0:
        for edge_y in (min_y, max_y):
            t = (edge_y - y) / dy
            x_intersect = x + t * dx
            if min_x <= x_intersect <= max_x:
                hits.append((x_intersect, edge_y))
    # Remove duplicate corner intersections.
    hits = list(dict.fromkeys(hits))
    return hits
def get_triangle_corners(hit1, hit2): #math done by ai
    #given two intersection points, return the third point of the triangle
    #the third point has to be at a corner.
    corners = [(0, 30), (0, 240), (320, 30), (320, 240)]
    def get_perimeter_pos(point):
        x, y = point
        if y == 30:
            return x
        elif x == 320:
            return 320 + (y - 30)
        elif y == 240:
            return 320 + 210 + (320 - x)
        elif x == 0:
            return 320 + 210 + 320 + (240 - y)
        return 0
    #find the corner that minimizes the perimeter
    pos1 = get_perimeter_pos(hit1)
    pos2 = get_perimeter_pos(hit2)

    #collect corners
    collected_corners = []
    for corner in corners:
        pos_corner = get_perimeter_pos(corner)
        if (pos1 < pos2) and (pos1 < pos_corner < pos2):
            collected_corners.append(corner)
        elif (pos_corner >= pos1) or (pos_corner <= pos2):
            collected_corners.append(corner)
    collected_corners.sort(key=lambda item: item[0] if pos1 < pos2 else (item[0] if item[0] > pos1 else item[0] + 1060)) # by ai, seems like a black box
    return collected_corners
def get_intersection_away(x, y, dx, dy):
    hits = get_intersection(x, y, dx, dy)
    if not hits:
        return None
    return max(hits, key=lambda point: (point[0] - x) ** 2 + (point[1] - y) * dy)
def hsv_to_rgb(h):#saturation and value are always 1
    h = h % 360
    c = 1
    x = c * (1 - abs((h / 60) % 2 - 1))
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return int(r * 255), int(g * 255), int(b * 255)
class Turtle: #fake, ofc
    def __init__(self, x=160, y=105):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.angle = 0.0 #rad
        self.pen_down = False
        self.friction = 0.9
        self.max_speed = 15.0
        #dum dum keypress detection
        self.time_since_last_keypress = 0
        self.last_direction = 0 #-1 ccw, 1 cw
        #last trail state
        self.l_x = x
        self.l_y = y
        #for background calculations
        self.tx = 0
        self.ty = 0
        self.lx = 0
        self.ly = 0
        self.rx = 0
        self.ry = 0
        #memory leak gimmick
        self.trail = []

    def forward(self, dir=1):
        self.vx += math.cos(self.angle) * 1.5 * dir
        self.vy += math.sin(self.angle) * 1.5 * dir
        #control speed
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > self.max_speed and speed != 0:
            self.vx = (self.vx / speed) * self.max_speed
            self.vy = (self.vy / speed) * self.max_speed
    def turn(self, dir):
        now = time.ticks_ms()

        if (time.ticks_diff(now, self.time_since_last_keypress) < 250) and (dir == self.last_direction):
            self.angle += math.radians(dir*30)
        else:
            self.angle += math.radians(dir*10)
        self.time_since_last_keypress = now
        self.last_direction = dir
    def update_trail(self):
        #distance based object creation
        if self.pen_down:
            dx = self.x - self.l_x
            dy = self.y - self.l_y
            distance = dx**2 + dy**2
            if distance >= 900:
                seg = Segment(self.l_x, self.l_y, self.x, self.y)
                self.trail.append(seg)
                self.l_x = self.x
                self.l_y = self.y
        #lifetime deletion
        alive = []
        for seg in self.trail:
            if not seg.expired():
                alive.append(seg)
        self.trail = alive
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= self.friction
        self.vy *= self.friction
        #bounce off edges
        if self.x < 0:
            self.x = 0
            self.vx *= -1
        elif self.x > 320:
            self.x = 320
            self.vx *= -1
        if self.y < 30:
            self.y = 30
            self.vy *= -1
        elif self.y > 240:
            self.y = 240
            self.vy *= -1
        self.update_trail()
    def render(self):
        #draw trail
        ti_graphics.setColor((255, 255, 255))
        while len(self.trail) > 7:
            self.trail.pop(0)
        for seg in self.trail:
            ti_graphics.drawLine(seg.x1, seg.y1, seg.x2, seg.y2)
        #draw turtle
        c = math.cos(self.angle)
        s = math.sin(self.angle)
        size = 10
        self.tx = self.x
        self.ty = self.y
        self.lx = self.tx + (-12 * c - 6 * s)
        self.ly = self.ty + (-12 * s + 6 * c)
        self.rx = self.tx + (-12 * c + 6 * s)
        self.ry = self.ty + (-12 * s - 6 * c)

        ti_graphics.setColor((255, 255, 255))
        ti_graphics.fillPolygon([(self.tx, self.ty), (self.lx, self.ly), (self.rx, self.ry)])
    def background(self):
        ti_graphics.setColor((0, 0, 0))
        #modified from ai code
        #cx = (self.tx + self.lx + self.rx) / 3
        #cy = (self.ty + self.ly + self.ry) / 3
        """
        hits_n = get_intersection(self.tx, self.ty, self.tx - self.lx, self.ty - self.ly)
        hits_l = get_intersection(self.lx, self.ly, self.lx - self.rx, self.ly - self.ry)
        hits_r = get_intersection(self.rx, self.ry, self.rx - self.tx, self.ry - self.ty)

        if not hits_n or not hits_l or not hits_r:
            return
        """
        #hit_n = hits_n[0]
        #hit_l = hits_l[0]
        #hit_r = hits_r[0]
        hit_n = get_intersection_away(self.tx, self.ty, self.tx - self.lx, self.ty - self.ly)
        hit_l = get_intersection_away(self.lx, self.ly, self.lx - self.rx, self.ly - self.ry)
        hit_r = get_intersection_away(self.rx, self.ry, self.rx - self.tx, self.ry - self.ty)
        if not hit_n or not hit_l or not hit_r:
            return

        corners_1 = get_triangle_corners(hit_n, hit_l)
        corners_2 = get_triangle_corners(hit_n, hit_r)
        corners_3 = get_triangle_corners(hit_l, hit_r)
        ti_graphics.fillPolygon([(self.tx, self.ty), hit_n] + corners_1 + [hit_l])
        ti_graphics.fillPolygon([(self.lx, self.ly), hit_l] + corners_2 + [hit_r])
        ti_graphics.fillPolygon([(self.rx, self.ry), hit_r] + corners_3 + [hit_n])
class Segment:
    def __init__(self, x1, y1, x2, y2, lifetime=15000, payload=64):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)
        self.created_at = time.ticks_ms()
        self.lifetime = lifetime
        self.payload = bytearray(payload) #memory leak gimmick
    def expired(self):
        now = time.ticks_ms()
        return time.ticks_diff(now, self.created_at) >= self.lifetime
def flush():
    #heh, manual garbage collection
    before = gc.mem_free()
    gc.collect()
    after = gc.mem_free()
    return max(0, after - before)

class Bullet:
    #literally just a laser beam that appears for 1 frame
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
    def render(self):
        #draw a fricking red line
        #let see here... so x_2 = x_1 + cos(angle) * length
        #and y_2 = y_1 + sin(angle) * length
        ti_graphics.setColor((255, 0, 0))
        ti_graphics.drawLine(self.x, self.y, self.x + math.cos(self.angle) * 400, self.y + math.sin(self.angle) * 400)
class Blob:
    #basic enemy that simply takes up a fixed amount of memory
    def __init__(self, size):
        self.data = bytearray(size)
'''
so, i have an idea...
if i have a turtle and i want the screen to be filled besides that
i could perhaps calculate the three right triangles that are formed
from the turtle edges and the screen corners, but how?
it keeps going to the wrong corner bruh

ah screw it, i'm just gonna fill the whole screen instead
'''
t = Turtle()
i=0 #test
'''
while True:
    i += 1
    i = i%10
    key = ti_system.get_key(0)
    if key == 45: #close
        break
    elif key == 25: #up
        t.forward()
    elif key == 34: #down
        t.forward(-1)
    elif key == 24: #left
        t.turn(-1)
    elif key == 26: #right
        t.turn(1)
    elif key == 22: #mode, toggle pen
        t.pen_down = not t.pen_down
    elif key == 21: #2nd, fire
        #check collision here.
        Bullet(t.x, t.y, t.angle).render()
        ti_system.sleep(0.01) #1 frame delay
    t.update()
    \'''
    if i == 0:
        t.background()
    else:
        ti_graphics.setColor((0, 0, 0))
        ti_graphics.fillRect(0, 30, 320, 240)
    \'''
    ti_graphics.drawString(0, 0, "Free Memory:%s" % gc.mem_free())
    ti_graphics.setColor((0, 0, 0))
    ti_graphics.fillRect(0, 30, 320, 240)
    t.render()
    #ti_system.sleep(0.01) #60fps
'''
#assert that it's always unique
colors = [hsv_to_rgb(h) for h in range(256)]
assert len(set(colors)) == 256