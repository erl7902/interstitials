import distutils.dir_util
from seleniumTest import runSelenium
from seleniumTest import readSites
from houghTrans import houghLines
import sys
import os
import argparse

# Take in filename of list of sites.
# Run selenium.
# feed results into houghTrans, one group at a time.
# Take those results, analyze using heuristics.
# Spit out a yes or no for each group of images.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sites", help="filename for list of sites to use")
    parser.add_argument("--s", help="include to skip selenium step", action="store_true")
    args = parser.parse_args()
    # Run selenium
    sites = readSites(args.sites)
    # Fast & dirty option to skip selenium by adding more args
    if(not args.s):
        runSelenium(sites)
    # Now we have screenshots located at ./screenshots
    # TODO: make directory customizable. Low priority
    for site in sites:
        images = pullImages(site[1], "screenshots")
        # Now we have a group. Throw that into Hough
        # Bonus: also filters to only include horiz/vertical lines
        candidates = houghLines(images)     
        # From candidates, we want to see the ones that persist
        persists = pruneLines(candidates)


# So we want to find duplicates. 
# A duplicate is a line that persists over multiple images
# However, there may be some fluctuation on theta & rho values
def pruneLines(candidates):
    results = []
    # If line appears more than once....keep it) 
    # Intersect lists and see what pops up
    for lineList in candidates:
        print lineList
         
		

#rho, theta values
def isSame(line1, line2):
    if(abs(line1[0] - line2[0]) < 2):
        if(abs(line1[1] - line2[1]) < 0.005):
            return True
    return False 
        

# Pull the list of images we need for each part
# E.g. substr = "Forbes", 
# we pull [screenshots/ImgForbes01, screenshots/ImgForbes02]
def pullImages(substr, dirToSearch):
    result = []
    for filename in os.listdir(dirToSearch):
        if substr in filename: 
            result.append(dirToSearch + "/" + filename)
    return result
        
    


if __name__ == "__main__":
    main()
