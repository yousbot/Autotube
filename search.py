## 1. Get random video from channel list
## 2. Download Audio

from pickle import TRUE
import re
from bs4 import BeautifulSoup
import pytube
from pytube import *
from pytube import Search
from googleapiclient.discovery import build
from pytube import Channel
import random
from termcolor import colored
from youtubesearchpython import *
import os

desktop_path = "your_desktop_path_here"
project_folder = desktop_path + "/AutoTube/"
competition_file = project_folder+"competition.txt"
keywords_file = project_folder+"keywords.txt"
API_KEY = "your_google-api"
audio_folder = project_folder+'audio/'
downloaded_videos = project_folder+'downloaded_videos.txt'

def check_used_url(url):
    with open(downloaded_videos) as myfile:
        if url in myfile.read():
            return True
        else :
            return False

def second_to_timecode(x: float) -> str:
    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)
    return '%.2d:%.2d:%.2d' % (hour, minute, second)

def add_url_to_usage_file(url, channel_id):
    os.system('echo \"'+url+';'+channel_id+'\" >> '+downloaded_videos)

def remove_channel(channel_id):
    print(colored("[ Removing channel from competitors file : "+channel_id+" ]",'blue'))
    with open(competition_file) as oldfile, open(competition_file, 'w') as newfile:
        for line in oldfile:
            if channel_id not in line :
                newfile.write(line)

def get_random_video(channel_id):
    playlist = Playlist(playlist_from_channel_id(channel_id))
    ## Filter by  video between 6 and 30 min
    filtered_playlist = [d for d in playlist.videos if len(d['duration'].split(':')) == 2 and int(d['duration'].split(':')[0]) <= 30 and int(d['duration'].split(':')[0]) >= 6]        
    print(colored("[ Number videos to select from : "+str(len(filtered_playlist))+" ]",'blue'))
    random_video = random.choice(filtered_playlist)
    random_video_url = random_video['link'].split('&')[0]
    file = open(downloaded_videos, "r")
    data = file.read()
    occurrences = data.count(channel_id)
    if occurrences == filtered_playlist :
        remove_channel(channel_id)
    else : 
        with open(downloaded_videos) as myfile:
            while random_video_url in myfile.read():
                random_video = random.choice(filtered_playlist)
                random_video_url = random_video['link'].split('&')[0]
                print(colored("[ The video selected is used. Searching for another one ... ]",'blue'))

    add_url_to_usage_file(random_video_url, channel_id)
    return random_video_url

def get_channel_info(video_url):
    yt = pytube.YouTube(video_url)
    video_title = yt.title
    publish_date = yt.publish_date.strftime("%Y-%m-%d")
    views = yt.views
    video_duration = yt.length
    print(colored("[ Title      : "+video_title+" ]",'blue'))
    print(colored("[ Views      : "+str(views)+" ]",'blue'))
    print(colored("[ Duration   : "+str(second_to_timecode(video_duration))+" ]",'blue'))
    print(colored("[ Published  : "+publish_date+" ]",'blue'))
    print(colored("[ Channel    : "+yt.author+" ]",'blue'))

def get_channel_id(video_url):
    yt = pytube.YouTube(video_url)
    return yt.channel_id

def video_to_mp3(url):
    print(colored("[ Downloading video in mp3 format ... ]",'blue'))
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=audio_folder)
    file_name = out_file.split('/')[6]
    clean_file_name = re.sub('[^a-zA-Z0-9 \n\.]', '', out_file.split('/')[6]).replace(' ','')
    base, ext = os.path.splitext(clean_file_name)    
    new_file = audio_folder + base + '.mp3'
    print(colored("[ Changing audio name to "+base+".mp3 ]",'blue'))
    os.rename(out_file, new_file)
    os.system("rm -rf "+audio_folder+'.DS_Store')
    print(colored("[ "+yt.title+" has been successfully downloaded. ]",'blue'))

def generate_audios(number_audio):
    file = open(competition_file)  
    content = file.readlines()
    num_lines = sum(1 for line in open(competition_file))
    os.system("rm -rf "+audio_folder+'.DS_Store')
    print(colored("[ Searching for "+str(number_audio)+" audios. ]",'blue'))
    
    for i in range(1,int(number_audio)+1) :
        print(colored("[ Chosing random competitor channel ... ]",'blue'))
        random_channel_id = content[random.randint(1, num_lines)-1].split(';')[1]
        print(colored("[ Channel selected : "+random_channel_id,'blue'))
        print(colored("[ Getting random video from the channel ... ]",'blue'))
        random_channel_video = get_random_video(random_channel_id)
        print(colored("[ Random video chosen : "+random_channel_video+" ",'blue'))
        get_channel_info(random_channel_video)
        video_to_mp3(random_channel_video)
    print("\n")


