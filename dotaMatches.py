import mutchIO as mIO
from mutchIO import printer as print
from mutchIO import lots

import SteamInfo as StIn
#file IO
"""
def readFile(filename):
	if "." not in filename: filename=filename+".dat"
	try:
		f = open(filename)
		fileDump = f.read()
		f.close()
	except IOError: return ""
	if not fileDump: return (0, "File Empty")
	import json as json
	fileInfo = json.loads(fileDump)
	return fileInfo
"""
"""
def writeFile(filename, data, type = "json"):
	if "." not in filename: filename=filename+"."+ type
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
"""	
def read_MatchHistoryLocal(ID=""):#takes id and returns a list of matches with date
	fileInfo = mIO.readFile("Dota2PlayerMatchHistories.json")
	if not fileInfo: return (0, "No file")

	if ID:
		if ID in fileInfo.keys():
			return fileInfo[ID]
		else: return (0, "Player Not in File")
	return fileInfo
	
def write_MatchHistoryLocal(dictMatchHistorytoWrite):
	if type(dictMatchHistorytoWrite) is not dict:
		return (0, "info to write is not in type dictionary")
	if not {k:v for k,v in dictMatchHistorytoWrite.items() if v}:
		return (0, "lists in dictionary are empty")
		
	existing_MatchHistories = read_MatchHistoryLocal()
	if type(existing_MatchHistories) is not dict: existing_MatchHistories = {}
	existing_MatchHistories.update(dictMatchHistorytoWrite)
	return mIO.writeFile("Dota2PlayerMatchHistories.json",existing_MatchHistories)
	
def read_MatchesLocal(IDs=("just get the keys out will you please",)):#takes id list and returns a dict of matches and info
	if type(IDs) is not tuple and type(IDs) is not list:
		return (0, "Was expecting a list but got%s" % type(IDs))
	if not IDs: return {}
	try:
		[int(f) for f in IDs]
	except:
		if IDs[0] == "just get the keys out will you please" or IDs[0] == "all": pass
		else: return (0, "At least one match ID is not correct")

	fileInfo = mIO.readFile("Dota2MatchInformation.json")
	if not fileInfo: return (0, "No file")
	
	fileInfo = {int(k):v for k,v in fileInfo.items()}

	if IDs[0] == "just get the keys out will you please":
		return list(fileInfo.keys())
	if IDs[0] == "all":
		return fileInfo

	return {k:v for k,v in fileInfo.items() if k in IDs}

def write_MatchesLocal(dictMatchestoWrite):
	if type(dictMatchestoWrite) is not dict:
		return (0, "info to write is not in type dictionary")
	
	existing_Matches = read_MatchesLocal(("all",))

	if type(existing_Matches) is not dict: existing_Matches = {}
	existing_Matches.update(dictMatchestoWrite)
	
	return mIO.writeFile("Dota2MatchInformation.json",existing_Matches)
	
#steam Info
def get_LatestMatchHistory(ID): #returns a list of match summary dictionaries
	listLocalHistories = read_MatchHistoryLocal(ID)
	if listLocalHistories[0] == 0: 
		lastLocalMatch = 0
		listLocalHistories = ()
	else: lastLocalMatch = listLocalHistories[0]["match_id"]
		
	listNewHistories = []
	MatchID = ""
	count = 0
	forLoopComplete = True
	while forLoopComplete:
		listSteamHistories = StIn.get_matchHistory(account_id=ID,start_at_match_id=MatchID,matches_requested="")
		#if ID is wrong???? or check ID first???
		if not listSteamHistories:break
		for f in listSteamHistories:
			if f["match_id"] != lastLocalMatch:
				listNewHistories.append(f)
			else:
				listNewHistories.extend(listLocalHistories)
				forLoopComplete = False
				break
		
		count = count + 1
		if count == 20: break

		MatchID = listNewHistories[-1]["match_id"] - 1
	#end while
	
	if not listLocalHistories and len(listNewHistories) == 500:
		lastID = listNewHistories[-1]["match_id"]
		listDotaBuffHistories = get_DotaBuffHistories(ID,lastID,500)
		listNewHistories.extend(listDotaBuffHistories)

		
	write_MatchHistoryLocal({ID:listNewHistories})
	
	return listNewHistories

def get_LatestMatches(listMatchIDs):#returns a dict of match info

	if type(listMatchIDs) is not tuple and type(listMatchIDs) is not list:
		return (0, "Was expecting a list but got%s" % type(listMatchIDs))
	listMatchesHave = read_MatchesLocal() #get local keys

	listMatchesFromSteam = [f for f in listMatchIDs if f not in listMatchesHave]
	listMatchesFromLocal = [f for f in listMatchIDs if f not in listMatchesFromSteam]

	dictMatchesFromSteam = {f:StIn.get_matchDetail(f) for f in listMatchesFromSteam}
	dictMatchesFromLocal = read_MatchesLocal(listMatchesFromLocal)

	if type(dictMatchesFromLocal) is tuple: dictMatchesFromLocal = {}

	if dictMatchesFromSteam: write_MatchesLocal(dictMatchesFromSteam)
	dictMatchesFromSteam.update(dictMatchesFromLocal)
	
	return dictMatchesFromSteam

#dotabuff parser	
def get_DotaBuffHistories(ID, earliestMatchID = 0, noMatchesToIgnore = 500):
	import dotaBuffParser as dBP	
	
	firstpage = int(noMatchesToIgnore/20) - 1
	IDtemp = StIn.acc64bit_to_acc32bit(ID)	
	
	listDotaBuffMatchIDs = dBP.createMatchList(IDtemp, firstpage)
	
	if not listDotaBuffMatchIDs: 
		print(lots)
		print("Found Nothing From DotaBuff")
		print(lots)
		return []

	if earliestMatchID in listDotaBuffMatchIDs:
		earliestMatchIndex = listDotaBuffMatchIDs.index(earliestMatchID)
		listDotaBuffMatchIDs = listDotaBuffMatchIDs[earliestMatchIndex + 1:]
	else:
		if earliestMatchID:
			print(lots)
			print("Earliest Match ID - ",earliestMatchID, ", not found in DotaBuff List")
			print(lots)
			
	dictMatchInfo = get_LatestMatches(listDotaBuffMatchIDs)
	
	listDotaBuffMatchHistories = [dBP.makeMatchHistoryEntry(dictMatchInfo[f]) for f in listDotaBuffMatchIDs]
	
	return listDotaBuffMatchHistories

print("Dota Matches")


if __name__ == "__main__":
	
	"""
	IDtemp = (StIn.resolve_VanityUrl("Mutch"))

	get_LatestMatchHistory(IDtemp)
	"""
	dictIDtemp = {76561197962462111:"Mutch",76561197960696226:"Taffy",76561197999491798:"Kilthix",76561197961524497:"YubYub"}#,76561198003122280:"Inverter"} 
	
	listMatchHistories = [get_LatestMatchHistory(f) for f in dictIDtemp.keys()]
	
	for f in listMatchHistories:
		get_LatestMatches(f)
	
	
		

