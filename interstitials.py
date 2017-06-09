#!/usr/bin/env python3

import distutils.dir_util
from seleniumTest import runSelenium
from seleniumTest import readSites
from houghTrans import houghLines
import sys
import os
import argparse
from itertools import chain
from collections import Counter

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
    sites = readSites(args.sites)
    # Skip selenium step by adding arg
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
        print (site[1] + ": %f" % (getConfidence(candidates)))


# So we want to find duplicates. 
# A duplicate is a line that persists over multiple images
# TODO: there may be some fluctuation on theta & rho values
def getConfidence(candidates):
    maxConf = 7
    confidence = 0
    results = []
    #If line appears more than once....keep it) 
    #Intersect lists and see what pops up
    results = Counter(list(chain(*candidates)))
    if (results):
        pruned = {k:v for k,v in results.items() if v > 1}
        prunedMore = {k:v for k,v in results.items() if v > 4}
        looseVert = {(rho,theta):v for (rho,theta),v in pruned.items() if theta  == 0}
        looseHorz = {(rho,theta):v for (rho,theta),v in pruned.items() if ((abs(1.57 - theta) < .005))}
        tightVert = {k:v for k,v in looseVert.items() if v > 4}
        tightHorz = {k:v for k,v in looseHorz.items() if v > 4}
        if(pruned):
            confidence += 1
        if(prunedMore): 
            confidence += 2 
        if(len(looseVert) > 1 and len(looseHorz) > 1): 
            confidence += 2
        if(len(tightVert) > 1 and len(tightHorz) > 1):
            confidence += 2
    return ((float(confidence)) / (float(maxConf)))
        

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
