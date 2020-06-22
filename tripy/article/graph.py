from tripy.article.article import ALL_ARTICLES, SENTIMENT
from tripy.geo.locations import INDEX_BY_NAME, NAME_BY_INDEX
import numpy as np 
import json
import os
import plotly.graph_objects as go

class Sentiment_graph:
    def __init__(self):
        self.sentiment = SENTIMENT

    def plot_graph(self):
        n = len(self.sentiment)
        x, y = zip(*self.sentiment.items())
        x1 = list(x)
        for i in range(len(x)):
            x1[i] = NAME_BY_INDEX[x[i]]

        width=[0.35]*n

        fig = go.Figure(data=[
            go.Bar(x=x1, y=y, text=y, textposition='outside', texttemplate='%{text:.4f}',width=width)
        ])
        fig.update_layout(title_text='Sentiment Score of All Country', barmode='group', yaxis=dict(range=[min(y)-1,max(y)+1]))
        fig.write_html(os.getcwd()+f'{os.sep}tripy{os.sep}assets{os.sep}datas{os.sep}'+'sentiment.html')



class Probability_distribution:
    def __init__(self, routes, country):
        self._routes = routes
        self._country = country


    def plot_graph(self):

        n = len(self._routes)
        lists = sorted(self._routes.items(), reverse=True)
        width = [0.35]*n
        y, x = zip(*lists)
        total_score = sum(y)

        y = [i/total_score for i in y]

        x1 = list(x)
        for i in range(len(x1)):
            for j in range(len(x1[i])):
                for k in range(len(x1[i][j])):
                    x1[i][j][k] = NAME_BY_INDEX[x[i][j][k]]
                x1[i][j] = '\n'.join(x1[i][j])
            x1[i] = ','.join(x1[i])

        fig = go.Figure(data=[
            go.Bar(x=x1, y=y, text=y, textposition='outside', texttemplate='%{text:0.4f}',width=width)
        ])
        fig.update_layout(title_text='Probability Distribution of '+self._country, barmode='group', yaxis=dict(range=[0,1]))
        fig.write_html(os.getcwd()+f'{os.sep}tripy{os.sep}assets{os.sep}datas{os.sep}'+self._country+'probability.html')
        
        

class Graph:
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


    def plot_all_graph(self):
        x1 = ["Article 1","Article 2","Article 3","Article 4","Article 5"]
        fig = go.Figure(data=[
            go.Bar(x=x1, y=self._total_words, name='Total words', text=self._total_words, textposition='auto'),
            go.Bar(x=x1, y=self._stop_words, name='Stop words', text=self._stop_words, textposition='auto'),
            go.Bar(x=x1, y=self._pos_words, name='Positive words', text=self._pos_words, textposition='auto'),
            go.Bar(x=x1, y=self._neg_words, name='Negative words', text=self._neg_words, textposition='auto')
        ])
        fig.update_layout(title_text='Total Words in '+self._country+' articles', barmode='group')
        fig.write_html(os.getcwd()+f'{os.sep}tripy{os.sep}assets{os.sep}datas{os.sep}'+self._country+'graph.html')
