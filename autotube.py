import glob
import pathlib
import shutil
import pyfiglet
import os, time
from termcolor import colored
from subtitles import clean_subtitle_file, speech_to_text,text_on_video, add_subtitles_to_video
from colored import fore, back, style
from upload import upload_videos_in_videos_folder
from os.path import exists as file_exists
from intelligent_editor import approval, auto_correction_highlights, before_approval
from intelligent_post import generate_multiple_quotes
from search import generate_audios, get_channel_id
from brand_settings import add_watermak
import datetime as dt
from moviepy.editor import *
from copyright import check_copyright

## GLOBAL VARIABLES

desktop_path = "your_desktop_path_here"
project_folder = desktop_path + "/AutoTube/"
shorts_folder = project_folder+"shorts/"
links_file = project_folder+"links.txt"
result = (fore.RED + pyfiglet.figlet_format("Intellectual Wave"))
shorts_file = project_folder+"shorts.txt"
merge_file = project_folder+"merge.txt"
downloads_folder = project_folder+"downloads"
audio_to_transcribe = project_folder+"audio/speech.mp3"
video_without_subtitles = desktop_path+ "/AutoTube/videos/final_video_without_subtitles.mp4"
subtitles_file = desktop_path + "/AutoTube/transcript/transcript.srt"
videos_folder = project_folder+"videos/"
temp_folder = project_folder+"temp/"
transcript_folder = project_folder+"transcript/"
transcript_file = transcript_folder+"transcript.srt"
video_usage_temp_file = temp_folder+"video_usage.txt"
audio_folder = project_folder+'audio/'
os.system("clear")

## GO BACK TO MAIN PAGE
def go_back():
    text = input(fore.WHITE + "\n     Press Enter ...")
    if text == "":
        os.system("python3 "+project_folder+"autotube.py")

## DRAW MAIN TITLE
def title():
    os.system("clear")
    print(result)
    print("\n")

##  MENU
def main_menu():
    print(result)
    print(fore.GREY_58 + "      1." + fore.RED + "     Intelligent Editor ..." + style.RESET)
    print(fore.GREY_58 + "      2." + fore.WHITE + "     Skip Silence")
    print(fore.GREY_58 + "      3." + fore.WHITE + "     Scan Highlights")
    print(fore.GREY_58 + "      4." + fore.RED + "     Video Storyboard ...")
    print(fore.GREY_58 + "      5." + fore.WHITE + "     Burn Captions")
    print(fore.GREY_58 + "      6." + fore.WHITE + "     Copyright")
    print(fore.GREY_58 + "      7." + fore.WHITE + "     Brand Settings")
    print(fore.GREY_58 + "      8." + fore.WHITE + "     Publish")
    print(fore.GREY_58 + "      9." + fore.RED + "     Useful Tools ... ")
    print(fore.GREY_58 + "      0." + fore.WHITE + "     Quit.    ")

##  BODY
main_menu()
choice = input(fore.WHITE + '\n      > ')
print("\n")
print("\n")


if int(choice) == 1:

    ## Intelligent Editor
    title()
    print(fore.GREY_58 + "      1." + fore.WHITE + "     Search for new ideas")
    print(fore.GREY_58 + "      2." + fore.WHITE + "     Download videos for audios")
    print(fore.GREY_58 + "      3." + fore.WHITE + "     Get videos to be approved")
    print(fore.GREY_58 + "      4." + fore.WHITE + "     Create Quotes")
    print(fore.GREY_58 + "      0." + fore.WHITE + "     Quit.    ")
    choice = input(fore.WHITE +'\n        > ')
    title()

    if int(choice) == 1:
        num = input(fore.WHITE + '\n     Number of audios to create : ')
        title()
        generate_audios(num)
        go_back()

    elif int(choice) == 2:
        before_approval()
        go_back()

    elif int(choice) == 3:
        approval()
        go_back()

    elif int(choice) == 4:
        num = input(fore.WHITE + '\n     Number of quotes to create : ')
        title()
        generate_multiple_quotes(num)
        go_back()

    else:
        os.system("python3 "+project_folder+"autotube.py")

