import sys
import os

# Get the path to the parent directory of the current script (the project root)
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

# Append the path of the project root to sys.path
sys.path.append(project_root)

import datetime
from urllib.parse import urlparse
import scrapy

from database_module import Database  # Ensure this is the correct import path


class ProductSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        "https://webscraper.io/test-sites/e-commerce/static/computers/laptops",  # Laptops
        "https://webscraper.io/test-sites/e-commerce/static/computers/tablets",  # Tablets
        "https://webscraper.io/test-sites/e-commerce/static/phones/touch",  # Phones
    ]

    def __init__(self):
        self.db = Database()  # Create an instance of the Database class
        self.db.connect()  # Connect to the database

    def parse(self, response):
        # Extract the category from the URL path
        category = urlparse(response.url).path.split("/")[-1]  # Last part of the URL

        # Capture the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract product information from each product card
        for product in response.css("div.col-md-4.col-xl-4.col-lg-4"):
            product_data = {
                "price": product.css("h4.price.float-end.card-title.pull-right::text")
                .get()
                .strip(),  # Price
                "name": product.css("a.title::text").get().strip(),  # Product name
                "rating": product.css(
                    "p[data-rating]::attr(data-rating)"
                ).get(),  # Rating
                "reviews": product.css("p.review-count.float-end::text")
                .get()
                .strip()
                .split()[0],  # Number of reviews
                "category": category,  # Category extracted from the URL
                "scraped_at": timestamp,  # Date and time of the scrape
            }

            # Insert the raw product data into the bronze table
            self.db.insert_to_bronze(product_data)

            # Optionally, you can also insert into the silver layer (next steps)
            # self.db.insert_product(product_data)  # Assuming you want to process and store in the silver layer

        # Handle pagination
        next_page = response.css("li.page-item a.page-link[rel=next]::attr(href)").get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def closed(self, reason):
        # Close the database connection when the spider is closed
        self.db.close()
