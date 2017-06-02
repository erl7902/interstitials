# -*- coding: utf-8 -*-

# adapted from https://stackoverflow.com/a/3935002
# and http://miriamposner.com/classes/medimages/3-use-opencv-to-find-the-average-color-of-an-image/


import sys
import numpy as np

from scipy.ndimage import imread
from scipy.misc import imresize
from scipy.linalg import norm
from scipy import sum, average

def main():
    file1, file2 = sys.argv[1:1+2]
    # read images as 2D arrays (convert to grayscale for simplicity)
    img1 = imread(file1)
    img2 = imread(file2)
    img2 = imresize(img2, (img1.shape[0], img1.shape[1]))
    #img1 = to_grayscale(img1.astype(float))
    #img2 = to_grayscale(img2.astype(float))
    

    # compare
    # Use SLIC to create grids of superpixels
    # Get the avg color of each superpixel
    # Intersect the two arrays of averages
    # Number of remaining numbers represents differences
    # Might be better just to do rows of pixels?
    # Should capture the scrolling behavior well? Maybe?
    
    # Since they're already the same size....
    
    nm = compare(img1, img2)
    print ("Num rows: ", nm)

    #n_m, n_0 = compare_images(img1, img2)
    #print ("Manhattan norm:", n_m, "/ per pixel:", n_m/img1.size)
    #print ("Zero norm:", n_0, "/ per pixel:", n_0*1.0/img1.size)


def compare(img1, img2):
    #Creates an array of the average color along each row
    i1 = np.average(img1, 0)
    i2 = np.average(img2, 0)
    found = intersect(i1, i2)
    return len(found)
    
def intersect(A,B):
    C=[]
    for a in A:
        for b in B:
            if (not (all(a==b))):
                C.append(a)
    return C

def compare_images(img1, img2):
    # normalize to compensate for exposure difference, this may be unnecessary
    # consider disabling it
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)

def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

if __name__ == "__main__":
    main()
