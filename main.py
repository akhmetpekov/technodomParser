import requests
import json
from bs4 import BeautifulSoup
import time
from selenium.webdriver import Chrome

def getData():

    for page_num in range(1, 6):

        # driver = Chrome(executable_path="chromedriver")
        # driver.get("https://www.technodom.kz/astana/catalog/noutbuki-i-komp-jutery/komp-jutery-i-monitory/monitory?page=" + str(page_num))
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        # time.sleep(10)

        headers = {
            "user-agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"
        }

        # url = "https://www.technodom.kz/astana/catalog/noutbuki-i-komp-jutery/komp-jutery-i-monitory/monitory"

        # req = requests.get(url, headers=headers)
        # src = req.text

        with open(f"index{page_num}.html") as file:
            src = file.read()

        # with open(f"index{page_num}.html", "w") as file:
        #     file.write(driver.page_source)

        soup = BeautifulSoup(src, "lxml")
        articles = soup.find_all("li", class_="category-page-list__item")
        print(articles[0])
        item_urls = []

        for item in range(0, 24):
            item_url = "https://www.technodom.kz" + articles[item].find("a", class_="category-page-list__item-link").get("href")
            item_urls.append(item_url)

        product_data_list = []
        count = 0
        for item_url in item_urls:
            req = requests.get(item_url, headers=headers)
            item_name = item_url.split("/")[-1]

            with open(f"data/{item_name}.html", "w") as file:
                file.write(req.text)

            with open(f"data/{item_name}.html") as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")
            try:
                item_title = soup.find("h1").text
            except Exception:
                item_title = "No Title"
            
            try:
                item_photo = "https://www.technodom.kz" + soup.find("div", class_="product-info__body").find("div", class_="product-info__gallery product-gallery").find("li", class_="slide selected").find("img").get("srcset").split("640w")[0]
            except Exception:
                item_photo = "No Photo"
            
            try:
                item_price = soup.find("div", class_="product-info__prices product-prices").find("p").text
            except Exception:
                item_price = "No Price"

            try:
                item_frequency = soup.find("p", text="Частота обновления кадров, Гц").find_parent("div", class_="product-description__item").find("p", class_="Typography product-description__right-text Typography__Body Typography__Body_Small").text
            except Exception:
                item_frequency = "No Frequency"

            try:
                item_resolution = soup.find("p", text="Разрешение экрана").find_parent("div", class_="product-description__item").find("p", class_="Typography product-description__right-text Typography__Body Typography__Body_Small").text
            except Exception:
                item_resolution = "No Resolution"

            try:
                item_href = soup.find("link", rel="canonical").get("href")
            except Exception:
                item_href = "No href"

            product_data_list.append(
                {
                    "name:": item_title,
                    "photo:": item_photo,
                    "price:": item_price,
                    "frequency:": item_frequency,
                    "resolution:": item_resolution,
                    "link:": item_href
                }
            )
            count += 1
            print("added" + str(count) + "item")
        with open("data/products_data.json", "a", encoding="utf-8") as file:
            json.dump(product_data_list, file, indent=4, ensure_ascii=False)
        
getData()
