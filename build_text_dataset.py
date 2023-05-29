import os
from extract_text import OCR
from pathlib import Path
import json 
import math
from tqdm import tqdm
import re
from textblob import Word

def distance(x1,x2,y1,y2):
    return math.hypot(float(x2)-float(x1), float(y2)-float(y1))
    
def clear_text(text):
    """
    Clears a text string - removes trailing and consecutive spaces, characters other than letters and interpunction, and
    converts the string to lowercase.
    :param text: String to process.
    :return: Cleared strin.
    """
    text = text.lower()

    text = re.sub(r'[^a-zA-Z.,?!\s]+', '', text)
    _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
    text = _RE_COMBINE_WHITESPACE.sub(" ", text).strip()

    return text


def autocorrect_text(text):
    """
    Uses autocorrect to correct the text.
    :param text: String to correct.
    :return: Corrected string.
    """
    words = text.split(' ')
    corrected = []
    for word in words:
        gfg = Word(word)
        spellcheck = gfg.spellcheck()
        if 0.75 < spellcheck[0][1] < 1:
            word = spellcheck[0][0]

        corrected.append(word)

    text = ' '.join(corrected)
    return clear_text(text)

if __name__ == "__main__":
 
    with open('detect_dilbert_boss.txt') as f:
        for line in tqdm(f):
            line = line.strip().split(" ")

            dilbert_centroid = [line[1], line[2]]
            boss_centroid = [line[3], line[4]]

            dilbert_text = ""
            boss_text = ""
            

            path = os.path.join("image_to_parse/", line[0])
            transcription_filename = Path(path).with_suffix('.txt')
            if(os.path.isfile(transcription_filename)):
               print(transcription_filename)
               f = open(transcription_filename)
               json_object = json.load(f) 
               for text in json_object:
                   
                   dilbert_distance = abs(distance(dilbert_centroid[0], text['centroid'][0], dilbert_centroid[1], text['centroid'][1]))            
                   boss_distance = abs(distance(boss_centroid[0], text['centroid'][0], boss_centroid[1], text['centroid'][1]))

                   dilbert_x_distance = abs(float(text['centroid'][0])  - float(dilbert_centroid[0]))
                   boss_x_distance = abs(float(text['centroid'][0])  - float(boss_centroid[0]))

                   # i check with a distance measurement. This part can be implemented further 
                   # to increase the accuracy and the binding logic
                   if(dilbert_distance > boss_distance):
                       boss_text = boss_text + " " + text['text']
                   else:
                       dilbert_text = dilbert_text + " " + text['text']

               f.close()

               dilbert_text = autocorrect_text(dilbert_text)
               boss_text = autocorrect_text(boss_text)
               if len(boss_text.strip()) == 0 or len(dilbert_text.strip()) == 0:
                   print(transcription_filename)                   
                   print("Not a dialogue")                   
                   continue

               dilbert_text = "DILBERT: " + autocorrect_text(dilbert_text)
               boss_text = "BOSS: " +  autocorrect_text(boss_text)
               hs = open('dataset.txt', 'a')
            
               if(float(dilbert_centroid[0]) < float(boss_centroid[0])):
                    hs.write(dilbert_text+"\n")
                    hs.write(boss_text+"\n")
               else:
                    hs.write(boss_text+"\n")
                    hs.write(dilbert_text+"\n")
               
               hs.write("\n")
               hs.close()