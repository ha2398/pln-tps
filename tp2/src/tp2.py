#!/usr/bin/env python3

'''
tp2.py: Trabalho Prático II - Processamento de Linguagem Natural
@author: Hugo Araujo de Sousa [2013007463]
@email: hugosousa@dcc.ufmg.br
@DCC030 - Processamento de Linguagem Natural - UFMG
'''


from sklearn import datasets
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn import svm

import argparse as ap
import numpy as np
import sys


vocab = {}
tags = {}


def parse_arguments():
	''' Add command line arguments to the program.

		@return:	Command line arguments.
		@rtype:		argparse.Namespace.
		'''

	parser = ap.ArgumentParser()
	parser.add_argument('train_file', type=str, help='Name of train file')
	parser.add_argument('test_file', type=str, help='Name of test file')
	parser.add_argument('validation_file', type=str,
		help='Name of validation file')
	return parser.parse_args()


def build_dataset(file):
	''' Read a file with words and their POS tags and create an array
		with words and their target POS.
	
		@param 	file: Input file.
		@type 	file: File.

		@return: 	Data and its targets.
		@rtype:		Numpy array, Numpy array
		'''

	global vocab, tags

	data = []
	target = []

	for line in file:
		raw_words = line.split()

		for raw_word in raw_words:
			temp = raw_word.split('_')
			token = temp[0].lower()
			tag = temp[1]

			if token not in vocab:
				vocab[token] = len(vocab) + 1
			
			data.append([vocab[token]])

			if tag not in tags:
				tags[tag] = len(tags) + 1
			
			target.append(tags[tag])

	data_array = np.array(data)
	data_array.shape = (len(data), 1)
	target_array = np.array(target)

	return data_array, target_array


def read_data(train_filename, test_filename, validation_filename):
	''' Read input data from input files.
		
		@param 	train_filename: Training data file name.
		@type 	train_filename: String.

		@param 	test_filename: Test data file name.
		@type 	test_filename: String.

		@param 	validation_filename: Validation data file name.
		@type 	validation_filename: String.

		@return: 	Training data, test data and validation data.
		@rtype:		Tuple of Tuple of Numpy Array	
		'''

	print('[+] Reading training file')
	train_file = open(train_filename, 'r')

	print('[+] Reading test file')
	test_file = open(test_filename, 'r')

	print('[+] Reading validation file')
	validation_file = open(validation_filename, 'r')

	train_data = build_dataset(train_file)
	test_data = build_dataset(test_file)
	validation_data = build_dataset(validation_file)

	train_file.close()
	test_file.close()
	validation_file.close()

	return train_data, test_data, validation_data


def main():

	args = parse_arguments()
	train_data, test_data, validation_data = \
		read_data(args.train_file, args.test_file, args.validation_file)

	print('Naive Bayes')
	mnb = MultinomialNB()
	predictor = mnb.fit(train_data[0], train_data[1])
	y_pred = predictor.predict(test_data[0])
	precision = ((test_data[1] == y_pred).sum()) / len(test_data[0])
	print('Test:', (precision*100), '%')
	y_pred = predictor.predict(validation_data[0])
	precision = ((validation_data[1] == y_pred).sum()) / len(validation_data[0])
	print('Validation:', (precision*100), '%')

	print('SVM')
	svmc = svm.SVC()
	predictor = svmc.fit(train_data[0], train_data[1])
	y_pred = predictor.predict(test_data[0])
	precision = ((test_data[1] == y_pred).sum()) / len(test_data[0])
	print('Test:', (precision*100), '%')
	y_pred = predictor.predict(validation_data[0])
	precision = ((validation_data[1] == y_pred).sum()) / len(validation_data[0])
	print('Validation:', (precision*100), '%')


main()