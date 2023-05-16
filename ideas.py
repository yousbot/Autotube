from youtubesearchpython import *
from collections import Counter
from colored import fore, back, style

desktop_path = "your_desktop_path_here"
keywords_file = desktop_path + '/AutoTube/keywords.txt'

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)
     

def top_10(keyword,period):

    top_num = 5
    res = []
    if period == 'today':
        customSearch = CustomSearch(str(keyword), VideoUploadDateFilter.today, limit = top_num)
    elif period == 'week':
        customSearch = CustomSearch(str(keyword), VideoUploadDateFilter.thisWeek, limit = top_num)
    elif period == 'month':
        customSearch = CustomSearch(keyword, VideoUploadDateFilter.thisMonth, limit = top_num)
    for i in range(top_num):
        video = {
            'order' : i,
            'title' : str(customSearch.result()['result'][i]['title']),
            'publishedTime' : str(customSearch.result()['result'][i]['publishedTime']),
            'viewCount' : str(customSearch.result()['result'][i]['viewCount']['short']),
            'video_id' : str(customSearch.result()['result'][i]['id']),
            'channel_name' : str(customSearch.result()['result'][i]['channel']['name']),
            'channel_id' : str(customSearch.result()['result'][i]['channel']['id'])
        }
        res.append(video)
    return res

def video_info(url):
    videoInfo = Video.getInfo(url, mode = ResultMode.json)

    return {
        'title' : videoInfo['title'],
        'duration' : videoInfo['duration']['secondsText'],
        'channel_name' : videoInfo['channel']['name'],
        'channel_id' : videoInfo['channel']['id'],
        'publish_date' : videoInfo['publishDate'],
        'upload_date' : videoInfo['uploadDate'],
        'viewCount' : int(videoInfo['viewCount']['text'])
    }


def channel_details(id):
    channel_info = Channel.get(id)
    return {
        'channel_id': channel_info['id'],
        'title' : channel_info['title'],
        'subscribers' : channel_info['subscribers'],
        'views' : channel_info['views']
    }

def top10_videos_for_channel(channel_id):
    playlist = Playlist(playlist_from_channel_id(channel_id))
    vid_playlist = playlist.videos
    list_videos = []
    for video in vid_playlist:
        video_id = video['id']
        list_videos.append(video_info(video_id))
    videos_sorted_by_views = sorted(list_videos, key=lambda d: d['viewCount']) 
    return videos_sorted_by_views[:5]

def last10_videos_for_channel(channel_id):
    playlist = Playlist(playlist_from_channel_id(channel_id))
    vid_playlist = playlist.videos
    list_videos = []
    for video in vid_playlist:
        video_id = video['id']
        list_videos.append(video_info(video_id))
    list_videos = list_videos[:2]
    return list_videos

def top10_stats(keyword,period):
    top_10_vids = top_10(str(keyword),period)
    channel_counts = Counter(d['channel_name'] for d in top_10_vids)
    most_common = {'channel_name': channel_counts.most_common(1)[0][0]}
    mean_time = 0
    for vid in top_10_vids:
        mean_time += int(video_info(vid['video_id'])['duration'])
    mean_time = int(mean_time/7)

    return {
        'channel_id' : vid['channel_id'],
        'top_channel' : most_common,
        'mean_duration' : mean_time
    }

def print_channel_details(channel_id):
    chan = channel_details(channel_id)
    print(fore.RED + '     |    |       |_ Subscribers : ' + fore.WHITE + str(chan['subscribers']['label']))
    print(fore.RED + '     |    |       |_ Total Views : ' + fore.WHITE + chan['views'])
    last10videos = last10_videos_for_channel(channel_id)
    for vid in last10videos:
        print(fore.RED + '     |    |       |      |')
        print(fore.RED + '     |    |       |      |_ Title : ' + fore.WHITE + vid['title'])
        print(fore.RED + '     |    |       |      |_ Views : ' + fore.WHITE + str(vid['viewCount']))
        print(fore.RED + '     |    |       |      |_ Duration : ' + fore.WHITE + str(convert(int(vid['duration']))))
        print(fore.RED + '     |    |       |      |_ Publish Date : ' + fore.WHITE + vid['publish_date'])
        print(fore.RED + '     |    |       |      |_______________________________________________________________ ')

def print_last_10(keyword, period):
    videos = top_10(str(keyword), str(period))
    stats = top10_stats(keyword,period)
    print(fore.RED + "     |    |")
    print(fore.RED + "     |    |_ TOP CHANNEL : " + fore.WHITE + str(stats['top_channel']['channel_name']))
    print(fore.RED + '     |    |_ MEAN DURATION : ' + fore.WHITE + str(convert(int(stats['mean_duration']))))

    for vid in videos:
        print(fore.RED + '     |    |     ')
        print(fore.RED + '     |    |_ Channel Name : ' + fore.WHITE + vid['channel_name'])
        print_channel_details(vid['channel_id'])
        
def print_keywords_analytics():

    file = open(keywords_file)  
    content = file.readlines()
    num_lines = sum(1 for line in open(keywords_file))
    i = 0
    while i < num_lines:
        keyword = str(content[i])
        print("\n")
        print(fore.RED + ' TOP 7 Videos')
        #print(fore.RED + '     |  ')
        #print(fore.RED + '     |_ Last 24h ')
        #print_last_10(keyword,'today')
        print(fore.RED + '     |  ')
        print(fore.RED + back.WHITE + '     |_ Last Week  ' +keyword + style.RESET)
        print_last_10(keyword,'week')
        print(fore.RED + '     |  ')
        print(fore.RED + back.WHITE + '     |_ Last Month  ' +keyword + style.RESET)
        print_last_10(keyword,'month')

        i += 1




print_keywords_analytics()

#top_10('Terence McKenna','hour')