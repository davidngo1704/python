from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def wait_gemini_response(locator, timeout=120, stable_duration=2):
    start = time.time()
    last_text = ""
    stable_since = None

    while time.time() - start < timeout:
        count = locator.count()
        if count == 0:
            time.sleep(0.2)
            continue

        current_text = locator.last.inner_text().strip()

        if current_text and current_text == last_text:
            if stable_since is None:
                stable_since = time.time()
            elif time.time() - stable_since >= stable_duration:
                return current_text
        else:
            last_text = current_text
            stable_since = None

        time.sleep(0.3)

    raise TimeoutError("Gemini chưa generate xong hoặc DOM đổi tiếp")

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

    input_box = page.locator(
        "div[contenteditable='true'][role='textbox']"
    ).first

    input_box.click()

    input_box.type(
        "bitcoin, ETH tin tức mới nhất hôm nay và dự đoán giá trong 7 ngày tới",
        delay=25
    )

    page.keyboard.press("Enter")

    response_blocks = page.locator(
        "structured-content-container .markdown.markdown-main-panel"
    )

    final_answer = wait_gemini_response(response_blocks)

    print("=== Gemini response ===")
    print(final_answer)

    Path("gemini_output.txt").write_text(
        final_answer,
        encoding="utf-8"
    )

  
    context.close()
