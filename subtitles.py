import os
from typing import Sequence
import pvleopard
from typing import Optional
from termcolor import colored
import re, math, glob
## speech_to_text(audio)                :   Turns audio into file transcript.srt ( 97% accuracy )
## text_on_video(text,in_vid,out_vid)   :   Writes the text on the video 

ACCESS_KEY="pvleopard_access_key"
#input_video = ""
#output_video = ""
desktop_path = "your_desktop_path_here"

font_file_path = desktop_path + "/AutoTube/fonts/greycliffcf-extrabold.otf"
audio_path = desktop_path + "/AutoTube/audio/speech.mp3"
subtitle_path = desktop_path + "/AutoTube/transcript/transcript.srt"
temp_folder = desktop_path + "/AutoTube/temp/"
video_with_subtitles = desktop_path + "/AutoTube/videos/final_video_with_subtitles.mp4"

def clean_subtitle_file():
    string = open(subtitle_path).read()
    new_str = re.sub('[^a-zA-Z0-9\n\.\-\:\,]', ' ', string)
    open(subtitle_path, 'w').write(new_str)

def divide_sentence(s):
    words_list=[]
    words = s.split()
    count = int(math.ceil(len(words)/8.0))
    for i in range(count):
        words_list.append(" ".join(words[i*8:(i+1)*8]))
    return words_list

def text_on_video(text,input_video,output_video,start_seconds,end_seconds):
    w = "(w-text_w)/2"
    h = "(h-text_h-text_h)/2"
    s_w = "(w-text_w)/2"
    s_h = "(h+text_h)/2"

    clean_text = text.strip("\'")
    clean_text = text.strip("\:")
    print(divide_sentence(clean_text))
    text_1 = divide_sentence(clean_text)[0]
    if len(divide_sentence(clean_text)) != 1:
        text_2 = divide_sentence(clean_text)[1]
    else :
        text_2 = ' '

    os.system("ffmpeg -i "+input_video+" -vf \"[in]drawtext=fontfile="+font_file_path+": \
    text=\'"+text_1+"\': fontcolor=white: fontsize=60: borderw=3: \
    x="+w+": y="+h+":enable=\'between(t,"+str(start_seconds)+","+str(end_seconds)+")\', \
    drawtext=fontfile="+font_file_path+": \
    text=\'"+text_2+"\': fontcolor=white: fontsize=60: borderw=3: \
    x="+s_w+": y="+s_h+":enable=\'between(t,"+str(start_seconds)+","+str(end_seconds)+")\'\" \
    -codec:a copy "+output_video)

def sequence_length(start_time,end_time) -> str:
    start_h = int(start_time.split((':'))[0])*3600
    start_min = int(start_time.split((':'))[1])*60
    start_sec = int(start_time.split((':'))[2])
    end_h = int(end_time.split((':'))[0])*3600
    end_min = int(end_time.split((':'))[1])*60
    end_sec = int(end_time.split((':'))[2])
    sequence_length = (start_h+start_min+start_sec)-(end_h+end_min+end_sec)
    return sequence_length

def timecode_to_second(x):
    h = int(x.split((':'))[0])*3600
    min = int(x.split((':'))[1])*60
    sec = int(x.split((':'))[2])
    return h+min+sec

def second_to_timecode(x: float) -> str:
    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)
    return '%.2d:%.2d:%.2d' % (hour, minute, second)

def to_srt(
        words: Sequence[pvleopard.Leopard.Word],
        endpoint_sec: float = 1.,
        length_limit: Optional[int] = 16) -> str:

    def _helper(end: int) -> None:
        lines.append("%d" % section)
        lines.append(
            "%s-%s-%s" %
            (
                second_to_timecode(words[start].start_sec),
                second_to_timecode(words[end].end_sec),
                sequence_length(second_to_timecode(words[start].start_sec),second_to_timecode(words[end].end_sec))
            )
        )
        lines.append(' '.join(x.word for x in words[start:(end + 1)]))
        lines.append('')

    lines = list()
    section = 0
    start = 0
    for k in range(1, len(words)):
        if ((words[k].start_sec - words[k - 1].end_sec) >= endpoint_sec) or \
                (length_limit is not None and (k - start) >= length_limit):
            _helper(k - 1)
            start = k
            section += 1
    _helper(len(words) - 1)

    return '\n'.join(lines)

def speech_to_text(audio_path):
    print(colored("[ Calling API ... ]",'blue'))
    leopard = pvleopard.create(access_key=ACCESS_KEY)
    transcript, words = leopard.process_file(audio_path)
    print(colored("[ Writing to transcript file ... ]",'blue'))
    with open(subtitle_path, 'w') as f:
        f.write(to_srt(words))
        
    print(colored("[ Done ! ]",'blue'))

def add_subtitles_to_video(video_path,subtitles_path):
    print(colored(" [ Opening subtitles file ... ] ",'blue'))
    file = open(subtitles_path)  
    content = file.readlines()
    num_lines = sum(1 for line in open(subtitles_path))

    if len(os.listdir(temp_folder)) != 0:
        latest_file = max(glob.glob(temp_folder+'*'), key=os.path.getmtime)
        i = int(latest_file.split('/')[-1].split('_')[1].split('.')[0])
    else:
        i = 0

    while i < num_lines:
        sequence_start = timecode_to_second(str(content[i+1].split('--')[0]).split('-')[0])
        sequence_end  = timecode_to_second(str(content[i+1].split('--')[0]).split('-')[1])
        sequence_length = int(content[i+1].split('--')[1])
        sequence_text = content[i+2]
        output_video = temp_folder+"subtitles_"+str(i)+".mp4"
        print(colored(" [ Addind subtitles from "+str(str(content[i+1].split('--')[0]).split('-')[0])+ " to " + str((content[i+1].split('--')[0]).split('-')[1]) + " ... ] ",'blue'))
        text_on_video(sequence_text,video_path,output_video,int(sequence_start),int(sequence_end))
        #os.system("rm -rf "+video_path)
        video_path = output_video
        
        i+=4
    os.rename(output_video,video_with_subtitles)
    print(colored(" [ Subtitles addedd successfully ! ] ",'blue'))
    print(colored(" [ Video with subtitles available at : "+video_with_subtitles+" ] ",'blue'))







