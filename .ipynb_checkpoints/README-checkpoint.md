# Video Game Review Bot

This applictaion will analyze a video game for its best features so you can decide what to play next. Input the name of a game you are thinking about buying and our app will analyze comments for what features players like best and which features they like least. 

## Setup

This only works with Chrome browser

Necessary packages:
1. numpy
2. pandas
3. matplotlib
4. sklearn
5. tensorflow
6. nltk
7. scrapy
8. scrapy-selenium (FOLLOW BELOW INSTRUCTIONS)
9. selenium

## Setting up scrapy-selenium

Follow the below instructions to use Selenium with Scrapy
instructions also found here with pictures: https://www.zenrows.com/blog/scrapy-selenium#install

1. pip install scrapy_selenium
    -this should also install selenium but if it doesnt: pip install selenium
    
2. pip install show
    -in the output, find the "location: "
    -for example: Location: /Users/nannan/opt/anaconda3/envs/PIC16B-2/lib/python3.11/site-packages
    
3. Follow the directory to the folder, then navigate into the folder called "scrapy_selenium"
    -this folder should contain __pycache__, __init__.py, http.py, and middlwares.py
    
4. Replace the middlewares.py file with the middleware.py file found in the "FOR SELENIUM" folder.
