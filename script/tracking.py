"""
desplaying map
"""
from turtle import color
from cv2 import split
import matplotlib.pyplot as plt
import numpy as np
 
def display_map():
    x1 = [0.0]
    y1 = [0.0]
    x2 = [0.0]
    y2 = [0.0]
    x3 = [0.0]
    y3 = [0.0]
    
    f = open('main.txt','r')
    n = 0
    for row in f:
        if n>0: 
            row = row.split(' ')
            if row[4] == '1\n':
                x1.append((float(row[0])))
                y1.append((float(row[1])))
            if row[4] == '2\n':
                x2.append((float(row[0])))
                y2.append((float(row[1])))
            if row[4] == '3\n':
                x3.append((float(row[0])))
                y3.append((float(row[1])))
        n += 1

    plt.title("tracking 1")
    plt.plot(np.array(x1),np.array(y1),color='green')
    plt.axis("equal")
    plt.savefig('tracking1.png')
    plt.show()

    plt.title("tracking 2")
    plt.plot(np.array(x2),np.array(y2),color='blue')
    plt.axis("equal")
    plt.savefig('tracking2.png')
    plt.show()

    plt.title("tracking 3")
    plt.plot(np.array(x3),np.array(y3),color='red')
    plt.axis("equal")
    plt.savefig('tracking3.png')
    plt.show()
        

if __name__ == "__main__" :
    display_map()
