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
    # الحصول على آخر تحديث لتجنب الرسائل القديمة
    start_res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()
    last_id = start_res['result'][-1]['update_id'] if start_res['result'] else 0
    while True:
        res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={'offset': last_id + 1}).json()
        if res['result']:
            return res['result'][-1]['message']['text']
        time.sleep(3)

# --- إعدادات ايفون كاملة ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# انتحال هوية iPhone 13 Pro
user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
chrome_options.add_argument(f"user-agent={user_agent}")

mobile_emulation = {
    "deviceMetrics": { "width": 390, "height": 844, "pixelRatio": 3.0 },
    "userAgent": user_agent
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

# منع كشف البوت
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)

# حذف أثر الـ WebDriver تماماً
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.navigator.chrome = { runtime: {},  };
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
  """
})

wait = WebDriverWait(driver, 30)

try:
    print("Connecting to Instagram via iPhone Fingerprint...")
    driver.get("https://www.instagram.com/accounts/emailsignup/")
    
    # انتظار عشوائي لتجنب الحظر
    time.sleep(random.randint(7, 12))

    # فحص الصفحة بصورة
    driver.save_screenshot("iphone_check.png")
    with open("iphone_check.png", 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': "📸 واجهة الايفون الحالية:"}, files={'photo': f})

    # طلب البريد
    email = wait_for_user_input("📧 البصمة محملة. أرسل البريد الإلكتروني الآن:")

    # تعبئة البيانات بحذر
    email_input = wait.until(EC.element_to_be_clickable((By.NAME, "emailOrPhone")))
    for char in email: # محاكاة كتابة بشرية حرفاً بحرف
        email_input.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

    driver.find_element(By.NAME, "fullName").send_keys("Jasser iPhone")
    driver.find_element(By.NAME, "username").send_keys(f"j_apple_{int(time.time())}")
    driver.find_element(By.NAME, "password").send_keys("Secure@Apple2026")
    
    time.sleep(2)
    submit = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit.click()
    
    otp = wait_for_user_input("🔢 أرسل كود التأكيد (OTP) الآن:")
    send_msg(f"تم استقبال الكود: {otp}")

except Exception as e:
    send_msg(f"⚠️ خطأ: {str(e)}")
    driver.save_screenshot("error.png")

finally:
    driver.quit()
