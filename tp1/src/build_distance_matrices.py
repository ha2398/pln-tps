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


def read_vectors():
	''' Read word vectors for all books. '''

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


def main(vocabs):
	''' Main program. '''

	vectors = read_vectors()
	print(vectors)