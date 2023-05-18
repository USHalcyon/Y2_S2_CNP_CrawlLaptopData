from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import json

# set up the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)

def TheGioiDiDong(product_type_link, prd_attrs):
    # navigate to the specified website
    driver.get(product_type_link)

    # wait to loading data
    time.sleep(5)          

    # retrieve the HTML source code of the page
    ps = driver.page_source
    
    # parse the HTML
    soup = BeautifulSoup(ps, 'html.parser')
    
    # find all the products on the page that match the specified product attributes
    products = soup.find_all('li', {'class': prd_attrs})

    data_result = []
    base_link = "https://www.thegioididong.com"
    
    for product in products:
        img = product.find('img', {'class': 'thumb'})
        img_src = img.attrs.get('data-src', img.attrs.get('src'))
        # break
        name = product.find('h3').text.strip()
        price = product.find('strong', {'class': 'price'}).text
        link = product.find('a')['href']
        data_result.append(["tgdd", img_src, name, price, base_link + link])
        # break

    return data_result    
  
def HaNoiComputer(base_url, prd_attrs, no_pages):    
    data_result = []
    for it in range(no_pages):
        # navigate to the website
        # base_url = "https://hacom.vn/laptop/"
        url = base_url + str(it + 1) + "/"
        
        driver.get(url)         # Open the website by the url.
        time.sleep(5)           # Wait a second for the website to load enough data.
        
        ps = driver.page_source  
        soup = BeautifulSoup(ps, 'html.parser')
        products = soup.find_all('div', {'class': prd_attrs})    # laptops_tgdd_attrs = 'item __cate_44'
        
        for product in products:
            img = product.find("div", {"class": ['p-img', 'p-img ajax-loading ajax-finished']})
            img_src = img.find("img", {"class": ["lazy", "lazy loaded"]})['data-src']
            
            name = product.find("h3").text.strip()
            price = product.find("span", {"class", "p-price js-get-minPrice"}).text
            link = product.find("a")["href"]
            data_result.append(["hnc", img_src, name, price, "https://hacom.vn" + link])
        # break
        
    return data_result    

def FPTShop(product_type_link, prd_attrs):
    # navigate to the website
    driver.get(product_type_link)

    time.sleep(5)

    ps = driver.page_source
    soup = BeautifulSoup(ps, 'html.parser')
    products = soup.find_all('div', {'class': prd_attrs})
    
    
    data_result = []
    base_link = "https://fptshop.com.vn"
    for product in products:
        img_src = "None"
        name = product.find('h3').text.strip()
        
        try:
            price = product.find('div', {'class': ['price', 'progress']}).text.strip()
            price.replace(" ", "")
        except:
            # price = "None"
            continue
        
        link = product.find('a')['href']
        data_result.append(["FPT", img_src, name, price, base_link + link])

    return data_result

def PhongVu(base_url, prd_attrs, no_pages):    
    
    data_result = []
    for it in range(1, no_pages):
        # navigate to the website
        # base_url = "https://phongvu.vn/c/laptop?page="
        url = base_url + str(it)
        
        driver.get(url)         # Open the website by the url.
        time.sleep(5)           # Wait a second for the website to load enough data.
        
        ps = driver.page_source  
        soup = BeautifulSoup(ps, 'html.parser')
        products = soup.find_all('div', {'class': prd_attrs})  
        
        for product in products:
            img = product.find("div", {"class": 'css-1uzm8bv'})
            img_src = img.find("img")['src']
            name = product.find("h3").text.strip()
            
            try:
                price = product.find("div", {"class", "att-product-detail-latest-price css-tzkko0"}).text
            except:
                # price = product.find("div", {"class", "css-quss1"}).text 
                continue       
            
            link = product.find("a")["href"]
            data_result.append(["phongvu", img_src, name, price, "https://phongvu.vn/" + link])

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
# new
pk_tgdd_url = "https://www.thegioididong.com/chuot-ban-phim#c=9386&o=8&pi=10"
pk_tgdd_attrs = ' item  __cate_86'

PC_tgdd_url = 'https://www.thegioididong.com/may-tinh-de-ban#c=5698&o=7&pi=5'
PC_tgdd_attrs = ' item  __cate_5698'

# HNC parameters
hnc_attrs = 'p-component item loaded'

laptops_hnc_no_pages = 20
laptops_hnc_url = "https://hacom.vn/laptop/"

tablets_hnc_no_pages = 5
tablets_hnc_url = "https://hacom.vn/may-tinh-bang/"

# new
lk_hnc_no_pages = 50
lk_hnc_url = "https://hacom.vn/linh-kien-may-tinh/"

pk_hnc_no_pages = 55
pk_hnc_url = "https://hacom.vn/phim-chuot-gaming-gear/"

PC_workstation_hnc_no_pages = 8
PC_workstation_hnc_url = "https://hacom.vn/pc-workstations/"

PC_hnc_no_pages = 12
PC_hnc_url = "https://hacom.vn/may-tinh-de-ban/"

PC_gmstrm_hnc_no_pages = 5
PC_gmstrm_hnc_url = "https://hacom.vn/pc-gaming-streaming/"


# FPT parameters
laptops_fpt_url = "https://fptshop.com.vn/may-tinh-xach-tay?sort=ban-chay-nhat&trang=20"
laptops_fpt_attrs = ['cdt-product', 'prd-lap', 'product-sale']

