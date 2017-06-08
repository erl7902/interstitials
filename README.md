# interstitials
 Currently a giant mishmash of scripts to attempt to recognize interstitial ads on webpages.  
 Main two files are selenium-test, which crawls through for screenshots, and the hough-transform.  
 NOTE: will no longer be updating screenshots folder. Run selenium-test for most up-to-date data.

requirements
-------------
Everything should work on python3. Some things may not work on python2.
To run all scripts, you will need: 
* selenium's python driver installed, 
* geckodriver installed,
* a reasonably up-to-date version of Firefox, and
* the following python libraries: scipy, numpy, scikitlearn (specifically skimage), opencv, matplotlib.


interstitials.py
----------------
 Leverages selenium-test.py and hough-transform.py  
 ```
 interstitials.py list [--s]
 ```
 Takes in the list of sites - see list.txt for example  
 Add the optional --s flag to skip crawling the sites  
 Goes through, runs selenium-test, then feeds results into hough-transform  
 Currently just returns lines, will update to return yes/no for each site

selenium-test.py
----------------
 Leverages selenium, geckodriver, and firefox.  
 Currently will go through and take screenshots, saving them to a "screenshots" folder.  
 If you do not have a screenshots directory where you are running the script, it will make one for you.  
 It will not preserve screenshots between runs. You may wish to add a timestamp if you want to avoid overwriting.  
 Essential to run this before running the other scripts
 
hough-transform.py
-----------------
 Leverages opencv and numpy  
 Takes in the directory of the images   
 ``` 
 hough-transform.py [image-dir]
 ```
 Will dump them in a 'results' directory. Will make one if you don't have one  
 Optional: the two commented lines in the main pertain to a rough hough transformation.  
 Uncommenting it will duplicate the images, one with hough transform and one with rough.  
 If no lines are found, it'll simply write that to console and not copy over the image.   
