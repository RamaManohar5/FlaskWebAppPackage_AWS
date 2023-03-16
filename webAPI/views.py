from flask import Blueprint, render_template, request
from flask_cors import CORS , cross_origin
import asyncio
import aiohttp

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import json

import logging
logging.basicConfig(filename='scraper.log', level=logging.INFO)

# Initialize the API component.
application = Blueprint("views", __name__)

# routes
@application.route('/')
def base():
    return render_template('index.html')


@application.route('/search', methods=['GET', 'POST'])
def get_content():
    try :
        if request.method == 'POST':
            channel_url = request.form['content']

            get_csv_data = asyncio.run(fetch_channel_data(channel_url))

            return render_template('results.html', csv_data=channel_url)
        
    except Exception as e:
        logging.INFO(e)

video_url_string = 'https://www.youtube.com/watch?v='
url = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}"
key = 'AIzaSyA8JeiyqrZeff8BL77Jcvvuibax34PJVis'

# captures all the final results
results = []

def get_video_ids(channel_url) : 
    try : 
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
        req = Request(url, headers=headers)
        response = urlopen(req)
        soup = BeautifulSoup(urlopen(req), features="html.parser")
        # channelID from metadata
        channel_id = soup.find_all('meta', {'itemprop' : 'channelId'})[0].attrs['content']
        # count set to 25, api will fetch javascript for those videos throug API
        channel_id_url = f"https://www.googleapis.com/youtube/v3/search?key={key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=100"
        # open the connection through google api
        resp = urlopen(channel_id_url) 
        # converts the resonse into json
        response_data = json.load(resp)
        # closes the connection
        resp.close() 
        # data is in dict format & fetch unique videoId of each video from the channel page.
        videos_ids = []
        for item in response_data['items']:
            for k in (item['id']).keys():
                if k == 'videoId':
                    videos_ids.append(item['id']['videoId'])

        return videos_ids
    
    except Exception as e:
        logging.INFO(e)

def fetch_channel_data(channel_url) :
    
    if (channel_url) :
        video_ids = get_video_ids(channel_url)
    return video_ids