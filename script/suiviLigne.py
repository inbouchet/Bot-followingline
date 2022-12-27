from turtle import pos
import cv2
import numpy as np


def position(color_start, color_end, cam):
    S1 = 0
    S2 = 0
    n1 = 0
    n2 = 0

    _, img = cam.read()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_start, color_end)

    # ligne de test allant de mask[0,0] à mask[img.shape[0],0]
    for y1 in range(0, img.shape[1]):
        if (mask[200, y1] == 255):
            S1 += y1
            n1 += 1

    # for y2 in range (img.shape[0],0, -1):
    #   if(mask[200,y2] == 255):
    #     B = y2
    #     break

    for y3 in range(0, img.shape[1]):
        if (mask[300, y3] == 255):
            S2 += y3
            n2 += 1

    # for y4 in range (img.shape[0],0, -1):
    #   if(mask[300,y4] == 255):
    #     D = y4
    #     break

    # position_x = 200
    # position_y =(((A + B)/2) + ((C + D)/2))/2

    if n2 == 0 and n1 == 0:
        position_y = 0
        position_x = 0
    elif n1 == 0:
        position_y = (S2 / n2)
        position_x = 300
    elif n2 == 0:
        position_y = (S1 / n1)
        position_x = 200
    else:
        position_y = ((S1 / n1) + (S2 / n2)) / 2
        position_x = 200

    # cv2.imshow('new_video',mask)

    return (position_x, position_y)


def get_swap(color_start, color_end, cam):
    _, img = cam.read()

    sum = 0

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_start, color_end)

    for x in range(0, img.shape[1]):
        if (mask[200, x] == 255):
            sum += 1
        if (mask[200, x] == 255):
            sum += 1

    if sum > 2 * (img.shape[1] * 0.5):
        return True

    return False
