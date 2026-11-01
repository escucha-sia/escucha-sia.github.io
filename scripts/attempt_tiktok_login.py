import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SCRATCH_DIR = BASE_DIR / "scratch"
PROFILE_DIR = BASE_DIR / "browser_profile_tiktok"

USER = "sia67486"
PASS = "S05Mayo1984#"

def attempt_login():
    print("Iniciando sesión en TikTok...")
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
            viewport={"width": 1280, "height": 850},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            locale="es-ES",
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)
        
        print("Navegando a formulario de login...")
        page.goto("https://www.tiktok.com/login/phone-or-email/email", wait_until="networkidle", timeout=45000)
        time.sleep(2)
        
        user_input = page.locator("input[name='username']")
        pass_input = page.locator("input[type='password']")
        
        print("Escribiendo usuario...")
        user_input.click()
        user_input.fill("")
        user_input.type(USER, delay=80)
        time.sleep(1)
        
        print("Escribiendo contraseña...")
        pass_input.click()
        pass_input.fill("")
        pass_input.type(PASS, delay=80)
        time.sleep(1)
        
        page.screenshot(path=str(SCRATCH_DIR / "tiktok_step1_filled.png"))
        
        print("Pulsando botón de Iniciar sesión...")
        # Submit button
        submit_btn = page.locator("button[type='submit']")
        submit_btn.click()
        
        # Wait up to 10 seconds to observe transition
        time.sleep(6)
        
        screenshot_after = SCRATCH_DIR / "tiktok_step2_after_click.png"
        page.screenshot(path=str(screenshot_after))
        print(f"Captura guardada en: {screenshot_after}")
        print(f"URL actual: {page.url}")
        print(f"Título: {page.title()}")
        
        # Check if captcha container exists
        captcha = page.locator("#captcha-verify-image, .captcha-verify-container, [id*='captcha'], [class*='captcha']").all()
        if captcha:
            print(f"⚠️ DETECTADO CAPTCHA: {len(captcha)} elementos de verificación")
        else:
            print("No se detectó contenedor evidente de captcha.")
            
        context.close()

if __name__ == "__main__":
    attempt_login()
