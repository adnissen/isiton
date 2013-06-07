#!/usr/bin/python

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
	if spotify_root[1].text != '0':
		spotify_attrib = spotify_root[4].attrib #this looks like {'href': 'spotify:track:5TdAgcKS5HlxMcclStHODW'}
		spotify_song = spotify_root[4][0].text
		return spotify_song
	else:
		return "no song"

if __name__ == "__main__":
	app.run(debug=True)