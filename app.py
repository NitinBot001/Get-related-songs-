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
        return jsonify({'error': 'Please provide a video_id'}), 400

    # Get related songs
    related_songs = ytmusic.get_watch_playlist(videoId=video_id, radio=True)['tracks']

    # Prepare response
    result = []
    for song in related_songs:
        result.append({
            'title': song['title'],
            'videoId': song['videoId'],
            'artists': ', '.join(artist['name'] for artist in song['artists']),
            'length': song['length'] or 'undefined',
        })

    return jsonify(result)

@app.route('/search_songs', methods=['GET'])
def search_songs():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Please provide a search query'}), 400

    # Dynamically get filter from query parameters, default to 'songs'
    filter_type = request.args.get('filter', default='songs')

    # Optional: Validate filter type
    valid_filters = ['songs', 'albums', 'artists', 'playlists', 'videos']
    if filter_type not in valid_filters:
        return jsonify({'error': 'Invalid filter type. Supported filters are: songs, albums, artists, playlists, videos'}), 400

    # Perform search with dynamic filter
    search_results = ytmusic.search(query, filter=filter_type)

    # Prepare response
    result = []
    for song in search_results:
        result.append({
            'title': song['title'],
            'videoId': song['videoId'],
            'artists': ', '.join(artist['name'] for artist in song['artists']),
            'duration': song['duration'] or 'undefined'
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)
