import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
PROFILE_DIR = BASE_DIR / "browser_profile_tiktok"
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"
PASS = "S05Mayo1984#"

def test():
    with sync_playwright() as p:
        browser_args = {
            "user_data_dir": str(PROFILE_DIR),
            "headless": False,
            "args": ["--disable-blink-features=AutomationControlled"],
            "viewport": {"width": 1280, "height": 850},
            "locale": "es-ES",
        }
        context = p.chromium.launch_persistent_context(**browser_args, channel="chrome")
        page = context.pages[0] if context.pages else context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        
        print("Navegando a TikTok QR...")
        page.goto("https://www.tiktok.com/login/qrcode", wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)
        print("URL actual:", page.url)
        page.screenshot(path=str(SCRATCH_DIR / "step1_current.png"))
        
        # Buscar elementos con texto 'Contraseña'
        elems = page.get_by_text("Contraseña").all()
        print(f"Elementos con texto 'Contraseña': {len(elems)}")
        for idx, el in enumerate(elems):
            try:
                tag = el.evaluate("el => el.tagName")
                cls = el.evaluate("el => el.className")
                text = el.text_content()
                print(f"  [{idx}] Tag: <{tag}> Class: '{cls}' Text: '{text}'")
            except Exception as e:
                print(f"  [{idx}] Error: {e}")
                
        if elems:
            print("Haciendo clic en el último elemento con 'Contraseña' (el más específico)...")
            elems[-1].click()
            time.sleep(3)
            page.screenshot(path=str(SCRATCH_DIR / "step2_after_click_pwd.png"))
            print("Captura guardada en step2_after_click_pwd.png")
            
            # Buscar inputs ahora
            inputs = page.locator("input").all()
            print(f"Inputs encontrados tras click: {len(inputs)}")
            for idx, inp in enumerate(inputs):
                itype = inp.get_attribute("type")
                name = inp.get_attribute("name")
                print(f"  Input [{idx}]: type='{itype}' name='{name}'")
                if itype == "password" or name == "password":
                    print("Escribiendo contraseña...")
                    inp.click()
                    inp.fill("")
                    inp.type(PASS, delay=80)
                    time.sleep(1)
                    
            # Buscar botones
            buttons = page.locator("button").all()
            for b in buttons:
                btext = b.text_content().strip()
                btype = b.get_attribute("type")
                print(f"  Button: type='{btype}' text='{btext}'")
                if btype == "submit" or "Iniciar sesión" in btext or "Siguiente" in btext or "Continuar" in btext:
                    print(f"Pulsando botón: '{btext}'...")
                    b.click()
                    time.sleep(4)
                    break
                    
            page.screenshot(path=str(SCRATCH_DIR / "step3_after_submit.png"))
            print("Captura guardada en step3_after_submit.png")
            print("URL tras submit:", page.url)
            
            # Check cookies
            cookies = context.cookies()
            auth = [c['name'] for c in cookies if 'session' in c['name'].lower() or 'sid' in c['name'].lower()]
            print("Cookies de auth encontradas:", auth)
            if any('session' in a for a in auth):
                context.storage_state(path=str(SESSION_FILE))
                print(f"¡EXITO! Sesión guardada en {SESSION_FILE}")
                
        context.close()

if __name__ == "__main__":
    test()
