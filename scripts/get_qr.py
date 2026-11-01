import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
PROFILE_DIR = BASE_DIR / "browser_profile_tiktok"
SCRATCH_DIR = BASE_DIR / "scratch"

def get_qr():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            viewport={"width": 1280, "height": 850},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://www.tiktok.com/login", wait_until="networkidle")
        time.sleep(2)
        
        # Click first button / item in login options
        # In the screenshot, "Use QR code" is the first option
        item = page.locator("text='Use QR code'").or_(page.locator("text='Usar código QR'")).or_(page.locator("a[href*='qrcode']"))
        if item.count() > 0:
            item.first.click()
            time.sleep(3)
        else:
            # Let's find by text contains QR
            qr = page.get_by_text("QR", exact=False)
            if qr.count() > 0:
                qr.first.click()
                time.sleep(3)
            else:
                # Try direct URL
                page.goto("https://www.tiktok.com/login/qrcode", wait_until="networkidle")
                time.sleep(3)
                
        out_path = SCRATCH_DIR / "tiktok_qr_code.png"
        page.screenshot(path=str(out_path))
        print(f"URL: {page.url}")
        print(f"Guardado QR en: {out_path}")
        context.close()

if __name__ == "__main__":
    get_qr()
