import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

REEL_FILE = BASE_DIR / "reels" / "sIA_Terror_01_Las_Escaleras_Reel.mp4"
CAPTION = "🌲 La regla no escrita que todo rescatista forestal aprende en su primer día: si ves unas escaleras solas en mitad del bosque profundo... JAMÁS subas por ellas. ⚠️ Silencio acústico y distorsiones electromagnéticas. Expediente completo en Spotify (sIA Podcast) y blog en perfil. #terror #misterio #creepypasta #redditparanormal #bosque #leyendasurbanas #searchandrescue #siapodcast"

def dismiss_modals(page):
    """Cierra cualquier modal o overlay que pueda bloquear la interacción."""
    for _ in range(3):
        modals = page.locator("div.TUXModal-overlay, div[data-floating-ui-portal], div[role='dialog']").all()
        dismissed = False
        for m in modals:
            if m.is_visible():
                btn = m.locator("button:has-text('Activar'), button:has-text('Cancelar'), button:has-text('Entendido'), button:has-text('Aceptar'), button[aria-label='close']").first
                if btn.count() > 0 and btn.is_visible():
                    print(f"[*] Cerrando modal interactivo (botón: {btn.text_content().strip()})...", flush=True)
                    btn.click()
                    time.sleep(1)
                    dismissed = True
        if not dismissed:
            page.keyboard.press("Escape")
            break

def main():
    print("==================================================")
    print("🌲 SUBIENDO TERROR #01: LAS ESCALERAS EN EL BOSQUE")
    print("==================================================")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 950},
            locale="es-ES",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("[*] Navegando a TikTok Studio Upload...", flush=True)
        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)
        
        page.mouse.click(600, 200)
        time.sleep(1)
        
        file_input = page.locator("input[type='file']").first
        print(f"[*] Adjuntando video: {REEL_FILE.name} ({REEL_FILE.stat().st_size / (1024*1024):.2f} MB)...", flush=True)
        file_input.set_input_files(str(REEL_FILE))
        
        print("[*] Esperando que termine la carga del video (20s)...", flush=True)
        time.sleep(20)
        
        dismiss_modals(page)
        time.sleep(1)
        
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)
        
        editor = page.locator("div.public-DraftEditor-content, div[contenteditable='true']").first
        print("[*] Localizando editor de leyenda...", flush=True)
        dismiss_modals(page)
        
        try:
            editor.click(force=True, timeout=5000)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            time.sleep(0.5)
            print("[*] Escribiendo texto y hashtags en la leyenda...", flush=True)
            page.keyboard.type(CAPTION, delay=25)
            time.sleep(2)
        except Exception as e:
            print(f"[!] Error DraftEditor: {e}. Usando fallback JS...", flush=True)
            page.evaluate(f"""() => {{
                const el = document.querySelector('div.public-DraftEditor-content, div[contenteditable="true"]');
                if (el) {{
                    el.innerText = `{CAPTION}`;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}""")
            time.sleep(1)
            
        dismiss_modals(page)
        
        step_screen = SCRATCH_DIR / "ready_to_post_terror_01.png"
        page.screenshot(path=str(step_screen))
        print(f"[+] Captura previa guardada en: {step_screen}", flush=True)
        
        page.evaluate("window.scrollTo(0, 1500)")
        time.sleep(1)
        dismiss_modals(page)
        
        post_btn = page.locator("button:has-text('Publicar'), button:has-text('Post')").first
        if post_btn.count() > 0:
            print("[🚀] Haciendo clic en 'Publicar'...", flush=True)
            try:
                post_btn.click(timeout=5000)
            except Exception:
                post_btn.click(force=True)
                
            print("[*] Esperando confirmación de TikTok (18s)...", flush=True)
            time.sleep(18)
            dismiss_modals(page)
            
            success_screen = SCRATCH_DIR / "published_terror_01.png"
            page.screenshot(path=str(success_screen))
            print(f"🎉 ¡VIDEO PUBLICADO EXITOSAMENTE: {REEL_FILE.name}!", flush=True)
            print(f"[+] Captura final guardada en: {success_screen}", flush=True)
        else:
            print("[-] No se encontró botón 'Publicar' visible.", flush=True)
            
        context.storage_state(path=str(SESSION_FILE))
        browser.close()

if __name__ == "__main__":
    main()
