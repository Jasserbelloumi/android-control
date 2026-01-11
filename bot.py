import os
import time
import requests
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"
TARGET_EMAIL = "psvuecpi@hi2.in"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': text})

def send_photo(file_path, caption=""):
    with open(file_path, 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': f})

def wait_for_user_input(prompt):
    send_msg(prompt)
    last_update_id = 0
    while True:
        try:
            res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={'offset': last_update_id + 1}).json()
            if res['result']:
                for update in res['result']:
                    last_update_id = update['update_id']
                    if 'message' in update: return update['message']['text']
        except: pass
        time.sleep(3)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]
chrome_options.add_argument(f"user-agent={random.choice(agents)}")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 40)

def run_automation():
    for i in range(5):
        try:
            print(f"Attempt {i+1}: Opening Instagram...")
            driver.get("https://www.instagram.com/accounts/emailsignup/")
            time.sleep(random.randint(15, 25))
            
            if "429" not in driver.title and "isn't working" not in driver.page_source:
                # إدخال البيانات
                email_field = wait.until(EC.element_to_be_clickable((By.NAME, "emailOrPhone")))
                for char in TARGET_EMAIL:
                    email_field.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
                
                driver.find_element(By.NAME, "fullName").send_keys("Jasser " + ''.join(random.choices(string.ascii_letters, k=4)))
                driver.find_element(By.NAME, "username").send_keys("jass_dev_" + ''.join(random.choices(string.digits, k=7)))
                driver.find_element(By.NAME, "password").send_keys("Secure_Pass_2026!")
                
                time.sleep(2)
                driver.find_element(By.XPATH, "//button[@type='submit']").click()
                
                # تاريخ الميلاد
                time.sleep(8)
                try:
                    month = wait.until(EC.presence_of_element_to_be_clickable((By.XPATH, "//select[@title='Month:']")))
                    Select(month).select_by_index(random.randint(1, 11))
                    Select(driver.find_element(By.XPATH, "//select[@title='Day:']")).select_by_index(random.randint(1, 25))
                    Select(driver.find_element(By.XPATH, "//select[@title='Year:']")).select_by_visible_text("1998")
                    driver.find_element(By.XPATH, "//button[text()='Next']").click()
                except: pass
                
                # إرسال لقطة شاشة فوراً بعد إدخال المعلومات (قبل طلب الكود)
                time.sleep(5)
                driver.save_screenshot("before_otp.png")
                send_photo("before_otp.png", "📸 هذه لقطة شاشة بعد إدخال المعلومات. إذا ظهرت خانة الكود، أرسله الآن.")

                # طلب الكود
                otp = wait_for_user_input(f"🔢 نجحت في تجاوز الحظر! تم إدخال {TARGET_EMAIL}\nأرسل كود الـ OTP الآن:")
                
                code_input = wait.until(EC.element_to_be_clickable((By.NAME, "email_confirmation_code")))
                code_input.send_keys(otp)
                time.sleep(2)
                driver.find_element(By.XPATH, "//button[@type='submit']").click()
                
                time.sleep(10)
                driver.save_screenshot("final.png")
                send_photo("final.png", "✅ النتيجة النهائية بعد إدخال الكود.")
                return True
            
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
    return False

run_automation()
driver.quit()
