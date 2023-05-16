from contextlib import contextmanager, redirect_stderr, redirect_stdout
from os import devnull
import os
import random
import re
import textwrap
from pyparsing import line
import requests
from bs4 import BeautifulSoup, NavigableString
from PIL import Image
from PIL import ImageDraw, ImageFont
from textwrap import wrap

from termcolor import colored

desktop_path = "your_desktop_path_here"
project_folder = desktop_path + '/AutoTube/'
temp_quotes_file = project_folder+'temp/quotes.txt'
image_folder = project_folder+'images/'
black_image = image_folder+'Generate_Quote.png'
# font_file = project_folder+'fonts/Gilmer_Heavy.otf'
# font_file = project_folder+'fonts/Lyons-Serif-Bold.ttf'
font_file = project_folder+'fonts/Sofia_Handwritten.otf'
new_black_image = image_folder+'1_black.png'
double_quotes = image_folder+'double_quotes.png'
author_font_file = project_folder+'fonts/OpenSans-Light.ttf'
keywords_file = project_folder+'keywords.txt'
logo = image_folder+'logo.png'
logo_font_file = project_folder+'PARISNN.ttf'
background_folder = image_folder+'background/'
quotes_folder = image_folder+"quotes/"

FONT_FAMILY = font_file
WIDTH = 2800
HEIGHT = 2800
FONT_SIZE = 110
V_MARGIN =  20
CHAR_LIMIT = 45
BG_COLOR = "black"
TEXT_COLOR = "white"
AUTHOR_TEXT_COLOR = "yellow"
LOGO = 'Intellectual Wave'
NUM_PICTURES = int(len(os.listdir(background_folder)))-1

@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)

def quotes_by_author(author, page_num):

	old_author = author

	author = author.replace(" ", "+")

	all_quotes = []

	# if page number not specified, get true page number
	if page_num is None:
		try:
			page = requests.get("https://www.goodreads.com/quotes/search?commit=Search&page=1" + "&q=" + author + "&utf8=%E2%9C%93")
			soup = BeautifulSoup(page.text, 'html.parser')
			pages = soup.find(class_="smallText").text
			a = pages.find("of ")
			page_num = pages[a+3:]
			page_num = page_num.replace(",", "").replace("\n", "")
			page_num = int(page_num)
			print("looking through", page_num, "pages")
		except:
			page_num = 1

	# for each page
	for i in range(1, page_num+1, 1):

		try:
			page = requests.get("https://www.goodreads.com/quotes/search?commit=Search&page=" + str(i) + "&q=" + author + "&utf8=%E2%9C%93")
			soup = BeautifulSoup(page.text, 'html.parser')
			print("scraping page", i)
		except:
			print("could not connect to goodreads")
			break
			
		try:
			quote = soup.find(class_="leftContainer")
			quote_list = quote.find_all(class_="quoteDetails")
		except:
			pass

		# get data for each quote
		for quote in quote_list:

			meta_data = []

			# Get quote's text
			try:
				outer = quote.find(class_="quoteText")
				inner_text = [element for element in outer if isinstance(element, NavigableString)]
				inner_text = [x.replace("\n", "") for x in inner_text]
				final_quote = "\n".join(inner_text[:-4])
				meta_data.append(final_quote.strip())
			except:
				pass 


			# Get quote's author
			try:
				author = quote.find(class_="authorOrTitle").text
				author = author.replace(",", "")
				# author = author.replace("\n", "")
				#meta_data.append(author.strip())
				# print(author)
			except:
				meta_data.append(None)

			# Get quote's book title
			try: 
				title = quote.find(class_="authorOrTitle")
				title = title.nextSibling.nextSibling.text
				title = title.replace("\n", "")
				#meta_data.append(title.strip())
				# print(title)
			except:
				meta_data.append(None)

			# Get quote's tags
			try:
				tags = quote.find(class_="greyText smallText left").text
				tags = [x.strip() for x in tags.split(',')]
				tags = tags[1:]
				#meta_data.append(tags)
				# print(tags)
			except:
				meta_data.append(None)

			# Get number of likes
			try:
				likes = quote.find(class_="right").text
				likes = likes.replace("likes", "")
				likes = int(likes)
				#meta_data.append(likes)
				# print(likes)
			except:
				meta_data.append(None)

			all_quotes.append(meta_data)


		for text in all_quotes:
			print(text)

	return all_quotes

