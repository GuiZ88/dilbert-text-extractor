import os
from extract_text import OCR

if __name__ == "__main__": 
    ocr = OCR()
    transcriptions = ocr.extract_text()