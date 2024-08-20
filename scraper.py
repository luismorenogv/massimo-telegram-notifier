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

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Selenium Stealth
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# URL of desired product
url = config.url

# Desired size
talla_objetivo = config.desired_size

async def revisar_disponibilidad():
    driver.get(url)
    
    # Wait time simulating human behavior
    time.sleep(random.uniform(5, 15))  
    
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Obtain the <ul> container
    contenedor_ul = soup.find('ul', class_='list-clear product-size-selector__ul content-center')
    
    # Ensure the container is found
    if contenedor_ul:
        # Now find all <li> with class 'product-size-selector__li' within the <ul> container
        tallas = contenedor_ul.find_all('li', class_='product-size-selector__li')
        
        for talla in tallas:
            nombre_talla = talla.find('span', class_='product-size-selector-name').text.strip()
            agotado = talla.find('div', {'data-title': 'dev.product.soldOut'})
            
            if nombre_talla == talla_objetivo:
                print(f"Verifying size {nombre_talla}:")
                if agotado:
                    print(f"Size {talla_objetivo} is sold out.")
                else:
                    # Telegram notification
                    mensaje = f"¡Size {talla_objetivo} is available! Buy here: {url}"
                    await bot.send_message(chat_id=CHAT_ID, text=mensaje)
                    print(mensaje)
                    return
    else:
        print("<ul> container not found.")

if __name__ == "__main__":
    asyncio.run(revisar_disponibilidad())
    driver.quit()
