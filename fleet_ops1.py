import os
import sys
import platform

# --- 1. AUTO-DETECT ENVIRONMENT ---
# Check if we are in Termux (Android)
if "com.termux" in os.environ.get("PREFIX", ""):
    DEVICE_NAME = "Pixel 8a (Mobile)"
    ROOT_DIR = "/storage/emulated/0/pixel8a/unexusi/"
    # Mobile specific config
else:
    DEVICE_NAME = "Laptop (Base)"
    # Update this path to match your actual laptop path exactly
    ROOT_DIR = "/home/sauron/unexusi/" 

# --- IMPORTS ---
try:
    from git import Repo
except ImportError:
    print(f"❌ Critical Error on {DEVICE_NAME}: 'GitPython' is not installed.")
    sys.exit()

# --- THE REST IS STANDARD ---

def check_permissions():
    if not os.path.exists(ROOT_DIR):
        print(f"⚠️  WARNING: Cannot find directory: {ROOT_DIR}")
        print(f"   Current Mode: {DEVICE_NAME}")
        return False
    return True

# ... [Copy the rest of the functions: get_git_status, sync_repo, etc. from v2] ...

def main_dashboard():
    if not check_permissions():
        input("Press Enter to exit...")
        return

    while True:
        os.system('clear') 
        print(f"\n🌍 --- FLEET COMMANDER: {DEVICE_NAME} ---")
        print(f"Scanning Sector: {ROOT_DIR}\n")
        
        # ... [Rest of the main loop is identical] ...
