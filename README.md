<a name="readme-top"></a>

<br />
<div align="center">
  <h3 align="center">Dilbert - Text Extractor</h3>

  <p align="center">
The main purpose of this repository is through the recognition of the text of the panels (identified in the first part of the 
[dilbert-boss-cascade-classifier by GuiZ88](project https://github.com/GuiZ88/dilbert-boss-cascade-classifier) ) using the Vision OCR.  
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

After identifying the cartoons with the Boss and Dilbert and thus obtaining the cartoons with both characters and their location contained in the file 'detect_dilbert_boss.txt'

We proceed first with the configuration of the authorization json for the Vision API (Google Cloud) by indicating the correct json in the "extract_text.py" file

```python
cloud_credentials = 'dilbert-text-extractor-95594094aff2.json'
```

Then it is possible to launch the script which, where it does not already exist, creates a txt file with the same name as the image, in the 'image_to_parse' folder with the OCR result, this also presents the centroid of the text block useful for the subsequent dataset construction stage

```sh
python3 extract_text_dataset.py
```

```json
[
    {
        "text": "CAN I HAVE A 25% RAISE TO GET MY COMPENSATION UP TO MARKET LEVELS? ",
        "centroid": [
            140.0,
            65.5
        ]
    },
    {
        "text": "NO. ",
        "centroid": [
            106.5,
            142.0
        ]
    }
]
```

The next step uses a distance measurement to compare the coordinates of Dilber and the Boss, present in the file 'detect_dilbert_boss.txt' with those of each single image, matching the text to the character. Thus a 'dataset.txt' file is generated with the "questions and answers" i.e. the mini dialogue.

```txt
DILBERT: what my budget?
BOSS: no budget.

BOSS: what are you doing?
DILBERT: you have to admit my system is better than whatever your doing over there
```


<u><b>In this repositories there are only some sample images for each folder.</b></u>

![Dilbert & Boss](dilbert-text-extractor/image_to_parse/2010-01-05_0.png?raw=true "Dilbert & Boss")
<p align="right">(<a href="#readme-top">back to top</a>)</p>
