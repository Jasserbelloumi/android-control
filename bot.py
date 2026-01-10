import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- إعدادات تليجرام ---
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': text})

def wait_for_user_input(prompt):
    send_msg(prompt)
    start_res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()
    last_id = start_res['result'][-1]['update_id'] if start_res['result'] else 0
    while True:
        res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={'offset': last_id + 1}).json()
        if res['result']:
            return res['result'][-1]['message']['text']
        time.sleep(3)

# --- إعدادات المتصفح ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--lang=en-US") # توحيد اللغة لضمان عمل الـ Selectors
user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
chrome_options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    print("Opening Instagram Signup...")
    driver.get("https://www.instagram.com/accounts/emailsignup/")
    
    # 1. التعامل مع نافذة الـ Cookies (إذا ظهرت)
    try:
        time.sleep(3)
        cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Allow') or contains(text(), 'Accept')]")))
        cookie_btn.click()
        print("Cookies accepted.")
    except:
        print("No cookie dialog found.")

    # 2. طلب البريد
    email = wait_for_user_input("🌐 أرسل لي البريد الإلكتروني الآن:")

    # 3. إدخال البيانات باستخدام محددات أكثر دقة
    try:
        # البحث عن الحقول بواسطة الاسم أو XPATH بديل
        email_field = wait.until(EC.presence_of_element_to_be_clickable((By.NAME, "emailOrPhone")))
        email_field.send_keys(email)
        
        driver.find_element(By.NAME, "fullName").send_keys("Jasser User")
        driver.find_element(By.NAME, "username").send_keys(f"juser_{int(time.time())}")
        driver.find_element(By.NAME, "password").send_keys("Pass@Jasser2026")
        
        time.sleep(2)
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_btn.click()
        print("Form submitted.")
    except Exception as e:
        img_error = "error_field.png"
        driver.save_screenshot(img_error)
        with open(img_error, 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': f"❌ فشل العثور على الحقول. تفحص الصورة:"}, files={'photo': f})
        raise e

    # 4. طلب الرمز
    otp_code = wait_for_user_input("🔢 أرسل كود التأكيد الذي وصلك:")
    
    # هنا تكمل عملية إدخال الرمز بنفس الطريقة...
    send_msg("⌛ جاري معالجة الكود...")

finally:
    driver.quit()
