import sys
import os
import pickle
from sklearn import datasets, svm, metrics
from collections import defaultdict
from sklearn.semi_supervised import label_propagation

# walk through the folder and pull all 'out.txt' files
# send files to other function
def mass_feature_gen(folder):
    ordered_lst = get_feature_order()
    mass_features = []
    ground_truth = []
    ys = [] 
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith('.data'):
                newfile = root + "/" + f.split('.')[0] + ".data"  
                with open(newfile, "rb") as inp: 
                    features = pickle.load(inp)
                    #truth = (root.split("/")[-1]).lower()
                    # We're going to have to use integers real quick
                    # 0 is going to be no interstitial, 1 yes, -1 unlabeled. 
                    path = root.split("/")
                    #ground_truth.append(path[-1].lower())
                    if(path[-2] == 'hand-labeled'):
                        mass_features.append(order(features, ordered_lst))
                        if(path[-1].lower() == "no"):
                            ys.append(0) 
                            ground_truth.append(0)
                        elif(path[-1].lower() == "yes"):
                            ys.append(1)
                            ground_truth.append(1)
                        #ys.append(path[-1].lower())
                    else:
                        if(path[-1].lower() == "no"):
                            ys.append(-1) 
                            ground_truth.append(0)
                            mass_features.append(order(features, ordered_lst))
                        elif(path[-1].lower() == "yes"):
                            ys.append(1)
                            ground_truth.append(1)
                            mass_features.append(order(features, ordered_lst))
                        #ys.append(path[-1].lower())
                        
                    #ground_truth.append(truth)
    #classifier = svm.SVC(gamma=0.001)
    classifier = label_propagation.LabelSpreading()
    # We learn the digits on the first half of the digits
    n_samples = len(mass_features)
    #classifier.fit(mass_features[:n_samples // 2], ground_truth[:n_samples // 2])
    classifier.fit(mass_features, ys)

    # Now predict the value of the digit on the second half:
    expected = ground_truth
    predicted = classifier.predict(mass_features)

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
        

