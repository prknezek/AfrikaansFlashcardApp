from gtts import gTTS
from io import BytesIO
import pygame

def speak(text, language='af'):
    global fp
    fp = BytesIO()
    tts = gTTS(text, lang=language)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

pygame.init()
pygame.mixer.init()
sound = speak("beast")
pygame.mixer.music.load(sound, 'mp3')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
