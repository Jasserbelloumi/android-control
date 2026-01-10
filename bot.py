import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- إعدادات تليجرام ---
TOKEN = "7665591962:AAFIIe-izSG4rd71Kruf0xmXM9j11IYdHvc"
CHAT_ID = "5653032481"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': text})

def wait_for_user_input(prompt):
    send_msg(prompt)
    print(f"Waiting for: {prompt}")
    
    # الحصول على ID لآخر تحديث موجود حالياً لتجنب قراءة الرسائل القديمة
    start_res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()
    last_update_id = 0
    if start_res['result']:
        last_update_id = start_res['result'][-1]['update_id']

    while True:
        try:
            res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={'offset': last_update_id + 1}).json()
            if res['result']:
                for update in res['result']:
                    if 'message' in update and str(update['message']['chat']['id']) == CHAT_ID:
                        return update['message']['text']
        except Exception as e:
            print(f"Error polling: {e}")
        time.sleep(3)

# --- إعدادات المتصفح ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
mobile_emulation = { "deviceName": "Nexus 5" }
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(options=chrome_options)

try:
    print("Opening Instagram Signup...")
    driver.get("https://www.instagram.com/accounts/emailsignup/")
    time.sleep(8)

    # طلب البريد
    email = wait_for_user_input("🌐 أرسل الآن البريد الإلكتروني الذي تريد استخدامه:")
    
    # محاولة إدخال البيانات (Selectors قد تحتاج تحديث حسب واجهة انستقرام الحالية)
    try:
        driver.find_element(By.NAME, "emailOrPhone").send_keys(email)
        driver.find_element(By.NAME, "fullName").send_keys("Jasser User")
        driver.find_element(By.NAME, "username").send_keys(f"user_{int(time.time())}")
        driver.find_element(By.NAME, "password").send_keys("Pass@Jasser2026")
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
    except Exception as e:
        send_msg(f"⚠️ خطأ أثناء إدخال البيانات: {str(e)[:100]}")

    # طلب الرمز
    otp_code = wait_for_user_input("🔢 وصلك كود التأكيد؟ أرسله هنا:")
    
    # التقاط صورة للتأكد من مكان الرمز
    driver.save_screenshot("step_otp.png")
    with open("step_otp.png", 'rb') as photo:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': photo})

finally:
    driver.quit()
