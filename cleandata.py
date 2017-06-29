import sys
import string
import requests
import tldextract
#First argument is data input
#Second argument is data output

def flip(url):
    url = url.split(".")
    return ('.'.join(url[::-1]))


def main():
    theinput = sys.argv[1]
    outloc = sys.argv[2]

    lines = []

    with open(theinput) as f: 
        lines = f.readlines()

    output = []
    for line in lines: 
        res = filter(lambda x: len(x) > 4, line.split("\\00"))
        output.append(res)
	
    with open(outloc, "w+") as r: 
        for line in output:
            for i in range(0, len(line)): # in line:
                url = line[i]
                #Clean up some of the artifacts
                if (url[-1] == ':'):
                    url = url[:-1]
                if(url[-5:] == ":http"):
                    url = url[:-5]
                first_slash = string.find(url, '/')
                if(first_slash == -1): 
                    url = (flip(url))
                else:
                    url = (flip(url[0:first_slash])) #+ url[first_slash:]) just want the sub, domain, and TLD
                    '''try:                
                        req = requests.head("http://" + url, timeout = 1)
                        rs = requests.head("https://" + url, timeout = 1)
                        rnumber = req.status_code
                        print rnumber
                        rsnumber = rs.status_code
                        print rsnumber
                        if ((rnumber < 300 and rsnumber > 199) or (rsnumber < 300 and rsnumber > 199)):'''
                extracted = tldextract.extract(url)
                url = extracted.domain + '.' + extracted.suffix              
                r.write(url + "\n")

if __name__ == "__main__":
    main()
