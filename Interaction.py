from p5 import *
from Charge import *
from Plot import *
import numpy as np
import random as rand
from time import asctime

import os
import atexit


def init():
    global F_FRAME,F_PLOT
    if not F_FRAME in os.listdir():
        os.mkdir(F_FRAME)
    if not F_PLOT in os.listdir():
        os.mkdir(F_PLOT)

def setup():
    size(scr_x, scr_y)
    Print()

def draw():
    background(0)
    global Q, q, n, F, V, PAUSE, bg_thread
    stroke_weight(1)
    stroke(255)
    F = q.mag*E(q,Q)
    # V = pot(q,*Q)
    q.accel(F.x,F.y)
    update()
    q.display()
    for i in range(0,len(Q)):
        Q[i].update()
        Q[i].display()
    # if not PAUSE: prnt.append("L: ",q.loc,"V: ",q.vel.magnitude,"\tA: ",q.acc.magnitude)
    textDraw()

def update():
    global q,PAUSE
    if not PAUSE:
        q.update()

def textDraw():
    fill(255)
    data = []
    data.append("fps: "+str(frame_rate))
    data.append("x: "+str(round(q.loc.x,2))+"  y:"+str(round(q.loc.y,2)))
    data.append("vx: "+str(round(q.vel.x,2))+"  vy:"+str(round(q.vel.y,2)))
    data.append("ax: "+str(round(q.acc.x,5))+"  ay:"+str(round(q.acc.y,5)))
    # loc = "x: "+str(round(q.loc.x,1))+"  y:"+str(round(q.loc.y,1))
    # prnt.append(text_width(loc))
    for i in range(0,len(data)):
        text(data[i],(3 ,scr_y-15*(len(data)-i)))

    if PAUSE: text("PAUSED",(scr_x - text_width("PAUSED"),scr_y-30))
    text("Magnitude: "+str(Q_sign*Q_mag),(scr_x - text_width("Magnitude: "+str(Q_sign*Q_mag)),scr_y-15))
    text("("+str(mouse_x)+","+str(mouse_y)+")",(3 ,5))

def Print():
    global prnt
    os.system("clear")
    print("\n".join(prnt))

def mouse_pressed():
    if mouse_button == "LEFT":
        q.vel *= 0
        q.acc *= 0
        q.loc.x,q.loc.y = mouse_x,mouse_y
    if mouse_button == "RIGHT":
        Q.append(Charge(0,Q_sign*Q_mag,mouse_x,mouse_y))
    if mouse_button == "CENTER":
        for i in range(0,len(Q)):
            if (((mouse_x-Q[i].loc.x)**2)+((mouse_y-Q[i].loc.y)**2)) <= abs(Q[i].mag):
                del(Q[i])
                break

def mouse_wheel(event):
    global Q_mag
    Q_mag += event.count
    if Q_mag>15: 
        Q_mag = 15
    elif Q_mag<0:
        Q_mag = 0

def key_pressed():
    global PAUSE,th,Q_mag,Q_sign,prnt
    if key == "C" or key == "c":
        Q.clear()
    if key == "P" or key == "p" :
        prnt.append("Main: Printing!")
        a = asctime().split(" ")
        cur_td = a[2]+" "+a[1]+" "+a[4]+" "+a[3]
        try:
            save_frame("./Frames/Frame "+cur_td+".png")
            prnt.append("Main: Frame saved")
        except Exception as ex:
            template = "\
                Error: Could not save current frame!\n  \
                An exception of type {0} occurred. Cause:\n \
                {0} \
                "
            message = template.format(type(ex).__name__, ex.__cause__)
            prnt.append(message)
        savepoint(q,*Q,TS = cur_td)
        prnt.append("Main: Added savepoint("+str(len(SP))+")!")
    if key == "q":
        print(SP)
    if key == "UP":
        Q_mag+= 1 if Q_mag<15 else 0
    if key == "DOWN":
        Q_mag-= 1 if Q_mag>0 else 0
    if key == "RIGHT":
        Q_sign*= -1
    if key == " ":
        PAUSE = not PAUSE
        prnt.append("\nMain: "+("Paused" if PAUSE else "Played"))
    Print()

def savepoint(*args, **kwargs):
    arg=[]
    for x in args:
        arg.append(x.copy())
    arg = args
    SP.append((kwargs["TS"],arg))

def E(t,D):
    e = Vector(0,0)
    for i in  range(0,len(D)):
        e+=-D[i].mag*(D[i].loc-t.loc)/((D[i].loc-t.loc).magnitude)**3
    return e

def pot(*args):
    p = np.zeros((scr_y,scr_x))
    progress = []
    for j in range(0,scr_x):
        for i in range(0,scr_y):
            pos = Vector(j,i)
            v=0
            for x in args:
                v+=x.mag/(1 if (x.loc-pos).magnitude==0 else (x.loc-pos).magnitude)
            p[i][j] = v
            progress.append((i,j))
        prog = "Progress: "+str(len(progress)*100/(scr_x*scr_y))+"%"
        Print()
        print(prog)
    return p


def exit_handler():
    prnt.append("Main: Saving all plots!\n")
    for i in range(0,len(SP)):
        prnt.append(str(plot(scr_x,scr_y,pot(*SP[i][1]),dir_p = F_PLOT,TS=SP[i][0])))
        prnt.append("Main: Savepoint("+str(i+1)+") saved successfully\n")
        Print()

n = 0
k = 2
scr_x = 200
scr_y = 200
Q_mag = 0
Q_sign = 1
Q = []
for i in range(0,n):
    Q.append(Charge(i,Q_sign*Q_mag,rand.randint(0,scr_x),rand.randint(0,scr_y)))
q = Charge(1,10,scr_x/2,scr_y/2,col = (255,255,0))
V = None
PAUSE = False
F_FRAME = "Frames"
F_PLOT = "Plots"
th=False
bg_thread = None
SP = []
prnt = []
atexit.register(exit_handler)

if __name__ == "__main__":
    init()
    run()