elif int(choice) == 2:

    ## Skip Silence
    title()
    os.system("python3 "+project_folder+"auto_edit.py -s")
    go_back()

elif int(choice) == 3:

    ## Scan Highlights
    title()
    if not file_exists(transcript_file):
        print(colored("[ Transcribing audio "+audio_to_transcribe+" ... ]",'blue'))
        speech_to_text(audio_to_transcribe)
        print(colored("[ Finished transcribing audio file. ]",'blue'))
        time.sleep(2)
        print(colored("[ Auto correction of transcription ... ]",'blue'))
        time.sleep(2)
        auto_correction_highlights()

    title()
    os.system("python3 "+project_folder+"auto_edit.py -k")
    go_back()

elif int(choice) == 4:

    ## Video Storyboard
    title()
    print(fore.GREY_58 + "      1." + fore.WHITE + "     Download Visuals")
    print(fore.GREY_58 + "      2." + fore.WHITE + "     Change Visuals")
    print(fore.GREY_58 + "      3." + fore.WHITE + "     Generate")
    print(fore.GREY_58 + "      0." + fore.WHITE + "     Quit.    ")
    choice = input(fore.WHITE +'\n        > ')
    title()

    if int(choice) == 1:
        try :
            os.system("python3 "+project_folder+"auto_edit.py -d")
        except :
            title()
            print(colored(" [ Error occured. Retrying another time ... ",'blue'))
            time.sleep(3)
            os.system("python3 "+project_folder+"auto_edit.py -d")
        go_back()

    elif int(choice) == 2:
        os.system("python3 "+project_folder+"auto_edit.py -c")
        go_back()

    elif int(choice) == 3:
        os.system("python3 "+project_folder+"auto_edit.py --Assemble")
        go_back()

    else:
        os.system("python3 "+project_folder+"autotube.py")

elif int(choice) == 5:

    ## Burn Captions
    title()
    if len(os.listdir(temp_folder)) != 0:
        latest_file = max(glob.glob(temp_folder+'*'), key=os.path.getmtime)
        os.system("rm -rf "+latest_file)
        latest_file = max(glob.glob(temp_folder+'*'), key=os.path.getmtime)
        i = int(latest_file.split('/')[-1].split('_')[1].split('.')[0])
        video = latest_file
    else:
        video = video_without_subtitles
    add_subtitles_to_video(video,subtitles_file)
    now = dt.datetime.now()
    current = now.year+now.month+now.day+now.hour+now.minute+now.second
    #os.system("mv "+videos_folder+"final_video_with_subtitles.mp4 "+videos_folder+str(current)+"final_video_with_subtitles.mp4")

    
    go_back()

elif int(choice) == 6:

    ## Music & Voice Effects
    title()
    check_copyright()
    go_back()

elif int(choice) == 7:

    ## Brand Settings
    title()
    add_watermak()
    go_back()

elif int(choice) == 8:

    ## Publish
    title()
    upload_videos_in_videos_folder()
    go_back()


