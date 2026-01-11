import os
import time
import requests
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': text})

# إعدادات متقدمة لإخفاء الهوية تماماً
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# تغيير الـ User-Agent عشوائياً في كل تشغيل لتضليل أنظمة الحماية
agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]
chrome_options.add_argument(f"user-agent={random.choice(agents)}")

driver = webdriver.Chrome(options=chrome_options)

def try_open_ig(retries=5):
    for i in range(retries):
        try:
            print(f"Attempt {i+1}: Opening Instagram...")
            driver.get("https://www.instagram.com/accounts/emailsignup/")
            time.sleep(random.randint(15, 30)) # تأخير عشوائي طويل لتجاوز 429
            
            if "429" not in driver.title and "isn't working" not in driver.page_source:
                print("✅ Success! Page bypassed the block.")
                return True
            
            print("❌ Still blocked (429). Waiting before retry...")
            time.sleep(60) # الانتظار دقيقة كاملة بين المحاولات لتهدئة السيرفر
        except Exception as e:
            print(f"Error during attempt: {e}")
    return False

if try_open_ig():
    driver.save_screenshot("success.png")
    with open("success.png", 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': "🔥 نجحت في تجاوز الحظر! أرسل لي الخطوة التالية."}, files={'photo': f})
else:
    send_msg("⚠️ للأسف، IP الخاص بـ GitHub محظور بشدة الآن. جرب Push بعد 10 دقائق.")

driver.quit()
