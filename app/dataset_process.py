#!/usr/bin/python
import pandas as pd
import json
import sys
import os
import pandas as pd
import numpy as np
import shutil
import logging
from PIL import Image
import datetime

def set_status(datasetPath, status, message):
	dset_status = {}
	dset_status["status"] = status
	dset_status["message"] = message
	with open (datasetPath + ".status.json", "w") as myfile:
		json.dump(dset_status, myfile)
	set_log(datasetPath, message)

def set_log(datasetPath, message):
	with open(datasetPath + ".log.txt", "a+") as logfile:
		logfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ") + message + "\n")

def getColType(datasetPath, value):
	try:
		v = float(value)
		return "Numeric"
	except:
		if os.path.isfile(datasetPath + value):
			filename = datasetPath + value
			try:
				npzfile = np.load(filename)
				if len(npzfile.files):
					return "Numpy"
			except:
				pass
			return "Image"
		elif ";" in value:
			return "Array"
		else:
			return "Categorical"

def process_dataset (datasetPath):
	
	if os.path.exists(datasetPath + 'train.csv'):
		try:
			df = pd.read_csv(datasetPath + 'train.csv')
		except Exception as e:
			set_status(datasetPath, "error", "Error in reading train.csv. Please make sure train.csv is a valid CSV file. System error: " + str(e))
			return
	else:
		set_status(datasetPath, "generating", "generating train.csv...")
		with open (datasetPath + "train.csv", "w") as myfile:
			myfile.write("Label,Filename\n")
			pathlen = len(datasetPath)
			for root, dirs, files in os.walk(datasetPath):
				if '__MACOSX' in root:
					continue
				if len(dirs) == 0:
					for filename in files:
						myfile.write(root[pathlen:] + ",./" + root[pathlen:] + "/" + filename + "\n")
		df = pd.read_csv(datasetPath + 'train.csv')
	
	set_log(datasetPath, "Found " + str(len(df.index)) + " records.")
	
	set_status(datasetPath, "checking", "checking dataset...")

	if df.isnull().values.any():
		set_status(datasetPath, "error", "dataset contains NULL values.")

		for col in df:
			nullIdx = df[df[col].isnull()].index.tolist()
			set_log(datasetPath,"Column '" + col + "' NULL indexes:\n" + str(nullIdx))
		return

	df2=df.apply(pd.Series.nunique)
	index = 0
	if not os.path.exists(datasetPath + "meta.json"):
		set_status(datasetPath, "generating", "generating type information...")
		meta_info = {}
		for col in df:
			
			meta_info[col] = {"port" : "InputPort0", "type" : getColType(datasetPath, df.iloc[0][col])}
			meta_info[col]['categories'] = int(df2[index])
			if meta_info[col]['categories'] > 1000 and (meta_info[col]["type"] == 'Categorical') :
				meta_info[col]["port"] = ""
			index = index + 1

			set_log(datasetPath,col + ":" + meta_info[col]["type"])

		with open (datasetPath + "meta.json", "w") as myfile:
			json.dump(meta_info, myfile)
	
	set_status(datasetPath, "ready", "")

if len(sys.argv) == 2:
	datasetPath = sys.argv[1] + "/"

process_dataset(datasetPath)