import string
import random
from groupMe import *
import time

class MarkovTextGen(object):
	"""Class to generate sentences based on given messages"""
	def __init__(self, messages):
		self.messages = messages
		self.matrix = {}
		self.unigrams = {}

	def readMessage(self,message):
		punct = string.punctuation.replace('\'','')
		for c in punct:
			message = message.replace(c," ")
		message = message.lower()
		words = message.split()
		return words

	def updateMatrix(self,words):
		nextWordList = [x for x in words[1:]]
		prevWordList = [words[i] for i in range(0,len(words) - 1)]
		for next,prev in zip(nextWordList,prevWordList):
			if prev not in self.matrix:
				self.matrix[prev] = {}
			if next in self.matrix[prev]:
				self.matrix[prev][next] += 1
			else:
				self.matrix[prev][next] = 1
	
	def updateUnigrams(self,words):
		for word in words:
			if word in self.unigrams:
				self.unigrams[word] += 1
			else:
				self.unigrams[word] = 1

	def buildMatrix(self):
		for message in self.messages:
			words = self.readMessage(message)
			self.updateMatrix(words)
			self.updateUnigrams(words)

	def getNextWord(self,word):
		row = self.matrix[word]
		countList = [counts for _,counts in row.items()]
		cumsum = sum(countList)
		num = random.uniform(0,cumsum)
		w = 0
		for keys,value in row.items():
			if num < value + w:
				return keys
			w += value

	def genSeed(self):
		countList = [counts for _,counts in self.unigrams.items()]
		cumsum = sum(countList)
		num = random.uniform(0,cumsum)
		w = 0
		for keys,value in self.unigrams.items():
			if num < value + w:
				return keys
			w += value

	def genSentence(self):
		sent = ''
		current = ''
		for i in range(10):
			if current in self.matrix:
				current = self.getNextWord(current)
			else:
				current = self.genSeed()
			sent = sent + current + " "
		return sent.capitalize()[:-1] + "."

if __name__ == '__main__':

	start = time.time()
	test = GroupMeUser("ab8b1250767b0131cfb75e1bee7e888d")
	test.setGroupID("6670487")
	test.getAllMessages()
	end = time.time()

	print "Getting messages took: %f" % (end - start)

	start = time.time()
	text = MarkovTextGen(test.messages)
	text.buildMatrix()
	end = time.time()
	print "Generating sentences took: %f" % (end - start)
	print len(text.messages)
	print text.genSentence()

