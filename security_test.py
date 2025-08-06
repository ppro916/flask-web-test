import os
import random
import string
import time
import requests
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from stem import Signal
from stem.control import Controller
from flask import Flask, request

# कॉन्फिगरेशन (GitHub वर अपलोड करण्यापूर्वी बदला!)
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
FLASK_PORT = 7700  # तुमचा Flask पोर्ट
TEST_OTP = "000000"  # तुमचा बॅकडोर OTP

app = Flask(__name__)

def send_telegram(message):
    """टेलिग्रामवर अलर्ट पाठवा"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})
    except Exception as e:
        print(f"Telegram error: {e}")

def rotate_tor_ip():
    """TOR IP अॅड्रेस बदला"""
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
        print("IP rotated via TOR")
    except Exception as e:
        print(f"TOR rotation failed: {e}")

def generate_credentials():
    """युनिक ईमेल आणि पासवर्ड तयार करा"""
    username = ''.join(random.choices(string.ascii_lowercase, k=8))
    email = f"{username}@securitytest.com"
    password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%', k=12))
    return email, password

def simulate_attack():
    """मुख्य सुरक्षा चाचणी प्रक्रिया"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Android {random.randint(10,14)}; Mobile; rv:109.0) Gecko/20100101 Firefox/118.0")
    
    # Termux मध्ये ChromeDriver सेटअप
    driver = webdriver.Chrome(
        executable_path="/data/data/com.termux/files/home/chromedriver",
        options=chrome_options
    )
    
    try:
        email, password = generate_credentials()
        rotate_tor_ip()  # प्रत्येक वेळी नवीन IP
        
        driver.get(f"http://127.0.0.1:{FLASK_PORT}/register")
        time.sleep(2)
        
        # फॉर्म भरणे
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "otp").send_keys(TEST_OTP)
        
        # सबमिट करणे
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)
        
        # टेलिग्रामवर पाठवणे
        message = f"🔥 नवीन अकाउंट तयार झाले!\n\nEMAIL: {email}\nPASSWORD: {password}\nIP: {current_tor_ip()}"
        send_telegram(message)
        
        print(f"सफलता: {email}")
    except Exception as e:
        error_msg = f"❌ चाचणी अयशस्वी: {str(e)}"
        send_telegram(error_msg)
        print(error_msg)
    finally:
        driver.quit()

def current_tor_ip():
    """सध्याचा TOR IP पत्ता मिळवा"""
    try:
        session = requests.session()
        session.proxies = {'http': 'socks5://127.0.0.1:9050'}
        return session.get("https://api.ipify.org").text
    except:
        return "IP Unknown"

def start_attacks(interval=30):
    """नियमित चाचण्या सुरू करा"""
    while True:
        simulate_attack()
        time.sleep(interval)

@app.route('/')
def home():
    return "Security Testing Server Running"

def start_flask():
    """Flask सर्व्हर चालू करा"""
    app.run(host='0.0.0.0', port=FLASK_PORT)

if __name__ == "__main__":
    print("""
    सुरक्षा चाचणी प्रणाली सुरू होत आहे...
    चरण 1: TOR सर्व्हर (पोर्ट 9050)
    चरण 2: Flask वेबसाइट (पोर्ट 7700)
    चरण 3: सुरक्षा चाचण्या
    """)
    
    # मल्टीथ्रेडिंग वापरून सर्व काही एकाच फाईलमध्ये
    threading.Thread(target=start_flask, daemon=True).start()
    threading.Thread(target=start_attacks, daemon=True).start()
    
    # मुख्य थ्रेड कायम चालू ठेवा
    while True:
        time.sleep(3600)
