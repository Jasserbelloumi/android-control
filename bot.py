import os
import time
import requests
import random
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

# --- إعدادات البصمة الرقمية (iPhone 13 Pro) ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 1. إعدادات اللغة والمنطقة
chrome_options.add_argument("--lang=en-US")

# 2. انتحال هوية iPhone 13 Pro بالكامل
user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
chrome_options.add_argument(f"user-agent={user_agent}")

# 3. إعدادات الشاشة واللمس الخاصة بالايفون
mobile_emulation = {
    "deviceMetrics": { "width": 390, "height": 844, "pixelRatio": 3.0 },
    "userAgent": user_agent
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

# 4. منع كشف الأتمتة (Anti-Detection)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)

# إخفاء خاصية webdriver من المتصفح برمجياً
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

wait = WebDriverWait(driver, 25)

try:
    print("Launching iPhone Emulator...")
    # الدخول لرابط الجوال مباشرة
    driver.get("https://www.instagram.com/accounts/emailsignup/")
    
    # محاولة تجاوز الـ 429 بالانتظار العشوائي
    time.sleep(random.randint(5, 10))

    # التقاط صورة للتأكد من الصفحة (هل تجاوزنا الحظر؟)
    driver.save_screenshot("check_iphone.png")
    with open("check_iphone.png", 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': "📱 فحص بصمة الايفون الجديدة:"}, files={'photo': f})

    # طلب البريد من المستخدم
    email = wait_for_user_input("📧 البصمة جاهزة، أرسل البريد الآن:")

    # إدخال البيانات
    email_field = wait.until(EC.presence_of_element_to_be_clickable((By.NAME, "emailOrPhone")))
    email_field.send_keys(email)
    time.sleep(random.uniform(1.5, 3.2)) # محاكاة سرعة الإنسان في الكتابة
    
    driver.find_element(By.NAME, "fullName").send_keys("Jasser iPhone")
    driver.find_element(By.NAME, "username").send_keys(f"j_apple_{int(time.time())}")
    driver.find_element(By.NAME, "password").send_keys("Apple@2026_Secure")
    
    submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_btn.click()
    
    otp = wait_for_user_input("🔢 تم! أرسل كود التأكيد:")
    send_msg(f"تم استقبال الكود: {otp}")

except Exception as e:
    send_msg(f"❌ وقع خطأ: {str(e)[:50]}")
    driver.save_screenshot("final_error.png")

finally:
    driver.quit()
