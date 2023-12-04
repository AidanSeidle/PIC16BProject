from steam_scraper.run_spider import Scraper

def process_name(x):
    x = x.lower()
    x = x.split()
    x = '+'.join(x)
    return x

scraper = Scraper()
scraper.run_spiders("Undertale")









# import sys
# import os

# sys.path.insert(0, 'steam_scraper')
# print("*"*200)
# print(os.getcwd())
# os.chdir('steam_scraper')
# print(sys.path)
# print("*"*200)
# from run_spider import scrape

# scrape("dave+the+diver")


