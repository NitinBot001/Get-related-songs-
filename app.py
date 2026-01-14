from flask import Flask, request, jsonify
from ytmusicapi import YTMusic
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)
ytmusic = YTMusic()

# Configure logging to see errors in your console
logging.basicConfig(level=logging.INFO)

def parse_song_data(song, source_type='watch'):
    """
    Helper function to standardize song data structure.
    source_type: 'watch' (from related) or 'search' (from search results)
    """
    try:
        # 1. Get Thumbnails (High Quality)
        # ytmusicapi usually returns a list; the last one is often highest res.
        thurl = f"https://wsrv.nl/?url=https://i.ytimg.com/vi_webp/{song.get('videoId')}/maxresdefault.webp&w=720&h=720&fit=cover"
        thumbnail_url = thurl

        # 2. Get Artists
        artists = song.get('artists', [])
        artist_names = ', '.join([a['name'] for a in artists]) if isinstance(artists, list) else "Unknown"

        # 3. Standardize Duration/Length
        # 'watch' endpoint uses 'length', 'search' uses 'duration'
        duration = song.get('length') if source_type == 'watch' else song.get('duration')

        return {
            'videoId': song.get('videoId'),
            'title': song.get('title'),
            'artists': artist_names,
            'album': song.get('album', {}).get('name') if song.get('album') else None,
            'duration': duration,
            'thumbnail': thumbnail_url,
            'isExplicit': song.get('isExplicit', False)
        }
    except Exception as e:
        logging.error(f"Error parsing song: {e}")
        return None

@app.route('/related_songs', methods=['GET'])
def get_related_songs():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Please provide a video_id'}), 400

    try:
        # Get related songs (radio=True is good for "Mix")
        data = ytmusic.get_watch_playlist(videoId=video_id, radio=True)
        
        # 'tracks' contains the list of songs
        related_songs = data.get('tracks', [])
        
        result = []
        for song in related_songs:
            parsed = parse_song_data(song, source_type='watch')
            if parsed:
                result.append(parsed)

        return jsonify(result)

    except Exception as e:
        logging.error(f"Related Songs Error: {e}")
        return jsonify({'error': 'Failed to fetch related songs', 'details': str(e)}), 500

@app.route('/search_songs', methods=['GET'])
def search_songs():
    query = request.args.get('query')
    filter_type = request.args.get('filter', default='songs') # songs, videos, albums, etc.
    
    if not query:
        return jsonify({'error': 'Please provide a search query'}), 400

    try:
        search_results = ytmusic.search(query, filter=filter_type)
        
        result = []
        
        # Handle Songs and Videos uniformly
        if filter_type in ['songs', 'videos']:
            for item in search_results:
                parsed = parse_song_data(item, source_type='search')
                if parsed:
                    result.append(parsed)
        
        # Handle Albums/Playlists differently if needed
        else:
            for item in search_results:
                # Basic fallback for other types
                result.append({
                    'title': item.get('title'),
                    'browseId': item.get('browseId'),
                    'thumbnail': item.get('thumbnails', [{}])[-1].get('url'),
                    'type': item.get('resultType')
                })

        return jsonify(result)

    except Exception as e:
        logging.error(f"Search Error: {e}")
        return jsonify({'error': 'Failed to search', 'details': str(e)}), 500

if __name__ == '__main__':
    # Threaded=True helps handle multiple requests slightly better in dev
    app.run(port=8000, host='0.0.0.0', debug=True, threaded=True)
