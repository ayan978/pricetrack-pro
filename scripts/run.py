from dotenv import load_dotenv
load_dotenv()  # loads .env if present

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pricetrack_pro.spiders.demo_store import DemoStoreSpider

if __name__ == "__main__":
    # Get default settings
    settings = get_project_settings()
    
    # Enable pause/resume by storing crawl state
    settings.set("JOBDIR", "data/crawl_state")
    
    process = CrawlerProcess(settings)
    process.crawl(DemoStoreSpider)
    process.start()