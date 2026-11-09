import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

session_file = Path(r"C:\Carlos\noticias_podcast\tiktok_session.json")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state=str(session_file))
    page = context.new_page()
    page.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded", timeout=40000)
    time.sleep(5)
    page.screenshot(path="C:/Carlos/noticias_podcast/scratch/tiktok_content_check.png")
    print("Screenshot guardado exitosamente.")
    browser.close()
