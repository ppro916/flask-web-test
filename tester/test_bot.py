import os
import random
import string
import time
import requests
import threading
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from stem import Signal
from stem.control import Controller
from flask import Flask
from dotenv import load_dotenv

# कॉन्फिगरेशन लोड करा
load_dotenv()
from config import *

app = Flask(__name__)

def send_telegram(message):
    """टेलिग्रामवर अलर्ट पाठवा"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        return True
    except Exception as e:
        print(f"✖️ Telegram error: {e}")
        return False

def start_tor():
    """Termux मध्ये TOR सर्व्हर सुरू करा"""
    try:
        # TOR कॉन्फिगरेशन तयार करा
        with open("torrc", "w") as f:
            f.write("SocksPort 9050\nControlPort 9051\nCookieAuthentication 1")
        
        # TOR सर्व्हर सुरू करा
        tor_process = subprocess.Popen(
            ["tor", "-f", "torrc"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✓ TOR सर्व्हर सुरू झाला")
        return tor_process
    except Exception as e:
        print(f"✖️ TOR सुरू करण्यात अयशस्वी: {e}")
        return None

def rotate_tor_ip():
    """TOR IP अॅड्रेस बदला"""
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
        print("✓ TOR IP बदलला")
        time.sleep(5)  # नवीन सर्किट स्थापित होण्याची वाट पहा
        return True
    except Exception as e:
        print(f"✖️ TOR IP बदलण्यात अयशस्वी: {e}")
        return False

def get_tor_ip():
    """सध्याचा TOR IP पत्ता मिळवा"""
    try:
        session = requests.Session()
        session.proxies = {'http': 'socks5://127.0.0.1:9050'}
        return session.get("https://api.ipify.org", timeout=10).text
    except Exception:
        return "IP Unknown"

def generate_credentials():
    """युनिक ईमेल आणि पासवर्ड तयार करा"""
    username = ''.join(random.choices(string.ascii_lowercase, k=8))
    email = f"{username}@securitytest.com"
    password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%', k=12))
    return email, password

def run_attack():
    """मुख्य सुरक्षा चाचणी फंक्शन"""
    print("🔓 सुरक्षा चाचण्या सुरू होत आहेत...")
    while True:
        try:
            # नवीन क्रेडेंशियल्स तयार करा
            email, password = generate_credentials()
            
            # TOR IP बदला
            rotate_tor_ip()
            current_ip = get_tor_ip()
            
            # ब्राउझर कॉन्फिगर करा
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
            
            # युनिक यूजर-एजंट
            user_agent = f"Mozilla/5.0 (Android {random.randint(10,14)}; Mobile; rv:109.0) Gecko/20100101 Firefox/{random.randint(100,120)}.0"
            chrome_options.add_argument(f"user-agent={user_agent}")
            
            # ChromeDriver लाँच करा
            driver = webdriver.Chrome(
                executable_path=CHROMEDRIVER_PATH,
                options=chrome_options
            )
            
            # वेबसाइट लोड करा
            driver.get(REGISTER_URL)
            time.sleep(2)
            
            # फॉर्म भरा
            driver.find_element(By.NAME, "email").send_keys(email)
            driver.find_element(By.NAME, "password").send_keys(password)
            driver.find_element(By.NAME, "otp").send_keys(TEST_OTP)
            
            # सबमिट करा
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(3)
            
            # टेलिग्रामवर निकाल पाठवा
            message = (
                "🔥 नवीन अकाउंट तयार झाले!\n"
                "--------------------------------\n"
                f"📧 ईमेल: `{email}`\n"
                f"🔑 पासवर्ड: `{password}`\n"
                f"🌐 IP: `{current_ip}`\n"
                f"🆔 यूजर-एजंट: `{user_agent}`\n"
                "--------------------------------\n"
                f"⏱️ वेळ: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            send_telegram(message)
            print(f"✓ अकाउंट तयार झाले: {email}")
            
            # ब्राउझर बंद करा
            driver.quit()
            
            # रँडम विलंब
            sleep_time = random.randint(10, ATTACK_INTERVAL)
            print(f"⏳ पुढील चाचणीसाठी {sleep_time} सेकंद थांबा...")
            time.sleep(sleep_time)
            
        except Exception as e:
            error_msg = f"✖️ चाचणी अयशस्वी: {str(e)}"
            print(error_msg)
            send_telegram(error_msg)
            time.sleep(10)

def start_flask_server():
    """Flask वेब सर्व्हर सुरू करा"""
    print(f"🌐 Flask सर्व्हर पोर्ट {FLASK_PORT} वर सुरू होत आहे...")
    app.run(host='0.0.0.0', port=FLASK_PORT)

if __name__ == "__main__":
    print("""
    ███████╗██╗  ██╗██████╗ ███████╗
    ██╔════╝╚██╗██╔╝██╔══██╗██╔════╝
    ███████╗ ╚███╔╝ ██████╔╝███████╗
    ╚════██║ ██╔██╗ ██╔═══╝ ╚════██║
    ███████║██╔╝ ██╗██║     ███████║
    ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝
    सुरक्षा चाचणी प्रणाली
    """)
    
    # TOR सर्व्हर सुरू करा
    tor_process = start_tor()
    time.sleep(10)  # TOR सुरू होण्याची वाट पहा
    
    # Flask सर्व्हर थ्रेडमध्ये सुरू करा
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()
    
    # अटॅक थ्रेड सुरू करा
    attack_thread = threading.Thread(target=run_attack, daemon=True)
    attack_thread.start()
    
    # मुख्य थ्रेडला सक्रिय ठेवा
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\n🛑 सिस्टीम बंद करत आहे...")
        if tor_process:
            tor_process.terminate()
        print("✅ सर्व प्रक्रिया बंद झाल्या")
