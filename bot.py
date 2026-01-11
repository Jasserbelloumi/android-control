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

# --- إعدادات التحكم ---
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"
TARGET_EMAIL = "psvuecpi@hi2.in"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': text})

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

# --- إعدادات الكمبيوتر العملاق (High-End Desktop) ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080") # دقة شاشة عالية

# User-Agent لجهاز كمبيوتر يعمل بنظام ويندوز 11 ومتصفح كروم حديث
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 35)

# محاكاة عميقة لإخفاء أثر السيرفر
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    print("🚀 محاكاة وضع سطح المكتب (PC Mode)...")
    driver.get("https://www.instagram.com/accounts/emailsignup/")
    time.sleep(15)

    # التحقق من ظهور صفحة الخطأ 429
    if "429" in driver.title or "isn't working" in driver.page_source:
        send_msg("⚠️ خطأ 429 (Desktop). سأحاول تغيير المسار وإعادة التحميل...")
        time.sleep(30)
        driver.refresh()
        time.sleep(10)

    # إدخال البيانات مباشرة (في وضع الكمبيوتر تظهر الحقول فوراً)
    email_field = wait.until(EC.element_to_be_clickable((By.NAME, "emailOrPhone")))
    
    # محاكاة كتابة بشرية سريعة لجهاز "كمبيوتر"
    for char in TARGET_EMAIL:
        email_field.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))

    driver.find_element(By.NAME, "fullName").send_keys("Jasser PC " + ''.join(random.choices(string.ascii_letters, k=3)))
    driver.find_element(By.NAME, "username").send_keys("pc_dev_" + ''.join(random.choices(string.digits, k=7)))
    driver.find_element(By.NAME, "password").send_keys("Secure_PC_2026!")
    
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    print("Main form submitted.")

    # التعامل مع تاريخ الميلاد في وضع سطح المكتب
    try:
        time.sleep(6)
        month = wait.until(EC.presence_of_element_to_be_clickable((By.XPATH, "//select[@title='Month:']")))
        Select(month).select_by_index(random.randint(1, 10))
        Select(driver.find_element(By.XPATH, "//select[@title='Day:']")).select_by_index(random.randint(1, 20))
        Select(driver.find_element(By.XPATH, "//select[@title='Year:']")).select_by_visible_text("1995")
        driver.find_element(By.XPATH, "//button[text()='Next']").click()
    except: pass

    # طلب الرمز
    otp = wait_for_user_input(f"🔢 وضع الكمبيوتر: تم إدخال {TARGET_EMAIL}\nأرسل الكود الآن:")
    
    code_in = wait.until(EC.element_to_be_clickable((By.NAME, "email_confirmation_code")))
    code_in.send_keys(otp)
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    time.sleep(10)
    driver.save_screenshot("pc_final.png")
    with open("pc_final.png", 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': "✅ تم بنجاح عبر وضع سطح المكتب!"}, files={'photo': f})

except Exception as e:
    driver.save_screenshot("pc_error.png")
    with open("pc_error.png", 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': f"❌ خطأ PC: {str(e)[:100]}"}, files={'photo': f})

finally:
    driver.quit()
