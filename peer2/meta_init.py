# This is meta_init.py file
import os
import sys
import time
import json

import rw

#only used to initialize the metadata.txt file.
name = raw_input('Enter file name: ')
pid  = raw_input('Enter pid: ')
path = os.path.join(os.getcwd(), 'files', 'original', name)
LMT = os.path.getmtime(path)
meta_dict = {
	'original': {
		name: {
			'mid': pid + '|' + str(2222 + 10 * int(pid)), 'version': 0, 'state': 'valid', 'TTR': 300, 'LMT': LMT
		}
	}
}

rw.write('metadata.txt', meta_dict)