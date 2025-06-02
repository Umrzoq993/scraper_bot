from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

BASE_URL = "https://kun.uz"
driver.get(BASE_URL)
time.sleep(2)

# Barcha turkum linklarini olish
category_links = []
soup = BeautifulSoup(driver.page_source, "html.parser")
menu_items = soup.select("ul.header-bottom__list li a.header-bottom__link")

for item in menu_items:
    href = item.get("href")
    if href.startswith("/news/category/"): # type: ignore
        category_links.append(BASE_URL + href) # type: ignore

print(f"🔗 Topilgan kategoriyalar: {len(category_links)} ta")

all_news = []

# Har bir turkumdagi yangiliklarni yig'ish
for category_url in category_links:
    print(f"📂 Turkum: {category_url}")
    driver.get(category_url)
    time.sleep(2)

    for page in range(10):  # Har bir turkumdagi sahifalarni aylantirish
        soup = BeautifulSoup(driver.page_source, "html.parser")
        news_cards = soup.select("a.news-page__item")

        for card in news_cards:
            link = BASE_URL + card.get("href") # type: ignore
            time_tag = card.select_one("div.gray-date p")
            title_tag = card.select_one("h3.news-page__item-title")
            time_text = time_tag.text.strip() if time_tag else ""
            title_text = title_tag.text.strip() if title_tag else ""

            # Har bir yangilik sahifasiga kirish
            try:
                driver.get(link)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "news-inner__content")))
                detail_soup = BeautifulSoup(driver.page_source, "html.parser")

                description = detail_soup.select_one("p.news-inner__content-desc")
                content_div = detail_soup.select_one("div.news-inner__content-page")
                image = detail_soup.select_one("div.news-inner__content-img img")
                tags = detail_soup.select("div.news-inner__tags a.news-inner__tag")

                all_news.append({
                    "category_url": category_url,
                    "title": title_text,
                    "time": time_text,
                    "link": link,
                    "description": description.get_text(strip=True) if description else "",
                    "image_url": image["src"] if image else "",
                    "content": content_div.get_text(" ", strip=True) if content_div else "",
                    "tags": ", ".join([tag.get_text(strip=True) for tag in tags])
                })
            except Exception as e:
                print(f"Sahifani ochishda xatolik: {link}")
                continue

        # Keyingi sahifani yuklash
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "div.point-view__footer button.point-view__footer-btn")
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(2)
        except:
            print("Ko'proq yangiliklar topilmadi.")
            break

driver.quit()

# csv ga saqlash
df = pd.DataFrame(all_news).drop_duplicates(subset=["link"])
df.to_csv("kunuz_by_category_news.csv", index=False, encoding="utf-8-sig")

print("Barcha turkumdagi yangiliklar to'plandi va saqlandi.")
