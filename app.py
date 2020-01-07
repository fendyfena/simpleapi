version= "2018© VHLittleBots 1.3"
api= "http://api.fckveza.com/"
mail="veza@fckveza.com"
from flask import Flask, request, abort, redirect, jsonify
from datetime import datetime
import requests, json, re, pafy, sys, os, base64
from re import match
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/') #https://yourdomain.com/
def homepage():
    return '''<!DOCTYPE html>
<html>
<head>
<title>VHLittleBots-Test-api</title>
</head>
<body>
<h1>EXAMPLE API VH</h1>
<h2>Add me</h2>
<div class="line-it-button" data-lang="en" data-type="friend" data-lineid="devilblack86" style="display: none;"></div>
 <script src="https://d.line-scdn.net/r/web/social-plugin/js/thirdparty/loader.min.js" async="async" defer="defer"></script>
</body>
</html>'''

#VHLITTLEBOTS



@app.route('/infoig=<un>', methods=['GET'])
def instaprofile(un):
    uReq = requests
    bSoup = BeautifulSoup
    website = uReq.get("https://www.instagram.com/{}/".format(str(un)))
    data = bSoup(website.content, "lxml")
    for getInfoInstagram in data.findAll("script", {"type":"text/javascript"})[3]:
        getJsonInstagram = re.search(r'window._sharedData\s*=\s*(\{.+\})\s*;', getInfoInstagram).group(1)
        data = json.loads(getJsonInstagram)
        for instagramProfile in data["entry_data"]["ProfilePage"]:
    	    username = instagramProfile["graphql"]["user"]["username"]
    	    name = instagramProfile["graphql"]["user"]["full_name"]
    	    picture = instagramProfile["graphql"]["user"]["profile_pic_url_hd"]
    	    biography = instagramProfile["graphql"]["user"]["biography"]
    	    followers = instagramProfile["graphql"]["user"]["edge_followed_by"]["count"]
    	    following = instagramProfile["graphql"]["user"]["edge_follow"]["count"]
    	    private = instagramProfile["graphql"]["user"]["is_private"]
    	    media = instagramProfile["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
    	    result = {
                "Creator": "VHLittleBots",
    			"result": {
    				"username": username,
    				"fullname": name,
    				"bio": biography,
    				"followers": followers,
    				"following": following,
    				"media": media,
    				"private": private,
    				"profile_img": picture
    			}
    		}
    	    return jsonify(result)

@app.route('/igstory=<username>', methods=['GET'])
def igtory(username):
    r = requests.get("https://saveig.com/?link={}".format(username))
    soup = BeautifulSoup(r.content,"lxml")
    result=[]
    try:
        data = soup.findAll('div',{'class':'line'})
        result = []
        for hasil in data:
            video = hasil.find('video')['src']
            result.append({'video':video})
    except:
        data = soup.findAll('div',{'class':'line'})
        for hasil in data:
            image=hasil.find('img')['src']
            result.append({'image':image})
    return jsonify(result)

@app.route('/postig=<usn>', methods=['GET'])
def instapost(usn):
    datas = []
    #result = {'status':'ok'}, data=datas
    link = 'https://instagram.com/{}'.format(usn)
    r = requests.get(link)
    soup = BeautifulSoup(r.content,"lxml")
    for getInfoInstagram in soup.findAll("script", {"type":"text/javascript"})[3]:
        getJsonInstagram = re.search(r'window._sharedData\s*=\s*(\{.+\})\s*;', getInfoInstagram).group(1)
        data = json.loads(getJsonInstagram)
        for insta in data["entry_data"]["ProfilePage"]:
            md = insta["graphql"]["user"]
            md = md["edge_owner_to_timeline_media"]
            for post in md["edges"]:
                url = post["node"]["display_url"]
                video = post["node"]["is_video"]
                datas.append({'url':url,'vid':video})
    return jsonify(datas)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
