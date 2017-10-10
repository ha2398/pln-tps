#!/usr/bin/env python3

'''
main.py
Trabalho Prático 1 - Processamento de Linguagem Natural
UFMG/DCC
@author: Hugo Araujo de Sousa [2013007463]
@DCC030
'''

import argparse as ap
import build_vectors as bv
import build_distance_matrices as bdm


# Global variables.
parser = ap.ArgumentParser()


def parse_arguments():
	''' Parse the program's arguments. 
		
		@rtype:		args.Namespace
		@return:	Program's arguments
		'''

	parser.add_argument('INPUT_FOLDER', type=str,
		help='Name of input folder')

	return parser.parse_args()


def main():
	''' Main program. '''
	args = parse_arguments()
	vocabs = bv.main(args.INPUT_FOLDER)
	bdm.main()
	
	
main()