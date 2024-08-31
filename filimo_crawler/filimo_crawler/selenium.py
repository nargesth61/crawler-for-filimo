from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# پیکربندی ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # برای باز کردن مرورگر در حالت تمام‌صفحه

# مسیر ChromeDriver
service = Service("C:\Program Files\Google\Chrome\Application")  # مسیر ChromeDriver خود را مشخص کنید
driver = webdriver.Chrome(service=service, options=chrome_options)

def open_links_and_check_network(links):
    for link in links:
        driver.get(link)
        time.sleep(5)  # منتظر بمانید تا صفحه بارگذاری شود
        # در اینجا می‌توانید کدهایی برای بررسی درخواست‌های شبکه اضافه کنید
        # به عنوان مثال: بررسی با استفاده از ابزارهای اضافی
        print(f"Opened {link}")

def load_links_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

if __name__ == "__main__":
    links = load_links_from_file('dataset.txt')
    open_links_and_check_network(links)
    driver.quit()  # بستن مرورگر پس از اتمام کار