import sys
import os
import pickle
from sklearn import datasets, svm, metrics
from collections import defaultdict

# walk through the folder and pull all 'out.txt' files
# send files to other function
def mass_feature_gen(folder):
    ordered_lst = get_feature_order()
    mass_features = []
    ground_truth = []
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith('.data'):
                newfile = root + "/" + f.split('.')[0] + ".data"  
                with open(newfile, "r") as inp: 
                    features = pickle.load(inp)
                    mass_features.append(order(features, ordered_lst))
                    truth = (root.split("/")[-1]).lower()
                    ground_truth.append(truth)
    classifier = svm.SVC(gamma=0.001)
    # We learn the digits on the first half of the digits
    n_samples = len(mass_features)
    classifier.fit(mass_features[:n_samples // 2], ground_truth[:n_samples // 2])

    # Now predict the value of the digit on the second half:
    expected = ground_truth[n_samples // 2:]
    predicted = classifier.predict(mass_features[n_samples // 2:])

    print("Classification report for classifier %s:\n%s\n"
        % (classifier, metrics.classification_report(expected, predicted)))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

def get_feature_order():
    ordered_list = []
    with open("Elem-Attr-Feature-List.txt", "r") as lst: 
        for line in lst:
            elem,attr = line.split()
            ordered_list.append((elem,attr))
    return ordered_list

def order(features, ordered_lst):
    ordered_features = [] 
    for pair in ordered_lst:
        ordered_features.append(features[pair])
    return ordered_features

if __name__ == "__main__":
    
    mass_feature_gen(sys.argv[1])
        

