import os
import time
import requests
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': text})

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]
chrome_options.add_argument(f"user-agent={random.choice(agents)}")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 40)

def try_open_ig(retries=5):
    for i in range(retries):
        try:
            print(f"Attempt {i+1}: Opening Instagram...")
            driver.get("https://www.instagram.com/accounts/emailsignup/")
            time.sleep(random.randint(20, 40)) # التأخير الذي نجح معك سابقاً
            
            if "429" not in driver.title and "isn't working" not in driver.page_source:
                print("✅ Success! Page bypassed.")
                
                # إدخال البيانات بسرعة (نفس المنطق القديم)
                driver.find_element(By.NAME, "emailOrPhone").send_keys("psvuecpi@hi2.in")
                driver.find_element(By.NAME, "fullName").send_keys("Jasser " + str(random.randint(1,999)))
                driver.find_element(By.NAME, "username").send_keys("jass_v_" + str(random.randint(1000,99999)))
                driver.find_element(By.NAME, "password").send_keys("Pass@2026_Secure")
                driver.find_element(By.XPATH, "//button[@type='submit']").click()
                
                # تجاوز صفحة الميلاد التي ظهرت لك في الصورة
                time.sleep(10)
                try:
                    month = wait.until(EC.presence_of_element_to_be_clickable((By.XPATH, "//select[@title='Month:']")))
                    Select(month).select_by_index(1)
                    Select(driver.find_element(By.XPATH, "//select[@title='Day:']")).select_by_index(5)
                    Select(driver.find_element(By.XPATH, "//select[@title='Year:']")).select_by_visible_text("1995")
                    driver.find_element(By.XPATH, "//button[text()='Next']").click()
                except: pass
                
                time.sleep(5)
                driver.save_screenshot("final.png")
                with open("final.png", 'rb') as f:
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': "🔥 نجحت! تفقد الصورة لترى خانة الكود."}, files={'photo': f})
                return True
            
            print("❌ Still 429. Waiting 60s...")
            time.sleep(60) # تهدئة السيرفر
        except Exception as e:
            print(f"Error: {e}")
    return False

try_open_ig()
driver.quit()
