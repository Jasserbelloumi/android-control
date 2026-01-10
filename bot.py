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

def get_last_msg():
    """وظيفة لجلب آخر رسالة أرسلتها أنت للبوت"""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    res = requests.get(url).json()
    if res['result']:
        # نأخذ آخر رسالة من المستخدم
        return res['result'][-1]['message']['text']
    return None

def wait_for_user_input(prompt):
    send_msg(prompt)
    last_id = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()['result'][-1]['update_id']
    print(f"Waiting for: {prompt}")
    while True:
        res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()
        if res['result']:
            new_msg = res['result'][-1]
            if new_msg['update_id'] > last_id:
                return new_msg['message']['text']
        time.sleep(3)

# --- إعدادات المتصفح ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. الدخول لصفحة التسجيل
    driver.get("https://www.instagram.com/accounts/emailsignup/")
    time.sleep(5)

    # 2. طلب البريد الإلكتروني منك عبر تليجرام
    email = wait_for_user_input("🌐 من فضلك أرسل البريد الإلكتروني لإنشاء الحساب:")
    
    # 3. ملء البيانات (مثال مبسط للإدخال)
    # ملاحظة: إنستقرام يغير أسماء العناصر (Selectors) باستمرار، يجب فحصها بدقة
    driver.find_element(By.NAME, "emailOrPhone").send_keys(email)
    driver.find_element(By.NAME, "fullName").send_keys("Jasser Bot")
    driver.find_element(By.NAME, "username").send_keys(f"jasser_bot_{int(time.time())}")
    driver.find_element(By.NAME, "password").send_keys("StrongPass123!")
    
    # النقر على زر التسجيل
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

    # 4. طلب رمز التأكيد (OTP)
    otp_code = wait_for_user_input("🔢 وصلك الرمز؟ أرسله لي الآن:")
    
    # إدخال الرمز
    driver.find_element(By.NAME, "email_confirmation_code").send_keys(otp_code)
    
    driver.save_screenshot("final_step.png")
    send_msg("✅ تمت العملية! تفحص الصورة في GitHub أو اطلبها هنا.")

finally:
    driver.quit()
