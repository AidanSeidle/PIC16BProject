# scrapy crawl steam_reviews -O results.csv

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class SteamSpider1(scrapy.Spider):
    name = "steam_reviews"
    
    # This is Selenium's replacement for Scrapy's start_urls = []
    def start_requests(self):
        # game = "MapleStory" # spaces in game name should be represented as "+"
        yield SeleniumRequest(url = f"https://store.steampowered.com/search/?term={self.game}", 
                              callback = self.search_bar,
                              wait_time = 10,
                              wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'search_result_row')),
                              cb_kwargs={"game" : self.game})
        
    def search_bar(self, response, game):
        driver = response.request.meta["driver"]
        
        # get the first search result (assuming the most relevant will be the correct game; games must be on Steam)
        url = driver.find_element(By.CSS_SELECTOR, "div.search_results a").get_attribute('href')
        
        yield SeleniumRequest(url = url, callback = self.view_all_comments, 
                              wait_time = 10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'view_all_reviews_btn')), 
                              cb_kwargs={"game" : game})
        
    def view_all_comments(self, response, game):
        driver = response.request.meta["driver"]
        
        for x in range(0,2):
            ActionChains(driver) \
                .scroll_by_amount(0, 10000) \
                .perform()
            time.sleep(2)

        # get the "view all reviews" button
        url = driver.find_element(By.CSS_SELECTOR, "div.view_all_reviews_btn a").get_attribute('href')
        
        yield SeleniumRequest(url = url, callback = self.parse, cb_kwargs={"game" : game})
    
    def parse(self, response, game):
        driver = response.request.meta["driver"]
        
        # scroll down by 10000 pixels 10 times (increase range for more comments, ~10 reviews per scroll)
        for x in range(0,20):
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
                
                    # steam censors swear words with hearts
                    # the date posted is at the front of the comment, but the format of the date is inconsistent
                    yield {"game" : game,
                            "is_Recommended" : recommended,
                            "hours_players" : hours,
                            "comment" : comment}
        
        

    
    