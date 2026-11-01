import sys
import time
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
PROFILE_DIR = BASE_DIR / "browser_profile_tiktok"
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
QR_IMG = SCRATCH_DIR / "tiktok_live_qr.png"
ARTIFACT_DIR = Path(r"C:\Users\c_a_c\.gemini\antigravity\brain\3d3829e3-9423-4249-b4ec-672aaf684c20")

def run():
    print("[*] Iniciando Playwright con ventana interactiva...", flush=True)
    browser_args = {
        "user_data_dir": str(PROFILE_DIR),
        "headless": False,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--window-size=1280,850",
            "--window-position=50,50",
        ],
        "viewport": {"width": 1280, "height": 850},
        "locale": "es-ES",
    }
    
    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(**browser_args, channel="chrome")
            print("[+] Usando Google Chrome nativo", flush=True)
        except Exception as e:
            print(f"[-] Usando Chromium integrado ({e})", flush=True)
            context = p.chromium.launch_persistent_context(**browser_args)
            
        page = context.pages[0] if context.pages else context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        
        print("[*] Navegando a TikTok QR...", flush=True)
        page.goto("https://www.tiktok.com/login/qrcode", wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)
        
        start_time = time.time()
        logged_in = False
        last_screenshot_time = 0
        
        while time.time() - start_time < 360:
            current_url = page.url
            cookies = context.cookies()
            auth_cookies = [c['name'] for c in cookies if c['name'] in ('sessionid', 'sessionid_ss', 'sid_tt', 'uid_tt', 'sid_guard')]
            
            # Chequeo 1: Presencia de cookies maestras de sesión
            if auth_cookies:
                logged_in = True
                print(f"\n[OK] Sesión detectada mediante cookies de autenticación: {auth_cookies}!", flush=True)
                break
                
            # Chequeo 2: Redirección fuera de login
            if "login" not in current_url and "tiktok.com" in current_url:
                logged_in = True
                print(f"\n[OK] Redirección exitosa a: {current_url}!", flush=True)
                break
                
            # Chequeo 3: Detección de avatar o botón de upload
            if page.locator("a[href*='upload'], a[href*='creator-center'], a[href*='tiktokstudio'], div[data-e2e='profile-icon']").count() > 0:
                logged_in = True
                print("\n[OK] Avatar o botón de Upload encontrado!", flush=True)
                break
                
            # Chequeo 4: Si el QR expiró, refrescarlo automáticamente
            refresh_btn = page.locator("text=Refresh, text=Actualizar, text=Recargar, div[class*='refresh']")
            if refresh_btn.count() > 0 and refresh_btn.first.is_visible():
                print("[!] QR expirado detectado, haciendo clic en refrescar...", flush=True)
                try:
                    refresh_btn.first.click()
                    time.sleep(2)
                except Exception:
                    pass
                    
            # Tomar captura cada 4 segundos
            if time.time() - last_screenshot_time > 4:
                try:
                    page.screenshot(path=str(QR_IMG))
                    if ARTIFACT_DIR.exists():
                        shutil.copy2(str(QR_IMG), str(ARTIFACT_DIR / "tiktok_live_qr.png"))
                    last_screenshot_time = time.time()
                except Exception:
                    pass
                    
            time.sleep(2)
            
        if logged_in:
            time.sleep(3)
            context.storage_state(path=str(SESSION_FILE))
            print(f"[SUCCESS] Sesión guardada en: {SESSION_FILE}", flush=True)
            
            # Export netscape cookies
            cookies = context.cookies()
            cookies_txt = BASE_DIR / "cookies.txt"
            with open(cookies_txt, "w", encoding="utf-8") as f:
                f.write("# Netscape HTTP Cookie File\n")
                for c in cookies:
                    domain = c.get("domain", "")
                    flag = "TRUE" if domain.startswith(".") else "FALSE"
                    path = c.get("path", "/")
                    secure = "TRUE" if c.get("secure") else "FALSE"
                    expires = str(int(c.get("expires", -1)))
                    name = c.get("name", "")
                    value = c.get("value", "")
                    f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expires}\t{name}\t{value}\n")
            print(f"[SUCCESS] Cookies exportadas a: {cookies_txt}", flush=True)
            
            # Tomar screenshot final
            page.screenshot(path=str(SCRATCH_DIR / "tiktok_login_success.png"))
            if ARTIFACT_DIR.exists():
                shutil.copy2(str(SCRATCH_DIR / "tiktok_login_success.png"), str(ARTIFACT_DIR / "tiktok_login_success.png"))
        else:
            print("[TIMEOUT] No se completó el login a tiempo.", flush=True)
            
        context.close()
        print("[FIN] Navegador cerrado.", flush=True)

if __name__ == "__main__":
    run()
