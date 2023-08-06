keys = []
values = []
ROWS = {}
def unpack(dictionary, nameName):
    for name1 in dictionary.keys():
        if type(dictionary[name1]) != dict:
            keys.append('{}_'.format(nameName) + name1)
            values.append(dictionary[name1])
        else:
            unpack(dictionary[name1], nameName)
    res = {keys[i]: values[i] for i in range(len(keys))} 
    return res

def passDataframe(df):
	# Create empty DataFrame
	import pandas as pd
	import numpy as np
	import json
	
	data = pd.DataFrame()

	for num1 in range(len(df)):
	    L = len(json.loads(df['contents'][num1]))

	    for num2 in range(L):
	        ROWS = {}
	        for name in df.columns:
	            if df[name].isna()[num1] == False:
	                key = []
	                value = []
	                if name not in ['business', 'contents', 'destination', 'origin', 'location']:
	                    ROWS[name] = df[name][num1]
	                elif name == 'business':
	                    ROWS.update(unpack(json.loads(df['business'][num1]), name))
	                elif name == 'contents':
	                    ROWS.update(unpack(json.loads(df['contents'][num1])[num2], name))
	                elif name == 'destination':
	                    ROWS.update(unpack(json.loads(df['destination'][num1]), name))
	                elif name == 'origin':
	                    ROWS.update(unpack(json.loads(df['origin'][num1]), name))
	                elif name == 'location':
	                    ROWS.update(unpack(json.loads(df['location'][num1]), name))
	            else:
	                ROWS[name] = 'Null'

	    data = data.append(ROWS, ignore_index=True)

	return data  


def mergeCSV(*argv):
	L = []
	for df in argv:
		L.append(df)
	dataFrame = pd.concat(L, axis = 0)
	return dataFrame