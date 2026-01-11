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

# --- إعدادات تليجرام ---
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': text})

def wait_for_user_input(prompt):
    send_msg(prompt)
    last_id = 0
    while True:
        try:
            res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={'offset': last_id + 1}).json()
            if res['result']:
                for update in res['result']:
                    last_id = update['update_id']
                    if 'message' in update: return update['message']['text']
        except: pass
        time.sleep(3)

# --- إعدادات البصمة (iPhone 13 Pro Max) ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.7 Mobile/15E148 Safari/604.1"
chrome_options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 30)

try:
    print("Step 1: Accessing Instagram...")
    driver.get("https://www.instagram.com/accounts/emailsignup/")
    time.sleep(12)

    # التحقق من وجود واجهة الهاتف (كما في صورتك الثانية) والتحويل للبريد
    try:
        email_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign up with email')]")))
        email_btn.click()
        print("Switched to Email Sign up mode.")
        time.sleep(3)
    except:
        print("Already on email field or button not found.")

    # إدخال البريد المحدد تلقائياً
    target_email = "psvuecpi@hi2.in"
    email_field = wait.until(EC.element_to_be_clickable((By.NAME, "emailOrPhone")))
    for char in target_email:
        email_field.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

    # تعبئة البيانات العشوائية
    driver.find_element(By.NAME, "fullName").send_keys("Jasser " + ''.join(random.choices(string.ascii_letters, k=4)))
    driver.find_element(By.NAME, "username").send_keys("jass_" + ''.join(random.choices(string.digits, k=8)))
    driver.find_element(By.NAME, "password").send_keys("Pass@2026_Secure")
    
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # مرحلة تاريخ الميلاد
    try:
        time.sleep(6)
        month_sel = wait.until(EC.presence_of_element_to_be_clickable((By.XPATH, "//select[@title='Month:']")))
        Select(month_sel).select_by_index(random.randint(1, 11))
        Select(driver.find_element(By.XPATH, "//select[@title='Day:']")).select_by_index(random.randint(1, 25))
        Select(driver.find_element(By.XPATH, "//select[@title='Year:']")).select_by_visible_text("1999")
        driver.find_element(By.XPATH, "//button[text()='Next']").click()
    except: pass

    # طلب الكود من تليجرام
    otp = wait_for_user_input(f"🔢 تم إدخال {target_email}\nأرسل كود التأكيد (OTP) الآن:")
    
    code_input = wait.until(EC.element_to_be_clickable((By.NAME, "email_confirmation_code")))
    code_input.send_keys(otp)
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    time.sleep(10)
    driver.save_screenshot("result.png")
    with open("result.png", 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})

except Exception as e:
    driver.save_screenshot("crash_report.png")
    with open("crash_report.png", 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': f"❌ تعطل: {str(e)[:100]}"}, files={'photo': f})

finally:
    driver.quit()
