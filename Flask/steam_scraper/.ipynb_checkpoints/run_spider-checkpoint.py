from steam_scraper.steam_scraper.spiders.steam_spider import SteamSpider1
# from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


class Scraper:
    def __init__(self):
        settings_file_path = 'steam_scraper.steam_scraper.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        # self.process = CrawlerProcess(get_project_settings())
        configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
        self.runner = CrawlerRunner(settings = get_project_settings())
        self.spider = SteamSpider1 # The spider you want to crawl

    def run_spiders(self, game):
        # self.process.crawl(self.spider, game = game)
        # self.process.start()  # the script will block here until the crawling is finished
        d = self.runner.crawl(self.spider, game = game)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()  # the script will block here until the crawling is finished






# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings


# def scrape(game):  
#     process = CrawlerProcess(get_project_settings())
#     process.crawl("steam_reviews", game = game)
#     process.start()  # the script will block here until the crawling is finished
    
# game = "hidden+through+time"

# scrape(game)




