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
        "file": BASE_DIR / "reels" / "sIA_Reel_Stupy_08_CodeMode_vs_MCP.mp4",
        "caption": "¿RIP MCP? Por qué la IA ya no llama a herramientas una por una: Cloudflare Code Mode, 2,500 endpoints en 1,000 tokens y sandboxes V8. Episodio completo en Spotify (sIA) y blog en perfil. #mcp #agentesia #cloudflare #anthropic #programacion #softwareengineer #siapodcast"
    },
    {
        "file": BASE_DIR / "reels" / "sIA_Reel_Stupy_09_Biqu_Panda_Treat.mp4",
        "caption": "¿Imprimir comida en tu impresora 3D? De pagar 5,000 dólares por una máquina industrial a personalizar galletas en tu cocina por 330 en total. Te explico cómo el BIQU Panda Treat hackeó a Bambu Lab. 🍪✨ #impresion3d #bambulab #pandatreat #bigtreetech #foodtech #reposteria #galletasdecoradas #maker #siapodcast"
    }
]

def dismiss_modals(page):
    """Cierra cualquier modal o overlay que pueda bloquear la interacción."""
    for _ in range(3):
        # 1. Botones dentro de TUXModal
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
            # Intentar tecla Escape por si acaso
            page.keyboard.press("Escape")
            break

def publish_single_video(page, context, video_path: Path, caption: str):
    print("="*60, flush=True)
    print(f"🎬 PROCESANDO: {video_path.name}", flush=True)
    print("="*60, flush=True)
    
    print("[*] Navegando a TikTok Studio Upload...", flush=True)
    page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
    time.sleep(4)
    
    # Descartar tooltips iniciales
    page.mouse.click(600, 200)
    time.sleep(1)
    
    file_input = page.locator("input[type='file']").first
    print(f"[*] Adjuntando video: {video_path.name} ({video_path.stat().st_size / (1024*1024):.2f} MB)...", flush=True)
    file_input.set_input_files(str(video_path))
    
    # Esperar a que el video cargue y el formulario se active
    print("[*] Esperando que termine la carga del video (20s)...", flush=True)
    time.sleep(18)
    
    # Limpiar modales
    dismiss_modals(page)
    time.sleep(1)
    
    # Scroll arriba para editar la leyenda / caption
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(1)
    
    # Localizar editor DraftEditor
    editor = page.locator("div.public-DraftEditor-content, div[contenteditable='true']").first
    print("[*] Localizando editor de leyenda...", flush=True)
    
    # Si aún hay un modal bloqueando, forzar descarte
    dismiss_modals(page)
    
    try:
        editor.click(force=True, timeout=5000)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        time.sleep(0.5)
        print("[*] Escribiendo texto y hashtags en la leyenda...", flush=True)
        page.keyboard.type(caption, delay=25)
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
    
    # Scroll abajo para ubicar botón de publicar
    page.evaluate("window.scrollTo(0, 1500)")
    time.sleep(1)
    
    # Descartar cualquier modal residual antes de hacer clic en Publicar
    dismiss_modals(page)
    
    # Localizar botón 'Publicar'
    post_btn = page.locator("button:has-text('Publicar'), button:has-text('Post')").first
    if post_btn.count() > 0:
        print("[🚀] Haciendo clic en 'Publicar'...", flush=True)
        try:
            post_btn.click(timeout=5000)
        except Exception:
            print("[*] Forzando clic en botón 'Publicar'...", flush=True)
            post_btn.click(force=True)
            
        # Esperar procesamiento y confirmación (18s)
        print("[*] Esperando que TikTok procese la publicación...", flush=True)
        time.sleep(18)
        
        # Descartar modales post-publicación si aparecen (ej. 'Administrar publicaciones', 'Cargar otro video')
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
    print("🔥 SUBIDA AUTOMATIZADA DE REELS A TIKTOK")
    print("==================================================")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 950},
            locale="es-ES"
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        
        uploaded_count = 0
        for item in REELS_TO_PUBLISH:
            success = publish_single_video(page, context, item["file"], item["caption"])
            if success:
                uploaded_count += 1
                print(f"[OK] {item['file'].name} subido con éxito.\n", flush=True)
                time.sleep(8) # Pausa estratégica entre reels
            else:
                print(f"[!] Error al publicar {item['file'].name}.\n", flush=True)
                
        # Guardar estado de sesión actualizado
        context.storage_state(path=str(SESSION_FILE))
        browser.close()
        print(f"\n✅ Total videos publicados con éxito: {uploaded_count}/{len(REELS_TO_PUBLISH)}", flush=True)

if __name__ == "__main__":
    main()
