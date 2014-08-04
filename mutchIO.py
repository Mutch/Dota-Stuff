from time import time, sleep

from pprint import pprint

global curTime
curTime = 0

lots = "The Secret to Life the universe and everything is love"

print()
print("mutchIO Loaded")
print()

#write log

def readWebAddress(url,waitTime = 1,tryAgain = True): 
	"""This gets information from web address"""
	import urllib.request, urllib.error, urllib.parse
	connection = False
	contents = (0,"a wild error appeared")
	global curTime

	if curTime + waitTime > time():
		sleep(waitTime)   
	curTime = time()
	print(url," accessed at ",curTime)
	print()

	try:
		connection = urllib.request.urlopen(url)
		contents = connection.read().decode("utf-8","ignore")
	except urllib.error.URLError as err:
		print(("-\n--\n-\nDidn't connect to server\n%s\n-\n--\n-" % err.reason))
		contents = (0,err.reason)
		if tryAgain:
			print("Waiting 30 seconds and trying again")
			sleep(30) 
			contents = readWebAddress(url,waitTime,False)
			if contents[0]:
				print("Success on the second go")
	finally: 
		if connection: connection.close()
		return contents

		
	
def changeEncoding(thing, encoding = "ascii", errorType = 'backslashreplace'):
	if type(thing) is str:
		return thing.encode(encoding, errorType)
	elif type(thing) is dict:
		return {changeEncoding(k, encoding, errorType):changeEncoding(v, encoding, errorType) for k,v in thing.items()}
	elif type(thing) is list or type(thing) is tuple:
		return [changeEncoding(l, encoding, errorType) for l in thing]
	elif type(thing) is int:return str(thing)
	elif type(thing) is set:return set(changeEncoding(list(thing), encoding, errorType))
	elif type(thing) is frozenset:return frozenset(changeEncoding(list(thing), encoding, errorType))
	elif thing is None:return thing
	else: print("%s is type %s and not touched." % (thing, type(thing)))
	return thing
	
def printer(thing = ""):

	if thing == lots:
		print()
		print()
		print()
		print()
		return

	#write log
	
	try:
		pprint(thing)
	except UnicodeEncodeError:
		pprint(changeEncoding(thing, "cp437"))
	

	
def writeFile(filename, data, type = "json",encoding = False):
	if "." not in filename: filename=filename+"."+ type
	if encoding:data = changeEncoding(data,encoding)
	try:
		if type == "json":
			import json as json
			with open(filename, 'w') as outfile:
				json.dump(data, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
		else:
			f = open(filename, 'w')
			f.write(data)
			f.close()
	except IOError: return (0, "IO error")
	return (1, "Success")

def readFile(filename):
	if "." not in filename: filename=filename+".json"
	type = filename[filename.rindex(".")+1:]
	try:
		f = open(filename)
		fileDump = f.read()
		f.close()
	except IOError: return ""
	if not fileDump: return (0, "File Empty")
	if type == "json":
		import json as json
		fileInfo = json.loads(fileDump)
	else: fileInfo = fileDump
	return fileInfo	
	

#csv writing
#http://java.dzone.com/articles/python-101-reading-and-writing
#https://docs.python.org/3/library/csv.html

"""
#testing Encoding
IDtemp = 76561197962462111

url = "http://dotabuff.com/players/" + str(IDtemp) + "/matches?page=5"
webDump = readWebAddress(url,10)	

#print(webDump)
printer(lots)
printer(webDump[70000:])
webDump = changeEncoding(webDump[70000:])
#print(webDump)
printer(lots)
print(type(webDump))
printer(lots)


webDump = webDump.decode(encoding="cp437", errors="replace")

#print(writeFile("test",webDump))
print(writeFile("test",webDump,"txt"))
"""

pass 
