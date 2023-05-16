import json
import os
from ShazamAPI import Shazam
from colored import fore, back, style
from termcolor import colored

desktop_path = "your_desktop_path_here"
project_folder = desktop_path + "/AutoTube/"
audio_folder = project_folder+"localmusic/"

def check_copyright():
    print(colored(" [ Verifying copyrighted materials ... ] ",'blue'))

    os.system("rm -rf "+audio_folder+'.DS_Store')
    for filename in os.listdir(audio_folder):
        mp3_file_content_to_recognize = open(audio_folder+filename, 'rb').read()
        shazam = Shazam(mp3_file_content_to_recognize)
        recognize_generator = shazam.recognizeSong()

        copyrighted = []
        for _,entry in recognize_generator:
            title = entry.get("track",{}).get("title","unknown")
            subtitle = entry.get("track",{}).get("subtitle","unknown")
            copyrighted.append(title + ' - ' + subtitle)
            #break

        if len(copyrighted) != 0:
            print(fore.RED+ " [ Copyright : " + fore.WHITE + filename + fore.RED +" ] ")
            for i in list(dict.fromkeys(copyrighted)):
                print(fore.RED + " [ Title : " + fore.WHITE + i + fore.RED + " ] ")

    print(colored(" [ Copyright verification finished. ",'blue'))


