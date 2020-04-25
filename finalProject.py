"""
finalProject.py
Name(s): Pranay Pherwani
NetId(s): prp12
Date: 4/24/20
"""

import math
import random

"""
transitionProbabilityMatrix calculates the transition
probability matrix for a given reference text

INPUTS
text:	the reference text

OUTPUTS
trans:	the transition probability matrix
"""
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
		 	
	return trans

"""
frequencyVector calculates the frequency vector
for a given reference text

INPUTS
text: the reference text

OUTPUTS
P: the frequency vector
"""
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


"""
decode applies a mapping on a given text

INPUTS
mapping:	the mapping to apply
cyphertext:	the text to apply the mapping to

OUTPUTS
decoded:	the decoded text
"""
def decode(mapping, cyphertext):
	# Initialize coded text and set to lowercase
	coded = cyphertext
	coded = coded.lower()
	# Initialize decoded text
	decoded = ''
	# Loop over characters in coded text and set in decoded based on the mapping
	for index in range(len(coded)):
		letter = coded[index]
		letterIndex = ord(letter)-97
		if letterIndex>=0 and letterIndex<26:
			decoded = decoded + mapping[letterIndex]
		else:
			# Keep other characters that are not letters the same
			decoded = decoded + letter

	return decoded

"""
logLikelihood calculates the log of the mapping's likelihood score

INPUTS
mapping:	the given mapping
cyphertext:	the text to apply to mapping on
P: the frequency vector
M:			the transition probability matrix

OUTPUT
logLike: the log of the mapping's likelihood score
"""
def logLikelihood(mapping, cyphertext, P, M):
	letters = [chr(x) for x in range(ord('a'), ord('z') + 1)]
	decoded = decode(mapping, cyphertext)
	logLike = 0
	logLike+= math.log(P[ord(decoded[0])-97])
	for i in range(len(decoded)-1):
		if decoded[i] in letters:
			index1=ord(decoded[i])-97
		else:
			index1=26

		if decoded[i+1] in letters:
			index2=ord(decoded[i+1])-97
		else:
			index2=26
		logLike+=math.log(M[index1][index2])

	return logLike

"""
mappingGenerator generates a random mapping

INPUTS
none

OUTPUTS
letters:	the randomly generated mapping
"""
def mappingGenerator():
	# Create a list of letters and shuffle it
	letters = [chr(x) for x in range(ord('a'), ord('z') + 1)]
	random.shuffle(letters)
	return letters

"""
mh_step goes through one step of the Metropolis algorithm

INPUTS
currentMapping:		the current mapping
currentLikelihood:	the likelihood score of the current mapping
cyphertext:	the text to apply to mapping on
P: the frequency vector
M:			the transition probability matrix

OUTPUTS
proposedMapping:	the proposed mapping
proposedLikelihood:	the likelihood score of the proposed mapping
"""
def mh_step(currentMapping, currentLikelihood, cyphertext, P, M):
	# Generate a random proposed mapping
	proposedMapping = switch(currentMapping)
	# Calculate its likelihood
	proposedLikelihood = logLikelihood(proposedMapping, cyphertext, P, M)
	# Calculate the ratio, and move if it's greater than 1
	# If it's less than 1, move with that probability
	ratio = math.exp(proposedLikelihood-currentLikelihood)
	if ratio>1:
		return (proposedMapping,proposedLikelihood)
	else:
		rand = random.random()
		if rand<ratio:
			return (proposedMapping,proposedLikelihood)

	return (currentMapping, currentLikelihood)

"""
switch swaps the values of a mapping at 2 random indices

INPUTS
mapping:	the mapping to perform the swap on

OUTPUTS
newMapping:	the new mapping with the swap applied
"""
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

"""
encrypt applies a random cipher to a text

INPUTS
text:		the text to encrypt

OUTPUTS
encrypted:	the encrypted text
"""
def encrypt(text):
	# Generate a random mapping and "decode" the real text 
	mapping = mappingGenerator()
	encrypted = decode(mapping,text)
	return encrypted

"""
decrypt uses Metropolis Sampling to find the cipher and decrypt the text

INPUTS
reference:	the reference text
cyphertext:	the encrypted text
iterations: the number of desired iterations

OUTPUTS
mapping:						the mapping that decrypts the text
decode(mapping, cyphertext):	the decrypted text
"""
def decrypt(reference, cyphertext, iterations):
	# Calculate frequency vector and transition matrix
	P = frequencyVector(reference)
	M = transitionProbabilityMatrix(reference)
	# Get intial mapping and likelihood
	mapping = mappingGenerator()
	likelihood = logLikelihood(mapping, cyphertext, P, M)
	# Computed the mh_step for the desired number of iterations
	for i in range(iterations):
		(mapping,likelihood) = mh_step(mapping,likelihood, cyphertext, P, M)
	# return the decoded text
	return (mapping,decode(mapping, cyphertext))



"""
main function
"""
if __name__ == '__main__':
	# Opens war and peace
	warAndPeace = open('WarAndPeace.txt', 'r')

	# Defines a string to be encrypted and decrypted
	plain_text = "As Oliver gave this first proof of the free and proper action of his lungs, \
	the patchwork coverlet which was carelessly flung over the iron bedstead, rustled; \
	the pale face of a young woman was raised feebly from the pillow; and a faint voice imperfectly \
	articulated the words, Let me see the child, and die. \
	The surgeon had been sitting with his face turned towards the fire: giving the palms of his hands a warm \
	and a rub alternately. As the young woman spoke, he rose, and advancing to the bed's head, said, with more kindness \
	than might have been expected of him: "

	# Encrypts the string
	encrypted = encrypt(plain_text)
	# Decrypts the string
	(mapping, decrypted) = decrypt(warAndPeace, encrypted, 10000)
	# Prints information
	print('ENCRYPTED:')
	print(encrypted)
	print('DECRYPTED:')
	print(decrypted)
	print('MAPPING:')
	print(mapping)


