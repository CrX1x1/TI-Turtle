import ti_graphics
import math
import ti_system
class Turtle: #porting turtle to calculator, no more game BS from before.
    def __init__(self, x=160, y=105, heading=0):
        self._position_x = x
        self._position_y = y
        self._home_x = x
        self._home_y = y
        self._origin_x = 0
        self._origin_y = 30#status bar offset

        self._full_circle = 360
        self._heading = math.radians(heading)
        self._home_heading = self._heading
        self._degree_per_au = self._full_circle / (2 * math.pi)

        self._drawing = True #functionally pen down
        self._shown = True
        self._pencolor = (0, 0, 0)  # Default to black
        self._fillcolor = (0, 0, 0)  # Default to black
        self._pensize = 0

        self._filling = False
        self._fill_path = []

        self._lines = [] #store as (start_x, start_y, end_x, end_y, color, width, heading)
        self._history = [] #compacted version for undoing
        self._undobuffersize = 50 #ehh, good and memory efficient and enough for most cases

        self.tx, self.ty = None, None
        self.lx, self.ly = None, None
        self.rx, self.ry = None, None

        self._delay = 0

    @property
    def x(self):
        return self._position_x

    @x.setter
    def x(self, value):
        self._position_x = value

    @property
    def y(self):
        return self._position_y

    @y.setter
    def y(self, value):
        self._position_y = value
    @property
    def heading(self):
        return self._heading * self._degree_per_au
    def degrees(self, full_circle=360):
        self._degree_per_au = full_circle / (2 * math.pi)
        self._full_circle = full_circle
    def radians(self):
        self._degree_per_au = 1.0
        self._full_circle = 2 * math.pi
    def _record(self, action):
        self._history.append(action)
        if len(self._history) > self._undobuffersize:
            self._history.pop(0) 
    def _ltov(self, x, y):
        return (int(x + self._origin_x), int(y + self._origin_y))
    def _step_to(self, x, y):
        ox, oy = self.x, self.y
        state_before = (
            ox, oy, self._heading,
            self._drawing, self._filling, self._pencolor, self._fillcolor, self._pensize
        )
        self.x, self.y = x, y
        if self._filling:
            if not self._fill_path:
                self._fill_path.append((int(ox), int(oy)))
            self._fill_path.append((int(self.x), int(self.y)))
        seg = None
        if self._drawing:
            seg = (ox, oy, self.x, self.y, self._pencolor, self._pensize, self._heading)
            self._lines.append(seg)
            self._draw_segment(seg)
        self._record(('line', state_before, seg, (self.x, self.y, self._heading)))
        self.draw_turtle()
    def _draw_segment(self, seg):
        x1, y1, x2, y2, color, width, heading = seg
        x1, y1 = self._ltov(x1, y1)
        x2, y2 = self._ltov(x2, y2)
        ti_graphics.setColor(color)
        ti_graphics.setPen(width, 0)
        ti_graphics.drawLine(int(x1), int(y1), int(x2), int(y2))
    def speed(self, delay):
        self._delay = delay * 100 # 0-1000ms
    def forward(self, d):
        nx = self.x + math.cos(self._heading) * d
        ny = self.y + math.sin(self._heading) * d
        self._step_to(nx, ny)

    def backward(self, d):
        self.forward(-d)
    def stamp(self):
        c = math.cos(self._heading)
        s = math.sin(self._heading)

        state_before = (
            self.x, self.y, self._heading,
            self._drawing, self._filling, self._pencolor, self._fillcolor, self._pensize
        )

        tx, ty = self._ltov(self.x, self.y)
        lx, ly = self._ltov(self.x + (-12 * c - 6 * s), self.y + (-12 * s + 6 * c))
        rx, ry = self._ltov(self.x + (-12 * c + 6 * s), self.y + (-12 * s - 6 * c))

        ti_graphics.setColor(self._pencolor)
        ti_graphics.drawPolyLine([(tx, ty), (lx, ly), (rx, ry), (tx, ty)])
        self._record(('stamp', state_before, (tx, ty, lx, ly, rx, ry), self._pencolor))
    def left(self, angle):
        self._heading -= angle / self._degree_per_au
        self.draw_turtle()
    def right(self, angle):
        self._heading += angle / self._degree_per_au
        self.draw_turtle()
    def goto(self, x, y=None):
        x_iterable = True
        try:
            iter(x)
        except TypeError:
            x_iterable = False
        if y is None and not x_iterable:
            raise ValueError("x must be a tuple or list of two values if y is None")
        if y is None and x_iterable:
            x, y = x
        self._step_to(x, y)
    def home(self):
        self.goto(self._home_x, self._home_y)
        self._heading = self._home_heading
        self.draw_turtle()
    def setheading(self, to_angle):
        self._heading = to_angle / self._degree_per_au
        self.draw_turtle()
    def xcor(self):
        return self.x
    def ycor(self):
        return self.y
    def setx(self, x):
        self.goto(x, self.y)
        self.draw_turtle()
    def sety(self, y):
        self.goto(self.x, y)
        self.draw_turtle()
    def position(self):
        return (self.x, self.y)
    def pos(self):
        return self.position()
    def isvisible(self):
        return self._shown
    def penup(self):
        self._drawing = False
    def pendown(self):
        self._drawing = True
    def isdown(self):
        return self._drawing
    def pensize(self, width):
        self._pensize = width
        ti_graphics.setPen(width, 0)
    def pencolor(self, r, g=None, b=None):
        if g is None and b is None:
            self._pencolor = r
        else:
            self._pencolor = (r, g, b)
    def fillcolor(self, r, g=None, b=None):
        if g is None and b is None:
            self._fillcolor = r
        else:
            self._fillcolor = (r, g, b)
    def begin_fill(self):
        self._filling = True
        self._fill_path = [(int(self.x), int(self.y))]
    def end_fill(self):
        self._filling = False
        # +30 offset for status bar
        if len(self._fill_path) >= 3:
            path = [self._ltov(x, y) for x, y in self._fill_path]
            ti_graphics.setColor(self._fillcolor)
            ti_graphics.fillPolygon(path)
            self._record(('fill', self._filling, path, self._fillcolor))
        self._fill_path.clear()
    def filling(self):
        return self._filling
    def draw_turtle(self):
        #clear the one from before by drawing white polygon
        if self.tx is not None:
            ti_graphics.setColor((255, 255, 255))
            ti_graphics.drawPolyLine([(self.tx, self.ty), (self.lx, self.ly), (self.rx, self.ry), (self.tx, self.ty)])
        if not self._shown:
            ti_system.sleep(self._delay / 1000) #to seconds
            return
        c = math.cos(self._heading)
        s = math.sin(self._heading)

        self.tx, self.ty = self._ltov(self.x, self.y)
        self.lx, self.ly = self._ltov(self.x + (-12 * c - 6 * s), self.y + (-12 * s + 6 * c))
        self.rx, self.ry = self._ltov(self.x + (-12 * c + 6 * s), self.y + (-12 * s - 6 * c)) 

        ti_graphics.setColor(self._pencolor)
        ti_graphics.drawPolyLine([(self.tx, self.ty), (self.lx, self.ly), (self.rx, self.ry), (self.tx, self.ty)])
        ti_system.sleep(self._delay / 1000) #to seconds
    def clear(self):
        self._lines.clear()
        self._history.clear()
        self._fill_path.clear()
        self._filling = False
        ti_graphics.cls()
        self.draw_turtle()
    def clearstamps(self):
        #get rid of stamps in histor and then redraw
        old = self._history
        self._history = [action for action in self._history if action[0] != 'stamp']
        if len(old) != len(self._history):
            ti_graphics.cls()
        self.redraw()
    def circle(self, radius, extent=None, segments=None):
        radius = -radius #make circle draw in right place
        if extent is None:
            extent = self._full_circle
        extent_rad = -(extent / self._degree_per_au)
        state_before = (
            self.x, self.y, self._heading,
            self._drawing, self._filling, self._pencolor, self._fillcolor, self._pensize
        )
        #if segments is none, then we use drawArc for speed because users don't have a choice lol
        if segments is not None and segments > 0:
            r_abs = abs(radius)
            if radius >= 0:
                cx = self.x - r_abs * math.sin(self._heading)
                cy = self.y + r_abs * math.cos(self._heading)
            else:
                cx = self.x + r_abs * math.sin(self._heading)
                cy = self.y - r_abs * math.cos(self._heading)
            angle = math.atan2(self.y - cy, self.x - cx)
            dtheta = extent_rad / segments
            for i in range(segments):
                angle += dtheta
                self._heading += dtheta
                nx = cx + r_abs * math.cos(angle)
                ny = cy + r_abs * math.sin(angle)
                self._step_to(nx, ny)
            return
        # native drawArc implementation
        extent_rad = -extent_rad #flip for drawArc
        r_abs = abs(radius)
        if radius >= 0:
            cx = self.x - r_abs * math.sin(self._heading)
            cy = self.y + r_abs * math.cos(self._heading)
        else:
            cx = self.x + r_abs * math.sin(self._heading)
            cy = self.y - r_abs * math.cos(self._heading)
        scale = 3600.0 / (2 * math.pi)
        start_deg = int(round(math.atan2(self.y - cy, self.x - cx) * scale))
        sweep_deg = int(round(extent_rad * scale))

        box_x = int(round(cx - r_abs))
        box_y = int(round(cy - r_abs))
        diameter = int(round(2 * r_abs))
        box_x, box_y = self._ltov(box_x, box_y)

        if self._drawing:
            ti_graphics.setColor(self._pencolor)
            ti_graphics.drawArc(box_x, box_y, diameter, diameter, start_deg, sweep_deg)
        if self._filling:
            ti_graphics.setColor(self._fillcolor)
            ti_graphics.fillArc(box_x, box_y, diameter, diameter, start_deg, sweep_deg)
        end_angle = math.atan2(self.y - cy, self.x - cx) + extent_rad
        self.x = cx + r_abs * math.cos(end_angle)
        self.y = cy + r_abs * math.sin(end_angle)
        self._heading += extent_rad
        self._record(('arc', 
                      state_before,
                      (box_x, box_y, diameter, start_deg, sweep_deg),
                      (self.x, self.y, self._heading)))
        self.draw_turtle()
    def dot(self, size=1, color=None):
        color_before = self._pencolor
        if color is None:
            color = self._pencolor
        state_before = (
            self.x, self.y, self._heading,
            self._drawing, self._filling, self._pencolor, self._fillcolor, self._pensize
        )
        x, y = self._ltov(self.x, self.y)
        ti_graphics.setColor(color)
        ti_graphics.fillCircle(int(x), int(y), int(size))

        self._record(('dot', state_before, (x, y, size, color), (self.x, self.y, self._heading)))
        self._pencolor = color_before
    def write(self, text, move=False, font=None, align="left"):
        if font is None:
            ti_graphics.setFont(ti_graphics.Font.MEDIUM)
        else:
            ti_graphics.setFont(font)
        state_before = (
            self.x, self.y, self._heading,
            self._drawing, self._filling, self._pencolor, self._fillcolor, self._pensize
        )
        x, y = self._ltov(self.x, self.y)
        text_width, _ = ti_graphics.string_size(str(text))
        if align == "right":
            x -= text_width
        elif align == "center":
            x -= text_width // 2
        ti_graphics.setColor(self._pencolor)
        ti_graphics.drawString(str(text), int(x), int(y))
        if move:
            if align == "center":
                self.x += text_width // 2
            elif align == "left":
                self.x += text_width
        self._record(('write', state_before, (x, y, text, font, align), (self.x, self.y, self._heading)))
        self.draw_turtle()
    def _redraw_recent(self, count=5):
        for action in self._history[-count:]:
            action_type = action[0]
            if action_type == 'line':
                _, state_before, seg, _ = action
                if seg is not None:
                    self._draw_segment(seg)
            elif action_type == 'arc':
                _, state_before, arc_params, _ = action
                box_x, box_y, diameter, start_deg, sweep_deg = arc_params
                if state_before[3]:
                    ti_graphics.setColor(state_before[5])
                    ti_graphics.drawArc(box_x, box_y, diameter, diameter, start_deg, sweep_deg)
                if state_before[4]:
                    ti_graphics.setColor(state_before[6])
                    ti_graphics.fillArc(box_x, box_y, diameter, diameter, start_deg, sweep_deg)
            elif action_type == 'dot':
                _, state_before, dot_params, _ = action
                x, y, size, color = dot_params
                ti_graphics.setColor(color)
                ti_graphics.fillCircle(int(x), int(y), int(size))
            elif action_type == 'stamp':
                _, _, stamp_coords, stamp_color = action
                tx, ty, lx, ly, rx, ry = stamp_coords
                ti_graphics.setColor(stamp_color)
                ti_graphics.drawPolyLine([(tx, ty), (lx, ly), (rx, ry), (tx, ty)])
            elif action_type == 'write':
                _, state_before, write_params, _ = action
                x, y, text, font, align = write_params
                ti_graphics.setFont(font)
                ti_graphics.setColor(state_before[5])
                ti_graphics.drawString(str(text), int(x), int(y))
            elif action_type == 'fill':
                _, state_before, view_path, fill_color = action
                if len(view_path) >= 3:
                    ti_graphics.setColor(fill_color)
                    ti_graphics.fillPolygon(view_path)
    def redraw(self):
        self._redraw_recent(len(self._history))
    
    def done(self, sec=None):
        if sec is None:
            input()
        else:
            ti_system.sleep(sec)
    def undo(self):
        if not self._history:
            return

        last_action = self._history.pop()
        action_type = last_action[0]
        state_before = last_action[1]

        if action_type == 'line':
            _, _, seg, _ = last_action
            if seg is not None and seg in self._lines:
                self._lines.remove(seg)
        (
            self.x,
            self.y,
            self._heading,
            self._drawing,
            self._filling,
            self._pencolor,
            self._fillcolor,
            self._pensize,
        ) = state_before

        ti_graphics.cls()

        for action in self._history:
            kind = action[0]
            act_state_before = action[1]
            prev_drawing = act_state_before[3]
            prev_filling = act_state_before[4]
            prev_pencolor = act_state_before[5]
            prev_fillcolor = act_state_before[6]

            if kind == 'line':
                _, _, seg, _ = action
                if seg is not None:
                    self._draw_segment(seg)
            elif kind == 'arc':
                _, _, arc_params, _ = action
                box_x, box_y, diameter, start_deg, sweep_deg = arc_params
                if prev_drawing:
                    ti_graphics.setColor(prev_pencolor)
                    ti_graphics.drawArc(box_x, box_y, diameter, diameter, start_deg, sweep_deg)
                if prev_filling:
                    ti_graphics.setColor(prev_fillcolor)
                    ti_graphics.fillArc(box_x, box_y, diameter, diameter, start_deg, sweep_deg)
            elif kind == 'dot':
                _, _, dot_params, _ = action
                x, y, size, color = dot_params
                ti_graphics.setColor(color)
                ti_graphics.fillCircle(int(x), int(y), int(size))
            elif kind == 'write':
                _, _, write_params, _ = action
                x, y, text, font, align = write_params
                ti_graphics.setFont(font)
                ti_graphics.setColor(prev_pencolor)
                ti_graphics.drawString(str(text), int(x), int(y))
            elif kind == 'fill':
                _, _, view_path, fill_color = action
                if len(view_path) >= 3:
                    ti_graphics.setColor(fill_color)
                    ti_graphics.fillPolygon(view_path)
            elif kind == 'stamp':
                _, _, stamp_coords, stamp_color = action
                tx, ty, lx, ly, rx, ry = stamp_coords
                ti_graphics.setColor(stamp_color)
                ti_graphics.drawPolyLine([(tx, ty), (lx, ly), (rx, ry), (tx, ty)])

        self.draw_turtle()
    def showturtle(self):
        self._shown = True
        self.draw_turtle()
    def hideturtle(self):
        self._shown = False
        self.draw_turtle()
    #aliases
    fd = forward
    bk = backward
    lt = left
    rt = right
    pu = penup
    pd = pendown
    st = showturtle
    ht = hideturtle
    seth = setheading
    setpos = setposition = goto
    pos = position
    width = pensize

