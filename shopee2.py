import asyncio
from playwright.async_api import async_playwright

async def scrape_website(url):
    # Launch the browser in headless mode
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the URL
        await page.goto(url)

        # Get the page content
        content = await page.content()
        with open("playwright.html", "w", encoding="utf-8") as f:
            f.write(content)

        # Print the page content
        print(content)

        # Close the browser
        await browser.close()


asyncio.run(scrape_website('https://shopee.co.th/shop/655760'))