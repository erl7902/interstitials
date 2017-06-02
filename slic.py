# import the necessary packages
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import matplotlib.pyplot as plt
import argparse
import cv2
import numpy as np
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())
 
# load the image and convert it to a floating point data type
image = img_as_float(cv2.imread(args["image"]))
 
# loop over the number of segments
for numSegments in (25, 100): #, 200, 300):
	# apply SLIC and extract (approximately) the supplied number
	# of segments
	segments = slic(image, n_segments = numSegments, sigma = 5, enforce_connectivity=True)
        print segments
	# show the output of SLIC
	fig = plt.figure("Superpixels -- %d segments" % (numSegments))
	ax = fig.add_subplot(1, 1, 1)
	ax.imshow(mark_boundaries(image, segments))
	plt.axis("off")
 
# show the plots
plt.show()

# loop over the unique segment values
for (i, segVal) in enumerate(np.unique(segments)):
	# construct a mask for the segment
	print "[x] inspecting segment %d" % (i)
        print segVal
	mask = np.zeros(image.shape[:2], dtype = "uint8")
	mask[segments == segVal] = 255
 
	# show the masked region
	cv2.imshow("Mask", mask)
	cv2.imshow("Applied", cv2.bitwise_and(image, image, mask = mask))
	cv2.waitKey(0)
