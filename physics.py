from shape import Rectangle, MovableRectangle
from shape import Circle, MovableCircle
from shape import Stand


def collide(input, x):
    # seed - brick
    # seed - wall
    # seed - stand
    # stand - reward
    # seed - 
    pass
    # if type(input) == 

def collide_up(a, b):
    # a hit b
    if a.y < b.y1 and a.y2 > b.y1:
        if a.x2 > b.x1 and a.x1 < b.x2:
            return True
    return False

def collide_down(a, b):
    if a.y > b.y2 and a.y1 < b.y2:
        if a.x > b.x1 and a.x < b.x2:
            return True
    return False

def collide_left(a, b):
    if a.x < b.x1 and a.x2 > b.x1:
        if a.y > b.y1 and a.y < b.y2:
            return True
    return False

def collide_right(a, b):
    if a.x > b.x2 and a.x1 < b.x2:
        if a.y > b.y1 and a.y < b.y2:
            return True
    return False

def collide_which_side(a, b):
    up = collide_up(a, b)
    down = collide_down(a, b)
    left = collide_left(a, b)
    right = collide_right(a, b)
    assert up + down + left + right <= 1, "collide more than one side at a time!"
    if up:
        return 'up'
    elif down:
        return 'down'
    elif left:
        return 'left'
    elif right:
        return 'right'
    else:
        return ''


def collide_boundary(a, wall):
    pass
    if a.y > wall.y2:
        return 'down'
        # remove_i.append(i)
        # print("remove!")
        # self.seeds.pop(i)
    if a.x + a.r > wall.x2:
        return 'right'
        a.x = wall.x2 - a.r

        a.rebound_x()
    if a.x - a.r < wall.x1:
        return 'left'
        a.x = wall.x1 + a.r
        a.rebound_x()
    if a.y - a.r < wall.y1:
        return 'up'
        a.rebound_y()
        a.y = wall.y1 + a.r