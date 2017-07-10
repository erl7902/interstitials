#!/usr/bin/env python3

import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import distutils.dir_util
import sys
import os
from itertools import groupby
from bs4 import BeautifulSoup 

# Little helper function to split the input. 
# Assumes whitespace separated.
# "urlname http://urlhere" -> ["urlname", "http://urlhere"]
def readSites(filename): 
    sites = []
    with open(filename) as infile:
        for line in infile: 
            sites.append(line.split())
    return sites

#TODO make target directory customizable
def runSelenium(sites):
    distutils.dir_util.mkpath("screenshots")
    distutils.dir_util.mkpath("htmlgrabs")
    #start firefox with marionette
    caps = DesiredCapabilities.FIREFOX
    caps["marionette"] = True;
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)
    browser = webdriver.Firefox(profile, executable_path='/usr/local/bin/geckodriver', capabilities=caps)

    iterations = 16

    for site in sites:
        location = "screenshots/" + site[0]
        distutils.dir_util.mkpath(location)
        try: 
            browser.get(site[1])
            content = browser.page_source
            soup = BeautifulSoup(content, "lxml")
            with open("htmlgrabs/" + site[0], "w+") as f:
                for line in soup.prettify('utf-8', 'minimal'):
                    f.write(str(line))
            #for scrolling height
            height = browser.execute_script("return document.body.scrollHeight")
            jump = height / iterations
            prev = -1
            distutils.dir_util.mkpath(site[0])
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
                location = site[0] + (str(x))
                browser.save_screenshot("screenshots/" + site[0] + "/" + location + ".png")
                script = "window.scrollTo(0,%d);" % scrollTo 
                browser.execute_script(script)
                prev = offset
                #wait- try to catch interstitials
                time.sleep(3)
            
        except: 
            continue

    browser.quit()    

if __name__ == "__main__":
    
    runSelenium(readSites(sys.argv[1]))
