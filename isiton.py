#!/usr/bin/python
from rdio import Rdio
from flask import Flask
import requests
import xml.etree.ElementTree as ET
app = Flask(__name__)

@app.route("/")
def isiton():
	return "Hello World!"

@app.route('/search/<song>')
def search(song):
	song = song.replace(';', '')
	spotify_request = requests.get('http://ws.spotify.com/search/1/track?q=%s' % song)
	spotify_root = ET.fromstring(spotify_request.content) #parse the xml out so we can do things with it
	spotify_song = ''
	if spotify_root[1].text != '0':
		spotify_attrib = spotify_root[4].attrib #this looks like {'href': 'spotify:track:5TdAgcKS5HlxMcclStHODW'}
		spotify_song = spotify_root[4][0].text
		#at this point, we have the spotify song
	
	#rdio is up next
	rdio = Rdio(("ad6x8mefbh2b2kh3deezgfq2", "tdWYdpKBfH"))
	rdio_song = rdio.call("search", {"query": song, "types": "Track"})
	if (rdio_song["status"] == "ok" and rdio_song["result"]["track_count"] != 0):
		return rdio_song["result"]["results"][0]["name"] + " " + rdio_song["result"]["results"][0]["artist"]
	else:
		return "didn't work"

if __name__ == "__main__":
	app.run(debug=True)