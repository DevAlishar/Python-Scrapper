import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class Agahi:
    def __init__(self, title, description, price, phone_number=None):
        self.title = title
        self.description = description
        self.price = price
        self.phone_number = phone_number

    def __repr__(self):
        return f'Title: {self.title}\nPrice: {self.price}\nDescription: {self.description}\nPhone Number: {self.phone_number}\n'

def get_Agahi_info(ad_element):
    try:
        title = ad_element.find('h2', class_='kt-post-card__title').text.strip()
        descriptions = ad_element.find_all('div', class_='kt-post-card__description')
        description = descriptions[0].text.strip() if len(descriptions) > 0 else "N/A"
        price = descriptions[1].text.strip() if len(descriptions) > 1 else "N/A"
        phone_number = None
        return Agahi(title, description, price, phone_number)
    except Exception as e:
        print(f"Error extracting Agahi info: {e}")
        return None

def save_to_csv(Agahi):
    with open('Agahi.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Description', 'Phone Number'])
        for ad in Agahi:
            writer.writerow([ad.title, ad.price, ad.description, ad.phone_number])

def main():
    city = input("Hello\nI can show you the information of the last ten ads on the <divar> site \nI actually want to crawl on the divar site!\nIn the first step, give me the required information to do it for you\nEnter city name: ")
    category = input("good\nso , Enter category:")

    try:
        service = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(f"https://divar.ir/s/{city}/{category}")
        
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "kt-post-card__title"))
        )
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        ad_elements = soup.find_all('article', class_='kt-post-card')
        Agahi = []

        for ad_element in ad_elements[:10]:
            ad_info = get_Agahi_info(ad_element)
            if ad_info:
                Agahi.append(ad_info)

        for ad in Agahi:
            print(ad)
        
        save_to_csv(Agahi)
        
        show_next_ads = input("Do you want to see the next 10? (yes/no): ")
        if show_next_ads.lower() == 'yes':
            next_Agahi = []
            for ad_element in ad_elements[10:20]:
                ad_info = get_Agahi_info(ad_element)
                if ad_info:
                    next_Agahi.append(ad_info)
            for ad in next_Agahi:
                print(ad)
            save_to_csv(next_Agahi)
        
        driver.quit()
        
    except Exception as e:
        print(f"Error loading page elements: {e}")

if __name__ == "__main__":
    main()
