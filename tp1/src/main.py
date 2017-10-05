#!/usr/bin/env python3

'''
main.py
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
parser = ap.ArgumentParser()
DATA_FOLDER = '__temp_data__'
BOOKS_FOLDER = 'books'
VECTORS_FOLDER = 'vectors'

NULL = None


def parse_arguments():
	''' Parse the program's arguments. 
		
		@rtype:		args.Namespace
		@return:	Program's arguments
		'''

	parser.add_argument('INPUT_FOLDER', type=str,
		help='Name of input folder')

	return parser.parse_args()


def setup():
	''' Set up current working folder. '''

	print('[+] Setting up')

	global NULL

	NULL = open(os.devnull, 'w')
	sp.call(['mkdir', DATA_FOLDER])
	sp.call(['mkdir', DATA_FOLDER + '/' + BOOKS_FOLDER])
	sp.call(['mkdir', DATA_FOLDER + '/' + VECTORS_FOLDER])

	print('\t- Building word2vec')
	sp.call(['make', 'all', '-C', 'word2vec'], stdout=NULL)

	return


def trim_file(input_folder, filename):
	''' Remove symbols from a particular book file, leaving only alphanumeric
		characters, and dump the result to file. 

		@type 	input_folder:	str
		@param 	input_folder:	Input folder path

		@type	filename:	str
		@param 	filename:	Name of the file to trim
		'''

	file = open(input_folder + '/' + filename, 'r')
	out_file = open(DATA_FOLDER + '/' + BOOKS_FOLDER + '/' + filename, 'w')

	print('\t- ' + filename)

	for line in file:
		out_file.write(re.sub(r'[^\w \n]', '', line))

	file.close()
	out_file.close()

	return


def pre_process(args):
	''' Process input books and produces new files without unnecessary
		characters.

		@type	args:	args.Namespace
		@param 	args:	Program's arguments
		'''

	print('[+] Processing input files')

	file_names = [f for f in os.listdir(args.INPUT_FOLDER)]
	file_names.sort()

	for filename in file_names:
		trim_file(args.INPUT_FOLDER, filename)

	return


def build_vectors():
	''' Build semantic word vectors for each book. '''

	print('[+] Building word vectors')
	book_names = [f for f in os.listdir(DATA_FOLDER + '/' + BOOKS_FOLDER)]
	book_names.sort()

	for book_name in book_names:
		vector_name = book_name[:-4] + '.bin'
		print('\t- ' + vector_name)
		sp.call([
			'./word2vec/word2vec',
			'-train',
			'{}/{}/{}'.format(DATA_FOLDER, BOOKS_FOLDER, book_name),
			'-output',
			'{}/{}/{}'.format(DATA_FOLDER, VECTORS_FOLDER, vector_name),
			'-cbow', '1', '-size', '200', '-window', '8', '-negative', '25',
			'-hs', '0', '-sample', '1e-4', '-threads', '20', '-binary', '1',
			'-iter', '15'])


def finish():
	''' Clean the directory and perform final operations. '''

	print('[+] Finishing...')

	print('\t- Cleaning files')
	sp.call(['rm', '-rf', DATA_FOLDER])
	sp.call(['make', 'clean', '-C', 'word2vec'], stdout=NULL)

	NULL.close()

	print('Done.')


def main():
	''' Main program. '''

	setup()
	args = parse_arguments()
	pre_process(args)
	build_vectors()
	finish()

main()