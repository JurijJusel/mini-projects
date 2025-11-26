from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.skelbiu_auto import SkelbiuAutoSpider
from crawler.spiders.autoplius import AutopliusSpider
from crawler.spiders.constants import SKELBIU_AUTO_OUTPUT_FILE, AUTOP_OUTPUT_FILE
from rich import print


if __name__ == "__main__":
    print("Starting crawlers...")

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(SkelbiuAutoSpider)
    process.crawl(AutopliusSpider)

    process.start()
    print("All crawlers finished.")
