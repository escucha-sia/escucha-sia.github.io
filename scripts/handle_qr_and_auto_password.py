import sys
import time
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

PASS = "S05Mayo1984#"

def run():
    print("[*] Iniciando Playwright con Auto-Password...", flush=True)
    browser_args = {
        "user_data_dir": str(PROFILE_DIR),
        "headless": False,
        "args": ["--disable-blink-features=AutomationControlled"],
        "viewport": {"width": 1280, "height": 850},
        "locale": "es-ES",
    }
    
    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(**browser_args, channel="chrome")
        except Exception:
            context = p.chromium.launch_persistent_context(**browser_args)
            
        page = context.pages[0] if context.pages else context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        
        print("[*] Cargando TikTok QR...", flush=True)
        page.goto("https://www.tiktok.com/login/qrcode", wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)
        
        # Guardar captura inicial del QR
        page.screenshot(path=str(QR_IMG))
        if ARTIFACT_DIR.exists():
            shutil.copy2(str(QR_IMG), str(ARTIFACT_DIR / "tiktok_live_qr.png"))
        print("[+] Codigo QR listo y guardado.", flush=True)
        
        start_time = time.time()
        logged_in = False
        password_handled = False
        
        while time.time() - start_time < 360:
            current_url = page.url
            cookies = context.cookies()
            auth_cookies = [c['name'] for c in cookies if c['name'] in ('sessionid', 'sessionid_ss', 'sid_tt', 'uid_tt')]
            
            # Chequeo 1: Cookies de sesión autenticada
            if auth_cookies:
                logged_in = True
                print(f"[OK] Sesion detectada con cookies: {auth_cookies}!", flush=True)
                break
                
            # Chequeo 2: Redirección fuera de login
            if "login" not in current_url and "tiktok.com" in current_url:
                logged_in = True
                print(f"[OK] Redireccion exitosa a: {current_url}!", flush=True)
                break
                
            # Chequeo 3: Detección de Avatar / Upload
            if page.locator("a[href*='upload'], a[href*='creator-center'], a[href*='tiktokstudio'], div[data-e2e='profile-icon']").count() > 0:
                logged_in = True
                print("[OK] Elemento de usuario logueado detectado!", flush=True)
                break
                
            # Chequeo 4: PANTALLA DE VERIFICACIÓN
            if not password_handled:
                # Ver si el input de contraseña ya está visible directamente
                pwd_input = page.locator("input[type='password'], input[name='password'], input[placeholder*='Contraseña'], input[placeholder*='password']")
                if pwd_input.count() > 0 and pwd_input.first.is_visible():
                    print("[*] Input de contraseña visible en pantalla. Escribiendo contraseña...", flush=True)
                    try:
                        pwd_input.first.click()
                        pwd_input.first.fill("")
                        pwd_input.first.type(PASS, delay=70)
                        time.sleep(1)
                        submit_btn = page.locator("button[type='submit'], button:has-text('Iniciar sesión'), button:has-text('Siguiente'), button:has-text('Continuar'), button:has-text('Verificar')")
                        if submit_btn.count() > 0:
                            print("[*] Clickeando botón de envío...", flush=True)
                            submit_btn.first.click()
                            password_handled = True
                            time.sleep(3)
                            page.screenshot(path=str(SCRATCH_DIR / "screen_after_submit.png"))
                    except Exception as e:
                        print(f"[-] Error llenando password directo: {e}", flush=True)
                else:
                    # Buscar opción de "Contraseña" para desplegar el input
                    pwd_matches = page.get_by_text("Contraseña").all()
                    if pwd_matches:
                        print(f"[!] Detectado texto 'Contraseña' ({len(pwd_matches)} elementos). Clickeando...", flush=True)
                        try:
                            pwd_matches[-1].click(timeout=3000)
                            time.sleep(2)
                            page.screenshot(path=str(SCRATCH_DIR / "screen_after_pwd_click.png"))
                        except Exception as e:
                            try:
                                pwd_matches[0].click(timeout=2000)
                            except Exception:
                                pass
                        
            # Si el QR expiró, refrescarlo
            refresh_btn = page.locator("text=Refresh, text=Actualizar, text=Recargar")
            if refresh_btn.count() > 0 and refresh_btn.first.is_visible():
                print("[!] Refrescando QR expirado...", flush=True)
                try:
                    refresh_btn.first.click()
                    time.sleep(2)
                    page.screenshot(path=str(QR_IMG))
                    if ARTIFACT_DIR.exists():
                        shutil.copy2(str(QR_IMG), str(ARTIFACT_DIR / "tiktok_live_qr.png"))
                except Exception:
                    pass
                    
            time.sleep(2)
            
        if logged_in:
            time.sleep(3)
            context.storage_state(path=str(SESSION_FILE))
            print(f"[SUCCESS] Sesion guardada en: {SESSION_FILE}", flush=True)
            
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
            
            page.screenshot(path=str(SCRATCH_DIR / "tiktok_login_success.png"))
        else:
            print("[TIMEOUT] Sesion no completada.", flush=True)
            
        context.close()
        print("[FIN] Navegador cerrado.", flush=True)

if __name__ == "__main__":
    run()
