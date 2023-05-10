from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import json

# set up the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)
    
def TheGioiDiDong(product_type_link, prd_attrs):
    driver = webdriver.Chrome(options=options)

    # navigate to the website
    driver.get(product_type_link)

    # wait to loading data
    time.sleep(5)

    ps = driver.page_source
    soup = BeautifulSoup(ps, 'html.parser')
    laptops = soup.find_all('li', {'class': prd_attrs})

    data_result = []
    base_link = "https://www.thegioididong.com"
    
    for laptop in laptops:
        img = laptop.find('img', {'class': 'thumb'})
        img_src = img.attrs.get('data-src', img.attrs.get('src'))
        # break
        name = laptop.find('h3').text.strip()
        price = laptop.find('strong', {'class': 'price'}).text
        link = laptop.find('a')['href']
        data_result.append(["Thế giới di động", img_src, name, price, base_link + link])
        # break

    # close the driver
    driver.quit()
    return data_result    
  
def HaNoiComputer(base_url, prd_attrs, no_pages):    
    driver = webdriver.Chrome(options=options)
    
    data_result = []
    for it in range(no_pages):
        # navigate to the website
        # base_url = "https://hacom.vn/laptop/"
        url = base_url + str(it + 1) + "/"
        
        driver.get(url)
        time.sleep(5)

        ps = driver.page_source
        soup = BeautifulSoup(ps, 'html.parser')
        laptops = soup.find_all('div', {'class': prd_attrs})
        
        for laptop in laptops:
            img = laptop.find("div", {"class": ['p-img', 'p-img ajax-loading ajax-finished']})
            img_src = img.find("img", {"class": ["lazy", "lazy loaded"]})['data-src']
            
            name = laptop.find("h3").text.strip()
            price = laptop.find("span", {"class", "p-price js-get-minPrice"}).text
            link = laptop.find("a")["href"]
            data_result.append(["Hà Nội Computer", img_src, name, price, "https://hacom.vn" + link])
        # break
        
    # close the driver
    driver.quit()
    
    return data_result    

def FPTShop(product_type_link, prd_attrs):
    driver = webdriver.Chrome(options=options)

    # navigate to the website
    driver.get(product_type_link)

    time.sleep(5)

    ps = driver.page_source
    soup = BeautifulSoup(ps, 'html.parser')
    laptops = soup.find_all('div', {'class': prd_attrs})
    
    
    data_result = []
    base_link = "https://fptshop.com.vn"
    for laptop in laptops:
        name = laptop.find('h3').text.strip()
        
        try:
            price = laptop.find('div', {'class': ['price', 'progress']}).text.strip()
            price.replace(" ", "")
        except:
            # price = "None"
            continue
        
        link = laptop.find('a')['href']
        data_result.append(["FPT Shop", "None", name, price, base_link + link])

    # close the driver
    driver.quit()
    return data_result


def jsonize(products, filename):
    json_data = []
    for product in products:
        json_data.append(
            {
                'retailer': product[0],
                'img_url': product[1],
                'name': product[2],
                'price': product[3],
                'url': product[4]
            }
        )
    with open(filename, 'w') as f:
        json.dump(json_data, f)


# TGDD parameters
laptops_tgdd_url = "https://www.thegioididong.com/laptop#c=44&o=17&pi=15"
laptops_tgdd_attrs = 'item __cate_44'

mobiles_tgdd_url = "https://www.thegioididong.com/dtdd#c=42&o=17&pi=10"
mobiles_tgdd_attrs = 'item ajaxed __cate_42'

tablets_tgdd_url = "https://www.thegioididong.com/may-tinh-bang#c=522&o=17&pi=5"
tablets_tgdd_attrs = 'item ajaxed __cate_522'

# HNC parameters
laptops_hnc_no_pages = 20
laptops_hnc_url = "https://hacom.vn/laptop/"
laptops_hnc_attrs = 'p-component item loaded'

tablets_hnc_no_pages = 5
tablets_hnc_url = "https://hacom.vn/may-tinh-bang/"
tablets_hnc_attrs = 'p-component item loaded'

# FPT parameters
laptops_fpt_url = "https://fptshop.com.vn/may-tinh-xach-tay?sort=ban-chay-nhat&trang=20"
laptops_fpt_attrs = ['cdt-product', 'prd-lap', 'product-sale']

mobiles_fpt_url = "https://fptshop.com.vn/dien-thoai?sort=ban-chay-nhat&trang=20"
mobiles_fpt_attrs = ['cdt-product', 'product-sale']

tablets_fpt_url = "https://fptshop.com.vn/may-tinh-bang?sort=ban-chay-nhat&trang=20"
tablets_fpt_attrs = ['cdt-product', 'product-sale']


def main():
    # Laptop
    laptops_tgdd = TheGioiDiDong(laptops_tgdd_url, laptops_tgdd_attrs)
    laptops_hnc = HaNoiComputer(laptops_hnc_url, laptops_hnc_attrs, laptops_hnc_no_pages)
    laptops_fpt = FPTShop(laptops_fpt_url, laptops_fpt_attrs)
    
    laptops = laptops_tgdd + laptops_hnc + laptops_fpt
    
    jsonize(laptops, "laptops.json")
    
    # Mobile
    mobiles_tgdd = TheGioiDiDong(mobiles_tgdd_url, mobiles_tgdd_attrs)
    mobiles_fpt = FPTShop(mobiles_fpt_url, mobiles_fpt_attrs)
    
    mobiles = mobiles_tgdd + mobiles_fpt
    
    jsonize(mobiles, "mobiles.json")
    
    # Tablet
    tablets_tgdd = TheGioiDiDong(tablets_tgdd_url, tablets_tgdd_attrs)
    tablets_hnc = HaNoiComputer(tablets_hnc_url, tablets_hnc_attrs, tablets_hnc_no_pages)
    tablets_fpt = FPTShop(tablets_fpt_url, tablets_fpt_attrs)
    
    tablets = tablets_tgdd + tablets_hnc + tablets_fpt
    
    jsonize(tablets, "tablets.json")


if __name__ == "__main__":
    main()