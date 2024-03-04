import requests
import os
import time
import glob
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

DATA_PATH = os.path.join("..", "data", "raw")
CATEGORY_FILENAME = "category_page"
PRODUCT_FILENAME = "product_page"
MAIN_URL = "https://www.amazon.com"
CATEGORY_URL = ["https://www.amazon.com/Best-Sellers-Health-Household-Sports-Nutrition-Plant-Protein-Powders/"
                "zgbs/hpc/6973714011/ref=zg_bs_pg_1_hpc?_encoding=UTF8&pg=1",
                "https://www.amazon.com/Best-Sellers-Health-Household-Sports-Nutrition-Plant-Protein-Powders/"
                "zgbs/hpc/6973714011/ref=zg_bs_pg_2_hpc?_encoding=UTF8&pg=2"]
HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; '
                   'Intel Mac OS X 10_15_7) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/118.0.0.0 Safari/537.36'),
    'Accept-Language': 'en-US, en;q=0.5'
}


def download_url(url: str, initial_filename: str, file_id: int):
    while True:
        # Wait before scraping to avoid 429 for too many requests
        pause_time = 3
        print(f"{pause_time}-secs pause before scraping {initial_filename} {file_id} ... ")
        time.sleep(pause_time)
        response = requests.get(url, headers=HEADERS)
        # If the request was successful
        if response.status_code == 200:
            # Save the content to an HTML file
            filename = os.path.join(DATA_PATH, f"{initial_filename}{file_id}.html")
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Downloaded {initial_filename} {file_id}")
            # Increment the page number for the next request
            file_id += 1
            return file_id
        else:
            print(f"Failed to download page {file_id}. Status: {response.status_code}. Proceed to scrape again...")
            continue


def download_category(urls: list):
    page: int = 1
    for url in urls:
        page = download_url(url, CATEGORY_FILENAME, page)


def download_product(path: str, category_file: str):
    pattern = os.path.join(path, 'category_page*.html')
    category_files = glob.glob(pattern)
    product_url_list = []
    for category_path in category_files:
        with open(category_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find all <a> tags with class 'a-link-normal'
        a_tags = soup.find_all('a', {'class': 'a-link-normal', 'tabindex': '-1'})
        for a in a_tags:
            product_url_list.append(MAIN_URL + a.get('href'))
    for i, product_url in enumerate(product_url_list):
        print(f'Scraping {PRODUCT_FILENAME}{i+1}...')
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(product_url)
            html_content = page.content()
        filename = os.path.join(DATA_PATH, f"{PRODUCT_FILENAME}{i+1}.html")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Downloaded {PRODUCT_FILENAME}{i+1}")


def main():
    download_category(CATEGORY_URL)
    download_product(DATA_PATH, CATEGORY_FILENAME)


if __name__ == "__main__":
    main()
