import os
import sys
from collections import defaultdict
import pickle

# Returns a zeroed out dictionary 
def elem_attr_list():
    elem_attrs = defaultdict(int)
    with open("Elem-Attr-Feature-List.txt", "r") as lst: 
        for line in lst:
            elem,attr = line.split() 
            elem_attrs[(elem,attr)] = 0
    return elem_attrs



# walk through the folder and pull all 'out.txt' files
# send files to other function
def mass_feature_gen(folder):
    d_dict = elem_attr_list()
    mass_features = []
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith('out.txt'):
                features = element_attr_feature_gen(root + "/" + f, d_dict)
                newfile = root + "/" + f.split('.')[0] + ".data" 
                with open(newfile, "w+") as output: 
                    pickle.dump(features,output)
                #mass_features.append(features)
    #print mass_features
    
            
def element_attr_feature_gen(filename, d_dict): 
    features = d_dict.copy()
    count = 0
    with open(filename, "r") as f:
        for line in f:
            # so we have element, attr, frequency
            elem,attr = line.split()
            attr = attr.split('-')[0]
            #key = elem + " " + attr
            features[(elem,attr)] += 1
    return features


if __name__ == "__main__":
    
    mass_feature_gen(sys.argv[1])
