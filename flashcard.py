# Imports
from tkinter import *
from tkinter.font import BOLD
import customtkinter
from PIL import Image, ImageTk
from gtts import gTTS
import pygame
from io import BytesIO
from threading import Timer
from datetime import datetime, timedelta
import sys

# reading data from previous lessons
with open('data.txt', 'r') as file:
    '''data is ordered as: 
    group_number, position, group_averages
    '''
    data = file.readlines()[0].split(';')

group_number = int(data[0])
position = int(data[1])

# score of recollection for each word: 1.0 is perfect recollection
word_score = 1.0
# reading data from file and converting it to a list
group_recollection_averages = data[2][1:-1].split(',')
avgs = []
for i in group_recollection_averages:
    i.lstrip()
    if i != '':
        avgs.append(int(i))
group_recollection_averages = avgs
group_recollection = 0

# importing spaced repetition 
sys.path.insert(1, 'D:/VSCode Projects/Afrikaans Flashcard App/spaced-master')
print(sys.path)
#import repetition as rep
import repetition as rep

# pygame setup for tts audio
pygame.init()
pygame.mixer.init()

# tkinter setup
root = customtkinter.CTk()
root.title('Afrikaans Flashcard App')
root.geometry("550x410")

# tkinter appearance changes
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

# turning word_list.txt into a list to be used in App
with open('word_list.txt') as file:
    lines = file.readlines()

# removing numbers from all lines
lines_words = ''.join([i for i in lines[0] if not i.isdigit()])
kv_pairs = lines_words.split('  ')

# Creating list containing tuples ordered as: (afrikaans word, english translation) 
words = []

for i in range(len(kv_pairs)):
    kv_pairs[i] = kv_pairs[i].lstrip()
    kv_pairs[i] = kv_pairs[i].split(' ')
    words.append((kv_pairs[i][0], kv_pairs[i][1]))

# Creating Learning groups
group_size = 10
learning_groups = []

# get a count of word list
num_words = len(words)

for j in range(0, num_words, group_size):
    group = []
    if j + group_size <= num_words: 
        for i in range(group_size):
            group.append(words[i + j])
        learning_groups.append(group)

# adding words that were left out of groups
rem = num_words % group_size
group = []
for i in range(num_words - rem, num_words):
    group.append(words[i])
learning_groups.append(group)


# TTS function
def translation():
    sound = speak(af_word)
    pygame.mixer.music.load(sound, 'mp3')
    pygame.mixer.music.play()

def speak(text, language='af'):
    global fp
    fp = BytesIO()
    tts = gTTS(text, lang=language)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# Displays next word
def next():
    global hinter, hint_count, af_word, eng_word, group_number, position, word_score
    global group_recollection, group_recollection_averages, group_size

    # Moves to next group when position reaches end of group
    if position >= len(learning_groups[group_number]):
        # resets group if reaches the end of learning groups
        if group_number >= len(learning_groups) - 1:
            print('list completed')
            group_number = 0
        else:
            # changes to next group when all words in learning group have been seen
            group_number += 1
            group_recollection_averages.append(group_recollection / group_size)
            group_recollection = 0.0
        position = 0

    # setting words
    af_word = learning_groups[group_number][position][0]
    eng_word = learning_groups[group_number][position][1]
    
    # Clear screen
    answer_label.configure(text="")
    hint_label.configure(text="")
    my_entry.delete(0, END)
    # Reset hints
    hinter = ""
    hint_count = 0

    # Update label with Afrikaans Word
    af_word_label.configure(text=af_word)

    # Read word to user
    # sets sound equal to current word
    sound = speak(af_word)
    pygame.mixer.music.load(sound, 'mp3')
    pygame.mixer.music.play()

    # incrementing position to next word
    position += 1
    # reset word_score for next word
    word_score = 1.0
    
# make answer key activate on enter key press
def handler(e):
    answer()

root.bind('<Return>', handler)

# Displays answer in english
def answer():
    global word_score, group_recollection
    if my_entry.get().capitalize() == eng_word.capitalize():
        answer_label.configure(text=f"Correct! {af_word} is {eng_word}", fg='#00A300')
        # adding word_score to group_recollection score for current group
        group_recollection += word_score

        # 2 second delay before moving on to next word
        # after answering correctly
        t = Timer(2, next)
        t.start()
    else:
        answer_label.configure(text=f"Incorrect, {af_word} is not {my_entry.get().capitalize()}", fg='#D22B2B')
        if word_score >= 0:
            word_score -= 0.1

