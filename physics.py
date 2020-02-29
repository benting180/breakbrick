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
    if a.y2 > b.y1:
        if a.x2 > b.x1 and a.x1 < b.x2:
            return True
    return False

def collide_boundary(a, wall):
    pass
    if b.y > wall.y2:
        return 'down'
        # remove_i.append(i)
        # print("remove!")
        # self.seeds.pop(i)
    if b.x + b.r > wall.x2:
        b.x = wall.x2 - b.r

        b.rebound_x()
    if b.x - b.r < wall.x1:
        b.x = wall.x1 + b.r
        b.rebound_x()
    if b.y - b.r < wall.y1:
        b.rebound_y()
        b.y = wall.y1 + b.r