import scrapy
from crawler.spiders.constants import AUTO_URLS, ADS_PER_PAGE
from crawler.models.skelbiu_models import SkelbiuAutoModel
from rich import print
from crawler.spiders.constants import SKELBIU_AUTO_OUTPUT_FILE


class SkelbiuAutoSpider(scrapy.Spider):
    """
    Spider for scraping car listings from Skelbiu.lt.

    The spider performs a multi-step crawl:
        1. Loads base category URLs from AUTO_URLS.
        2. Extracts total number of ads and calculates pagination count.
        3. Queues all paginated listing pages.
        4. Extracts structured ad data from each listing page.
        5. Outputs items as dictionaries via Pydantic model validation.

    Attributes
    ----------
    name : str
        Unique name used by Scrapy to identify the spider.
    start_urls : list[str]
        Initial category URLs defined in AUTO_URLS.
    collected_urls : list[str]
        Internal list storing every paginated URL that is crawled.
    """
    custom_settings = {
        "FEEDS": {
            SKELBIU_AUTO_OUTPUT_FILE: {
                "format": "jsonlines",
                "encoding": "utf-8",
                "overwrite": True,
            }
        }
    }

    name = 'skelbiu_spider'
    start_urls = AUTO_URLS
    collected_urls = []

    def parse(self, response):
        """
        Parse the initial category page to determine pagination.
        This method:
            - Reads total ad count from the page header.
            - Calculates total number of pages based on ADS_PER_PAGE.
            - Generates URLs for all listing pages.
            - Dispatches requests to `parse_ads`.
        Parameters
        ----------
        response : scrapy.http.Response
            The HTTP response received for a category page.
        Yields

        scrapy.Request
            Requests for each paginated listing page.
        """
        print(f"Parsing base URL: {response.url}")
        ads_count_text = response.css('li.change-and-submit.active span::text').get()
        ads_count = int(ads_count_text.strip(' ()\n').replace(' ', ''))
        total_pages = (ads_count // ADS_PER_PAGE) + (1 if ads_count % 24 != 0 else 0)
        print(f"Total ads: {ads_count if ads_count_text else 'unknown'} Total pages: {total_pages}")

        for page in range(1, total_pages + 1):
            if page == 1:
                url = response.url
            else:
                url = f"{response.url}{page}"
            self.collected_urls.append(url)
            print(f"Queueing URL: {url}")
            yield scrapy.Request(url, callback=self.parse_ads)

    def parse_ads(self, response):
        """
        Parse a paginated listing page and extract individual ads.
        This method extracts:
            - Item ID
            - Title
            - Location and creation time
            - Parameters
            - Price
            - Listing URL
            - Image URL
        Each ad is converted to a Pydantic `SkelbiuAutoModel`,
        validated, and output as a dictionary.

        Parameters
        ----------
        response : scrapy.http.Response
            HTTP response for a paginated listing page.
        """
        print(f"Parsing page: {response.url}")
        ads = response.css('a.gallery-item-element-link.js-cfuser-link')
        print(f"Number of ads on this page: {len(ads)}")

        for ad in ads:
            href = ad.attrib.get('href')
            full_link = response.urljoin(href)
            item_id = ad.attrib.get('data-item-id')
            title = ad.css('h3::text').get(default='').strip()
            image_url = ad.css('img::attr(src)').get(default='')
            second_dataline = ad.css('div.info-line::text').get(default='N/A').split()
            city = second_dataline[0] if second_dataline else 'N/A'
            input_date = ' '.join(second_dataline[1:]) if len(second_dataline) > 1 else 'N/A'
            price = ad.css('div.price::text').get(default='N/A').strip('€').replace(' ', '')
            item_params = ad.css('div.params .param::text').getall()

            data = {
                "Item_ID": item_id,
                "Title": title,
                "City": city,
                "Creation date": input_date,
                "Item Params": item_params,
                "Price": price,
                "Link": full_link,
                "Image URL": image_url
            }

            item = SkelbiuAutoModel(**data)
            yield item.model_dump()


    def closed(self, reason):
        """
        Called automatically when the crawl finishes.

        Logs a summary of:
        - Total paginated URLs that were queued
        - Reason the spider stopped

        Parameters
        ----------
        reason : str
            Message provided by Scrapy describing why the spider closed.
        """
        print("\n\n--- Skelbiu Crawl Finished ---")
        print(f"Total collected URLs: {len(self.collected_urls)}")
        for url in self.collected_urls:
            print(url)
        print(f"Reason for closure Skelbiu crawler: {reason}")
