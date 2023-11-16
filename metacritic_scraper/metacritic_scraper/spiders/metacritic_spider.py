import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from scrapy.selector import Selector
import time

'''
scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36' {url}

https://stackoverflow.com/questions/58074683/how-to-crawl-multiple-urls-from-csv-using-selenium-and-scrapy
'''


class MetacriticSpider1(scrapy.Spider):
    name = "metacritic_reviews"
    
    game = "stardew-valley"
    
    def start_requests(self):
        # game = "stardew-valley"
        self.driver = webdriver.Chrome()
        yield SeleniumRequest(url = f"https://www.metacritic.com/game/{self.game}/critic-reviews/",
                              callback = self.parse,
                              wait_time = 10,
                              wait_until=EC.presence_of_element_located((By.CLASS_NAME, 'c-siteReview')),
                              cb_kwargs={"game" : self.game})
        
        # for url in urls:
        #     self.driver.get(url)
        #     for item in self.parse(text= self.driver.page_source, game = game):
        #         yield item
        
    def parse(self, response, game):
        # response = Selector(text = text)
        driver = response.request.meta["driver"]

        # element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "c-siteReview"))
        # )
        
        critic_or_user = response.url.split("/")[-2]
        n = 0
        if critic_or_user == "user-reviews":
            n = 10
        else:
            n = 2
        
        for x in range(0,n):
            ActionChains(driver) \
                .scroll_by_amount(0, 10000) \
                .perform()
            time.sleep(2)
            
        for review in driver.find_elements(By.CSS_SELECTOR, "div.c-pageProductReviews_row div.c-siteReview"):
            score = review.find_element(By.CSS_SELECTOR, "div.c-siteReviewScore span").text
            comment = review.find_element(By.CSS_SELECTOR, "div.c-siteReview_quote span").text
            yield {"game" : game,
                   "score" : score,
                   "comment" : comment,
                   "type" : critic_or_user}
            
        yield SeleniumRequest(url = f"https://www.metacritic.com/game/{game}/user-reviews/",
                              callback = self.parse,
                              wait_time = 10,
                              wait_until= EC.presence_of_element_located((By.CLASS_NAME, 'c-siteReview')),
                              cb_kwargs={"game" : game})

        
        
class MetacriticSpider2(scrapy.Spider):
    name = "metacritic_platforms"

    start_urls=["https://www.metacritic.com"]
    
    def parse(self, response):
        games = ["stardew-valley", "minecraft"]
        for game in games:
            yield scrapy.Request(f"https://www.metacritic.com/game/{game}/", callback = self.parse_platforms, cb_kwargs={"game" : game})
            
    def parse_platforms(self, response, game):
        # List of available platforms
        platforms = [a.attrib['href'].split('=')[-1] for a in response.css("div.c-gamePlatformsSection_list.u-grid-columns a")]
        
        yield {"Game" : game, "Platforms" : platforms}
        
        
        

            

            
# class MetacriticSpider1(scrapy.Spider):
#     name = "metacritic_reviews"

#     start_urls=["https://www.metacritic.com"]

#     def parse(self, response):
#         games = ["stardew-valley", "minecraft"]
#         for game in games:
#             yield scrapy.Request(f"https://www.metacritic.com/game/{game}/", callback = self.parse_reviews, cb_kwargs={"game" : game})
        
#     def parse_reviews(self, response, game):
#         # List of critic comments
#         critic_comments = response.css("div.c-reviewsSection_criticReviews div.c-reviewsSection_carousel div.c-siteReview_quote.g-outer-spacing-bottom-small span::text").getall()
        
#         # List of critic numeric scores (out of 100)
#         critic_scores = response.css("div.c-reviewsSection_criticReviews div.c-reviewsSection_carousel div.c-siteReviewScore.u-flexbox-column span::text").getall()
        
#         # List of user comments
#         user_comments = response.css("div.c-reviewsSection_userReviews div.c-reviewsSection_carousel div.c-siteReview_quote.g-outer-spacing-bottom-small span::text").getall()
        
#         # List of user numeric scores (out of 10)
#         user_scores = response.css("div.c-reviewsSection_userReviews div.c-reviewsSection_carousel div.c-siteReviewScore.u-flexbox-column span::text").getall()
        
#         for i in range(len(critic_comments)): 
#             yield {"Game" : game, "Comment" : critic_comments[i], "Score" : critic_scores[i], "Type" : "Critic"}
            
#         for j in range(len(user_comments)):
#             yield {"Game" : game, "Comment" : user_comments[j], "Score" : user_scores[j], "Type" : "User"}