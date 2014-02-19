# This is pullrenew.py file
import rw

def renew(iterm, name, data):
	meta_dict = rw.readDict('metadata.txt')
	meta_dict['download'][name][iterm] = data
	rw.write('metadata.txt', meta_dict)
	print 'renew ' + iterm + ': ' + data