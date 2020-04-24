"""
finalProject.py
Name(s): Pranay Pherwani
NetId(s): prp12
Date: 4/24/20
"""

import math
import random

P = 

def transitionProbabilityMatrix(text):
	# Initialize letters array
	letters = [chr(x) for x in range(ord('a'), ord('z') + 1)]
	# Set all characters in text to lowercase
	for line in text:
		line = line.lower()
	# Reset reading position
	text.seek(0)

	# Initialize transition probability matrix with 1's to avoid a probability of 0
	trans = [[1]*27 for x in range(27)]

	# Loop over the lines in text
	for line in text:
			# Loop over the characters in a line of text
			for i in range(len(line)-1):
				# Based on any two consecutive characters, update the trans matrix
				# Account for spaces and other characters by using the last row/column of trans
				first = line[i]
				second = line[i+1]

				if (first in letters) and (second in letters):
					# Convert from character to index in the indices
					trans[ord(first)-97][ord(second)-97]+=1
				elif (first in letters):
					trans[ord(first)-97][26]+=1
				elif (second in letters):
					trans[26][ord(second)-97]+=1

	# Normalize each row
	count = 0
	for row in trans:
		row = [float(i)/sum(row) for i in row]
		trans[count] = row
		count+=1
		 	




	# # loop over letters
	# for l in letters:
	# 	# Initialize a row of the transition probability matrix
	# 	transRow = [0]*27
	# 	# Loop over the lines in text
	# 	for line in text:
	# 		print('hi')
	# 		# Loop over the characters in a line of text
	# 		for i in range(len(line)):
	# 			print('hi')
	# 			# If the character matches the current letter, add one
	# 			# to the index of the letter after it (a is 0, b is 1, etc)
	# 			if line[i]==l:
					
	# 				index = ord(line[i+1])-97
	# 				transRow[index]+=1
	# 				# If the letter is followed by a space, comma, etc, add 1 to index 27
	# 				if index<0 or index>25:
	# 					transRow[26]+=1

	# 		# Normalize the row and add it to the matrix with the index of the current letter
	# 		transRow = [float(i)/sum(transRow) for i in transRow]
	# 		trans[ord(l)-97]=transRow

	return trans

def frequencyVector(text):
	# Initialize letters array
	letters = [chr(x) for x in range(ord('a'), ord('z') + 1)]
	# Initialize frequency vector
	P = [0]*26
	# Ensure the text reads at the beginning
	text.seek(0)
	# Loop over the lines in text
	for line in text:
			# Loop over the characters in a line of text
			# Increment frequency of the letter being read
			for i in range(len(line)):
				if line[i] in letters:
					P[ord(line[i])-97]+=1
	# Normalize P
	P = [float(i)/sum(P) for i in P]

	return P




def decode(mapping, cyphertext):
	# Initialize coded text and set to lowercase
	coded = cyphertext
	coded = coded.lower
	# Initialize decoded text
	decoded = ''
	# Loop over characters in coded text and set in decoded based on the mapping
	for index in range(len(coded)):
		letter = coded[index]
		letterIndex = ord(letter)-97
		if letterIndex>0 and letterIndex<26:
			decoded = decoded + mapping[letter]
		else:
			# Keep other characters that are not letters the same
			decoded = decoded + letter

	return decoded

def logLikelihood(mapping, cyphertext, P, M):
	decoded = decode(mapping, cyphertext)
	logLike = 0
	logLike+= math.log(P[ord(y[0])-97])
	for i in range(len(decoded)-1):
		logLike+=math.log(M[ord(decoded[i])-97][ord(decoded[i+1])-97])

	return logLike




def mappingGenerator():
	# Create a list of letters and shuffle it
	letters = [chr(x) for x in range(ord('a'), ord('z') + 1)]
	mapping = random.shuffle(letters)
	return mapping

def mh_step(currentMapping, currentLikelihood, cyphertext, P, M)
	proposedMapping = switch(currentMapping)
	proposedLikelihood = logLikelihood(proposedMapping, cyphertext, P, M)
	ratio = proposedLikelihood/currentLikelihood
	if ratio>1:
		return (proposedMapping,proposedLikelihood)
	else:
		rand = random.random()
		if rand<ratio:
			return (proposedMapping,proposedLikelihood)

	return (currentMapping, currentLikelihood)

def switch(mapping):
	# Generate 2 random distinct indices to swap
	index1 = random.randrange(0,26)
	index2 = random.randrange(0,26)
	while index2==index1:
		index2 = random.randrange(0,26)
	# Make a new list and apply the swap to it
	newMapping = mapping.copy()
	newMapping[index1] = mapping[index2]
	newMapping[index2] = mapping[index1]

	return newMapping

def encrypt(text):
	# Generate a random mapping and "decode" the real text 
	mapping = mappingGenerator()
	encrypted = decode(mapping,text)
	return encrypted

def decrypt(reference, cyphertext, iterations):
	# Calculate frequency vector and transition matrix
	P = frequencyVector(reference)
	M = transitionProbabilityMatrix(reference)
	# Get intial mapping and likelihood
	mapping = mappingGenerator()
	likelihood = logLikelihood(initialMapping, cyphertext, P, M)
	# Computed the mh_step for the desired number of iterations
	for i in range(iterations)
		(mapping,likelihood) = mh_step(mapping,likelihood, cyphertext, P, M)
	# return the decoded text
	return decode(mapping, cyphertext)



"""
main function
"""
if __name__ == '__main__':
	letters = [chr(x) for x in range(ord('a'), ord('z') + 1)]
	warAndPeace = open('WarAndPeace.txt', 'r')

	matrix = transitionProbabilityMatrix(warAndPeace)
	print(matrix[16][20])

