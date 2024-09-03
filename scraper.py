import asyncio
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import telegram
import time
import random
import config
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Bot telegram configuration
TOKEN = config.TOKEN
CHAT_ID = config.CHAT_ID
bot = telegram.Bot(token=TOKEN)

# Chrome services and browser options
chrome_service = Service(ChromeDriverManager().install())
chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36"
]
for option in options:
    chrome_options.add_argument(option)

async def revisar_disponibilidad(url, desired_size):
    with webdriver.Chrome(service=chrome_service, options=chrome_options) as driver:
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        
        try:
            driver.get(url)
            logging.info(f"Fetching URL: {url}")

            # Explicit wait instead of sleep
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'product-size-selector__ul'))
            )

            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')

            container_ul = soup.find('ul', class_='list-clear product-size-selector__ul content-center')
            title = soup.find('h1', class_='product-name title-l mb-4 ttu')
            if title:
                title = title.text.strip()

            if container_ul:
                sizes = container_ul.find_all('li', class_='product-size-selector__li')
                for size in sizes:
                    size_name = size.find('span', class_='product-size-selector-name').text.strip()
                    if size_name == desired_size:
                        sold_out = size.find('div', {'data-title': 'dev.product.soldOut'})
                        if sold_out:
                            logging.info(f"Size {desired_size} for {title} is sold out.")
                        else:
                            msg = f"¡Size {desired_size} for {title} is available! Buy here: {url}"
                            await bot.send_message(chat_id=CHAT_ID, text=msg)
                            logging.info(f"Sent message: {msg}")
                        return
            else:
                logging.warning("<ul> container not found.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

async def main(items):
    tasks = [revisar_disponibilidad(item[0], item[1]) for item in items]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main(config.items))


