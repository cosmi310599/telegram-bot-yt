import yt_dlp

def get_video_qualities(video_url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'forceurl': True,
        'simulate': True,
        'no_warnings': True,
        'youtube_include_dash_manifest': False,
        'youtube_include_hls_manifest': False,
        'listformats': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict.get('formats', None)

    if not formats:
        return []

    qualities = []
    for f in formats:
        if f.get('ext') == 'mp4' and f.get('vcodec') != 'none':
            quality = f.get('format_note', 'unknown')
            if quality not in qualities:
                qualities.append(quality)

    return qualities

print(get_video_qualities("https://www.youtube.com/watch?v=UNqdRnhRmmE"))