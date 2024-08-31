from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from moviepy.editor import VideoFileClip

# مسیر پروفایل Firefox خود را اینجا قرار دهید
firefox_profile_path = r'C:\Users\ASUS\AppData\Roaming\Mozilla\Firefox\Profiles\dw6spr7y.default-release'

# پیکربندی FirefoxDriver
firefox_options = Options()
firefox_options.add_argument(f'-profile {firefox_profile_path}')  # استفاده از پروفایل موجود
firefox_options.add_argument("--start-maximized")  # برای باز کردن مرورگر در حالت تمام‌صفحه

# مسیر geckodriver
service = Service('C:\\geckodriver.exe')  # مسیر geckodriver خود را مشخص کنید

try:
    driver = webdriver.Firefox(service=service, options=firefox_options)
except Exception as e:
    print(f"Failed to initialize WebDriver: {e}")
    exit(1)

def random_sleep(min_time=5, max_time=10):
    """خواب تصادفی برای شبیه‌سازی رفتار انسانی"""
    time.sleep(random.uniform(min_time, max_time))

def check_for_dubbed_and_subtitles():
    """بررسی اینکه آیا ویدیو دارای دوبله و زیرنویس است"""
    random_sleep()
    try:
        # پیدا کردن عنصر با XPATH جدید و بررسی متن آن
        th_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[1]/div/div[5]/div[1]/div[2]/div[4]/table/tbody/tr[2]/th"))
        )
        th_text = th_element.text
        if 'دوبله شده' in th_text and 'با زیرنویس' in th_text:
            print("Video is dubbed and has subtitles.")
            return True
        else:
            print("Video does not have the required attributes.")
            return False
    except Exception as e:
        print(f"Failed to find the 'th' element: {e}")
        return False
    
def download_subtitle(url, file_path):
    """دانلود زیرنویس و ذخیره آن در یک فایل"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # بررسی موفقیت آمیز بودن درخواست
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Subtitle downloaded and saved to {file_path}")
    except Exception as e:
        print(f"Failed to")

def download_video(video_url, file_path):
    """دانلود ویدئو و ذخیره آن در یک فایل"""
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()  # بررسی موفقیت آمیز بودن درخواست
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Video downloaded and saved to {file_path}")
    except Exception as e:
        print(f"Failed to download video: {e}")

def convert_video_to_audio(video_path, audio_path):
    """تبدیل ویدیو به فایل صوتی و ذخیره آن در مسیر مشخص شده"""
    try:
        # بارگیری ویدیو
        video_clip = VideoFileClip(video_path)
        # استخراج صوت
        audio_clip = video_clip.audio
        # ذخیره فایل صوتی
        audio_clip.write_audiofile(audio_path)
        print(f"Audio saved to {audio_path}")
    except Exception as e:
        print(f"Failed to convert video to audio: {e}")

def open_links_in_address_bar(links):
    random_sleep()
    
    for link in links:
        print(f"Opening link: {link}")
        driver.get(link)  # باز کردن لینک در همان تب
        
        random_sleep()  # صبر برای بارگذاری صفحه
        if check_for_dubbed_and_subtitles():
            random_sleep()
            try:
                element = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div[1]/div/div[5]/div[2]/div[2]/div/a")
                driver.execute_script("arguments[0].scrollIntoView(true);", element)  # پیمایش به عنصر
                time.sleep(1)  # صبر برای اطمینان از پیمایش
                driver.execute_script("arguments[0].click();", element)  # کلیک با استفاده از جاوااسکریپت
                time.sleep(30)
            
                tracks = driver.find_elements(By.TAG_NAME, 'track')
                random_sleep()
                for track in tracks:
                   label = track.get_attribute('label')
                   if label == "فارسی":
                     subtitle_src = track.get_attribute('src')
                     print(f"Persian subtitle link: {subtitle_src}")
                    
                     subtitle_folder = r'C:\Users\ASUS\Desktop\filimo\subtitles'  # تغییر به مسیر موردنظر
                     os.makedirs(subtitle_folder, exist_ok=True)  # ایجاد پوشه اگر وجود ندارد
                     file_name = f"subtitle_{int(time.time())}.vtt"  # نام فایل زیرنویس
                     file_path = os.path.join(subtitle_folder, file_name)  # مسیر کامل فایل
                     download_subtitle(subtitle_src, file_path)
                     time.sleep(5)
                        
                print("Persian subtitle not found.")
                
                driver.back()
                time.sleep(3)
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(3)
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/div/div[1]/div/div[5]/div[2]/div[1]/div[2]/div/button"))
                    )
                button.click()  # کلیک بر رو
                     
                random_sleep()            
                try:
                    ul_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[1]/div/div[5]/div[2]/div[1]/div[2]/div/ul"))
                    )
                    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
                    if li_elements:  # بررسی اگر li_elements خالی نباشد
                        last_li = li_elements[-1]  # آخرین عنصر li
                        video_link_element = last_li.find_element(By.TAG_NAME, 'a')
                        video_url = video_link_element.get_attribute('href')
                        print(f"Video link: {video_url}")
                        
                        # دانلود ویدئو
                        video_file_name = f"video_{int(time.time())}.mp4"  # نام فایل ویدئو
                        video_file_path = os.path.join(subtitle_folder, video_file_name)  # مسیر کامل فایل
                        download_video(video_url, video_file_path)
                        
                        video_folder = r'C:\Users\ASUS\Desktop\filimo\subtitles'
                        video_file_name = video_file_name
                        video_file_path = os.path.join(video_folder, video_file_name)
                        
                        audio_folder = 'C:/Users/ASUS/Desktop/filimo/subtitles'
                        audio_file_name = f"audio_{int(time.time())}.mp3"   # نام فایل صوتی
                        audio_file_path = f"{audio_folder}/{audio_file_name}"
  
                        convert_video_to_audio(video_file_path, audio_file_path)
                        
                    else:
                        print("No video links found.")
                except Exception as e:
                            print(f"Failed to find or click video link: {e}")  
            except Exception as e:
                print(f"Failed to click element: {e}")  # کلیک بر روی عنصر
                random_sleep()  # صبر برای بارگذاری صفحه
        else:
          print("Skipping this video as it does not meet the criteria.")
          random_sleep()
        
        print(f"Completed opening for link: {link}")
        random_sleep()

def load_links_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Failed to load links from file {filename}: {e}")
        exit(1)

if __name__ == "__main__":
    # خواندن لینک‌ها از فایل
    links = load_links_from_file('dataset.txt')
    random_sleep()  # صبر برای بارگذاری ویدیو
        # جستجو و دانلود لینک زیرنویس فارسی
    open_links_in_address_bar(links)

    
    driver.quit()  # بستن مرورگر پس از اتمام کار