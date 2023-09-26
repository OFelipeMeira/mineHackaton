import numpy as np
import cv2
from pylibdmtx import pylibdmtx
import time

def scan_matrix():

    #set up camera object
    cap = cv2.VideoCapture(0)

    while True:

        #get the image
        _, img = cap.read()

        #image = cv2.imread('datamatrix_sample1_130x116.png', cv2.IMREAD_UNCHANGED);

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        msg = pylibdmtx.decode(thresh, max_count=1, threshold=50, min_edge=20, max_edge=60)

        
        if msg:
            return(str(msg[0].data, "utf-8"))