import glob, os, fnmatch
import pandas as pd

def thread_loader(thread_name_substring):
	#print(os.getcwd())
	path="./flaskexample/static/data/"
	file_name_pattern="*"+thread_name_substring+"*.csv"
	for root, dirs, files in os.walk(path):
		for name in files:
			if fnmatch.fnmatch(name,file_name_pattern):
				return	pd.read_csv(path+name)
	

if __name__ == '__main__':
	thread_loader("tak")