def clean_line(line) -> str:
    if "[''" not in line and line not in ['\n', '\r\n'] :
        clean_text = line.replace(', None','')
        clean_text = line#.split('\“')[1]
        print(clean_text)

def get_y_and_heights(text_wrapped, dimensions, margin, font):
    ascent, descent = font.getmetrics()
    line_heights = [
        font.getmask(text_line).getbbox()[3] + descent + margin
        for text_line in text_wrapped
    ]
    line_heights[-1] -= margin
    height_text = sum(line_heights)
    y = (dimensions[1] - height_text) // 2
    return (y, line_heights)

def text_on_image(quote, author):

    font = ImageFont.truetype(FONT_FAMILY, FONT_SIZE)
    #img = Image.new("RGB", (WIDTH, HEIGHT), color=BG_COLOR)
    img = Image.open(background_folder+str(random.randint(1,NUM_PICTURES))+'.png')
    draw_interface = ImageDraw.Draw(img)

    text_lines = wrap(quote, CHAR_LIMIT)
    y, line_heights = get_y_and_heights(
        text_lines,
        (WIDTH, HEIGHT),
        V_MARGIN,
        font
    )
    for i, line in enumerate(text_lines):
        line_width = font.getmask(line).getbbox()[2]
        x = ((WIDTH - line_width) // 2)
        draw_interface.text((x, y), line, font=font, fill=TEXT_COLOR)
        y += line_heights[i]
    
    line_width = font.getmask(author).getbbox()[2]
    x = ((WIDTH - line_width) // 2)
    font = ImageFont.truetype(author_font_file, FONT_SIZE)
    draw_interface.text((x, y+100), author, font=font, fill=(255,232,158,255))

    line_width = font.getmask(LOGO).getbbox()[2]
    font = ImageFont.truetype(logo_font_file, FONT_SIZE)
    draw_interface.text((140, 2600), LOGO, font=font, fill=(255,232,158,255))

    img.save(black_image)

    ## add_double_quotes to image
    im1 = Image.open(black_image)
    im1.paste(Image.open(double_quotes), (60,60),Image.open(double_quotes))
    im1.save(black_image, quality=100)


def generate_quote():

	file = open(keywords_file)  
	content = file.readlines()
	print(colored(" [ Chosing random author from list ... ]",'blue'))
	author = str(random.choice(content))
	with suppress_stdout_stderr():
		list_quotes = quotes_by_author(author, 10)

	with open(temp_quotes_file, 'w') as f:    
		for line in list_quotes :
			print(line, file=f)

	file = open(temp_quotes_file)  
	content = file.readlines()
	print(colored(" [ Cleaning quotes ... ]",'blue'))
	clean_quotes_list = []
	for quote in content:
		if '“' in quote :
			clean_quotes_list.append(quote[quote.find('“')+len('“'):quote.rfind('”')].replace('\', None]','').replace('\\n',' ').replace(',\', None, None]',''))
	del clean_quotes_list[-1]

	clean_quotes_list = [x for x in clean_quotes_list if len(x) <= 300]
	quote_author = random.choice(clean_quotes_list)
	print(colored(" [ Displaying quote on image ... ]",'blue'))
	text_on_image(quote_author,author)
	print(colored(" [ Done ! ]",'blue'))

def generate_multiple_quotes(num):
	os.system("rm -rf "+quotes_folder+"/*")
	for i in range(1,int(num)+1):
		generate_quote()
		os.system("cp "+black_image+" "+quotes_folder+"quote_"+str(i)+".png")
		print(colored(" [ Quote ready under :"+quotes_folder+"quote_"+str(i)+".png ]",'blue'))
		os.system("rm -rf "+black_image)