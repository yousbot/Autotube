import os, getopt, sys
from termcolor import colored
import subprocess, glob
from datetime import datetime

project_folder = "your_desktop_path"
videos_folder = project_folder+"videos/"
shorts_folder = project_folder+"shorts/"
GDrive = "/Users/youssef/Google Drive/My Drive/"
GDrive_shorts = GDrive+"Shorts/"
GDrive_videos = GDrive+"YouTube Videos/"

## GET LENGTH OF VIDEO
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def upload_videos_in_videos_folder():

    list_of_files = filter( os.path.isfile,glob.glob(videos_folder + '*') )
    list_of_files = sorted( list_of_files, key = os.path.getmtime, reverse=False)
    now = datetime.now()
    current = now.year+now.month+now.day+now.hour+now.minute+now.second

    for vid in list_of_files:
        if int(get_length(vid)) > 60 :
            os.system("cp "+videos_folder+vid+" "+'"'+GDrive_videos+current+'_'+vid+'"')
            print(colored(" [ Long synchronized with Google Drive. ] ",'blue'))
        else :
            os.system("cp "+shorts_folder+vid+" "+'"'+GDrive_videos+current+'_'+vid+'"')
            print(colored(" [ Short synchronized with Google Drive. ] ",'blue'))



