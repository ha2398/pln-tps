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
from sklearn.feature_extraction import FeatureHasher
from sklearn.naive_bayes import GaussianNB


# Add command line arguments to the program.
parser = ap.ArgumentParser()
parser.add_argument('train_file', type=str, help='Name of train file')
parser.add_argument('test_file', type=str, help='Name of test file')
parser.add_argument('validation_file', type=str,
	help='Name of validation file')
parser.add_argument('-s', dest='RSEED', default=0, type=int,
	help='Random number generation seed')

args = parser.parse_args()


# Global variables
tags = {}
id_tag = {}


def features(sentence, index):
	''' Return the features of the word at a given index in the sentence.

		@param 	sentence: 	Sentence in which the word is.
		@type 	sentence: 	List of String.

		@param 	index:		Index of word in the sentence.
		@type 	index: 		Integer.

		@return: 	Word features.
		@rtype: 	Dictionary.
		'''

	word = sentence[index].split('_')[0]

	return {
		'word': word.lower(),
		'is_first': index == 0,
		'is_last': index == len(sentence) - 1,
		'is_capitalized': word[0].upper() == word[0],
		'is_all_caps': word.upper() == word,
		'is_all_lower': word.lower() == word,
		'prefix-1': word[0].lower(),
		'prefix-2': word[:2].lower(),
		'prefix-3': word[:3].lower(),
		'suffix-1': word[-1].lower(),
		'suffix-2': word[-2:].lower(),
		'suffix-3': word[-3:].lower(),
		'prev_tag': '' if index == 0 else sentence[index - 1].split('_')[1],
		'next_tag': '' if index == len(sentence) - 1 else \
			sentence[index + 1].split('_')[1],
		'has_hyphen': '-' in word,
		'is_numeric': word.isdigit(),
	}

def build_dataset(file):
	''' Read a file with words and their POS tags and create an array
		with words and their target POS.
	
		@param 	file: Input file.
		@type 	file: File.

		@return: 	Data and its targets.
		@rtype:		Numpy array, Numpy array
		'''

	global tags

	h = FeatureHasher(n_features=17)

	data = []
	target = []

	for line in file:
		words = line.split()

		for index in range(len(words)):
			data.append(features(words, index))
			tag = words[index].split('_')[1]

			if tag not in tags:
				tag_id = len(tags)
				tags[tag] = tag_id
				id_tag[tag_id] = tag

			tag = tags[tag]
			target.append(tag)

	data_array = h.transform(data).toarray()
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
	train_data = build_dataset(train_file)

	print('[+] Reading validation file')
	validation_file = open(validation_filename, 'r')
	validation_data = build_dataset(validation_file)

	print('[+] Reading test file')
	test_file = open(test_filename, 'r')
	test_data = build_dataset(test_file)

	train_file.close()
	test_file.close()
	validation_file.close()

	print()

	return train_data, test_data, validation_data


def print_most_precise_pos(real_output, model_output):
	''' Print the POS tags for which the model was more precise.

		@param 	real_output: Real data outputs.
		@type 	real_output: Numpy Array.

		@param 	model_output: Model outputs.
		@type 	model_output: Numpy Array.
		'''

	hits = [0] * len(tags)
	counts = [0] * len(tags)

	for i in range(len(real_output)):
		tag_id = real_output[i]
		predicted_tag_id = model_output[i]

		counts[tag_id] += 1

		if tag_id == predicted_tag_id:
			hits[tag_id] += 1

	precision = [0] * len(tags)
	for tag in tags:
		tag_id = tags[tag]
		tag_precision = hits[tag_id] / counts[tag_id]
		precision[tag_id] = (tag, tag_precision)

	precision = sorted(precision, key=lambda x: x[1], reverse=True)

	for i in range(len(precision)):
		tag_precision = round(precision[i][1] * 100, 2)
		print('\t', precision[i][0], 'precision: {}%'.format(tag_precision))

	print()


def main():

	train_data, test_data, validation_data = \
		read_data(args.train_file, args.test_file, args.validation_file)

	print('\tNAIVE BAYES\n')
	gnb = GaussianNB()
	predictor = gnb.fit(train_data[0], train_data[1])

	nb_y_valid = predictor.predict(validation_data[0])
	precision = ((validation_data[1] == nb_y_valid).sum()) \
		/ len(validation_data[0])
	print('[+] Validation precision: {}%'.format(round((precision*100), 2)))
	print_most_precise_pos(validation_data[1], nb_y_valid)

	nb_y_test = predictor.predict(test_data[0])
	precision = ((test_data[1] == nb_y_test).sum()) / len(test_data[0])
	print('[+] Test precision: {}%'.format(round((precision*100), 2)))
	print_most_precise_pos(test_data[1], nb_y_test)

	print(('-' * 80) + '\n')
	
	print('\tSVM\n')
	svmc = svm.SVC(random_state=args.RSEED)
	predictor = svmc.fit(train_data[0], train_data[1])

	svm_y_valid = predictor.predict(validation_data[0])
	precision = ((validation_data[1] == svm_y_valid).sum()) \
		/ len(validation_data[0])
	print('[+] Validation precision: {}%'.format(round((precision*100), 2)))
	print_most_precise_pos(validation_data[1], svm_y_valid)

	svm_y_test = predictor.predict(test_data[0])
	precision = ((test_data[1] == svm_y_test).sum()) / len(test_data[0])
	print('[+] Test precision: {}%'.format(round((precision*100), 2)))
	print_most_precise_pos(test_data[1], svm_y_test)
	

main()