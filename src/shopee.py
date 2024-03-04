import asyncio
import os

import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


def beautiful_scrape(url):
    # Specify the URL you want to scrape
    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (Macintosh; '
                       'Intel Mac OS X 10_15_7) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/118.0.0.0 Safari/537.36'),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    DATA_PATH = ""
    # Use requests to retrieve data from a given URL
    response = requests.get(url, headers=HEADERS)

    print(response.text)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        filename = os.path.join(DATA_PATH, f"beautifulSoup.html")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Downloaded html")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


async def scrape_website(url):
    # Launch the browser in headless mode
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the URL
        await page.goto(url)

        # Get the page content
        content = await page.content()

        # Print the page content
        print(content)

        # Close the browser
        await browser.close()


beautiful_scrape('https://shopee.co.th/shop/655760')
# asyncio.run(scrape_website('https://shopee.co.th/shop/655760'))