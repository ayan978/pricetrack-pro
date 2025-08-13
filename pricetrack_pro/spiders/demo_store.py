import re
from urllib.parse import urljoin
import scrapy

class DemoStoreSpider(scrapy.Spider):
    name = "demo_store"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {"DOWNLOAD_DELAY": 1.0}  # extra politeness

    def parse(self, response):
        # iterate product cards on the listing page
        for card in response.css("article.product_pod"):
            detail_url = urljoin(response.url, card.css("h3 a::attr(href)").get())
            yield scrapy.Request(detail_url, callback=self.parse_detail)

        # follow pagination
        next_rel = response.css("li.next a::attr(href)").get()
        if next_rel:
            yield scrapy.Request(urljoin(response.url, next_rel), callback=self.parse)

    def parse_detail(self, response):
        name = response.css("div.product_main h1::text").get()
        price_text = response.css("p.price_color::text").get()  # e.g., "£51.77"
        price = float(re.sub(r"[^\d.]", "", price_text)) if price_text else None

        # availability text contains whitespace/newlines → normalize
        avail_bits = response.css("p.instock.availability::text").getall()
        availability = "".join(t.strip() for t in avail_bits).lower()
        in_stock = "in stock" in availability

        # product_id: prefer UPC from table (stable), else fallback to URL tail
        upc = response.xpath("//th[normalize-space()='UPC']/following-sibling::td/text()").get()
        product_id = upc or response.url.rsplit("/", 1)[-1]

        yield {
            "product_id": product_id,
            "name": name,
            "price": price,
            "in_stock": in_stock,
            "url": response.url,
        }