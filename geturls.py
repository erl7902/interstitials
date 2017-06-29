import json
import os

with open('latimes-list') as f_in, open('temp-list', 'w') as f_out: 
    for line in f_in:
        if len(line) > 1:
            parsed = json.loads(line.strip())
            f_out.write(parsed['url'] + '\n')
        
