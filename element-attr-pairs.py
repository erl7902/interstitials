from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join


elements = []
with open("htmelements.txt") as elem:
	for line in elem:
		elements.append(line.strip())
		
files = [('htmlgrabs/' + f)  for f in listdir('htmlgrabs') if f.endswith('.html')]


for filename in files: 
	with open(filename) as f, open(filename + "out.txt", "w+") as output: 
		soup = BeautifulSoup(f, "lxml")
		for element in elements:
			tags = soup(element)
			for tag in tags:
				for key,val in tag.attrs.items():
					output.write(element + " " + key + "\n")
