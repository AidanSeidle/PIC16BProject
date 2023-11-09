# scrapy crawl steam_reviews -O results.csv

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By

class SteamSpider1(scrapy.Spider):
    name = "steam_reviews"
    
    # This replaces start_urls = [] when using Selenium
    def start_requests(self):
        games = ["stardew+valley"]
        yield SeleniumRequest(url = "https://steamcommunity.com/app/413150/reviews/?browsefilter=toprated&snr=1_5_100010_",
                              callback = self.parse)
    
    def parse(self, response):
        driver = response.request.meta["driver"]
        
        # scroll down by 10000 pixels 10 times (increase range for more comments, 10 scrolls gets 650 reviews)
        for x in range(0,10):
            ActionChains(driver) \
                .scroll_by_amount(0, 10000) \
                .perform()
            
            # wait for comments to load
            time.sleep(2)
            
            for page in driver.find_elements(By.CSS_SELECTOR, "div.apphub_Cards div"):
                for row in page.find_elements(By.CSS_SELECTOR, "div.apphub_CardRow"):
                    for quote in row.find_elements(By.CSS_SELECTOR, "div.apphub_Card.modalContentLink.interactable"):
                        recommended = quote.find_element(By.CSS_SELECTOR, "div.vote_header div.title").text
                        hours = quote.find_element(By.CSS_SELECTOR, "div.vote_header div.hours").text.split()[0]
                        comment = quote.find_element(By.CSS_SELECTOR, "div.apphub_CardTextContent").text
                    
                        yield {"is_Recommended" : recommended,
                               "hours_players" : hours,
                               "comment" : comment}
        
        

    
    