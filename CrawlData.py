# import requests
# from bs4 import BeautifulSoup

# api_key = '79f614df9711c11bf365c10e000b29b5'

# # url = f'http://api.scraperapi.com/?api_key={api_key}&url=https://www.thegioididong.com/laptop#c=44&o=17&pi=11'
# url= "https://www.thegioididong.com/laptop#c=44&o=17&pi=11"
# # url = "https://fptshop.com.vn/may-tinh-xach-tay"

# # urls = []
# # for i in range(12):
# #     urls.append(base_url + str(i))

# payload = {
#     'api_key': api_key,
#     'url': url,
#     'render': 'true',
#     'timeout': 100000,  # 10 seconds
#     'method': "GET",
#     'headers': "HEADERS"
# }

# # for url in urls:
# response = requests.get('http://api.scraperapi.com', params=payload)
# html_content = response.text

# soup = BeautifulSoup(html_content, 'html.parser')
# laptops = soup.find_all('li', {'class': 'item __cate_44'})

# for laptop in laptops:
#     # print(i = i + 1)
#     # print(laptop)
#     # print(laptop.find_all("data-name"))
#     name = laptop.find('h3').text.strip()
#     price = laptop.find('strong', {'class': 'price'}).text.strip()
#     print(name + ' - ' + price)
#     # break

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

# set up the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)
    
def TheGioiDiDong():
    # chrome_options.add_argument("--headless")  # uncomment this line to run in headless mode
    driver = webdriver.Chrome(options=options)

    # navigate to the website
    url = "https://www.thegioididong.com/laptop#c=44&o=17&pi=10"
    driver.get(url)

    time.sleep(3)

    ps = driver.page_source
    # print(ps)
    soup = BeautifulSoup(ps, 'html.parser')
    laptops = soup.find_all('li', {'class': 'item __cate_44'})

    names_prices = []
    base_link = "https://www.thegioididong.com"
    for laptop in laptops:
        name = laptop.find('h3').text.strip()
        price = laptop.find('strong', {'class': 'price'}).text
        link = laptop.find('a')['href']
        # print(link)
        names_prices.append([name, price, base_link + link])
        # break
        # print(name + ' - ' + price)

    # close the driver
    driver.quit()
    return names_prices
    
def HaNoiComputer():
    names_prices = []
    
    driver = webdriver.Chrome(options=options)
    
    for it in range(20):
        # navigate to the website
        base_url = "https://hacom.vn/laptop/"
        url = base_url + str(it + 1) + "/"
        
        driver.get(url)
        time.sleep(5)

        ps = driver.page_source
        # print(ps)
        soup = BeautifulSoup(ps, 'html.parser')
        laptops = soup.find_all('div', {'class': 'p-info'})
        for laptop in laptops:
            # print(laptop)
            name = laptop.find("h3").text.strip()
            price = laptop.find("span", {"class", "p-price js-get-minPrice"}).text
            link = laptop.find("a")["href"]
            names_prices.append([name, price, "https://hacom.vn" + link])
        
    # close the driver
    driver.quit()
    
    return names_prices    

def FPTShop():
    # chrome_options.add_argument("--headless")  # uncomment this line to run in headless mode
    driver = webdriver.Chrome(options=options)

    # navigate to the website
    url = "https://fptshop.com.vn/may-tinh-xach-tay?sort=ban-chay-nhat&trang=20"
    driver.get(url)

    time.sleep(3)

    ps = driver.page_source
    # print(ps)
    soup = BeautifulSoup(ps, 'html.parser')
    laptops = soup.find_all('div', {'class': 'cdt-product__info'})
    # print(laptops)
    
    names_prices = []
    base_link = "https://fptshop.com.vn"
    for laptop in laptops:
        name = laptop.find('h3').text.strip()
        try:
            # price = laptop.find('div', {'class': 'progress pdiscount2'}).text.strip()
            price = laptop.find('div', {'class': 'progress'}).text.strip()
        except:
            price = laptop.find('div', {'class': 'cdt-product__price'}).text.strip()
        price.replace(" ", "")
        link = laptop.find('a')['href']
        names_prices.append([name, price, base_link + link])

    # close the driver
    driver.quit()
    return names_prices

def main():
    # print(TheGioiDiDong())
    # print(HaNoiComputer())
    # print(FPTShop())
    result = TheGioiDiDong() + HaNoiComputer() + FPTShop()
    for i in result:
        print(i)

if __name__ == "__main__":
    main()