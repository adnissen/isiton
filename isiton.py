#!/usr/bin/python
from rdio import Rdio
from flask import Flask
from flask import jsonify
from flask import render_template
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import requests
import xml.etree.ElementTree as ET
app = Flask(__name__)

@app.route("/")
def isiton():
    return render_template('home.html')

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/search/<song>')
@crossdomain(origin='*')
def search(song):
    song = song.replace(';', '')
    song = song.replace('&', '')
    song = song.replace('With Lyrics', '')
    song = song.replace('(Official Video)', '')
    song = song.replace('(Official Music Video)', '')
    song = song.replace('[Official Video]', '')
    song = song.replace('[Official Music Video]', '')
    song = song.replace('-', '')

    spotify_request = requests.get('http://ws.spotify.com/search/1/track?q=%s' % song)
    spotify_root = ET.fromstring(spotify_request.content) #parse the xml out so we can do things with it
    spotify_song = ''
    spotify_attrib =''
    if spotify_root[1].text != '0':
        spotify_attrib = spotify_root[4].attrib #this looks like {'href': 'spotify:track:5TdAgcKS5HlxMcclStHODW'}
        spotify_attrib = spotify_attrib["href"]
        spotify_song = spotify_root[4][0].text
        spotify_attrib = spotify_attrib.replace('spotify:track:', 'http://open.spotify.com/track/');
        #at this point, we have the spotify song
    
    #rdio is up next
    rdio_title = ''
    rdio_artist = ''
    rdio_url = ''
    rdio = Rdio(("ad6x8mefbh2b2kh3deezgfq2", "tdWYdpKBfH"))
    rdio_song = rdio.call("search", {"query": song, "types": "Track"})
    if (rdio_song["status"] == "ok" and rdio_song["result"]["track_count"] != 0):
        rdio_turl = rdio_song["result"]["results"][0]["url"]
        rdio_url = "http://rdio.com"
        rdio_url += rdio_turl
    
    return jsonify(spotify_url = spotify_attrib, rdio_url = rdio_url)

if __name__ == "__main__":
    app.run()