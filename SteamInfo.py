#YOUR STEAM KEY GOES IN ANOTHER FILE

import SteamKey
steamkey = SteamKey.key


import mutchIO as mIO
from mutchIO import printer as print
from mutchIO import lots

#steam ID conversions
def acc32bit_to_acc64bit(accNum32Bitdec):
	try: 
		accNum32Bitdec = int(accNum32Bitdec)
	except ValueError: 
		print ("Wrong Type")
		return (0, "wrong type")
	
	accNum64Bit = accNum32Bitdec + 76561197960265728
	return accNum64Bit

def acc64bit_to_acc32bit(accountNumdec):
	try: 
		accountNumdec = int(accountNumdec)
	except ValueError: 
		print ("Wrong Type")
		return (0, "wrong type")
	if accountNumdec < 76561197960265728:
		return accountNumdec
	
	return accountNumdec - 76561197960265728
	

def steamID_to_acc64bit(steamID):
	"""
	STEAM_0:y:z
	To convert a Steam ID to a Community ID, use the following equation:
	ID = 76561197960265728 + y + (z X 2)
	"""
	#y is always one char long

	accountNum = 76561197960265728 + (int(steamID[8])) + (2*(int(steamID[10:])))
	
	return accountNum
	
def acc64bit_to_steamID(accountNum):
	"""
	STEAM_0:y:z
	To convert a Community ID to a Steam ID, use the following equation:
	z = (CommunityID - 76561197960265728 - y) / 2
	
	Note: Determining the y value is simple. 
	If the Community ID is an even number y must be equal to 0, 
	and if it is an odd number y must be equal to 1.
	"""
	
	if accountNum % 2 == 0: y = 0
	else: y = 1
	z = int((accountNum - 76561197960265728 - y) / 2)
	return "STEAM_0:" + str(y) + ":" + str(z)
	

#steam API calls
def get_friendsList(accountNum,IDOnly = False): #takes 64bit accNo
	#and returns a list of dictionaries from steam server

	if type(accountNum) is int: accountNum = str(accountNum)
	elif type(accountNum) is not str: return [0,"accountNum is wrong type"]
	elif int(accountNum) < 76561197960265728: return [0,"accountNum is too low to be a valid ID"]
	
	url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?"
	
	url = url +  "key=%s&steamid=%s" % (steamkey, accountNum)

	f = mIO.readWebAddress(url)
	if not f: return [0,"Could Not Download from Steam Server"]
	
	import json as json
	fileDump = json.loads(f)

	if IDOnly: return [int(f["steamid"]) for f in fileDump["friendslist"]["friends"]]
	else: return fileDump["friendslist"]["friends"]

