import cv2
from tqdm import tqdm
import os
from pathlib import Path
import json 

from text_extractor.VisionOCR import VisionOCR

class OCR:
    cloud_credentials = 'dilbert-text-extractor-95594094aff2.json'

    def __init__(self):
        self.extractor = VisionOCR(self.cloud_credentials)

    def extract_text(self):
        """
        Extracts text from images.
        :param img_paths: A list of paths to images for processing.     
        :return: A dictionary mapping image paths to the extracted names.        """
        result = {}
        with open('detect_dilbert_boss.txt') as f:
            for line in tqdm(f):
                line = line.strip().split(" ")
                path = os.path.join("image_to_parse/", line[0])
                print(line)

                transcription_filename = Path(path).with_suffix('.txt')
    
                if(os.path.isfile(path)):
                    if(not os.path.isfile(transcription_filename)):
                        image = cv2.imread(path)
                        result[path] =  self.extractor.extract_text(image)                     
                
                        hs = open(transcription_filename, 'w+')

                        json_object = json.dumps(result[path], indent = 4) 
                        hs.write(json_object)
                        
                        hs.close()
                    else:
                        print("ALREADY PROCESSED")

        return result