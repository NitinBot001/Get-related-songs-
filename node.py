from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/fetch-genyt-content', methods=['GET'])
def fetch_genyt_content():
    try:
        # Make the request to genyt.net
        response = requests.get('https://www.genyt.net')
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract song information
        songs = []
        divs = soup.select('div.col-lg-12.col-md-12.gytbox.mb-3')
        
        for div in divs:
            a_tag = div.find('a')
            video_url = a_tag.get('href')
            video_id = video_url.replace('https://video.genyt.net/', '')
            title = div.select_one('h5.gytTitle a').text.strip()
            thumbnail = div.find('img').get('src')
            songs.append({
                'videoId': video_id,
                'title': title,
                'thumbnail': thumbnail
            })
        
        return jsonify(songs)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from genyt.net: {e}")
        return jsonify({"error": "Failed to fetch data"}), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000,debug=True)
