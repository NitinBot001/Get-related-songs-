from flask import Flask, request, jsonify
from ytmusicapi import YTMusic
from flask_cors import CORS
from youtubesearchpython import VideosSearch


app = Flask(__name__)
CORS(app)
ytmusic = YTMusic()

@app.route('/related_songs', methods=['GET'])
def get_related_songs():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Please provide a video ID'}), 400
    
    # Assuming this functionality stays the same with YTMusic
    ytmusic = YTMusic()
    related_songs = ytmusic.get_watch_playlist(videoId=video_id)['tracks']
    
    # Prepare response
    result = []
    for song in related_songs:
        result.append({
            'title': song['title'],
            'videoId': song['videoId'],
            'artists': ', '.join(artist['name'] for artist in song['artists'])
        })
    
    return jsonify(result)

@app.route('/search_songs', methods=['GET'])
def search_songs():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Please provide a search query'}), 400
    
    # Use youtube-search-python for song search
    videos_search = VideosSearch(query, limit=10)
    search_results = videos_search.result()['result']
    
    # Prepare response
    result = []
    for video in search_results:
        result.append({
            'title': video['title'],
            'videoId': video['id'],
            'artists': video['channel']['name']
        })
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)
