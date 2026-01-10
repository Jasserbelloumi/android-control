import os
import time

def run_command(cmd):
    os.system(f"adb shell {cmd}")

# انتظر قليلاً ليتأكد من تشغيل المحاكي
print("Checking for device...")
time.sleep(5)

# 1. فتح المتصفح والذهاب لإنستقرام
print("Opening Instagram on Browser...")
run_command("am start -a android.intent.action.VIEW -d https://www.instagram.com")

# 2. انتظر التحميل ثم خذ لقطة شاشة للتأكد
time.sleep(10)
print("Taking confirmation screenshot...")
os.system("adb shell screencap -p /sdcard/insta.png")
os.system("adb pull /sdcard/insta.png .")
print("Done! Check insta.png in your repository.")
