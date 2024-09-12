from flask import Flask, request, jsonify
from ytmusicapi import YTMusic
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
ytmusic = YTMusic()

@app.route('/related_songs', methods=['GET'])
def get_related_songs():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Please provide a video ID'}), 400
    
    # Get related songs
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

if __name__ == '__main__':
    app.run(port=8000,host='0.0.0.0',debug=True)
