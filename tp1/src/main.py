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
BOOKS_FOLDER = 'books'


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

	sp.call(['rm', '-rf', BOOKS_FOLDER])
	sp.call(['mkdir', BOOKS_FOLDER])

	return


def trim_file(input_folder, filename):
	''' Remove symbols from a particular file, leaving only alphanumeric
		characters, and dump the result to file. 

		@type 	input_folder:	str
		@param 	input_folder:	Input folder path

		@type	filename:	str
		@param 	filename:	Name of the file to trim
		'''

	file = open(input_folder + '/' + filename, 'r')
	out_file = open(BOOKS_FOLDER + '/' + filename, 'w')

	print('\t- ' + filename)

	for line in file:
		out_file.write(re.sub(r'[^\w \n]', '', line))

	file.close()
	out_file.close()

	return


def pre_process(args):
	''' Process input books and produces new files without unnecessary
		characters and tokenized words.

		@type	args:	args.Namespace
		@param 	args:	Program's arguments
		'''

	print('[+] Processing input files')

	file_names = [f for f in os.listdir(args.INPUT_FOLDER)]
	file_names.sort()

	for filename in file_names:
		trim_file(args.INPUT_FOLDER, filename)

	return


def main():
	''' Main program. '''

	setup()
	args = parse_arguments()
	pre_process(args)


main()