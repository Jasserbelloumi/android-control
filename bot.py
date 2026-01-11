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
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 40)

try:
    print("🚀 استكمال العملية من صفحة تاريخ الميلاد...")
    driver.get("https://www.instagram.com/accounts/emailsignup/")
    time.sleep(15)

    # 1. إدخال البيانات الأولية (إذا لم تكن مسجلة)
    try:
        email_f = wait.until(EC.element_to_be_clickable((By.NAME, "emailOrPhone")))
        email_f.send_keys(TARGET_EMAIL)
        driver.find_element(By.NAME, "fullName").send_keys("Jasser " + ''.join(random.choices(string.ascii_letters, k=4)))
        driver.find_element(By.NAME, "username").send_keys("jass_v_" + ''.join(random.choices(string.digits, k=7)))
        driver.find_element(By.NAME, "password").send_keys("Secure_2026_!")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)
    except: pass

    # 2. التعامل مع صفحة تاريخ الميلاد (الموجودة في الصورة)
    try:
        print("🎂 ضبط تاريخ الميلاد...")
        # انتظار تحميل القوائم المنسدلة
        month = wait.until(EC.presence_of_element_to_be_clickable((By.XPATH, "//select[@title='Month:']")))
        Select(month).select_by_index(random.randint(1, 10))
        Select(driver.find_element(By.XPATH, "//select[@title='Day:']")).select_by_index(random.randint(1, 20))
        Select(driver.find_element(By.XPATH, "//select[@title='Year:']")).select_by_visible_text("1995")
        
        # الضغط على Next
        driver.find_element(By.XPATH, "//button[text()='Next']").click()
        print("✅ تم الضغط على Next في صفحة الميلاد.")
        time.sleep(8)
    except Exception as e:
        print(f"Birthday page error: {e}")

    # 3. إرسال لقطة شاشة لخانة الكود
    driver.save_screenshot("otp_step.png")
    send_photo("otp_step.png", "📸 السكربت الآن في صفحة الكود. تفقد بريدك وأرسل الرمز هنا.")

    # 4. انتظار الكود من تليجرام
    otp = wait_for_user_input("🔢 أرسل كود الـ OTP الآن:")
    
    code_input = wait.until(EC.element_to_be_clickable((By.NAME, "email_confirmation_code")))
    code_input.send_keys(otp)
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    time.sleep(12)
    driver.save_screenshot("final_result.png")
    send_photo("final_result.png", "✅ النتيجة النهائية. هل تم إنشاء الحساب؟")

except Exception as e:
    driver.save_screenshot("error.png")
    send_photo("error.png", f"❌ تعطل السكربت: {str(e)[:100]}")

finally:
    driver.quit()
