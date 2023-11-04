import scrapy

'''
scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36' {url}

<div class="c-gameReviews g-inner-spacing-top-medium g-inner-spacing-bottom-medium">
    <div class="c-reviewWrapper">
    <div class="c-reviewWrapper">
    
scraping from https://www.metacritic.com/game/stardew-valley/
    response.css("div.c-reviewsSection_criticReviews div.c-reviewsSection_carousel div.c-siteReview_quote.g-outer-spacing-bottom-small span::text").getall()
    ^gets the critic comment reviews available in the preview carousel in a list
    
    response.css("div.c-reviewsSection_criticReviews div.c-reviewsSection_carousel div.c-siteReviewScore.u-flexbox-column span::text").getall()
    ^gets the critic numeric reviews
    
    response.css("div.c-reviewsSection_userReviews div.c-siteReview_quote.g-outer-spacing-bottom-small span::text").getall()
    ^gets the user comment reviews available in the preview carousel in a list
    
    response.css("div.c-reviewsSection_userReviews div.c-reviewsSection_carousel div.c-siteReviewScore.u-flexbox-column span::text").getall()
    ^gets the user numeric reviews
'''

class MetacriticSpider(scrapy.Spider):
    name = "metacritic_spider"

    start_urls=["https://www.metacritic.com"]

    def parse(self, response):
        games = ["stardew-valley", "minecraft"]
        for game in games:
            yield scrapy.Request(f"https://www.metacritic.com/game/{game}/", callback = self.parse_reviews, cb_kwargs={"game" : game})
        
    def parse_reviews(self, response, game):
        # List of critic comments
        critic_comments = response.css("div.c-reviewsSection_criticReviews div.c-reviewsSection_carousel div.c-siteReview_quote.g-outer-spacing-bottom-small span::text").getall()
        
        # List of critic numeric scores (out of 100)
        critic_scores = response.css("div.c-reviewsSection_criticReviews div.c-reviewsSection_carousel div.c-siteReviewScore.u-flexbox-column span::text").getall()
        
        # List of user comments
        user_comments = response.css("div.c-reviewsSection_userReviews div.c-reviewsSection_carousel div.c-siteReview_quote.g-outer-spacing-bottom-small span::text").getall()
        
        # List of user numeric scores (out of 10)
        user_scores = response.css("div.c-reviewsSection_userReviews div.c-reviewsSection_carousel div.c-siteReviewScore.u-flexbox-column span::text").getall()
        
        for i in range(len(critic_comments)): 
            yield {"Game" : game, "Comment" : critic_comments[i], "Score" : critic_scores[i], "Type" : "Critic"}
            
        for j in range(len(user_comments)):
            yield {"Game" : game, "Comment" : user_comments[j], "Score" : user_scores[j], "Type" : "User"}
        