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

REELS_TO_PUBLISH = [
    {
        "file": BASE_DIR / "reels" / "sIA_Reel_Stupy_11_TV_Boxes_Malware_Videostrong.mp4",
        "caption": "¿Tienes una TV Box barata en tu sala? Google desmanteló una red de 1.3 millones de decodificadores infectados con el backdoor x.cpe instalado desde fábrica. El fabricante Videostrong (MECOOL) usó tu Wi-Fi como proxy para cibercriminales y fue vetado de por vida. Expediente completo en Spotify (sIA Podcast) y sIA Journal. #ciberseguridad #androidtv #mecool #google #malware #seguridadinformatica #hackers #siapodcast"
    },
    {
        "file": BASE_DIR / "reels" / "sIA_Reel_Stupy_12_Knight_Capital_Bug_440M.mp4",
        "caption": "¿Cómo un desarrollador destruyó 440 millones de dólares en 45 minutos por reutilizar una sola variable booleana? En 2012, Knight Capital dominaba el 17% de Wall Street. Un técnico olvidó 1 de 8 servidores y desató un bucle infinito que compraba caro y vendía barato. El post-mortem de DevOps en Spotify y sIA Journal. #programacion #devops #wallstreet #finanzas #bugs #ingenieriadesoftware #trading #siapodcast"
    },
    {
        "file": BASE_DIR / "reels" / "sIA_Reel_Stupy_13_XZ_Utils_Backdoor_500ms.mp4",
        "caption": "¿Cómo un retraso de 500 milisegundos en una terminal salvó al internet entero? Un atacante pasó 2 años ganándose al mantenedor de xz e inyectó un backdoor indetectable en OpenSSH. Andrés Freund notó el micro-lag y frenó el mayor ciberataque de la historia. Escúchalo en Spotify y lee el análisis en sIA Journal. #ciberseguridad #linux #openssh #xzutils #programacion #seguridad #hackers #siapodcast"
    }
]

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

def publish_single_video(page, context, video_path: Path, caption: str):
    print("="*60, flush=True)
    print(f"🎬 PROCESANDO: {video_path.name}", flush=True)
    print("="*60, flush=True)
    
    print("[*] Navegando a TikTok Studio Upload...", flush=True)
    page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
    time.sleep(4)
    
    page.mouse.click(600, 200)
    time.sleep(1)
    
    file_input = page.locator("input[type='file']").first
    print(f"[*] Adjuntando video: {video_path.name} ({video_path.stat().st_size / (1024*1024):.2f} MB)...", flush=True)
    file_input.set_input_files(str(video_path))
    
    print("[*] Esperando que termine la carga del video (20s)...", flush=True)
    time.sleep(18)
    
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
        page.keyboard.type(caption, delay=20)
        time.sleep(2)
    except Exception as e:
        print(f"[!] Aviso al escribir con DraftEditor: {e}. Intentando fill alternativo...", flush=True)
        page.evaluate(f"""() => {{
            const el = document.querySelector('div.public-DraftEditor-content, div[contenteditable="true"]');
            if (el) {{
                el.innerText = `{caption}`;
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        }}""")
        time.sleep(1)
        
    dismiss_modals(page)
    
    step_screen = SCRATCH_DIR / f"ready_to_post_{video_path.stem}.png"
    page.screenshot(path=str(step_screen))
    print(f"[+] Captura con texto guardada en: {step_screen}", flush=True)
    
    page.evaluate("window.scrollTo(0, 1500)")
    time.sleep(1)
    dismiss_modals(page)
    
    post_btn = page.locator("button:has-text('Publicar'), button:has-text('Post')").first
    if post_btn.count() > 0:
        print("[🚀] Haciendo clic en 'Publicar'...", flush=True)
        try:
            post_btn.click(timeout=5000)
        except Exception:
            print("[*] Forzando clic en botón 'Publicar'...", flush=True)
            post_btn.click(force=True)
            
        print("[*] Esperando que TikTok procese la publicación (18s)...", flush=True)
        time.sleep(18)
        dismiss_modals(page)
        
        success_screen = SCRATCH_DIR / f"published_{video_path.stem}.png"
        page.screenshot(path=str(success_screen))
        print(f"🎉 ¡VIDEO PUBLICADO EXITOSAMENTE: {video_path.name}!", flush=True)
        print(f"[+] Captura final guardada en: {success_screen}", flush=True)
        return True
    else:
        print(f"[-] No se encontró botón 'Publicar' visible para {video_path.name}", flush=True)
        return False

def main():
    print("==================================================")
    print("🔥 SUBIDA BATCH DE NUEVOS REELS A TIKTOK")
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
        
        success_count = 0
        for item in REELS_TO_PUBLISH:
            vpath = item["file"]
            caption = item["caption"]
            
            if not vpath.exists():
                print(f"[!] Archivo no encontrado: {vpath}. Omitiendo...", flush=True)
                continue
                
            ok = publish_single_video(page, context, vpath, caption)
            if ok:
                success_count += 1
                print(f"[OK] {vpath.name} subido con éxito.\n", flush=True)
                time.sleep(5)
            else:
                print(f"[FAIL] Error al publicar {vpath.name}.\n", flush=True)
                
        print(f"\n✅ Total videos publicados con éxito: {success_count}/{len(REELS_TO_PUBLISH)}")
        context.storage_state(path=str(SESSION_FILE))
        browser.close()

if __name__ == "__main__":
    main()
