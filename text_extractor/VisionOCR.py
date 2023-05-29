import io
import os
import cv2
from google.cloud import vision
import numpy as np

class VisionOCR:
    def __init__(self, credentials_path):
        """
        :param credentials_path: a path to the Google Cloud credentials .json file.
        """
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

    def centroid(self, bounding_box):
        x = 0
        y = 0
        n = len(bounding_box.vertices)
        for vertix in bounding_box.vertices:
            x += vertix.x
            y += vertix.y

        return (x/n, y/n) 

    def extract_text(self, image):
        """
        Performs OCR text extraction using Google Cloud Vision API OCR.
        :param image: image to detect text in.
        :return: tuple of lists, one containing the detected strings, the other containing the b-boxes.
        """
        #print(image)
        client = vision.ImageAnnotatorClient()
        cv2.imwrite("temp.png", image)
        with io.open("temp.png", 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        #print(texts)
        #print(response.full_text_annotation)
        breaks = vision.TextAnnotation.DetectedBreak.BreakType
    
        result = []
        word_text = ""
        aaa = response.full_text_annotation
        for page in aaa.pages:
            for block in page.blocks:
                word_text = ""
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            word_text += symbol.text
                            #print(word_text)
                            if symbol.property.detected_break.type:
                                if symbol.property.detected_break.type == breaks.SPACE or symbol.property.detected_break.type == breaks.HYPHEN or symbol.property.detected_break.type == breaks.EOL_SURE_SPACE  or symbol.property.detected_break.type == breaks.LINE_BREAK:
                                    word_text += " "
                                #else:
                                    #print word_text ,symbol.property.detected_break
                                    #word_text = ""

                #print(paragraph)
                #print(block)
                #print(word_text)
                detect = {}
                detect['text'] = word_text
                detect['centroid'] = self.centroid(block.bounding_box)           
                result.append(detect)
               

        """
        words = []
        bboxes = []
        for text in texts[1:]:
            words.append(text.description)
            pts = np.array([[vertex.x, vertex.y] for vertex in text.bounding_poly.vertices], np.int32)
            xmin = np.min([x[0] for x in pts])
            ymin = np.min([x[1] for x in pts])
            xmax = np.max([x[0] for x in pts])
            ymax = np.max([x[1] for x in pts])
            bboxes.append((xmin, ymin, xmax, ymax))
        """

        return result