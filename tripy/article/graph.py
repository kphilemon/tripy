from tripy.article.article import ALL_ARTICLES
from tripy.geo.locations import INDEX_BY_NAME, NAME_BY_INDEX
import numpy as np 
import matplotlib.pyplot as plt
import json
import os

class probability_distribution:
    def __init__(self, routes):
        self._routes = routes

    def plot_graph(self, width):
        plt.clf()
        n = len(self._routes)
        lists = sorted(self._routes.items())
        #y = Cost, x =Country index
        y, x = zip(*lists)
        total_cost = sum(y)
        print("Cost: ", y)
        #Probabollity of a route = total cost - cost of route / summation of total cost - cost of route
        y = [total_cost - i for i in y]
        total2 = sum(y)
        y = [self.calculate_probability(total2, i) for i in y]
        print("Probability: ",y)
        #Convert country index to name
        x1 = list(x)
        for i in range(len(x1)):
            for j in range(len(x1[i])):
                for k in range(len(x1[i][j])):
                    x1[i][j][k] = NAME_BY_INDEX[x[i][j][k]]
                x1[i][j] = '\n'.join(x1[i][j])
            x1[i] = ','.join(x1[i])

        #Plot Graph of probability distribution
        index  = np.arange(n)
        plt.subplot(1,1,1)
        plt.bar(index, y)
        plt.ylabel("Probability")
        scale_factor = 0.2
        ymin, ymax = plt.ylim()
        plt.ylim(min(y) - 0.1, ymax)
        plt.title("Probability Distribution of All Path")
        plt.xticks(index+width/2, x1)
        plt.legend(loc='best')
        plt.tight_layout()
        return plt.gcf()
        
    def calculate_probability(self,total, cost):
        return cost / total

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
        plt.bar(index, self._pos_words, width, label="Positive Word Count", color='green')
        plt.bar(index + width, self._neg_words, width, label="Negative Word Count", color='red')
        plt.ylabel("Word", fontsize=9)
        plt.title("Number of Positive and Negative Word", fontsize=9)
        plt.xticks(index+width/2, index)
        plt.legend(loc='best')

        plt.subplot(1,3,2)
        plt.bar(index, self._total_words, width, label="Total Word Count")
        plt.bar(index + width, self._stop_words, width, label="Stop Word Count")
        plt.ylabel("Word", fontsize=9)
        plt.title("Number of Stop Word", fontsize=9)
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
        plt.ylabel("Word", fontsize=9)
        plt.xticks([])
        plt.title("Total type of words in "+self._country+" article", fontsize=9)
        plt.suptitle(self._country+" article", fontsize=12)
        plt.legend(loc='best')
        plt.tight_layout()
        #prevent main title overlap with graph title
        plt.subplots_adjust(top=0.85)

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
        plt.tight_layout()
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
        plt.tight_layout()
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
        plt.xticks([])
        plt.legend(loc='best')
        plt.tight_layout()
        return plt.gcf()

