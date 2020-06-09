import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import re
import json
import os


#from nltk import ngrams

class RabinKarp:
	def __init__(self, text, n):
		self._text = text 
		self._hash = 0
		self._n = n

		for i in range(0, n-1):
			self._hash =(256 * self._hash + ord(self._text[i]))%101

		self._start = 0
		self._end = n 

	def window_text(self):
		return self._text[self._start:self._end]

class country_article:
	def __init__(self):
		self.all_articles = {0: []}
		self.all_country = ["Jakarta", "Bangkok", "Taipei", "HongKong", "Tokyo", "Beijing", "Seoul"]
		articles = [[] for x in self.all_country]

		#with open("../assets/countryLink.json") as json_file:
		with open(os.getcwd() + f'{os.sep}tripy{os.sep}assets{os.sep}countryLink.json') as json_file:
			self._links = json.load(json_file)
		for i in range(len(self.all_country)):
			k = 0
			print("-Reading article: "+ self.all_country[i]+ "......")
			for j in self._links[self.all_country[i]]:
				articles[i].append(article(j,self.all_country[i],k))
				k+=1
			self.all_articles[i+1] = articles[i]

	def get_all_articles(self):
		return self.all_articles

	def get_sentiment(self):
		sentiment = {}
		for key in self.all_articles:
			score = 0;
			if len(self.all_articles[key]) == 0:
				sentiment[key] = score
				continue
			for i in range (len(self.all_articles[key])):
				score += (self.all_articles[key])[i].get_sentiment_score()
			score = score/len(self.all_articles[key])
			sentiment[key] = score

		return sentiment

class article:

	def __init__(self, url, country, i):
		self._words = self.readUrl(url)
		self._neg_freq = 0
		self._pos_freq = 0
		self._data = None
		self._stopword_frequency = 0
		self._country = country
		self._i = i
		self._cleanWords = self.get_clean_words()

		# self.twograms = ngrams(self.cleanWords, 2)
		# for grams in self.twograms:
		# 	print(grams)
		try:
			#"../assets/countryLink.json"
			#with open("../assets/datas/"+self._country +'article' + str(self._i) +'.json') as json_file:
			with open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}datas{os.sep}"+self._country +'article' + str(self._i) +'.json') as json_file:
				self._data = json.load(json_file)
				json_file.close()
			self._pos_freq = self._data['Positive']
			self._neg_freq = self._data['Negative']
		except:
			pass

	def readUrl(self, url):
	    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	    reg_url = url
	    req = urllib.request.Request(url=reg_url, headers=headers)
	    html = urllib.request.urlopen(req).read()
	    soup = BeautifulSoup(html, features="lxml")
	    for script in soup(["script", "style"]):
	        script.extract()

	    text = soup.get_text().lower()
	    lines = (line.strip() for line in text.splitlines())
	    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	    text = '\n'.join(chunk for chunk in chunks if chunk)
	    return text

	def get_sentiment_score(self):
		return (self._pos_freq/self.get_total_word()) * 100

	def get_stopword_freq(self):
		return len(self._words.split()) - len(self._cleanWords)

	def get_total_word(self):
		return len(self._words.split())

	def get_pos_freq(self):
		return self._pos_freq

	def get_neg_freq(self):
		return self._neg_freq

	def get_clean_text(self):
		regex = re.compile(r'[^a-zA-Z+-+\s]+')
		cleanText = re.sub(regex, '', self._words)
		return cleanText

	def get_clean_words(self):
		regex = re.compile(r'[^a-zA-Z+-+\s]+')
		cleanWords = re.sub(regex, '', self._words).split()
		cleanWords = self.remove_stop_words(cleanWords)
		return cleanWords

	def remove_stop_words(self, list):
		stopwords = []
		#file = open("../assets/wordlists/stopword.txt", "r", encoding='utf-8')
		file = open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}wordlists{os.sep}stopword.txt", "r", encoding='utf-8')
		stopwords = file.read().splitlines()
		file.close()
		for i in stopwords:
			if self.rabin_karp(i, list) == True:
				list.remove(i)
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

	def calculate_words(self):
		self._data = {}
		file = open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}wordlists{os.sep}positiveword.txt", "r", encoding='utf-8')
		pos_words = set(file.read().splitlines())
		file.close()

		file = open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}wordlists{os.sep}negativeword.txt", "r", encoding='utf-8')
		neg_words = set(file.read().splitlines())
		file.close()

		for i in self._cleanWords:
			if i in pos_words:
				self._pos_freq += 1
			elif i in neg_words:
				self._neg_freq +=1

		self._data['Stop'] = self.getStopWordTotal()
		self._data['Positive'] = self._pos_freq
		self._data['Negative'] = self._neg_freq
		with open(os.getcwd() + f"{os.sep}tripy{os.sep}assets{os.sep}datas{os.sep}"+self._country +'article' + str(self._i) +'.json', 'w') as outfile:
			json.dump(self._data, outfile)
			outfile.close()

ARTICLES = country_article()
ALL_ARTICLES = ARTICLES.get_all_articles()
SENTIMENT = ARTICLES.get_sentiment()
# if __name__ == "__main__":
# 	articles = set()
# 	clist = ["Jakarta", "Bangkok", "Taipei", "HongKong", "Tokyo", "Beijing", "Seoul"]
# 	j = 0
# 	for i in links.Taipei:
# 		articles.add(article(i, "Taipei", j).calculateWords())
# 		j+=1
# 	j = 0
# 	for i in links.HongKong:
# 		articles.add(article(i, "HongKong", j).calculateWords())
# 		j+=1
# 	j = 0
# 	for i in links.Tokyo:
# 		articles.add(article(i, "Tokyo", j).calculateWords())
# 		j+=1
# 	j = 0
# 	for i in links.Beijing:
# 		articles.add(article(i, "Beijing", j).calculateWords())
# 		j+=1
# 	j = 0
# 	for i in links.Seoul:
# 		articles.add(article(i, "Seoul", j).calculateWords())
# 		j+=1
# 	j = 0
# 	for i in links.Jakarta:
# 		articles.add(article(i, "Jakarta", j).calculateWords())
# 		j+=1
# 	j = 0
# 	for i in links.Bangkok:
# 		articles.add(article(i, "Bangkok", j).calculateWords())
# 		j+=1