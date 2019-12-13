from p5 import *
class Charge:
    id = 0
    mag = 0
    y = 0
    x = 0
    vy = 0
    vx = 0
    ay = 0
    ax = 0
    fixed = None
    loc = None
    vel = None
    acc = None
    col = None
    _array = []
    def __init__(self,_id,_mag,*args,fix = False,col = None):
        self.id = _id
        self.mag = _mag
        (self.x, self.y)=args
        self.fixed = fix
        self.loc = Vector(self.x,self.y)
        self.vel = Vector(self.vx,self.vy)
        self.acc = Vector(self.ax,self.ay)
        self.col = col
        self._array = [id,self.mag,*args]
        
    def veloc(self,_x,_y):
        self.vx = _x
        self.vy = _y
        self.vel = Vector(self.vx,self.vy)

    def accel(self,_x,_y):
        self.ax = _x
        self.ay = _y
        self.acc = Vector(self.ax,self.ay)
 
    def update(self):
        self.vel += self.acc
        self.loc += self.vel
        self.acc.limit(5)
        self.vel.limit(5)

    def display(self):
        col = ((255,0,0)if self.mag>0 else (0,0,255)) if self.col == None else self.col
        fill(*col)
        circle((self.loc.x,self.loc.y),abs(self.mag))
    
    def copy(self):
        return self.__class__(*self._array)