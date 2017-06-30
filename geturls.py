import json
import os
import tldextract
import requests
import random

#TODO: use this in conjunction with cdx-client to strip incoming data.
'''with open('latimes-list') as f_in, open('temp-list', 'w') as f_out: 
    for line in f_in:
        if len(line) > 1:
            parsed = json.loads(line.strip())
            f_out.write(parsed['url'] + '\n')
'''
def get_from_common_crawl(domain):
    session = requests.Session()
    r = session.get('http://index.commoncrawl.org/CC-MAIN-2017-22-index?url=%2A.'+ domain +'&fl=url&page=0', stream=True, timeout=30).content
    if ('No Captures found' in r):
        return None
    results = r.split("\n")
    return [x for x in results if (('robots.txt' not in x) and (x != ''))]


def main():
    with open("uniquedomains.txt") as domains, open("urllist.txt", "w+") as output: 
        counter = 0
        for domain in domains:
            print "domain: " + domain
            if counter > 200:
                return "done"
            results = get_from_common_crawl(domain)
            if(results):
                r = random.randint(0, len(results)-1)
                print results[r]
                domain = tldextract.extract(results[r]).domain
                output.write(domain + " " + results[r] + "\n")
                counter += 1


if __name__ == "__main__":
    main()


