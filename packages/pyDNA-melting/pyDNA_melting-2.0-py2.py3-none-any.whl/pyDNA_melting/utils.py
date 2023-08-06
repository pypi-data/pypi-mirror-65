

import os
import uuid
import pandas as pd
import numpy as np
import argparse
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
code_dir = p_dir+"scripts/"
def run_matlab_code(seq):
	
	# step 1: copy matlab code to users folder because matlab scripts can't take parameters
	random_folder = "."+str(uuid.uuid4()).split("-")[-1]
	os.system("mkdir {0};cd {0};ln -s {1}* .".format(random_folder,code_dir))
	
	# step 2: run matlab
	command = """cd %s;matlab -nodisplay -nodesktop -nosplash -nojvm -r "weka_run(char('%s'),10,0.1,6); exit ; exit()" """%(random_folder,seq)
	print (command)
	os.system(command)
	
	# step3 parse job.out
	df = pd.read_csv("%s/job.out"%(random_folder))
	print (df.head())
	
	# step4 delete dir
	os.system("rm -r %s"%(random_folder))
	
	return df


def ML_features(seq):
	"""Return a list of 8 values for ML table"""
	df = run_matlab_code(seq)	
	melting_mean = df['predicted'].mean()
	df['ratio'] = df['predicted']/melting_mean
	df['ratio'] = df['ratio'].apply(lambda x: np.log2(x))
	first_two = df['ratio'].tolist()[:2]
	last_two = df['ratio'].tolist()[-2:]
	ratio_max = df['ratio'].max()
	ratio_min = df['ratio'].min()
	ratio_std = df['ratio'].std()
	return first_two+last_two+[melting_mean,ratio_max,ratio_min,ratio_std]


