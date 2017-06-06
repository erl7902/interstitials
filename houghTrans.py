# Adapted from http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html

import cv2
import numpy as np
import sys
import os
import distutils.dir_util

#Make the screenshot folder if it doesn't exist
distutils.dir_util.mkpath("results")

def main():
    screenshots = sys.argv[1] #Take in directory
    print screenshots
    for filename in os.listdir(screenshots):
        print screenshots+'/'+filename
        img = cv2.imread(screenshots + '/' + filename)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        hough(filename, img, edges)


def hough(filename, img, edges):
    lines = cv2.HoughLines(edges,1,np.pi/180,350)
    if(lines is None):
        print "No lines were found."
    else:
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            rise = y2 - y1
            run = x2 - x1
            #if vertical or horizontal
            if((run == 0) or (abs(float(rise)/(float(run))) < 0.01)):
                #Visualization part. Mostly for debugging, now.                 
                cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
                location = 'results/ModHough2-'+filename+'.jpg'
                cv2.imwrite(location,img)


if __name__ == "__main__":
    main()

'''
def rough_hough(filename, img, edges):
    minLineLength = 100
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    if(lines is None):
        print "No lines were found."
    else:
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        location = 'results/rHough' + filename + '.jpg'
        cv2.imwrite(location,img)
'''

