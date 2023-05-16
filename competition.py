import pytube
from pytube import *
from pytube import Search
from googleapiclient.discovery import build

desktop_path = "your_desktop_path_here"
project_folder = desktop_path + "/AutoTube/"
competition_file = project_folder+"competition.txt"
keywords_file = project_folder+"keywords.txt"
API_KEY = "your_google_api"

    
def get_info_on_channel(channel_id):

    # Create YouTube Object
    youtube = build('youtube', 'v3',  developerKey=API_KEY)
    ch_request = youtube.channels().list( part='statistics', id=channel_id)
    ch_response = ch_request.execute()
    sub = ch_response['items'][0]['statistics']['subscriberCount']
    vid = ch_response['items'][0]['statistics']['videoCount']
    views = ch_response['items'][0]['statistics']['viewCount']
    print(" | ", sub)
    print(" |_ Total Subscriber : ", sub)
    print(" |_ Total Number of Videos : ", vid)
    print(" |_ Total Views: ", views)

    '''
    c = Channel(yt.channel_url+'/videos')
    for url in c.video_urls :
        print(url)
    '''

def get_info_on_video(link):
    yt = pytube.YouTube(link)
    video_title = yt.title
    channel_url = yt.channel_url
    publish_date = yt.publish_date.strftime("%Y-%m-%d")
    views = yt.views
    video_duration = yt.length
    print('Title : ' + video_title)
    print('Views : ' + str(views))
    print('Duration : ' + str(video_duration))
    print('Publish Date ' + publish_date)
    print('Channel : ' + yt.author)
    get_info_on_channel(yt.channel_id)


## Loop through keywords

with open(keywords_file, "r") as keys_file:
    for keyword in keys_file:
        ## search on YouTube
        s = Search(keyword)
        for i in s.results[:5]:
            url = 'https://www.youtube.com/watch?v='+i.video_id
            get_info_on_video(url)


# Create YouTube Object










'''

'''