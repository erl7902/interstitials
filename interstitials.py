import distutils.dir_util
from seleniumTest import runSelenium
from seleniumTest import readSites
from houghTrans import houghLines

# Take in filename of list of sites.
# Run selenium.
# feed results into houghTrans, one group at a time.
# Take those results, analyze using heuristics.
# Spit out a yes or no for each group of images.
def main():
    # Run selenium
    sites = readSites(sys.argv[1])
    runSelenium(sites)
    # Now we have screenshots located at ./screenshots
    # TODO: make directory customizable. Low priority
    for site in sites:
        images = pullImages(sites[1], "screenshots")
        # Now we have a group. Throw that into Hough
        candidates = houghLines(images)
        # From candidates, start applying heuristics
        # See: notepad at work for details.
        

# Pull the list of images we need for each part
# E.g. substr = "Forbes", 
# we pull [screenshots/ImgForbes01, screenshots/ImgForbes02]
def pullImages(substr, dirToSearch):
    result = []
    for filename in os.listdir(dirToSearch):
        if substr in filename: 
            results.append(dirToSearch + "/" + filename)
    return result
        
    


if __name__ == "__main__":
    main()