def get_playerInfo(accountNumlist): #takes a list of accountNums and returns
	
	if type(accountNumlist) is list or type(accountNumlist) is tuple: #pre test value
		templist = [str(f) for f in accountNumlist if (type(f) is str or type(f) is int)]
		if not len(templist) == len(accountNumlist):
			return [0,"element in list is wrong type"]
		templist = [f for f in templist if int(f) > 76561197960265728]
		if not len(templist) == len(accountNumlist):
			return [0,"element in list is too low to be a valid ID"]
	elif type(accountNumlist) is int or type(accountNumlist) is str:
		if int(accountNumlist) < 76561197960265728:
			return [0,"accountNum is too low to be valid"]
		else: templist = [str(accountNumlist)]
	else: return [0,"accountNum is wrong type"]
	listPlayers = []
	intIDs = len(templist)
	sectionStart = 0
	sectionEnd = 100
	
	while True: #break is later.
		if intIDs < sectionEnd:
			sectionEnd = intIDs
	
		url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?"
		
		url = url +  "key=%s&steamids=%s" % (steamkey, ",".join(templist[sectionStart:sectionEnd]))
		#http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=A3EE86FFD33DF8E396FC9DC17EA28123&steamids=76561197962462111,76561197960696226
		
		f = mIO.readWebAddress(url)
		if not f: return [0,"Could Not Download from Steam Server"]
		
		import json as json
		fileDump = json.loads(f)
		
		#expected format
		"""
		{
			"response": {
				"players": [
					{
						"steamid": "76561197962462111",
						"communityvisibilitystate": 3,
						"profilestate": 1,
						"personaname": "Mutch",
						"lastlogoff": 1398683575,
						"profileurl": "http://steamcommunity.com/id/Mutch/",
						"avatar": "http://media.steampowered.com/steamcommunity/public/images/avatars/34/348c0ea5da0ca5e9da7bb68038c345d2ed40a44c.jpg",
						"avatarmedium": "http://media.steampowered.com/steamcommunity/public/images/avatars/34/348c0ea5da0ca5e9da7bb68038c345d2ed40a44c_medium.jpg",
						"avatarfull": "http://media.steampowered.com/steamcommunity/public/images/avatars/34/348c0ea5da0ca5e9da7bb68038c345d2ed40a44c_full.jpg",
						"personastate": 1,
						"realname": "Mitch Carter",
						"primaryclanid": "103582791429601458",
						"timecreated": 1067655710,
						"personastateflags": 0,
						"loccountrycode": "AU",
						"locstatecode": "QLD",
						"loccityid": 4909
					},
					{
						"steamid": "76561197960696226",
						"communityvisibilitystate": 3,
						"profilestate": 1,
						"personaname": "Taffy #roadto1000mmr",
						"lastlogoff": 1398612822,
						"profileurl": "http://steamcommunity.com/id/NamTaf/",
						"avatar": "http://media.steampowered.com/steamcommunity/public/images/avatars/75/75e135a335e18d077bee909f6b4c73380f4870d3.jpg",
						"avatarmedium": "http://media.steampowered.com/steamcommunity/public/images/avatars/75/75e135a335e18d077bee909f6b4c73380f4870d3_medium.jpg",
						"avatarfull": "http://media.steampowered.com/steamcommunity/public/images/avatars/75/75e135a335e18d077bee909f6b4c73380f4870d3_full.jpg",
						"personastate": 3,
						"realname": "Nam Taf",
						"primaryclanid": "103582791429601458",
						"timecreated": 1063607484,
						"personastateflags": 0
					}
				]
				
			}
		}	
		"""
		
		listPlayers.append(fileDump["response"]["players"])
		
		if sectionEnd == intIDs: break
		else:
			sectionStart = sectionStart + 100
			sectionEnd = sectionEnd + 100
		
	
	return listPlayers #returns a list of dictionaries

def resolve_VanityUrl(vanityURL): #takes vanity url and returns accno64bit
	if type(vanityURL) is not str:
		return (0,"VanityURL is not a string and it should be")
	
	url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=%s&vanityurl=%s" % (steamkey,vanityURL)
		
	f = mIO.readWebAddress(url)
	
	import json as json
	fileDump = json.loads(f)	

	if fileDump["response"]["success"] != 1:
		print(fileDump["response"]["message"])
		return (0,fileDump["response"]["message"]) 

	return fileDump["response"]["steamid"]

def get_playerItems(accountNum, gameNum = "570"):#570 is dota2
	if type(accountNum) is int: accountNum = str(accountNum)
	elif type(accountNum) is not str: return [0,"accountNum is wrong type"]
	elif int(accountNum) < 76561197960265728: return [0,"accountNum is too low to be a valid ID"]
	
	url = "http://api.steampowered.com/IEconItems_%s/GetPlayerItems/v0001/?key=%s&steamid=%s&language=en" % (gameNum,steamkey,accountNum)
		
	f = mIO.readWebAddress(url)
	
	import json as json
	fileDump = json.loads(f)	

	if fileDump["result"]["status"] != 1:
		if fileDump["result"]["status"] == 8:
			tempmsg = "The Steam ID was invalid"
		elif fileDump["result"]["status"] == 15:
			tempmsg = "The Backpack was Private"
		elif fileDump["result"]["status"] == 18:
			tempmsg = "The Steam ID doesnt Exist"
		else: tempmsg = "WTFBBQ, who knows what went down??"
		tempmsgExpanded = "There was an error. %s" % (tempmsg)
		print(tempmsgExpanded)
		return (0,tempmsgExpanded) 

	return fileDump["result"]["items"]

def get_itemSchema(gameNum = "570",language = "en"):#570 is dota2
	
	url = "http://api.steampowered.com/IEconItems_%s/GetSchema/v0001/?key=%s&language=%s" % (gameNum,steamkey,language)
		
	f = mIO.readWebAddress(url)
	
	import json as json
	fileDump = json.loads(f)	

	if fileDump["result"]["status"] != 1:
		tempmsg = "WTFBBQ, who knows what went down??"
		tempmsgExpanded = "There was an error. %s" % (tempmsg)
		print(tempmsgExpanded)
		return (0,tempmsgExpanded) 

	return fileDump["result"]["items"]

	
	#dota API calls
