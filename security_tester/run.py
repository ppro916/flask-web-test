import argparse
from modules import (
    captcha_bypass,
    tor_proxy_manager,
    email_generator,
    csrf_token_grabber,
    fingerprint_spoof
)
from utils.logger import setup_logger

logger = setup_logger()

MODULES = {
    "captcha": captcha_bypass,
    "tor": tor_proxy_manager,
    "email": email_generator,
    "csrf": csrf_token_grabber,
    "fingerprint": fingerprint_spoof
}

def run_module(module_name, target_url=None):
    try:
        logger.info(f"Starting {module_name} module")
        module = MODULES[module_name]
        result = module.execute(target_url)
        logger.success(f"{module_name} completed: {result}")
        return result
    except KeyError:
        logger.error(f"Invalid module: {module_name}")
    except Exception as e:
        logger.error(f"Module failed: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Security Testing Framework")
    parser.add_argument("--module", required=True, help="Module to execute")
    parser.add_argument("--target", help="Target URL")
    
    args = parser.parse_args()
    run_module(args.module, args.target)
