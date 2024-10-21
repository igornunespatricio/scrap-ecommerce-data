# E-commerce Data Scraper

<p align="center">
    <img src="images/scrapy-logo.png" alt="Scrapy Logo" width="200" style="display: inline-block;"/>
    <img src="images/sql-server-logo.png" alt="SQL Server Logo" width="200" style="display: inline-block;"/>
</p>


## Overview
Welcome to the **E-commerce Data Scraper**! This project leverages **Scrapy** to extract valuable data from a test e-commerce website and store it in an on-premises SQL Server database. Whether you're looking to analyze product information or build your own dataset, this scraper is a powerful tool to get you started!

## Features
- Scrapes multiple product categories, including:
  - **Laptops**: [View Link](https://webscraper.io/test-sites/e-commerce/static/computers/laptops)
  - **Tablets**: [View Link](https://webscraper.io/test-sites/e-commerce/static/computers/tablets)
  - **Phones**: [View Link](https://webscraper.io/test-sites/e-commerce/static/phones/touch)
- Saves the extracted data in a structured format directly into an on-premises SQL Server database.

## Database Table
The scraper requires a SQL Server table named `products_bronze` with the following columns:

- **name**: The product name
- **price**: The product price
- **rating**: The product rating
- **reviews**: The number of reviews
- **category**: The product category
- **scraped_at**: The timestamp when the data was scraped

## Requirements
To run this project, ensure you have the following:

- **Python 3.x**
- **Scrapy** library
- **SQL Server** installed on-premises

## Environment Configuration
You'll need to set up an environment file (`.env`) containing the following SQL Server credentials:

```plaintext
SERVER=SERVER_NAME
DATABASE=DATABASE_NAME
USERNAME=USERNAME
PASSWORD=PASSWORD
DRIVER=DRIVER
