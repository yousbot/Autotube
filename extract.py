from moviepy.editor import concatenate_audioclips, AudioFileClip
from audioclipextractor import AudioClipExtractor
import os 
import shutil
from termcolor import colored

## python3 extract.py       : Extract Audios + Concatenate them 

## General Variables
desktop_path = "your_desktop_path_here"
project_folder = desktop_path + "/AutoTube/"
lecture_folder = project_folder
index_file_name = project_folder+"speech.txt"
audio_folder = project_folder+"audio/"
output_file =  audio_folder+"speech_merged.mp3"
temporary_folder = lecture_folder+"temp/"
num_line = 1

## Concat Audio Function
def concatenate_audio_moviepy(audio_clips_folder, output_file):
    dir_list = os.listdir(audio_clips_folder)
    clips = [AudioFileClip(audio_clips_folder+c) for c in dir_list if not c.startswith('.')]
    print(clips)
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_file) 
    print(colored(" [ Audio Exported at : "+output_file+" ... ] ",'blue'))

## Remove Temporary Files
def clean_up_temp():
    shutil. rmtree(temporary_folder) 
    os.mkdir(temporary_folder)

## Loop through Speech.txt
f = open(index_file_name, 'r')
for line in f:
    file_name = str(line.split(',')[0])
    StrtMin = int(line.split(',')[1])
    StrtSec = int(line.split(',')[2])
    EndMin = int(line.split(',')[3])
    EndSec = int(line.split(',')[4])
    audio_name = file_name
    StrtTime = str(StrtMin*60+StrtSec)
    EndTime = str(EndMin*60+EndSec)
    print(colored(" [ Extracting audio from : "+file_name+" ... ] ",'blue'))
    ext = AudioClipExtractor(audio_name)
    specs = str(StrtTime+"   "+EndTime+" "+file_name)
    ext.extract_clips(specs, temporary_folder)
    os.rename(temporary_folder+"clip1.mp3", temporary_folder+"Temp_clip_"+str(num_line)+".mp3")
    print(colored(" [ Audio Extracted. ] ",'blue'))
    num_line += 1

print(colored(" [ Merging Audio ... ] ",'blue'))
os.system("rm -rf "+temporary_folder+"video_usage.txt")
concatenate_audio_moviepy(temporary_folder,output_file)
print(colored(" [ Cleaning Temp Files ... ] ",'blue'))
clean_up_temp()
