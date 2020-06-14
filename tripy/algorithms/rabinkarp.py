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