mobiles_fpt_url = "https://fptshop.com.vn/dien-thoai?sort=ban-chay-nhat&trang=20"
mobiles_fpt_attrs = ['cdt-product', 'product-sale']

tablets_fpt_url = "https://fptshop.com.vn/may-tinh-bang?sort=ban-chay-nhat&trang=20"
tablets_fpt_attrs = ['cdt-product', 'product-sale']

# new
lk_fpt_url = "https://fptshop.com.vn/linh-kien?sort=ban-chay-nhat"
lk_fpt_attrs = 'product product__item product--absolute'

pk_mouse_fpt_url = "https://fptshop.com.vn/phu-kien/chuot?sort=ban-chay-nhat"
pk_mouse_fpt_attrs = ['product-item product-sale', 'product-item ']

pk_keyboard_fpt_url = "https://fptshop.com.vn/phu-kien/ban-phim?sort=ban-chay-nhat"
pk_keyboard_fpt_attrs = ['product-item product-sale', 'product-item ']

PC_fpt_url = "https://fptshop.com.vn/may-tinh-de-ban?sort=ban-chay-nhat&trang=5"
PC_fpt_attrs = ['cdt-product', 'product-sale']

# Phong Vu parameters
pv_attrs = 'css-13w7uog'

laptops_pv_no_pages = 21
laptops_pv_url = "https://phongvu.vn/c/laptop?page="

lk_pv_no_pages = 51
lk_pv_url = "https://phongvu.vn/c/linh-kien-may-tinh?page="

pk_pv_no_pages = 26
pk_pv_url = "https://phongvu.vn/c/phu-kien-pc?page="

PC_pv_no_pages = 9
PC_pv_url = "https://phongvu.vn/c/pc?page="



def main():
    # Laptop
    laptops_tgdd = TheGioiDiDong(laptops_tgdd_url, laptops_tgdd_attrs)
    laptops_hnc = HaNoiComputer(laptops_hnc_url, hnc_attrs, laptops_hnc_no_pages)
    laptops_fpt = FPTShop(laptops_fpt_url, laptops_fpt_attrs)
    laptops_pv = PhongVu(laptops_pv_url, pv_attrs, laptops_pv_no_pages)
    
    laptops = laptops_tgdd + laptops_hnc + laptops_fpt + laptops_pv
    
    jsonize(laptops, "laptops.json")
    
    # PC
    PCs_tgdd = TheGioiDiDong(PC_tgdd_url, PC_tgdd_attrs)
    PCs_hnc = HaNoiComputer(PC_gmstrm_hnc_url, hnc_attrs ,PC_gmstrm_hnc_no_pages) + HaNoiComputer(PC_workstation_hnc_url, hnc_attrs, PC_workstation_hnc_no_pages) + HaNoiComputer(PC_hnc_url, hnc_attrs, PC_hnc_no_pages)
    PCs_fpt = FPTShop(PC_fpt_url, PC_fpt_attrs)
    PCs_pv = PhongVu(PC_pv_url, pv_attrs, PC_pv_no_pages)
    
    PCs = PCs_tgdd + PCs_hnc + PCs_fpt + PCs_pv
    
    jsonize(PCs, "PCs.json")
    
    # Linh kiện
    LKs_hnc = HaNoiComputer(lk_hnc_url, hnc_attrs, lk_hnc_no_pages)
    LKs_fpt = FPTShop(lk_fpt_url, lk_fpt_attrs)
    LKs_pv = PhongVu(lk_pv_url, pv_attrs, lk_pv_no_pages)
    
    LKs = LKs_hnc + LKs_fpt + LKs_pv 
    
    jsonize(LKs, "LinhKien.json")
    
    # Phụ kiện
    PKs_tgdd = TheGioiDiDong(pk_tgdd_url, pk_tgdd_attrs)
    PKs_hnc = HaNoiComputer(pk_hnc_url, hnc_attrs, pk_hnc_no_pages)
    PKs_fpt = FPTShop(pk_mouse_fpt_url, pk_mouse_fpt_attrs) + FPTShop(pk_keyboard_fpt_url, pk_keyboard_fpt_attrs)
    PKs_pv = PhongVu(pk_pv_url, pv_attrs, pk_pv_no_pages)
    
    PKs = PKs_tgdd + PKs_hnc + PKs_fpt + PKs_pv
    
    jsonize(PKs, "PhuKien.json")
    
    # Mobile
    mobiles_tgdd = TheGioiDiDong(mobiles_tgdd_url, mobiles_tgdd_attrs)
    mobiles_fpt = FPTShop(mobiles_fpt_url, mobiles_fpt_attrs)
    
    mobiles = mobiles_tgdd + mobiles_fpt
    
    jsonize(mobiles, "mobiles.json")
    
    # Tablet
    tablets_tgdd = TheGioiDiDong(tablets_tgdd_url, tablets_tgdd_attrs)
    tablets_hnc = HaNoiComputer(tablets_hnc_url, hnc_attrs, tablets_hnc_no_pages)
    tablets_fpt = FPTShop(tablets_fpt_url, tablets_fpt_attrs)
    
    tablets = tablets_tgdd + tablets_hnc + tablets_fpt
    
    jsonize(tablets, "tablets.json")
    driver.quit()
    

if __name__ == "__main__":
    main()
