from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def wait_until_text_stable(locator, timeout=30, stable_duration=2):
    start_time = time.time()
    last_text = ""
    stable_start = None

    while time.time() - start_time < timeout:
        current_text = locator.inner_text().strip()

        if current_text == last_text and current_text != "":
            if stable_start is None:
                stable_start = time.time()
            elif time.time() - stable_start >= stable_duration:
                return current_text
        else:
            stable_start = None
            last_text = current_text

        time.sleep(0.3)

    raise TimeoutError("Gemini chưa generate xong")

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