def get_matchHistory(player_name="",hero_id="",skill="",date_min="",date_max="",account_id="",start_at_match_id="",league_id="",matches_requested=""):
	#arguments
	"""
		player_name=<name> # Search matches with a player name, exact match only
		hero_id=<id> # Search for matches with a specific hero being played, hero id's are in dota/scripts/npc/npc_heroes.txt in your Dota install directory
		skill=<skill>  # 0 for any, 1 for normal, 2 for high, 3 for very high skill
		date_min=<date> # date in UTC seconds since Jan 1, 1970 (unix time format)
		date_max=<date> # date in UTC seconds since Jan 1, 1970 (unix time format)
		account_id=<id> # Steam account id (this is not SteamID, its only the account number portion)
		league_id=<id> # matches for a particular league
		start_at_match_id=<id> # Start the search at the indicated match id, descending										
	"""	
	arguments = ""
	#if argument is passed add it to url. No checking is done.
	if player_name: 
		arguments = arguments + "&player_name=" + str(player_name)
	if hero_id: 
		arguments = arguments + "&hero_id=" + str(hero_id)
	if skill: 
		arguments = arguments + "&skill=" + str(skill)
	if date_min: 
		arguments = arguments + "&date_min=" + str(date_min)
	if date_max: 
		arguments = arguments + "&date_max=" + str(date_max)
	if league_id:
		arguments = arguments + "&league_id=" + str(league_id)
	if account_id: 
		arguments = arguments + "&account_id=" + str(account_id)
	if start_at_match_id: 
		arguments = arguments + "&start_at_match_id=" + str(start_at_match_id)
	if matches_requested: 
		arguments = arguments + "&matches_requested=" + str(matches_requested)
	if arguments: 
		arguments = arguments + "&key=" + steamkey	
	
	url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?%s" % arguments
	
	f = mIO.readWebAddress(url)
	
	import json as json
	fileDump = json.loads(f)
	
	if fileDump["result"]["status"] != 1:
		print(fileDump["result"]["statusDetail"])
		return (0,fileDump["result"]["statusDetail"])
	"""
	expected format below
			"matches": [
			{
				"match_id": 633544171,
				"match_seq_num": 575616768,
				"start_time": 1398773559,
				"lobby_type": 0,
				"players": [
					{
						"account_id": 82463417,
						"player_slot": 0,
						"hero_id": 36
					},
					{
						"account_id": 86162800,
						"player_slot": 1,
						"hero_id": 102
					},
					{
						"account_id": 44843016,
						"player_slot": 2,
						"hero_id": 31
					},
					{
						"account_id": 66526697,
						"player_slot": 3,
						"hero_id": 21
					},
					{
						"account_id": 23793398,
						"player_slot": 4,
						"hero_id": 78
					},
					{
						"account_id": 2196383,
						"player_slot": 128,
						"hero_id": 2
					},
					{
						"account_id": 39226070,
						"player_slot": 129,
						"hero_id": 19
					},
					{
						"account_id": 42856552,
						"player_slot": 130,
						"hero_id": 57
					},
					{
						"account_id": 430498,
						"player_slot": 131,
						"hero_id": 58
					},
					{
						"account_id": 52804658,
						"player_slot": 132,
						"hero_id": 75
					}
				]
				
			},
	"""
	return fileDump["result"]["matches"]#returns a list of dictionaries.

def get_matchDetail(matchID,waitTime = 1):# takes match id and returns match dictionary
	if type(matchID) is str:pass
	elif type(matchID) is int: matchID = str(matchID)
	else: return (0,"the Match ID is the wrong type")
	
	
	url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key=%s&match_ID=%s" % (steamkey,matchID)
	
	f = mIO.readWebAddress(url,waitTime)

	try:
		import json as json
		fileDump = json.loads(f)
	except TypeError:
	
		print(lots)
		print("Match ID: " + str(matchID))
		print("Error: " + f[1])
		return

	return fileDump["result"]#returns a list of dictionaries.

def get_HeroDict():
	url = "https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?"
	url = url +  "key=%s" % (steamkey)
	
	f = mIO.readWebAddress(url)
	if not f: return [0,"Could Not Download from Steam Server"]
	
	import json as json
	fileDump = json.loads(f)
	
	dictHero = {f["id"]:f["name"][14:] for f in fileDump["result"]["heroes"]}
	
	return dictHero
	
if __name__ == "__main__":
	print("Steam Key Being Used Is: " + steamkey)
	
	
pass 