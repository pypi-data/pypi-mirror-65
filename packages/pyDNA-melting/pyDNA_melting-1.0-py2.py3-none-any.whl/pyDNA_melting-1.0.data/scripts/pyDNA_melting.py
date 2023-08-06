#!python

from pyDNA_melting.utils import *


"""

module load matlab
module load java


"""



def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-s','--seq',  help="seq", required=True)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	
	print (ML_features(args.seq))

if __name__ == "__main__":
	main()

	



