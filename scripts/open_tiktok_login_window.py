import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
PROFILE_DIR = BASE_DIR / "browser_profile_tiktok"
SESSION_FILE = BASE_DIR / "tiktok_session.json"

def open_window():
    print("==================================================")
    print("[*] ABRIENDO VENTANA DE TIKTOK EN TU PANTALLA")
    print("==================================================")
    print("Se abrira una ventana de navegador frente a ti.")
    print("Puedes escanear el Codigo QR con la app de TikTok o iniciar sesion.")
    print("El script detectara automaticamente cuando hayas entrado.")
    print("--------------------------------------------------")
    
    browser_args = {
        "user_data_dir": str(PROFILE_DIR),
        "headless": False,
        "args": ["--disable-blink-features=AutomationControlled"],
        "viewport": {"width": 1280, "height": 850},
        "locale": "es-ES"
    }
    
    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(**browser_args, channel="chrome")
        except Exception as e:
            print(f"Aviso: Chrome nativo no disponible ({e}), usando Chromium integrado...")
            context = p.chromium.launch_persistent_context(**browser_args)
            
        page = context.pages[0] if context.pages else context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        print("Navegando a la pantalla de QR de TikTok...")
        page.goto("https://www.tiktok.com/login/qrcode", wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)
        
        # Guardar captura del QR por si Carlos la necesita consultar en archivo
        qr_capture = BASE_DIR / "scratch" / "tiktok_qr_code.png"
        qr_capture.parent.mkdir(parents=True, exist_ok=True)
        try:
            page.screenshot(path=str(qr_capture))
            print(f"[+] QR visible en ventana emergente y respaldo guardado en: {qr_capture}")
        except Exception:
            pass
            
        print("\n>>> Por favor, enfoca la ventana abierta en tu pantalla o escanea el QR con tu móvil:")
        print("    (TikTok App -> Perfil -> Menú de 3 líneas -> Mi código QR -> Escanear)\n")
        
        # Monitor for login completion
        logged_in = False
        start_time = time.time()
        
        while time.time() - start_time < 360: # 6 minutos de margen
            current_url = page.url
            # Si salimos de login y estamos en la app
            if "login" not in current_url and "tiktok.com" in current_url:
                logged_in = True
                print(f"\n[OK] LOGIN DETECTADO CON EXITO! URL: {current_url}")
                break
                
            # Verificar si aparece el avatar de usuario o botón de upload
            if page.locator("a[href*='upload'], a[href*='creator-center'], a[href*='tiktokstudio'], div[data-e2e='profile-icon'], img[data-e2e='user-avatar']").count() > 0:
                logged_in = True
                print("\n[OK] AVATAR / SESION DETECTADA CON EXITO!")
                break
                
            time.sleep(2)
            
        if logged_in:
            time.sleep(3)
            context.storage_state(path=str(SESSION_FILE))
            print(f"[OK] Sesion guardada permanentemente en: {SESSION_FILE}")
            
            # Export netscape cookies for compatibility
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
            print(f"[OK] Cookies exportadas a: {cookies_txt}")
        else:
            print("[!] Tiempo de espera agotado. Vuelve a ejecutar cuando estés listo.")
            
        context.close()

if __name__ == "__main__":
    open_window()
