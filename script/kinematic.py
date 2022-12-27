import numpy as np
from constants import R, L

def next_position(previous, va, vb):
    x, y, o = previous
    if(va - vb == 0):
        on = o
        xn = x + va * np.cos(o)
        yn = y + va * np.sin(o)
        return np.array([xn, yn, on])
    else:
        OG = L/2 * (va + vb)/(vb - va)
        do = (vb - va) / L
        xn = x + OG * (np.sin(o + do) - np.sin(o))
        yn = y - OG * (np.cos(o + do) - np.cos(o))
        on = o + do
        return np.array([xn, yn, on])

def angle_diff(a,b):
    d = a - b
    if(d>np.pi):
        d -= 2*np.pi
    if(d<-np.pi):
        d += 2*np.pi
    return d

def point_to_point(p1, p2):
    d = p1 - p2[0:2]
    return [angle_diff(np.arctan2(d[1], d[0]), p2[2]), np.linalg.norm(d)]

def speed_control(vr, vl):
        return (vl + vr * L  * np.array([-1, 1]))/R