Dota-Stuff
==========

Dota Stats from the steam API


SteamInfo.py 
  Designed for basic calls to the steam/dota api
  
dotaMatches.py 
  Grabs the latest matches/match history for players. Saves to local .json file

dotaBuffParser.py 
  Should scrape dotabuff for a players match history.
    Currently broken for some reason.
    Gets most of the way through and errors at the end.
    I suspect ive been an idiot.
  
mutchIO.py
  Various ways of interacting with other things.
  Vitally includes the getWebAddress Function used by SteamInfo.
    This will limit API calls to 1 every 1(by default) second as per the dota dev forums request
  