elif int(choice) == 9:

    ## Useful Tools
    title()
    print(fore.GREY_58 + "      1." + fore.WHITE + "     Download Media" + style.RESET)
    print(fore.GREY_58 + "      2." + fore.WHITE + "     Clean Workspace")
    print(fore.GREY_58 + "      3." + fore.WHITE + "     Crop & "+ fore.GREEN +"Merge" + fore.WHITE + " Audio")
    print(fore.GREY_58 + "      4." + fore.WHITE + "     Crop & "+ fore.GREEN +"Merge" + fore.WHITE + " Video")
    print(fore.GREY_58 + "      5." + fore.WHITE + "     Crop & "+ fore.RED +"Split" + fore.WHITE + " Video")
    print(fore.GREY_58 + "      6." + fore.WHITE + "     Crop & "+ fore.RED +"Split" + fore.WHITE + " Videos ( 9:16 )")
    print(fore.GREY_58 + "      7." + fore.WHITE + "     Get Channel ID")
    print(fore.GREY_58 + "      8." + fore.WHITE + "     Convert to mp3")
    print(fore.GREY_58 + "      0." + fore.WHITE + "     Quit")
    choice = input(fore.WHITE +'\n        > ')
    print("\n")
    if int(choice) == 1:

        ## Download Media
        print(colored("[ Downloading Videos in "+project_folder+"download.txt ... ]",'blue'))
        os.system("wget -i "+project_folder+"download.txt -P "+downloads_folder)
        print(colored("[ Videos downloaded at "+downloads_folder+" ]",'blue'))
        go_back()

    elif int(choice) == 2:

        ## Clean Workspace
        print(colored(" [ Cleaning downloads folder ... ]",'blue'))
        os.system("rm -rf "+downloads_folder+"/*")
        print(colored(" [ Cleaning Audio folder ... ]",'blue'))
        os.system("rm -rf "+audio_folder+"/*")
        print(colored(" [ Cleaning shorts folder ... ]",'blue'))
        files=os.listdir(shorts_folder)
        for fname in files:
            shutil.copy2(os.path.join(shorts_folder,fname), videos_folder)
        os.system("rm -rf "+shorts_folder+"/*")
        print(colored(" [ Empty shorts file ... ]",'blue'))
        os.system("rm -rf "+shorts_file)
        os.system("touch "+shorts_file)
        print(colored(" [ Empty Temp folder ... ]",'blue'))
        os.system("rm -rf "+temp_folder+"/*")
        print(colored(" [ Empty Transcript folder ... ]",'blue'))
        os.system("rm -rf "+transcript_folder+"/*")
        os.system("rm -rf "+project_folder+"temp_extracted_files.txt")
        print(colored(" [ Empty Tempo Video Usage File ... ]",'blue'))
        os.system("rm -rf "+video_usage_temp_file)
        os.system("touch "+video_usage_temp_file)
        os.system("rm -rf "+videos_folder+"temp*")

        go_back()

    elif int(choice) == 3:

        ## Crop & Merge Audios
        os.system("python3 "+project_folder+"extract.py")
        print("\n")
        go_back()

    elif int(choice) == 4:

        ## Crop & Merge Videos
        os.system("python3 "+project_folder+"shortify.py -e -m ")
        print("\n")
        print(colored("[ Videos Exported at : "+shorts_folder+" ]",'blue'))
        go_back()

    elif int(choice) == 5:

        ## Crop & Split Videos
        os.system("python3 "+project_folder+"shortify.py -e")
        print("\n")
        print(colored("[ Videos Exported at : "+shorts_folder+" ]",'blue'))
        go_back()

    elif int(choice) == 6:

        ## Crop & Split Videos ( 9:16 )
        os.system("python3 "+project_folder+"shortify.py -c")
        print("\n")
        print("Shorts Exported at : "+shorts_folder)
        go_back()

    elif int(choice) == 7:

        title()
        url = input(fore.WHITE + '\n     Enter a video URL : ')
        print(fore.WHITE +"\n     Channel URL : "+ fore.RED + get_channel_id(url))
        go_back()
        
    elif int(choice) == 8:

        title()
        path = input(fore.WHITE + '\n     Video Path : ')
        video = VideoFileClip(os.path.join(path))
        print(fore.WHITE +"\n     Converting Video " + path)
        mp3_name = path.split('.')[0]
        video.audio.write_audiofile(os.path.join(mp3_name+'.mp3'))
        print(fore.WHITE +"\n     Audio exported to : " + os.path.join(mp3_name+'.mp3'))
        go_back()

    else:
        os.system("python3 "+project_folder+"autotube.py")

       
else:
    print("\n")
    os.system("clear")

    exit()
    


