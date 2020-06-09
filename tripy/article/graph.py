#import plotly.graph_objects as go
from tripy.article.article import ALL_ARTICLES
from tripy.geo.locations import INDEX_BY_NAME
import numpy as np 
import matplotlib.pyplot as plt
import json
import os


class graph:
    def __init__(self, country):
        self._articles = ALL_ARTICLES[INDEX_BY_NAME[country]]
        self._total_words = []
        self._country = country
        self._neg_words = []
        self._pos_words = []
        self._stop_words = []
        self._total_total_word = 0
        self._total_neg_word = 0
        self._total_pos_word = 0
        self._total_stop_word = 0
        for i in range(len(self._articles)):
            self._total_words.append(self._articles[i].get_total_word())
            self._total_total_word += self._total_words[i]
            self._stop_words.append(self._articles[i].get_stopword_freq())
            self._total_stop_word += self._stop_words[i]
            self._pos_words.append(self._articles[i].get_pos_freq())
            self._total_pos_word += self._pos_words[i]
            self._neg_words.append(self._articles[i].get_neg_freq())
            self._total_neg_word += self._neg_words[i]

    def plot_all_graph(self, width):
        plt.clf()
        n = len(self._articles)
        index  = np.arange(n)
        plt.subplot(1,3,1)
        plt.bar(index, self._pos_words, width, label="Positive Word Count")
        plt.bar(index + width, self._neg_words, width, label="Negative Word Count")
        plt.ylabel("Word")
        plt.title("Number of Positive and Negative Word in "+self._country+" article")
        plt.xticks(index+width/2, index)
        plt.legend(loc='best')

        plt.subplot(1,3,2)
        plt.bar(index, self._total_words, width, label="Total Word Count")
        plt.bar(index + width, self._stop_words, width, label="Stop Word Count")
        plt.ylabel("Word")
        plt.title("Number of Stop Word in "+self._country+" article")
        plt.xticks(index+width/2, ('1','2','3','4','5'))
        plt.legend(loc='best')

        n = 1
        total_word = [self._total_total_word]
        neg_word = [self._total_neg_word]
        pos_word = [self._total_pos_word]
        stop_word =[self._total_stop_word]
        index  = np.arange(n)
        plt.subplot(1,3,3)
        plt.bar(index, total_word, width, label="Total Word Count")
        plt.bar(index + width, stop_word, width, label="Stop Word Count")
        plt.bar(index + 2 * width, pos_word, width, label="Positive Word Count")
        plt.bar(index + 3 * width, neg_word, width, label="Negative Word Count")
        plt.ylabel("Word")
        plt.title("Total type of words in "+self._country+" article")
        plt.xticks(index+width/2, index)
        plt.legend(loc='best')

        return plt.gcf()

    def plot_pos_neg(self, width):
        plt.clf()
        n = len(self._articles)
        index  = np.arange(n)
        plt.subplot(1,1,1)
        plt.bar(index, self._pos_words, width, label="Positive Word Count")
        plt.bar(index + width, self._neg_words, width, label="Negative Word Count")
        plt.ylabel("Word")
        plt.title("Number of Positive and Negative Word in "+self._country+" article")
        plt.xticks(index+width/2, index)
        plt.legend(loc='best')
        #plt.savefig('figure/'+self._country+'_pos_neg.svg')
        return plt.gcf()

    def plot_stop_words(self, width):
        plt.clf()
        n = len(self._articles)
        print(self._total_words)
        print(self._stop_words)
        index  = np.arange(n)
        plt.subplot(1,1,1)
        plt.bar(index, self._total_words, width, label="Total Word Count")
        plt.bar(index + width, self._stop_words, width, label="Stop Word Count")
        plt.ylabel("Word")
        plt.title("Number of Stop Word in "+self._country+" article")
        plt.xticks(index+width/2, ('1','2','3','4','5'))
        plt.legend(loc='best')
        #plt.savefig('figure/'+self._country+'_stop.svg')
        return plt.gcf()

    def plot_overall(self, width):
        plt.clf()
        n = 1
        total_word = [self._total_total_word]
        neg_word = [self._total_neg_word]
        pos_word = [self._total_pos_word]
        stop_word =[self._total_stop_word]
        index  = np.arange(n)
        plt.subplot(1,1,1)
        plt.bar(index, total_word, width, label="Total Word Count")
        plt.bar(index + width, stop_word, width, label="Stop Word Count")
        plt.bar(index + 2 * width, pos_word, width, label="Positive Word Count")
        plt.bar(index + 3 * width, neg_word, width, label="Negative Word Count")
        plt.ylabel("Word")
        plt.title("Total type of words in "+self._country+" article")
        plt.xticks(index+width/2, index)
        plt.legend(loc='best')
        #plt.savefig('figure/'+self._country+'_overall.svg')
        return plt.gcf()

# if __name__ == "__main__":
#     graph1 = graph("Bangkok")
#     graph2 = graph("Jakarta")
#     plt.show(graph1.plot_all_graph(0.35))
#     plt.show(graph2.plot_all_graph(0.35))
