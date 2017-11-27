#!/usr/bin/env python3

'''
tp2.py: Trabalho Prático II - Processamento de Linguagem Natural
@author: Hugo Araujo de Sousa [2013007463]
@email: hugosousa@dcc.ufmg.br
@DCC030 - Processamento de Linguagem Natural - UFMG
'''


import argparse as ap
import numpy as np
from sklearn import svm
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
import sys


# Add command line arguments to the program.
parser = ap.ArgumentParser()
parser.add_argument('train_file', type=str, help='Name of train file')
parser.add_argument('test_file', type=str, help='Name of test file')
parser.add_argument('validation_file', type=str,
	help='Name of validation file')
parser.add_argument('-s', dest='RSEED', default=0, type=int,
	help='Random number generation seed')

args = parser.parse_args()

def build_dataset(file):
	''' Read a file with words and their POS tags and create an array
		with words and their target POS.
	
		@param 	file: Input file.
		@type 	file: File.

		@return: 	Data and its targets.
		@rtype:		Numpy array, Numpy array
		'''

	vec = HashingVectorizer(n_features=2, alternate_sign=False)

	data = []
	target = []

	for line in file:
		raw_words = line.split()
		previous_tag = '-'

		for raw_word in raw_words:
			temp = raw_word.split('_')
			token = temp[0].lower()
			tag = temp[1]
			data.append(' '.join([previous_tag, token]))
			target.append(tag)
			previous_tag = tag

	data_array = vec.transform(data).toarray()
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

	train_data, test_data, validation_data = \
		read_data(args.train_file, args.test_file, args.validation_file)

	print(train_data[0], train_data[1])
	
	print('Naive Bayes')
	gnb = GaussianNB()
	predictor = gnb.fit(train_data[0], train_data[1])
	y_pred = predictor.predict(validation_data[0])
	precision = ((validation_data[1] == y_pred).sum()) / len(validation_data[0])
	print('Validation:', (precision*100), '%')
	y_pred = predictor.predict(test_data[0])
	precision = ((test_data[1] == y_pred).sum()) / len(test_data[0])
	print('Test:', (precision*100), '%')

	print('SVM')
	svmc = svm.SVC(random_state=args.RSEED)
	predictor = svmc.fit(train_data[0], train_data[1])
	y_pred = predictor.predict(validation_data[0])
	precision = ((validation_data[1] == y_pred).sum()) / len(validation_data[0])
	print('Validation:', (precision*100), '%')
	y_pred = predictor.predict(test_data[0])
	precision = ((test_data[1] == y_pred).sum()) / len(test_data[0])
	print('Test:', (precision*100), '%')

main()