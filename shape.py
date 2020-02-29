class Circle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.auto_complete()
    
    def auto_complete(self):
        self.cx = self.x
        self.cy = self.y
        self.x1 = self.x - self.r
        self.x2 = self.x + self.r
        self.y1 = self.y - self.r
        self.y2 = self.y + self.r

    def get_coord(self):
        return (int(self.x), int(self.y))

class MovableCircle(Circle):
    def __init__(self, x, y, r, vx, vy):
        super().__init__(x, y, r)
        self.vx = vx
        self.vy = vy
        self.speed = 300

    def nex(self, dt):
        self.x = self.x + self.vx * dt * self.speed
        self.y = self.y + self.vy * dt * self.speed
        self.auto_complete()

    def rebound_x(self):
        self.vx = -self.vx

    def rebound_y(self):
        self.vy = -self.vy

class Seed(MovableCircle):
    def __init__(self, x, y, r, vx, vy):
        super().__init__(x, y, r, vx, vy)
        self.speed = 300


class Rectangle(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.auto_complete()
    
    def auto_complete(self):
        self.cx = self.x + self.w / 2
        self.cy = self.y + self.h / 2
        self.x1 = self.x
        self.x2 = self.x + self.w
        self.y1 = self.y
        self.y2 = self.y + self.h
    
    def get_coord(self):
        return (int(self.cx), int(self.cy))
    
    def get_dim(self):
        return (int(self.x), int(self.y), int(self.w), int(self.h))


class MovableRectangle(Rectangle):
    def __init__(self, x, y, w, h, vx, vy):
        super().__init__(x, y, w, h)
        self.vx = vx
        self.vy = vy
        self.speed = 300
    
    def nex(self, dt):
        self.x = self.x + self.vx * dt * self.speed
        self.y = self.y + self.vy * dt * self.speed
        self.auto_complete()


class Stand(MovableRectangle):
    def __init__(self, x, y, w, h, vx=0, vy=0):
        super().__init__(x, y, w, h, vx, vy)
        
    def move_left(self, dt, x_min):
        self.x = self.x - dt * self.speed
        if self.x < x_min:
            self.x = x_min
        self.auto_complete()
        
    def move_right(self, dt, x_max):
        self.x = self.x + dt * self.speed
        if self.x > x_max - self.w:
            self.x = x_max - self.w
        self.auto_complete()


    def enlong(self):
        self.x -= 5
        self.w += 10
        self.auto_complete()
        # boundary checking

    def enshort(self):
        self.x += 5
        self.w -= 10
        self.auto_complete()
        # boundary checking


class Wall():
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        return

class Reward():
    def __init__(self, x, y, r=7, vx=0, vy=1):
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.update()
        self.speed = 300

    def update(self):
        self.x1 = self.x - self.r
        self.x2 = self.x + self.r
        self.y1 = self.y - self.r
        self.y2 = self.y + self.r
        self.w = self.r * 2
        self.h = self.r * 2
        return

    def nex(self, dt):
        self.x = self.x + self.vx * dt * self.speed
        self.y = self.y + self.vy * dt * self.speed
        self.update()
        return
    
    def get_coord(self):
        return (int(self.x), int(self.y))