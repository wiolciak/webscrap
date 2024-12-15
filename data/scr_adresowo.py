import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import logging
import ssl
import json

CHROME_DRIVER_PATH = r"C:\Users\wmwsz\OneDrive\Desktop\chro\chromedriver.exe"

logging.basicConfig(filename='scraper.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure SSL module is initialized correctly
ssl._create_default_https_context = ssl._create_unverified_context

def get_driver():
    options = Options()
    options.add_argument('--headless') 
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def parse_price(price):
    cleaned_str = price.replace("zł", "").replace(" ", "").strip()
    return int(cleaned_str) if cleaned_str.isdigit() else None

def fetch_adresowo(driver):
    base_url = "https://adresowo.pl/mieszkania/krakow/"
    page = 1
    listings = []
    max_pages = 3  # Limit to 3 pages

    while page <= max_pages:
        url = base_url + "?page=" + str(page)
        driver.get(url)

        # załadowanie wszystkich elementów artykułów na stronie, 30 to czas ładowania
        articles = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-results__item'))
        )
        for article in articles:
            try:
                title_element = article.find_element(By.CSS_SELECTOR, 'div.result-info__header strong')
                title = title_element.text.strip()
            except NoSuchElementException:
                title = 'Brak tytułu'
            try:
                street_element = article.find_element(By.CLASS_NAME, 'result-info__address')
                street = street_element.text.strip() 
            except NoSuchElementException:
                street = 'Brak ulicy'

            try:
                room_element = article.find_element(By.CLASS_NAME, 'result-info__basic')
                b_room_elements = room_element.find_elements(By.TAG_NAME, 'b')
                room = b_room_elements[0].text.strip()
                # room_element = article.find_element(By.CSS_SELECTOR, 'div.result-info__basic b')
                # room = room_element.text.strip()
            except NoSuchElementException:
                room = 'Brak informacji o ilości pokoi'
            try:
                pow_elements = article.find_elements(By.CLASS_NAME, 'result-info__basic')
                pow = None
                for elem in pow_elements:
                    bold_elements = elem.find_elements(By.TAG_NAME, 'b')
                    if bold_elements and "m²" in elem.text:  
                        pow = bold_elements[0].text.strip()
                        break
            except NoSuchElementException:
                pow = 'Brak informacji o powierzchni'

            try:
                price_element = article.find_element(By.CSS_SELECTOR, 'div.result-info__price span')
                price = price_element.text.strip()
            except NoSuchElementException:
                price = 'Brak ceny'
            try:
                price_m2_element = article.find_element(By.CSS_SELECTOR, 'div.result-info__price--per-sqm span')
                price_m2 = price_m2_element.text.strip()
            except NoSuchElementException:
                price_m2 = 'Brak ceny'

            try:
                link_element = article.find_element(By.TAG_NAME, 'a')
                link = link_element.get_attribute('href')
            except NoSuchElementException:
                link = 'Brak linku'

            price_value = parse_price(price)
            if price_value is not None:
                listings.append({
                    'title': title,
                    'street': street,
                    'pow': pow,
                    'room': room,
                    'price': price,
                    'price_m2': price_m2,
                    'link': link,
                    'source': 'Adresowo'
                })
        page += 1
    return listings
def save_to_json(data, filename='listings.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def json_to_csv(input_filename='listings.json', output_filename='listings.csv'):

    with open(input_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    df['pow'] = pd.to_numeric(df['pow'], errors='coerce')  # zamienia na liczby z błędami na NaN 
    df['room'] = pd.to_numeric(df['room'], errors='coerce')
    df['price'] = pd.to_numeric(df['price'].replace(' zł', '').str.replace(' ', ''), errors='coerce')
    df['price_m2'] = pd.to_numeric(df['price_m2'].replace(' zł/m²', '').str.replace(' ', ''), errors='coerce')

    # Zapis do pliku CSV
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')

    print(f"Dane zapisano do pliku {output_filename}.")


if __name__ == "__main__":
    driver = get_driver()
    try:
        adresowo_listings = fetch_adresowo(driver)
        all_listings =  adresowo_listings
        print(f'Znaleziono {len(all_listings)} ogłoszeń.')
        save_to_json(all_listings)
        print('Dane zapisane do pliku listings.json.')
        json_to_csv()
        print('Dane przekształcono i zapisano do pliku listings.csv.')
    finally:
        driver.quit()