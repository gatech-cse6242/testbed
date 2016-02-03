from pickle import load, dump
from sklearn.svm import SVC
from random import shuffle
import numpy as np

if __name__ == '__main__':

    base_feature_file = 'feature_set.pickle'
    print 'Loading data'

    features = load(open(base_feature_file))

    train_feats = []
    test_feats = []
    train_classes = []
    test_classes = []

    feature_map = {}

    print 'Splitting data'

    for i, disease_class in enumerate(features.keys()):
        feats = features[disease_class]
        shuffle(feats)
        feature_map[i] = disease_class
        train_feats.extend( [feat[0].flatten() for feat in feats[:len(feats)/2]])
        test_feats.extend([feat[0].flatten() for feat in feats[len(feats)/2:]])
        train_classes.extend( [i for _ in range(0,len(feats)/2)])
        test_classes.extend( [i for _ in range(0,len(feats)/2)])


    train_set = (train_feats, train_classes)
    test_set  = (test_feats, test_classes)
    print 'Serializing test split'

    dump((train_set, test_set, feature_map), open( 'test_split.pickle', 'w'))


    print 'Training classifier'

    svc = SVC()
    svc.fit(train_feats, train_classes)

    print 'Serializing classifier'
    dump(svc, open('svc.pickle', 'w'))

    classifications = [ svc.predict( feat ) for feat in test_feats]

