import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import distutils.dir_util

#Make the screenshot folder if it doesn't exist
distutils.dir_util.mkpath("screenshots")

#start firefox with marionette
caps = DesiredCapabilities.FIREFOX
caps["marionette"] = True;
browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', capabilities=caps)

#TODO: Store this in a file & parse
#Not all have interstitials - OCV and DSP
sites = [("http://forbes.com", "forbes"),("http://hbr.com", "HBR"), 
    ("https://www.techwalla.com/articles/how-to-convert-int-to-string-in-python", "techwalla"),
    ("http://www.dspguide.com/ch24/6.htm", "DSP"),
    ("http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html", "OCV"),
    ("https://www.theatlantic.com/business/archive/2013/02/how-airline-ticket-prices-fell-50-in-30-years-and-why-nobody-noticed/273506/", "ATL"),
    ("http://www.latimes.com/local/california/la-me-ln-irvine-immigrants-20170511-htmlstory.html", "LATimes"),
    ("https://www.searchenginejournal.com/counts-intrusive-interstitial/180023/", "SEJ")]
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
