"""
finalProject.py
Name(s): Pranay Pherwani
NetId(s): prp12
Date: 4/24/20
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

def decode(mapping, cyphertext):
	# Initialize coded text and set to lowercase
	coded = cyphertext
	coded = coded.lower
	# Initialize decoded text
	decoded = ''
	# Loop over characters in coded text and set in decoded based on the mapping
	for index in range(len(coded)):
		letter = ord(coded[index])-97
		decoded = decoded + mapping[letter]

	return decoded





"""
main function
"""
if __name__ == '__main__':
	letters = [chr(x) for x in range(ord('a'), ord('z') + 1)]
	warAndPeace = open('WarAndPeace.txt', 'r')

	matrix = transitionProbabilityMatrix(warAndPeace)
	print(matrix[16][20])

