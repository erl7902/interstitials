import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import distutils.dir_util
import sys
import os
from itertools import groupby 

# Little helper function to split the input. 
# Assumes whitespace separated.
# "http://urlhere urlname" -> ["http://urlhere", "urlname"]
def readSites(filename): 
    sites = []
    with open(filename) as infile:
        for line in infile: 
            sites.append(line.split())

def runSelenium(sites):
    distutils.dir_util.mkpath("screenshots")
    #start firefox with marionette
    caps = DesiredCapabilities.FIREFOX
    caps["marionette"] = True;
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)
    browser = webdriver.Firefox(profile, executable_path='/usr/local/bin/geckodriver', capabilities=caps)
    #browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', capabilities=caps)

    iterations = 16

    for site in sites:
        browser.get(site[0])
        #for scrolling height
        height = browser.execute_script("return document.body.scrollHeight")
        jump = height / iterations
        prev = -1
        for x in range (0, iterations):
            # scroll 1/iteration down the page
            offset = browser.execute_script("return window.pageYOffset")
            scrollTo = int(jump*(x+1))
            # This keeps us from grabbing multiple screencaps of the same area
            # Due to weird issues with page height being reported incorrectly
            # TODO: revisit. 
            if((offset == prev) and (x > (iterations/2))):
                #print "breakpoint"            
                break
            location = site[1] + (str(x))
            browser.save_screenshot("screenshots/" + location)
            script = "window.scrollTo(0,%d);" % scrollTo 
            browser.execute_script(script)
            prev = offset
            #wait- try to catch interstitials
            time.sleep(3)

    browser.quit()    

if __name__ == "__main__":
    
    runSelenium(readSites(sys.argv[1]))
