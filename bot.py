import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- إعدادات تليجرام ---
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481" 

def send_to_telegram(image_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': CHAT_ID, 'caption': '📸 تم التقاط الصورة من داخل سيرفرات GitHub بنجاح!'}
            response = requests.post(url, data=data, files=files)
            return response.json()
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

# --- إعدادات المتصفح (Headless) ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
mobile_emulation = { "deviceName": "Nexus 5" }
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(options=chrome_options)

try:
    print("Opening Instagram...")
    driver.get("https://www.instagram.com")
    time.sleep(10) # ننتظر 10 ثوانٍ لضمان تحميل الصفحة
    
    img_name = "insta_check.png"
    driver.save_screenshot(img_name)
    print("Screenshot captured.")
    
    # إرسال الصورة إلى تليجرام
    print("Sending to Telegram...")
    res = send_to_telegram(img_name)
    print(f"Telegram Response: {res}")
    
finally:
    driver.quit()