# Keep track of hints
hinter = ""
hint_count = 0

# gives one letter at a time to help user
def hint():
    global hint_count, hinter, word_score

    # stops giving hints if entire word is shown
    if hint_count < len(eng_word):
        hinter = hinter + eng_word[hint_count]
        hint_label.configure(text=hinter)
        hint_count += 1
        if word_score >= 0:
            word_score -= 0.05

# reset function
def reset():
    window = customtkinter.CTkToplevel()
    window.geometry('300x200')
    window.title("Reset")

    label = customtkinter.CTkLabel(window, text = "Are you sure you want to reset?",
        text_font=('Arial', 10, 'bold'))
    label.pack(side='top', fill = 'both', expand=True, padx=40, pady=40)
    
    # yes and no functions for options of reset
    def yes():
        global group_number, position
        group_number = 0
        position = 0
        window.destroy()
        next()

    def no():
        window.destroy()

    yes_button = customtkinter.CTkButton(master=window, text='Yes', height=35, width=50,
        text_font=('Arial', 15,'bold'), command = yes)
    yes_button.place(x=90, y=120)
    
    no_button = customtkinter.CTkButton(master=window, text='No', height=35, width=50,
        text_font=('Arial', 15,'bold'), command = no)
    no_button.place(x=160,y=120)
    
# Defining Images
next_image = ImageTk.PhotoImage(Image.open("gui/next_arrow.png").resize((20,20), Image.Resampling.LANCZOS))
check_image = ImageTk.PhotoImage(Image.open("gui/check.png").resize((20,20), Image.Resampling.LANCZOS))
hint_image  = ImageTk.PhotoImage(Image.open("gui/q_mark.png").resize((20,20), Image.Resampling.LANCZOS))
translate_image = ImageTk.PhotoImage(Image.open('gui/translate.png').resize((20,20), Image.Resampling.LANCZOS))

# Creating Buttons
next_button = customtkinter.CTkButton(master=root, image=next_image, text="Next",
    width=80, height=35, compound='left', command=next, 
    text_font=('Arial', 15,'bold'))
next_button.place(x=342, y=300)

answer_button = customtkinter.CTkButton(master=root, image=check_image, text="Answer",
    width=80, height=35, compound='left', fg_color='#D35B58', hover_color='#C77C78', command=answer,
    text_font=('Arial', 15, 'bold'))
answer_button.place(x=214, y=300)

hint_button = customtkinter.CTkButton(master=root, image=hint_image, text="Hint",
    width=80, height=35, compound='left', command=hint, 
    text_font=('Arial', 15,'bold'))
hint_button.place(x=117, y=300)

translate_button = customtkinter.CTkButton(master=root, image=translate_image, text="Repeat",
    width=80, height=35, compound='left', command=translation, 
    text_font=('Arial', 15,'bold'))
translate_button.place(x=215,y=342)

reset_button = customtkinter.CTkButton(master=root, text="Reset",
    width=80, height=35, compound='left', command=reset, 
    text_font=('Arial', 15,'bold'))
reset_button.place(x=20,y=20)

# Creating Labels & Entry
hint_label = customtkinter.CTkLabel(master=root, text='',
    text_font=('Arial', 14, 'underline'))
hint_label.place(x=275, y=100, anchor='center')

af_word_label = customtkinter.CTkLabel(master=root, text='', text_font=('Arial', 30),
    width=200)
af_word_label.place(x=176, y=130)

answer_label = customtkinter.CTkLabel(master=root, text='', text_font=('Arial', 14),
    wraplength=300, justify='center')
answer_label.place(x=277, y=205, anchor='center')

my_entry = customtkinter.CTkEntry(master=root, text_font=('Arial', 18),
    width=220, height=36)
my_entry.place(x=165, y=235)

# Run next function when program starts
next()
root.mainloop()

# Run save data after program is closed
with open('data.txt', 'w') as file:
    '''data is ordered as: 
    group_number, position, temp word_score, group_averages
    '''
    def avgs():
        return [i for i in group_recollection_averages]

    file.write('{group};{pos};{avgs}'
    .format(group = group_number, pos = position - 1, avgs = avgs()))
