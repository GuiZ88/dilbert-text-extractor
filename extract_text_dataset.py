import os
from extract_text import OCR

if __name__ == "__main__": 

    images_paths = [os.path.join("image_to_parse/", file) for file in os.listdir("image_to_parse/")]
    ocr = OCR()

    transcriptions = ocr.extract_text(images_paths, clustering=True)