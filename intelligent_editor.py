import os, glob
from os.path import exists as file_exists
import re
import shutil
from termcolor import colored
from subtitles import clean_subtitle_file, speech_to_text,text_on_video, add_subtitles_to_video, timecode_to_second
from datetime import datetime
import fileinput

desktop_path = "your_desktop_path_here"
project_folder = desktop_path + '/AutoTube/'
approval_folder = project_folder+'approval/'
audios_folder = project_folder+'audio/'
downloads_folder = project_folder+'downloads/'
transcript_folder = project_folder+'/transcript/'
transcript_file = transcript_folder+'transcript.srt'
corrected_transcript_file = transcript_folder+'corrected_transcript.srt'
shorts_folder = project_folder+'shorts/'
shorts_file = project_folder+'shorts.txt'
temp_folder = project_folder+'temp/'
videos_folder = project_folder+'videos/'
video_usage_temp_file = temp_folder+"video_usage.txt"

def clean_workspace():
    print(colored(" [ Cleaning downloads folder ... ]",'blue'))
    os.system("rm -rf "+downloads_folder+"/*")
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

def auto_correction_highlights():

    print(colored("[ Starting transcript correction ... ]",'blue'))

    errors = 1
    while errors != 0:
        errors = 0
        file = open(transcript_file)  
        content = file.readlines()
        num_lines = sum(1 for line in open(transcript_file))
        i = 0
        os.system("rm -rf "+corrected_transcript_file)
        os.system("touch "+corrected_transcript_file)
        with open(corrected_transcript_file, 'a') as new_transcript:

            while i < num_lines:
                sequence_id = content[i]
                sequence_time_line = content[i+1]
                sequence_start_time = content[i+1].split('-')[0]
                sequence_end_time = content[i+1].split('-')[1]
                sequence_clean_text = str(re.sub('[^a-zA-Z0-9 \.]', '', content[i+2]))
                sequence_length = content[i+1].rsplit('-', 1)[-1]

                if int(sequence_length) <= 3 and i+6 < num_lines :           
                    errors += 1
                    print(colored("[ Error found in highlights. Sequence Length : + " + sequence_length +" seconds. ]",'blue'))
                    sequence_clean_text = str(sequence_clean_text) + ' ' + str(re.sub('[^a-zA-Z0-9 \n\.]', '', content[i+6]))
                    new_time_line = str(sequence_start_time)+'-'+str(content[i+5].split('-')[1])+'--'+str(int(sequence_length)+int(content[i+5].rsplit('-', 1)[-1]))
                    new_transcript.write(str(sequence_id))
                    new_transcript.write(str(new_time_line)+'\n')
                    new_transcript.write(str(sequence_clean_text))
                    new_transcript.write(str(' \n'))
                    i += 4

                else :
                    new_transcript.write(str(sequence_id))
                    new_transcript.write(str(sequence_time_line))
                    new_transcript.write(str(sequence_clean_text)+'\n')
                    new_transcript.write(str(' \n'))

                i += 4

        print(colored("[ Backuping old transcript file to temp. ]",'blue'))
        os.system("rm -rf " + temp_folder+'transcript.srt')
        shutil.move(transcript_file,temp_folder)
        print(colored("[ Saving new transcript as principal. ]",'blue'))
        os.rename(corrected_transcript_file,transcript_file)
        print(colored("[ "+str(errors)+" errors found in transcript file. ]",'blue'))

    print(colored("[ Highlight Correction terminated successfully ! ]",'blue'))


def before_approval():
    for audio in os.listdir(audios_folder):
        ## Create PROJECT folder & rename audio to speech.mp3
        project_name = audio.split('.')[0]
        os.system("mkdir "+approval_folder+project_name)
        os.rename(audios_folder+audio, audios_folder+'speech.mp3')
        
        ## skip silence
        os.system("python3 "+project_folder+"auto_edit.py -s")

        ## Scan Highlights
        if not file_exists(transcript_file):
            print(colored("[ Transcribing audio "+audios_folder+'speech.mp3'+" ... ]",'blue'))
            speech_to_text(audios_folder+'speech.mp3')
            print(colored("[ Finished transcribing audio file. ]",'blue'))

        ## Auto-Correction of highlights
        auto_correction_highlights()

        ## Download Visuals
        os.system("python3 "+project_folder+"auto_edit.py -d")

        ## Move downloads to PROJECT folder
        file_names = os.listdir(downloads_folder)
        for file_name in file_names:
            shutil.move(os.path.join(downloads_folder, file_name), approval_folder+project_name)
        ## move transcript to PROJECT folder
        shutil.move(transcript_file,approval_folder+project_name)
        os.rename(audios_folder+'speech.mp3',audios_folder+audio)

        ## Clean Workspace
        clean_workspace()

def approval():

    now = datetime.now()
    current = now.year+now.month+now.day+now.hour+now.minute+now.second
    ## Get last non-approved project
    if os.listdir(approval_folder):
        try:
            os.replace(videos_folder+'final_video_without_subtitles.mp4',videos_folder+'_'+str(current)+'final_video_without_subtitles.mp4')
            os.replace(videos_folder+'final_video_with_subtitles.mp4',videos_folder+'_'+str(current)+'final_video_with_subtitles.mp4')
        except:
            print(colored(" [ No final videos exist yet. Nothing to be replaced. ]",'blue'))

        clean_workspace()
        latest_folder = max(glob.glob(os.path.join(approval_folder, '*/')), key=os.path.getmtime)
        shutil.move(latest_folder+'/transcript.srt',transcript_folder)
        file_names = os.listdir(latest_folder)
        for file_name in file_names:
            shutil.move(os.path.join(latest_folder, file_name), downloads_folder)
        os.system("rm -rf "+latest_folder)

    else :
        print(colored(" [ No more projects waiting approval. ]",'blue'))



