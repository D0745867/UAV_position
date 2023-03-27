#!/usr/bin/env python
import cv2
import numpy as np

def qrdetector(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,150,300,apertureSize = 3)
    im2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours):
        hierarchy = hierarchy[0]
    for i in range(len(contours)):
        k = i
        c = 0
        while hierarchy[k][2] != -1:
            k = hierarchy[k][2]
            c = c + 1
        if hierarchy[k][2] != -1:
            c = c + 1
        if c >= 5:
            yield contours[i] 