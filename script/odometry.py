import motor
from plotter import Plotter
from kinematic import angle_diff, next_position
import numpy as np
from constants import R

if __name__=="__main__":
    P = np.array([0, 0, 0])
    plotter = Plotter(1000, 1000, 6)
    m = motor.motor()
    posa_a, pos_b = m.get_position()
    with open("odometry.txt", 'w') as fp:
        for j in range(len(P)):
            fp.write(str(P[j]))
            if(j < len(P) - 1):
                fp.write(" ")
            else:                   
                fp.write("\n")
        try:
            while(True):
                pos_a_new, pos_b_new = m.get_position()

                plotter.plot2(P[0], P[1])
                P = next_position(P, R * angle_diff(pos_a_new, posa_a), -R * angle_diff(pos_b_new, pos_b))
                posa_a = pos_a_new
                pos_b = pos_b_new
        
                for j in range(len(P)):
                    fp.write(str(P[j]))
                    if(j < len(P) - 1):
                        fp.write(" ")
                    else:                   
                        fp.write("\n")
        finally:
            m.stop()
            m.unclock()