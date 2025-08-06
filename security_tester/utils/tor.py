import requests
from stem import Signal
from stem.control import Controller
from config import Config

def rotate_tor_ip():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(Config.TOR_PASSWORD)
            controller.signal(Signal.NEWNYM)
        return True
    except Exception as e:
        return False

def get_tor_session():
    session = requests.session()
    session.proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    return session
