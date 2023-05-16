import os
import subprocess
from termcolor import colored

desktop_path = "your_desktop_path_here"
font_file_path = desktop_path + '/AutoTube/fonts/PARISNN.ttf'
input_video = desktop_path + '/AutoTube/videos/final_video_with_subtitles.mp4'
output_video = desktop_path + '/AutoTube/videos/final_video_with_subtitles_with_brand.mp4'
watermark_text = "Intellectual Wave"

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)
    
def text_on_video(text,input_video,output_video,start_seconds,end_seconds):
    w = "40"
    h = "60"
    os.system("ffmpeg -i "+input_video+" -vf \"drawtext=fontfile="+font_file_path+": \
    text=\'"+text+"\': fontcolor=white: fontsize=40: \
    x="+w+": y="+h+":enable=\'between(t,"+str(start_seconds)+","+str(end_seconds)+")\'\" \
    -codec:a copy "+output_video)

def add_watermak():
    start_seconds = 0
    end_seconds = get_length(input_video)
    print(colored("[ Adding watermak to video with subtitles ... ]",'blue'))
    text_on_video(watermark_text,input_video,output_video,start_seconds,end_seconds)
    print(colored("[ Video exported at : "+output_video+" ]",'blue'))

