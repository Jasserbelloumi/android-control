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
    start_res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()
    last_id = start_res['result'][-1]['update_id'] if start_res['result'] else 0
    while True:
        res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={'offset': last_id + 1}).json()
        if res['result']: return res['result'][-1]['message']['text']
        time.sleep(3)

# --- إعدادات البصمة ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1"
chrome_options.add_argument(f"user-agent={user_agent}")
mobile_emulation = {"deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0}, "userAgent": user_agent}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(options=chrome_options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"})

wait = WebDriverWait(driver, 35)

try:
    # 1. الدخول والمراوغة
    time.sleep(random.randint(20, 40))
    driver.get("https://www.instagram.com/accounts/emailsignup/")
    time.sleep(random.uniform(5, 8))

    # 2. طلب البريد
    email = wait_for_user_input("📧 السكربت شغال! أرسل البريد الآن:")

    # 3. ملء البيانات الأساسية
    wait.until(EC.element_to_be_clickable((By.NAME, "emailOrPhone"))).send_keys(email)
    
    full_name = "Jasser " + ''.join(random.choices(string.ascii_lowercase, k=5))
    username = "jasser_" + ''.join(random.choices(string.digits + string.ascii_lowercase, k=7))
    
    driver.find_element(By.NAME, "fullName").send_keys(full_name)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys("Secure@2026_Test!")
    
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    print("Main form submitted.")

    # 4. خطوة تاريخ الميلاد (المرحلة الجديدة)
    time.sleep(5)
    try:
        # اختيار الشهر واليوم والسنة عشوائياً (عمر أكبر من 18)
        Select(wait.until(EC.presence_of_element_to_be_clickable((By.XPATH, "//select[@title='Month:']")))).select_by_index(random.randint(1, 12))
        Select(wait.until(EC.presence_of_element_to_be_clickable((By.XPATH, "//select[@title='Day:']")))).select_by_index(random.randint(1, 28))
        Select(wait.until(EC.presence_of_element_to_be_clickable((By.XPATH, "//select[@title='Year:']")))).select_by_visible_text(str(random.randint(1990, 2000)))
        
        driver.find_element(By.XPATH, "//button[text()='Next']").click()
        print("Birthday step completed.")
    except:
        send_msg("⚠️ لم تظهر صفحة تاريخ الميلاد، ربما هناك حظر أو صفحة مختلفة.")

    # 5. طلب الرمز
    otp = wait_for_user_input(f"🔢 البيانات المدخلة:\nالاسم: {full_name}\nاليوزر: {username}\n\nأرسل كود الـ OTP الآن:")
    
    # إدخال الرمز
    otp_field = wait.until(EC.presence_of_element_to_be_clickable((By.NAME, "email_confirmation_code")))
    otp_field.send_keys(otp)
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    send_msg("✅ تم إرسال الكود بنجاح. انتظر التحقق...")
    time.sleep(10)
    driver.save_screenshot("final.png")
    with open("final.png", 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID}, files={'photo': f})

except Exception as e:
    send_msg(f"❌ حدث خطأ: {str(e)[:100]}")

finally:
    driver.quit()
