import mutchIO as mIO
from mutchIO import printer as print
from mutchIO import lots
print()
print("Dota Buff Parser")
print()
#url2Parse = "http://dotabuff.com/players/430498/matches?page=66"

def findInfo(text, strStart, strEnd, startLoc = 0):
	start = True
	end = True	
	indexStart = startLoc
	
	try: #find existing data
		indexStart = text.index(strStart, startLoc)
	except ValueError: start = False
	finally:
		try: indexEnd = text.index(strEnd, indexStart) + len(strEnd)
		except ValueError: end = False
		
	if start and end: return (text[indexStart:indexEnd],indexStart,indexEnd)
	return ("",0,0)

def extractInfoFromPage(htmlDump):

	(tableDump,dump1,dump2) = findInfo(htmlDump, "/th></tr></thead><tbody><tr", "</td></tr></tbody></table>")
	foundRow = True
	listRows = []
	rowStart = 0
	
	staTR = "<tr" #rows are <tr class="inactive"> for bot games etc
	endTR = "</tr>"
	staTD = "<td"
	endTD = "</td>"

	#break out the table into a list of lists
	#  0 ,  1   ,   2    ,   3    , 4 ,  5
	#Hero,Result,Match ID,Duration,KDA,Items
	while foundRow:
		(rowText,foundRow,rowStart) = findInfo(tableDump, staTR, endTR, rowStart)

		foundCell = True
		listCells = []
		cellStart = 0
		
		while foundCell:
			(cellText,foundCell,cellStart) = findInfo(rowText, staTD, endTD, cellStart)
		
			if cellText:
				listCells.append(cellText)
		#end while

		if listCells:
			listRows.append(listCells)
		else: break
	#end while

	#   0    , 1
	#Match ID,Hero,

	listMatchIDs = [f[1] for f in listRows]

	staMid = 'href="/matches/'
	endMid = '">'
	listMatchIDs = [findInfo(f, staMid, endMid) for f in listMatchIDs]

	#seperates it out into the actual ID
	listMatchIDs = [int(f[0][len(staMid):-len(endMid)]) for f in listMatchIDs]
	
	
	print("Match IDs")
	print(listMatchIDs)
	print(lots)
	return listMatchIDs
	
def createMatchList(dotaId,pageNum = 1):

	url = "http://dotabuff.com/players/" + str(dotaId) + "/matches?page="
	
	listMatchIDs = []
	
	doubleNothing = False
	
	while True:
		url2Parse = url + str(pageNum)
		
		webDump = mIO.readWebAddress(url2Parse,10)
		
		if not webDump[0]:
			return webDump

		endPageText = "Sorry, there's no data for this period."
		if endPageText in webDump:
			break

		listNewIDs = extractInfoFromPage(webDump)

		if listNewIDs:
			listMatchIDs.extend(listNewIDs)
		elif doubleNothing: break
		else: doubleNothing = True
		
		pageNum = pageNum + 1
		if pageNum == 100000: break
		
	return listMatchIDs
	
def makeMatchHistoryEntry(dictMatchDetailEntry):
	
	try:
		print("Making Match History Entry for Match: " + str(dictMatchDetailEntry["match_id"]))
		print()
	except KeyError:
		print(dictMatchDetailEntry)
		return
		
	
	newEntry = {}
	tupKeys2Keep = ("lobby_type","match_id","match_seq_num","players","start_time")
	tupPlayerKeys2Keep = ("account_id","hero_id","player_slot")
	
	newEntry = {f:dictMatchDetailEntry[f] for f in tupKeys2Keep}

	newPlayers = []
	
	for f in newEntry["players"]:
	
		try:f = {g:f[g] for g in tupPlayerKeys2Keep}
		except KeyError:
			tempDict = {}
			for g in tupPlayerKeys2Keep:
				if g in f:
					tempDict.update({g:f[g]})
			f = tempDict.copy()
					
		newPlayers.append(f)
			
	newEntry["players"] = newPlayers
	
	return newEntry
	

	
if __name__ == "__main__":
	#test stuff
	import SteamInfo as StIn

	IDtemp = StIn.acc64bit_to_acc32bit(76561198003122280)
	
	tempList = createMatchList(IDtemp,62)

	print(lots)
	print(len(tempList))
	print(lots)
	print(tempList)	
	
	
	print(lots)
	
	
	
	"""
	matchdetail = StIn.get_matchDetail(709503626)
	matchHistory = makeMatchHistoryEntry(matchdetail)

	print(matchHistory)
	
	tempList = [StIn.get_matchDetail(f) for f in tempList]
	
	print(lots)
	print(tempList)		
	print(lots)
	
	listmatchHistories = [makeMatchHistoryEntry(f) for f in tempList]
	print(listmatchHistories[0])

	IDtemp = 76561197960696226
	tempList = createMatchList(IDtemp,74)
	tempList = [StIn.get_matchDetail(f) for f in tempList]
	listmatchHistories = [makeMatchHistoryEntry(f) for f in tempList]
	print(listmatchHistories[0])
	"""
	
	
	



pass
