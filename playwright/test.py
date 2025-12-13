from playwright.sync_api import sync_playwright
from pathlib import Path
import time

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

USER_DATA_DIR = Path(r"D:\playwright_profiles\chrome_main")

USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        executable_path=CHROME_PATH,
        user_data_dir=str(USER_DATA_DIR),
        headless=False,
        slow_mo=80,
        args=["--disable-blink-features=AutomationControlled"]
    )

    page = context.new_page()

    page.goto("https://gemini.google.com/app")
   
    page.pause()