#basis
'''
>>> dir(turtle.Turtle)
['DEFAULT_ANGLEOFFSET', 'DEFAULT_ANGLEORIENT', 'DEFAULT_MODE',
'START_ORIENTATION', '__class__', '__delattr__', '__dict__',
'__dir__', '__doc__', '__eq__', '__firstlineno__', '__format__',
'__ge__', '__getattribute__', '__getstate__', '__gt__', 
'__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', 
'__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', 
'__repr__', '__setattr__', '__sizeof__', '__static_attributes__', 
'__str__', '__subclasshook__', '__weakref__', '_cc', '_clear', 
'_clearstamp', '_color', '_colorstr', '_delay', '_drawturtle', 
'_getshapepoly', '_go', '_goto', '_newLine', '_pen', '_polytrafo', 
'_reset', '_rotate', '_screen', '_setDegreesPerAU', '_setmode', 
'_tracer', '_undo', '_undogoto', '_update', '_update_data', 
'_write', 'back', 'backward', 'begin_fill', 'begin_poly', 'bk', 
'circle', 'clear', 'clearstamp', 'clearstamps', 'clone', 'color', 
'degrees', 'distance', 'dot', 'down', 'end_fill', 'end_poly', 
'fd', 'fill', 'fillcolor', 'filling', 'forward', 'get_poly', 
'get_shapepoly', 'getpen', 'getscreen', 'getturtle', 'goto', 
'heading', 'hideturtle', 'home', 'ht', 'isdown', 'isvisible', 
'left', 'lt', 'onclick', 'ondrag', 'onrelease', 'pd', 'pen', 
'pencolor', 'pendown', 'pensize', 'penup', 'poly', 'pos', 
'position', 'pu', 'radians', 'reset', 'resizemode', 'right', 
'rt', 'screens', 'seth', 'setheading', 'setpos', 'setposition', 
'setundobuffer', 'setx', 'sety', 'shape', 'shapesize', 
'shapetransform', 'shearfactor', 'showturtle', 'speed', 'st', 
'stamp', 'teleport', 'tilt', 'tiltangle', 'towards', 
'turtlesize', 'undo', 'undobufferentries', 'up', 'width', 
'write', 'xcor', 'ycor']
'''
#calculator lib reference:
'''
['__class__', '__name__', 'Color', 'Font', 'Style',
 'checkImageExists', 'cls', 'drawArc', 'drawImage',
 'drawLine', 'drawPolyLine', 'drawRect', 'drawString',
 'fillArc', 'fillCircle', 'fillPolygon', 'fillRect',
 'getPixel', 'hsv_to_rgb', 'popImage', 'pushImage',
 'setColor', 'setFont', 'setPen', 'setPixel',
 'string_size']
'''