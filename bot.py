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
        if res['result']: return res['result'][-1]['message']['text']
        time.sleep(3)

# --- إعدادات iPhone 13 Pro العميقة ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--lang=en-US,en;q=0.9")

user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1"
chrome_options.add_argument(f"user-agent={user_agent}")

# محاكاة أبعاد الشاشة وبصمة اللمس
mobile_emulation = {
    "deviceMetrics": { "width": 390, "height": 844, "pixelRatio": 3.0 },
    "userAgent": user_agent
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)

# --- استخدام بروتوكول CDP لتزييف البصمة (WebGL & Navigator) ---
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    # تزييف كرت الشاشة ليكون Apple GPU
    const getParameter = list => {
      const param = list[0];
      if (param === 37445) return 'Apple Inc.';
      if (param === 37446) return 'Apple GPU';
      return list[1];
    };
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
  """
})

wait = WebDriverWait(driver, 35)

try:
    # إضافة "وقت راحة" عشوائي في البداية لتفادي كشف النمط
    wait_start = random.randint(40, 70)
    print(f"Waiting for {wait_start}s to bypass GitHub patterns...")
    time.sleep(wait_start)

    driver.get("https://www.instagram.com/accounts/emailsignup/")
    
    # تأخير عشوائي (Jitter)
    time.sleep(random.uniform(5.5, 10.2))

    driver.save_screenshot("check.png")
    with open("check.png", 'rb') as f:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={'chat_id': CHAT_ID, 'caption': "📱 تم تشغيل البصمة العميقة..."}, files={'photo': f})

    email = wait_for_user_input("📧 أرسل البريد الآن:")

    # إدخال البريد بمحاكاة بشرية (حرف حرف)
    email_field = wait.until(EC.element_to_be_clickable((By.NAME, "emailOrPhone")))
    for char in email:
        email_field.send_keys(char)
        time.sleep(random.uniform(0.1, 0.4))

    # ملء باقي البيانات عشوائياً
    driver.find_element(By.NAME, "fullName").send_keys("Jasser iPhone")
    driver.find_element(By.NAME, "username").send_keys(f"j_ios_{int(time.time())}")
    driver.find_element(By.NAME, "password").send_keys("Secure@Apple2026!")
    
    time.sleep(random.uniform(2, 4))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    otp = wait_for_user_input("🔢 أرسل كود الـ OTP:")
    send_msg(f"تم الاستلام: {otp}")

except Exception as e:
    send_msg(f"⚠️ hخطأ: {str(e)[:60]}")
    driver.save_screenshot("error.png")

finally:
    driver.quit()
