import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SCRATCH_DIR = BASE_DIR / "scratch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
PROFILE_DIR = BASE_DIR / "browser_profile_tiktok"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

USER = "sia67486"
PASS = "S05Mayo1984#"

def test_login():
    print("Iniciando Playwright para TikTok...")
    with sync_playwright() as p:
        # Launch persistent context
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            channel="chrome", # Try real Chrome if available, fallback to chromium
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
            viewport={"width": 1280, "height": 850},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            locale="es-ES",
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        print("Navegando a TikTok Login...")
        page.goto("https://www.tiktok.com/login/phone-or-email/email", wait_until="domcontentloaded", timeout=45000)
        time.sleep(3)
        
        screenshot_path = SCRATCH_DIR / "tiktok_login_initial.png"
        page.screenshot(path=str(screenshot_path))
        print(f"Captura guardada en: {screenshot_path}")
        print(f"URL actual: {page.url}")
        print(f"Título: {page.title()}")
        
        # Check for username / email input
        inputs = page.locator("input").all()
        print(f"Inputs encontrados: {len(inputs)}")
        for idx, inp in enumerate(inputs):
            name = inp.get_attribute("name") or ""
            placeholder = inp.get_attribute("placeholder") or ""
            inp_type = inp.get_attribute("type") or ""
            print(f"  [{idx}] name='{name}' placeholder='{placeholder}' type='{inp_type}'")
            
        context.close()

if __name__ == "__main__":
    try:
        test_login()
    except Exception as e:
        print("Error con Chrome channel, probando chromium estándar:", e)
        # Fallback to standard chromium
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(PROFILE_DIR),
                headless=True,
                args=["--disable-blink-features=AutomationControlled"],
                viewport={"width": 1280, "height": 850},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            )
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://www.tiktok.com/login/phone-or-email/email", wait_until="domcontentloaded", timeout=45000)
            time.sleep(3)
            page.screenshot(path=str(SCRATCH_DIR / "tiktok_login_initial.png"))
            print(f"URL actual: {page.url}")
            context.close()
