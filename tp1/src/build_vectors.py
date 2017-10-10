#!/usr/bin/env python3

'''
build_vectors.py
Trabalho Prático 1 - Processamento de Linguagem Natural
UFMG/DCC
@author: Hugo Araujo de Sousa [2013007463]
@DCC030
'''


import argparse as ap
import os
import re
import subprocess as sp


# Global variables.
DATA_FOLDER = '__temp_data__'
BOOKS_FOLDER = 'books'
VECTORS_FOLDER = 'vectors'

NULL = None
vocabs = None


def setup():
	''' Set up current working folder. '''

	print('[+] Setting up')

	global NULL
	global vocabs

	NULL = open(os.devnull, 'w')
	vocabs = {}
	sp.call(['mkdir', DATA_FOLDER])
	sp.call(['mkdir', DATA_FOLDER + '/' + BOOKS_FOLDER])
	sp.call(['mkdir', DATA_FOLDER + '/' + VECTORS_FOLDER])

	print('\t- Building word2vec')
	sp.call(['make', 'all', '-C', 'word2vec'])

	return


def trim_file(input_folder, filename):
	''' Remove symbols from a particular book file, leaving only alphanumeric
		characters, and dump the result to file. 

		@type 	input_folder:	str
		@param 	input_folder:	Input folder path

		@type	filename:	str
		@param 	filename:	Name of the file to trim
		'''

	global vocabs

	file = open(input_folder + '/' + filename, 'r')
	out_file = open(DATA_FOLDER + '/' + BOOKS_FOLDER + '/' + filename, 'w')

	print('\t- ' + filename)

	content = file.read()

	# Normalize text.
	new = re.sub('(\s|\W)+', ' ', content).lower()
	out_file.write(new)

	vocab = set(new.split())
	vocabs[filename[:-4]] = vocab

	file.close()
	out_file.close()

	return


def pre_process(input_folder):
	''' Process input books and produces new files without unnecessary
		characters.

		@type	input_folder:	string
		@param 	input_folder:	Name of input folder
		'''

	print('[+] Processing input files')

	file_names = [f for f in os.listdir(input_folder)]
	file_names.sort()

	for filename in file_names:
		trim_file(input_folder, filename)

	return


def build_vectors():
	''' Build word vectors for each book. '''

	print('[+] Building word vectors')
	book_names = [f for f in os.listdir(DATA_FOLDER + '/' + BOOKS_FOLDER)]
	book_names.sort()

	for book_name in book_names:
		vector_name = book_name[:-4] + '.vec'
		print('\t- ' + vector_name)
		sp.call([
			'./word2vec/word2vec',
			'-train',
			'{}/{}/{}'.format(DATA_FOLDER, BOOKS_FOLDER, book_name),
			'-output',
			'{}/{}/{}'.format(DATA_FOLDER, VECTORS_FOLDER, vector_name),
			'-cbow', '1', '-size', '200', '-window', '8', '-negative', '25',
			'-hs', '0', '-sample', '1e-4', '-threads', '20', '-binary', '0',
			'-iter', '15'])


def finish():
	''' Clean the directory and perform final operations. '''

	print('[+] Finishing...')

	print('\t- Cleaning files')
	sp.call(['rm', '-rf', DATA_FOLDER])
	sp.call(['make', 'all', '-C', 'word2vec'])

	NULL.close()
	print('Done.')


def main(input_folder):
	''' Main program. 

		@type	input_folder:	string
		@param 	input_folder:	Name of input folder
		'''

	setup()
	pre_process(input_folder)
	build_vectors()
	finish()

	return vocabs