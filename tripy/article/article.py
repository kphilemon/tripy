import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import re
import json
import os
from tripy.algorithms.rabinkarp import RabinKarp

class Country_article:
	def __init__(self):
		self._all_articles = {}
		self._all_country = ["KualaLumpur","Jakarta", "Bangkok", "Taipei", "HongKong", "Tokyo", "Beijing", "Seoul"]
		articles = [ [] for x in self._all_country]

		#Read links from json file
		with open(os.getcwd() + f'{os.sep}tripy{os.sep}assets{os.sep}countryLink.json') as json_file:
			self._links = json.load(json_file)

		#Store all articles into dict
		for i in range(len(self._all_country)):
			k = 0
			print("-Reading article: "+ self._all_country[i]+ "......")
			for j in self._links[self._all_country[i]]:
				articles[i].append(Article(j,self._all_country[i],k))
				k+=1
			self._all_articles[i] = articles[i]

	def get_all_articles(self):
		return self._all_articles

	#Get sentiment score for all articles
	def get_sentiment(self):
		sentiment = {}
		for key in self._all_articles:
			score = 0;
			for i in range (len(self._all_articles[key])):
				score += (self._all_articles[key])[i].get_sentiment_score()
			score = score/len(self._all_articles[key])
			sentiment[key] = score
		return sentiment

class Article:

	def __init__(self, url, country, i):
		self._country = country
		self._i = i
		self._words = self.readUrl(url)
		self._neg_freq = 0
		self._pos_freq = 0
		self._data = None
		self._stopword_frequency = 0
		#self._cleanWords = self.get_clean_words()
		self._cleanWords_string = self.get_clean_text()
		self.calculate_words_string()


	def readUrl(self, url):
		html = None
		try:
			with open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}htmls{os.sep}"+ self._country +'article' + str(self._i)+'.html') as html_file:
				html = html_file.read()
				html_file.close()
		except :
			#Read html
		    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
		    reg_url = url
		    req = urllib.request.Request(url=reg_url, headers=headers)
		    html = urllib.request.urlopen(req).read()
		    with open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}htmls{os.sep}"+ self._country +'article' + str(self._i)+'.html', 'w') as html_file:
		    	html_file.write(str(html))
		    	html_file.close()
		soup = BeautifulSoup(html, features="lxml")
		for script in soup(["script", "style"]):
			script.extract()
		text = soup.get_text().lower()
		lines = (line.strip() for line in text.splitlines())
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		text = '\n'.join(chunk for chunk in chunks if chunk)
		return text

	# Sentiment score = ( Positive % - Negative % + 100 ) / 200
	def get_sentiment_score(self):
		return (((self._pos_freq - self._neg_freq) / len(self._cleanWords_string.split())) + 1 ) * 100/ 2

	def get_stopword_freq(self):
		return len(self._words.split()) - len(self._cleanWords_string.split())

	def get_total_word(self):
		return len(self._words.split())

	def get_pos_freq(self):
		return self._pos_freq

	def get_neg_freq(self):
		return self._neg_freq

	#Get a String text with stop words without symbols 
	def get_clean_text(self):
		regex = re.compile(r'[^a-zA-Z+-]+')
		self._words= re.sub(r'\\.', ' ', self._words)
		cleanText = re.sub(regex, ' ', self._words)
		cleanText = self.remove_stop_words_string(cleanText)
		return cleanText

	#Get a wordlist without stopword
	def get_clean_words(self):

		regex = re.compile(r'[^a-zA-Z+-]+')
		self._words= re.sub(r'\\.', ' ', self._words)
		cleanWords = re.sub(regex, ' ', self._words).split()
		cleanWords = self.remove_stop_words(cleanWords)
		return cleanWords

	def remove_stop_words_string(self, text):
		stopwords = []
		#Read stop word list
		list = text.split()
		file = open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}wordlists{os.sep}stopword.txt", "r", encoding='utf-8')
		stopwords = file.read().splitlines()
		file.close()

		#Find stop word and remove it 
		for i in stopwords:
			if self.rabin_karp(i, list) == True:
				list = [item for item in list if item != i]
		text = " ".join(list)
		return text

	#Remove stop words from list of words
	def remove_stop_words(self, list):
		stopwords = []
		#Read stop word list
		file = open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}wordlists{os.sep}stopword.txt", "r", encoding='utf-8')
		stopwords = file.read().splitlines()
		file.close()

		#Find stop word and remove it 
		for i in stopwords:
			if self.rabin_karp(i, list) == True:
				list = [item for item in list if item != i]
		return list

	def rabin_karp(self, pattern, list):
		for i in list:
			text_hash = RabinKarp(i, len(i))
			pattern_hash = RabinKarp(pattern, len(pattern))

			for j in range(len(i) - len(pattern) + 1):
				if text_hash._hash == pattern_hash._hash:
					if text_hash.window_text() == pattern:
						return True
		return False

	#Calculate Positive,Negative words and store into json file
	def calculate_words(self):
		#Read positive word list
		file = open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}wordlists{os.sep}positiveword.txt", "r", encoding='utf-8')
		pos_words = set(file.read().splitlines())
		file.close()

		#Read negative word list
		file = open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}wordlists{os.sep}negativeword.txt", "r", encoding='utf-8')
		neg_words = set(file.read().splitlines())
		file.close()

		#search for positive and negative words
		for i in self._cleanWords:
			if i in pos_words:
				self._pos_freq += 1
			elif i in neg_words:
				self._neg_freq +=1

	def calculate_words_string(self):
		#Read positive word list
		file = open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}wordlists{os.sep}positiveword.txt", "r", encoding='utf-8')
		pos_words = set(file.read().splitlines())
		file.close()

		#Read negative word list
		file = open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}wordlists{os.sep}negativeword.txt", "r", encoding='utf-8')
		neg_words = set(file.read().splitlines())
		file.close()

		#search for positive and negative words
		for i in pos_words:
			self._pos_freq += self._cleanWords_string.count(i)
		for i in neg_words:
			self._neg_freq += self._cleanWords_string.count(i)



#Get all articles
ARTICLES = Country_article()
ALL_ARTICLES = ARTICLES.get_all_articles()
SENTIMENT = ARTICLES.get_sentiment()
print("----------------------",SENTIMENT)
