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

def find_features(document):
    words = word_tokenize(document)
    features = {}
    k = open('sentiment/all_words.pickle','rb')
    all_words = pickle.load(k)
    k.close()
    all_words = nltk.FreqDist(all_words)
    word_features = list(all_words.keys())[:5000]
    for w in word_features:
        features[w] = (w in words)
    return features

def load_model(file_path): 
    classifier_f = open(file_path, "rb")
    classifier = pickle.load(classifier_f)
    classifier_f.close()
    return classifier

def sentiment(text):
    MNB_Clf = load_model('sentiment/MNB_clf.pickle')
    ensemble_clf = Sentiment(MNB_Clf) 
    feats = find_features(text)
    return ensemble_clf.classify(feats), ensemble_clf.confidence(feats)
import sys
def main():
    sent = sys.argv[1]
    dic = {'pos':'positive','neg':'negative'}
    print("My experience says that the text is "+dic[sentiment(sent)[0]])

if __name__=="__main__":
    main()