#!/usr/bin/env python3

'''
build_distance_matrices.py
Trabalho Prático 1 - Processamento de Linguagem Natural
UFMG/DCC
@author: Hugo Araujo de Sousa [2013007463]
@DCC030
'''

import os

# Global variables.
DATA_FOLDER = '__temp_data__'
VECTORS_FOLDER = 'vectors'

vocabs = {}
dmatrices = {}

def read_vectors():
	''' Read word vectors for all books.
	
		@rtype:		Dictionary
		@return:	Dictionary with filename strings as keys and dictionaris 
					as values. These values are word string -> float list
					dictionaries.
		'''

	print('[+] Reading word vectors')
	path = DATA_FOLDER + '/' + VECTORS_FOLDER
	vector_names = [f for f in os.listdir(path)]
	vector_names.sort()

	vectors = {}

	for vector_name in vector_names:
		print('\t- ' + vector_name)

		vector_file = open(path + '/' + vector_name, 'r')

		index = vector_name[:-4]

		vectors[index] = {}

		# Ignore header
		vector_file.readline()

		for line in vector_file:
			line_list = line.strip().split(' ')
			word = line_list[0]
			vector = [float(v) for v in line_list[1:]]

			vectors[index][word] = vector

	return vectors


def cosine_similarity(vector1, vector2):
	''' Get the cosine similarity of two vectors.

		@type	vector1:	float list
		@param	vector1: 	First vector

		@type	vector2:	float list
		@param	vector2: 	Second vector
		'''

	num = sum([(a*b) for (a,b) in zip(vector1, vector2)])
	den1 = sum((a ** 2 for a in vector1)) ** 0.5
	den2 = sum((b ** 2 for b in vector2)) ** 0.5

	return num/(den1 * den2)


def build_distance_matrices(vectors):
	''' Build distance matrices for all books, where each entry in these
		matrices represents a pair of words.

		@type	vectors:	Dictionary
		@param 	vectors:	Dictionary with filename strings as keys and
							dictionaries as values. These values are word
							string -> float list dictionaries.
		'''

	global vocabs
	global dmatrices

	print('[+] Creating distance matrices')

	for filename in vectors:
		print('\t- ' + filename)
		matrix = {}
		cur_vocab = set()

		key = int(filename.split(' ')[0])

		distances = vectors[filename]
		words = list(distances)

		# For each pair of words, calculate distance.
		for word1 in words:
			cur_vocab.add(word1)
			for word2 in words:
				if word1 <= word2 and (word1, word2) not in matrix:
					matrix[word1, word2] = cosine_similarity(distances[word1],
						distances[word2])

		dmatrices[key] = matrix
		vocabs[key] = cur_vocab

	return


def compare_matrices(book1, book2):
	''' Compare two matrices and calculate how similar they are.

		@type	matrixA:	int
		@param	matrixA:	Index of first book to compare.

		@type	matrixB:	int
		@param	matrixB:	Index of second book to compare.

		@rtype:		float
		@return:	A number that represents the distance between the two input
					matrices.
		'''

	matrixA = dmatrices[book1]
	matrixB = dmatrices[book2]

	vocab1 = vocabs[book1]
	vocab2 = vocabs[book2]
	
	vocab = vocab1.union(vocab2)

	dist = 0
	for word1 in vocab:
		for word2 in vocab:
			if (word1 > word2):
				continue

			if (word1, word2) in matrixA:
				aij = matrixA[word1, word2]
			else:
				aij = 0

			if (word1, word2) in matrixB:
				bij = matrixB[word1, word2]
			else:
				bij = 0

			dist += (aij - bij) ** 2

	dist = dist ** 0.5
	return dist


def get_books_distances():
	''' Calculate the distance between all books. '''

	global dmatrices

	path = DATA_FOLDER + '/' + VECTORS_FOLDER
	names = [f[:-4] for f in os.listdir(path)]

	for name1 in names:
		for name2 in names:
			print('Comparing books:')

			book1 = int(name1.split(' ')[0])
			book2 = int(name2.split(' ')[0])

			print(name1)
			print(name2)
			dist = compare_matrices(book1, book2)
			print('Distance:', dist)


def main():
	''' Main program. '''

	vectors = read_vectors()
	build_distance_matrices(vectors)
	get_books_distances()
	