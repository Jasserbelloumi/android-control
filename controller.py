import os
import time

def screen_click(x, y):
    """النقر على إحداثيات معينة"""
    os.system(f"adb shell input tap {x} {y}")

def send_text(text):
    """كتابة نص برمجياً"""
    os.system(f"adb shell input text '{text}'")

def take_screenshot():
    """أخذ لقطة شاشة وحفظها"""
    os.system("adb shell screencap -p /sdcard/screen.png")
    os.system("adb pull /sdcard/screen.png .")

# تجربة بسيطة
print("جارٍ تنفيذ الأوامر على الهاتف الوهمي...")
send_text("Hello_from_Jasser")
time.sleep(2)
screen_click(500, 500)
