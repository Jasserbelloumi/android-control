from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# إعدادات المتصفح ليعمل كأنه هاتف
chrome_options = Options()
chrome_options.add_argument("--headless") # بدون واجهة رسومية ليعمل في GitHub
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
mobile_emulation = { "deviceName": "Nexus 5" }
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(options=chrome_options)

try:
    print("Opening Instagram...")
    driver.get("https://www.instagram.com")
    time.sleep(5) # انتظر التحميل
    
    # التقاط لقطة شاشة
    driver.save_screenshot("insta_check.png")
    print("Screenshot saved as insta_check.png")
    
finally:
    driver.quit()
