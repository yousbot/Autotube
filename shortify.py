from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import sys, shutil, os, getopt
from termcolor import colored
from moviepy.editor import *
import glob


## python3 shortify.py -e          : Extract Clips ( Cut & Split Files )
## python3 shortify.py -e -m       : Extract Clips ( Cut & Merge Files )
## python3 shortify.py -c          : Extract Clips + Crop it 9:16 ( Cut, Crop & Split Files )

## General Variables
desktop_path = "your_desktop_path_here"
project_folder = desktop_path + "/AutoTube/"
videos_folder = project_folder+"videos/"
temp_folder = project_folder+"temp/"
short_file_name = project_folder+"shorts.txt"
#short_file_name = str(sys.argv[1])
shorts_folder = project_folder+"shorts/"
temp_extracted_files = project_folder+"temp_extracted_files.txt"
num_line = 1

## Remove Temporary Files
def clean_up_temp():
    shutil. rmtree(temp_folder) 
    os.mkdir(temp_folder)

def merge_videos(input_folder,output_file):
    videos_to_merge = []
    list_of_files = filter( os.path.isfile,glob.glob(input_folder + '*') )
    list_of_files = sorted( list_of_files, key = os.path.getmtime, reverse=False)
    for vid in list_of_files:
        videos_to_merge.append(VideoFileClip(shorts_folder+vid))
    fade_duration = 0.5 # 1-second fade-in for each clip
    clips = [clip.crossfadein(fade_duration) for clip in videos_to_merge]
    clips = [clip.crossfadeout(fade_duration) for clip in videos_to_merge]
    final_clip = concatenate_videoclips(clips,method='compose')
    final_clip.write_videofile(output_file, temp_audiofile=temp_folder+'temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")
    

## Loop through shorts.txt
argumentList = sys.argv[1:]
options = "ecm"
long_options = ["Extract","Crop","Merge"]
arguments, values = getopt.getopt(argumentList, options, long_options)

os.system("touch "+temp_extracted_files)
f = open(short_file_name, 'r')
video_to_merge = []
audio_to_merge = []

for line in f:
    file_name = str(line.split(',')[0])
    StrtMin = int(line.split(',')[1])
    StrtSec = int(line.split(',')[2])
    EndMin = int(line.split(',')[3])
    EndSec = int(line.split(',')[4])
    StrtTime = StrtMin*60+StrtSec
    EndTime = EndMin*60+EndSec
    target_name = str(line.split(',')[0]).rsplit('/', 1)[-1].split(',')[0]
    new_temp_mame = "temp_"+str(num_line)+target_name
    ffmpeg_extract_subclip(file_name, StrtTime, EndTime, targetname=new_temp_mame)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-e", "--Extract"):
            ## Extract Portion of a video
            os.rename(new_temp_mame,shorts_folder+"temp_"+str(num_line)+target_name)
            print(colored(" [ "+shorts_folder+"temp_"+str(num_line)+target_name+" exported. ] ",'blue'))
            filePath = shorts_folder+"temp_"+str(num_line)+target_name
            video = VideoFileClip(filePath)
            video_to_merge.append(video)

        elif currentArgument in ("-c", "--Crop"):
            ## Crop Ratio 9:16
            short_name = shorts_folder+"Short"+str(num_line)+".mp4"
            os.system("ffmpeg -i '"+new_temp_mame+"' -vf \"crop=ih*(9/16):ih\" -crf 21 '"+short_name+"'")
            print(colored(" [ "+short_name+" exported. ] ",'blue'))

    num_line += 1

for currentArgument, currentValue in arguments:
    if currentArgument in ("-m", "--Merge"):

        fade_duration = 1 # 1-second fade-in for each clip
        clips = [clip.crossfadein(fade_duration) for clip in video_to_merge]
        clips = [clip.crossfadeout(fade_duration) for clip in video_to_merge]
        final_clip = concatenate_videoclips(clips,method='compose')
        final_clip.write_videofile(shorts_folder+"merged_long_videos.mp4", temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")
    
print(colored(" [ Cleaning Temp Files. ] ",'blue'))
clean_up_temp()