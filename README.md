# AutoTube ( Beta )
## Turn your speech to a video

Autotube is a Python-based project that allows you to convert audio speeches into videos. 
The project automates the entire video creation process by taking an English audio recording as input. 
Initially designed for motivational videos, Autotube has expanded to include other functionalities that can be beneficial to anyone managing similar channels. These additional features include a copyright checker, quotes creator, shorts creator, MP3 converter and more.

## Functional Architecture
AutoTube is composed of two main components : Automated editor, and Quotes Generator.
**Automated Editor :**
The user inputs **speech.mp3** which is the speech in english to be treated.
![automated_editor_architecture](https://raw.githubusercontent.com/yousbot/Autotube/main/Screenshot%202023-05-16%20at%2012.56.45%20(2)%20copy.png)  

The entire process is either automated from begining to end ( with approvals ), or it's divided into each step in the menu to leave more flexibility to the user to alter the outcome of each process (Ex. Changing the downloaded videos)

**Quotes Generator :**
The user inputs a number of quotes to be generated, and AutoTube will be based on random authors from the list, and the quotes will be parsed from **GoodReads**.
![quotes_generator_architecture](https://raw.githubusercontent.com/yousbot/Autotube/main/file.png) 

The entire process is automated, and generates a number of quotes as requested.

## Features

Once *AutoTube* is launched, the main menu opens and everything can be controlled from here.
*( Except parameter files that should be modified upon need. more details on **explanation.txt** )*
![quotes_generator_architecture](https://raw.githubusercontent.com/yousbot/Autotube/main/menu.png) 

- **Intelligent Editor** : 
***"1. Search for new ideas"*** based on competitors list at competitors.txt. 
***"2. Download videos for audios"*** based on audio files in ../audio, the it creates a folder for each audio file under ../approval, and once 
***"3. Get videos to be approved"*** is chosen, it brings up the menu of "Video Storyboard" to change videos and/or generate video. 
***"4. Create Quotes"*** takes a number of quotes to be created, based on random choice from list of authors in **keywords.txt**, then parse and extract them from **GoodReads**, then clean the text, chose random background locally, and burn text and watermark, font ... and the process repeated for the number of quotes requested, stored under *(../images/quotes/)*. ( An example of quote here : https://github.com/yousbot/Autotube/blob/main/quote_3.png)
- **Skip Silence** : Remove the silence parts in the audio *(../audio/speech.mp3)*
- **Scan Highlights** : It transcribes the audio file *(if it's not already transcribed)*. Then scan each line from the transcription, and extract the most important keywords that constructs the meaning of the sentence. ( Using RAKE algorithm ). ***An update : Keyword Extraction is also available through GPT-4 using openAI's api. It's commented in the code, it's more accurate.*** After that the transcript is outputed, with the important keywords colored, and the user can modify the transcript file. 
- **Video Storyboard** : 
***"1. Download Visuals"***  launch the process of looking up videos based on the Extracted Keywords. Firstly, it calculates the videos to be requested for this line, as each sequences shouldn't exceed 7 seconds *(to avoid long sequences)*. Then it consults the dictionary of videos stored locally *(local_videos.txt)*, if the keyword isn't found, it requests the search on Pexels for Stock Footages, which returns a list of videos and randomly chose those needed, once downloaded, it stores the video locally and updates the dictionary. 
***"2. Change Visuals"*** where the user enters the ID of sequences to be changed, and it launches the process of video download just for that sequence. 
***"3. Generate"*** compiles all the seuqnces downloaded in order, by adding fading transitions. ( !! This requires a lot of processing power.)
- **Burn Captions** : Writes subtitles based on transcripts on the video generated.
- **Copyright**: Checks copyright of the audio files listed under (*../localmusic*)
- **Brand Settings**: Add watermark and intro/outro sequences to the video generated with subtitles.
- **Publish** : Moves files to an Google Drive local file synchronized. ( This should be updated to YouTube directly thorugh API )
- **Useful Tools** : are a set of usual tools needed to make the editing quicker.
***"1. Download Media"*** : It downloads all media listed under *(../downloads.txt)* and store them in *(../Downloads)*
***"2. Clean Workspace"*** : Deletes temporary files and previous project files and structures a clean workspace for next video.
***Crop & Merge*** is a tool used to crop a sequences from long video or audio, based on file speech.txt (for audios) or shorts.txt (for videos)
***"6. Crop & Split videos (9:16)"*** : Create Short Video formats from on 16:9 videos.
***"7. Get channel ID"*** : Get a YouTube's channel ID
***"8. Convert to mp3"*** : Tool to convert mp4 file to mp3

## Note
The tool is in Beta version, and the entire process is functional and working perfectly.
I chose purposefully to be store data on Files and use free open source APIs ( except OpenAI ) and not integrate any databases, which would've made the project even better or history or login or web interface ... or any of the other functionalities that make a perfect tool. 
More componants will be introduced later on, and reshape the tool to make it easily manipulatable and can be used by anybody, and perhaps presented through a platform. If you have any ideas or suggestions I'd like to hear them.

## Installation
*!! As this is a Beta version, hands-on this project would require manual tweaking, next version will be better. !!*

AutoTube was developed and tested on a MacOS Ventura 13.2.1.
Download this repo and name it AutoTube, and put it under ../Desktop
Change your desktop path and APIs where needed in all the python files.
```sh
cd ~/Desktop/AutoTube/
mkdir {approval,audio,downloads,fonts,images,localmusic,shorts,temp,videos}
mv ./*.otf ./fonts/
mkdir /images/background
mkdir /images/quotes
mv ./*.jpg ./images/background
mv ./*.png ./images/background
```
then install pip requirements using
```sh
pip install -r requirements.txt
```
## Author
Youssef Sbai Idrissi, https://www.linkedin.com/in/sbaiidrissiyoussef/



