import sys

import motor
import cv2
import numpy as np
from colors import Colors
from autopilot import Autopilot
from kinematic import speed_control
from suiviLigne import *
import time
from kinematic import angle_diff, next_position
from constants import R

MODE = "RACING"
(COLOR_START, COLOR_END) = Colors.GREEN.value
VID_WIDTH = 600
TARGET_X = VID_WIDTH // 2
MAX_SPEED = 1
DELTA_MAX = 1000
TRACK = 0

if __name__ == "__main__":

    if sys.argv.__len__() == 2:
        MODE = sys.argv[1]
    elif sys.argv.__len__() == 3:
        color = sys.argv[2]
        if color == "RED":
            TRACK = 2
            (COLOR_START, COLOR_END) = Colors.RED.value
        if color == "BLUE":
            TRACK = 1
            (COLOR_START, COLOR_END) = Colors.BLUE.value
        if color == "GREEN":
            (COLOR_START, COLOR_END) = Colors.GREEN.value
        if color == "BLACK":
            (COLOR_START, COLOR_END) = Colors.BLACK.value

    robot = motor.motor()
    cam = cv2.VideoCapture(0)
    VID_WIDTH = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    TARGET_X = VID_WIDTH // 2
    autopilot = Autopilot(MAX_SPEED, DELTA_MAX)
    yel_start, yel_end = Colors.YELLOW.value

    t = [0, 0, 0]
    t_start = time.time()
    t_end = 0


    P = np.array([0, 0, 0])
    pos_a, pos_b = robot.get_position()

    with open("main.txt", 'w') as fp:
        for j in range(len(P)):
            fp.write(str(P[j]))
            if(j < len(P) - 1):
                fp.write(" ")
            else:                   
                fp.write("\n")
        try:
            while True:
                t_end = time.time()
                if t_end - t_start > 10:
                    if get_swap(np.array(yel_start), np.array(yel_end), cam):
                        t[TRACK] = t_end - t_start
                        TRACK += 1
                        t_start = time.time()
                        if TRACK == 1:
                            (COLOR_START, COLOR_END) = Colors.BLUE.value
                        elif TRACK == 2:
                            (COLOR_START, COLOR_END) = Colors.RED.value
                        elif TRACK == 3:
                            robot.stop()
                            robot.unclock()
                            print(t[0], t[1], t[2])
                            break


                (y, x) = position(np.array(COLOR_START), np.array(COLOR_END), cam)

                print(TARGET_X, " ", VID_WIDTH, " ",x)

                delta = TARGET_X - x

                a = 0.0033
                b = 1000
                c = 6

                if TRACK == 0:
                    a = 0.0025
                    c = 25

                if TRACK == 1:
                    a = 0.0037
                    c = 14

                if np.absolute(delta) > 310 :
                    a = 0

                if np.absolute(delta) > 310 and TRACK == 1:
                    delta = - np.absolute(delta)
                    a = 0.001

                if np.absolute(delta) > 310 and TRACK == 2:
                    delta = np.absolute(delta)
                    a = 0.001

                [speed_1, speed_2] = speed_control(a * delta, np.exp(-delta * delta / b / b) * c)

                print(speed_1, " ", speed_2)
                robot.move(left_value=speed_1, right_value=speed_2)

                pos_a_new, pos_b_new = robot.get_position()

                P = next_position(P, R * angle_diff(pos_a_new, pos_a), -R * angle_diff(pos_b_new, pos_b))
                pos_a = pos_a_new
                pos_b = pos_b_new
                
                for j in range(len(P)):
                    fp.write(str(P[j]))
                    if(j < len(P) - 1):
                        fp.write(" ")
                    else:                   
                        fp.write("\n")
        finally:
            print("exit")
            cam.release()
            cv2.destroyAllWindows()
            robot.stop()
            robot.unclock()
