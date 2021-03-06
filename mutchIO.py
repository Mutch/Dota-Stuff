from time import time, sleep
from pprint import pprint
import shutil
import os

#backup directory for writes
backupDir = "./Backup"

global curTime
curTime = 0

lots = "The Secret to Life the universe and everything is love"

print()
print("mutchIO Loaded")
print()

#write log

def readWebAddressLocalCache(url,cacheTimeDateTime,waitTime = 1,tryAgain = 2):
	import datetime as dt
	#cache directory for lookups
	cacheDir = "./URL Cache"
	dateTimeStrFormat = "%d-%m-%Y-%H-%M"
	urlFileName = "".join(c for c in url if c.isalnum() or c == ".")
	
	if not (os.path.isdir(cacheDir)):
		os.mkdir(cacheDir)
	
	if type(cacheTimeDateTime) is dt.datetime:
		pass
	elif type(cacheTimeDateTime) is dt.date:
		time = dt.time(hour=23, minute=59)
		cacheTimeDateTime = dt.combine(cacheTimeDateTime, time)
	elif type(cacheTimeDateTime) is dt.timedelta:
		cacheTimeDateTime = dt.datetime.today() - cacheTimeDateTime
	elif type(cacheTimeDateTime) is int or type(cacheTimeDateTime) is float:
		cacheTimeDateTime = dt.datetime.today() - dt.timedelta(days=cacheTimeDateTime)

	urlInfo = False
	fileName = ""
	#read cache
	if type(cacheTimeDateTime) is dt.datetime:
		cacheList = os.listdir(cacheDir)
		cacheList = [f for f in cacheList if f.startswith(urlFileName)]
		
		if cacheList:
			fileName =  cacheList[0]
			fileNameList = fileName.split(".")
			fileNameDateString = fileNameList[-2]
			#try
			fileDateTime = dt.datetime.strptime(fileNameDateString, dateTimeStrFormat)

			if cacheTimeDateTime < fileDateTime:
				urlInfo = readFile(os.path.join(cacheDir,fileName))
				print()
				print("Local Cache of", url,"accessed at",dt.datetime.today())
				print("Cache was grabbed at",fileDateTime)
				print()
				
	#write cache	
	if not urlInfo: 
		urlInfo = readWebAddress(url,waitTime,tryAgain)
		
		accessTime = dt.datetime.today()
		accessTimeString = accessTime.strftime(dateTimeStrFormat)
		
		cacheFileName = urlFileName + "." + accessTimeString
		
		if os.path.isfile(os.path.join(cacheDir,fileName)):
			os.remove(os.path.join(cacheDir,fileName))
			
		writeFile(os.path.join(cacheDir,cacheFileName), urlInfo, type = "txt")
		print(url, "Saved to local cache")

	return(urlInfo)

def readWebAddress(url,waitTime = 1,tryAgain = 2): 
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
			print("...")
			contents = readWebAddress(url,waitTime,tryAgain - 1)
			if contents[0]:
				print("Success on the second go")
				print()
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
		if type(thing) == str:
			print(thing)
			return
		else:
			pprint(thing)
	except UnicodeEncodeError:
		pprint(changeEncoding(thing, "cp437"))
	
def backupFile(origFileName,backupFileName):

	if not (os.path.isdir(backupDir)): #make backup dir
		os.mkdir(backupDir)
	else:#is there an existing backup?
		if (os.path.isfile(backupFileName)):
			oldBackupFileName = backupDir + "/" + origFileName + ".oldbackup"
			shutil.copy2(backupFileName,oldBackupFileName)
	
	if not (os.path.isfile(origFileName)): return None
	else:
		shutil.copy2(origFileName,backupFileName)

	pass
	
def writeFile(filename, data, type, encoding = False):
	if not filename.endswith(type): 
		filename=filename+"."+ type
	else:
		tempIndex = filename.rindex(".")
		type = filename[tempIndex+1:]
	
	filenameOnly = os.path.split(filename)[1]
	backupFileName = os.path.join(backupDir,filenameOnly + ".backup")
	backupFile(filenameOnly,backupFileName)
	
	if encoding:data = changeEncoding(data,encoding)
	
	try:
		if type == "json":
			import json as json
			with open(filename, 'w') as outfile:
				json.dump(data, outfile, sort_keys = True, indent = 4, ensure_ascii=True)
		else:
			f = open(filename, 'w')
			f.write(data)
			f.close()
	except: #restoring backup
		
		print()
		print("Trying to Restore Backed Up File")
		print()
		try:
			shutil.copy2(backupFileName,filename)
			print("Backup Restored Successfully")
		except FileNotFoundError: 
			os.remove(filename)
			print("Backup Does Not Exist - This was First File Creation")

		print()
		
		raise
	
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
		try: fileInfo = json.loads(fileDump)
		except ValueError: return ""

	else: fileInfo = fileDump
	return fileInfo	

def exitProgram(closeNote = "Program Will Now Terminate"):
	import sys
	sys.exit(closeNote)	

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

if __name__ == "__main__":
	printer(lots)
	printer("Nothing To See Here")
	printer(lots)


pass 
