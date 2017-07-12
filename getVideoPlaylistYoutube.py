from __future__ import unicode_literals
import youtube_dl
from urllib.request import urlopen
import json
import os
BASE_DIR = os.getcwd()
googleApiKey = 'AIzaSyATWJ9P-AeIBmBpKQ6Ne7fFWi7mqCImZlw'
videosPerPage = 20
f = open("playlist.txt","r")
rows = f.read().split("\n")
f.close()
playListIdList = []

for row in rows:
	playListIdList.append( row.split("&list=")[1].strip() )


for playListId in playListIdList:
	videoList = []
	f = open("codio.txt","a")
	url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults={}&playlistId={}&key={}'.format(videosPerPage,playListId, googleApiKey)
	jsonResponse = json.loads( ( urlopen( url ).read() ).decode('utf-8') )
	totalResults = jsonResponse["pageInfo"]["totalResults"]
	resultsPerPage = jsonResponse["pageInfo"]["resultsPerPage"]
	for i in range( min( resultsPerPage, totalResults ) ):
		description =  jsonResponse["items"][i]["snippet"]["description"] 
		videoId = jsonResponse["items"][i]["snippet"]["resourceId"]["videoId"] 
		videoList.append( videoId )
		title = jsonResponse["items"][i]["snippet"]["title"]
		#print("scrivo")
		f.write("{} {} {}\n".format( videoId, title, description ))
	try:
		nextPageToken = jsonResponse["nextPageToken"]
	except:
		nextPageToken = 0	
		
	while (nextPageToken):
		url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults={}&playlistId={}&key={}&pageToken={}'.format(videosPerPage,playListId, googleApiKey, nextPageToken)
		jsonResponse = json.loads( ( urlopen( url ).read() ).decode('utf-8') )
		totalResults = jsonResponse["pageInfo"]["totalResults"]
		for i in range( min( resultsPerPage, totalResults ) ): 
			## Only now I see in the json you have not the number count of results per page
			try:
				videoId = jsonResponse["items"][i]["snippet"]["resourceId"]["videoId"]
				videoList.append( videoId )
			except:
				continue
			description =  jsonResponse["items"][i]["snippet"]["description"] 
			title = jsonResponse["items"][i]["snippet"]["title"]
			f.write("{} {} {}\n".format( videoId, title, description ))
		try:
			nextPageToken = jsonResponse["nextPageToken"]
		except:
			nextPageToken = 0		
	f.close()

	os.chdir(BASE_DIR)
	#print(playListId)
	if not os.path.exists(playListId):
		os.makedirs(playListId)
	os.chdir(playListId)
	for vid in videoList:
		ydl_opts = {}
		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download(['http://www.youtube.com/watch?v={}'.format(vid)])
		except:
			f1 = open("log.txt","a")
			f1.write(vid + "\n")
			f1.close()
