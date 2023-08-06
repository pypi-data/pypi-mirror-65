import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
import re
import os

class Sentiment(ClassifierI):
    
    def __init__(self, *classifiers):
        self._classifiers = classifiers
    
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)
    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

def load_model(file_path): 
    classifier_f = open(file_path, "rb")
    classifier = pickle.load(classifier_f)
    classifier_f.close()
    return classifier

def sentiment(text):
    MNB_Clf = load_model('MNB_clf.pickle')
    ensemble_clf = Sentiment(MNB_Clf) 
    feature_list = [f[0] for f in testing_set]
    ensemble_preds = [ensemble_clf.classify(features) for features in feature_list]
    feats = find_features(text)
    return ensemble_clf.classify(feats), ensemble_clf.confidence(feats)

def main():
    try:
        sent = sys.argv[1]
        print(sentiment(sent)) 	
    except:
        print("Exception occurred")
if __name__=="__main__":
    main()