#!/usr/bin/env python3
"""
upload_reel_to_tiktok.py - Uploader Modular y Determinista a TikTok Studio
Permite publicar cualquier video reel vertical de sIA usando la sesión persistente de Playwright.
Uso:
  python upload_reel_to_tiktok.py --video reels/mi_video.mp4 --caption "Texto del post con #hashtags"
"""

import sys
import time
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

def dismiss_modals(page):
    for _ in range(4):
        turn_on_btn = page.locator("button:has-text('Turn on'), button:has-text('Activar')").first
        if turn_on_btn.count() > 0 and turn_on_btn.is_visible():
            turn_on_btn.click()
            time.sleep(1)

        modals = page.locator("div.TUXModal-overlay, div[data-floating-ui-portal], div[role='dialog']").all()
        dismissed = False
        for m in modals:
            if m.is_visible():
                btn = m.locator("button:has-text('Turn on'), button:has-text('Activar'), button:has-text('Cancel'), button:has-text('Cancelar'), button:has-text('Entendido'), button:has-text('Aceptar'), button[aria-label='close']").first
                if btn.count() > 0 and btn.is_visible():
                    btn.click()
                    time.sleep(1)
                    dismissed = True
        if not dismissed:
            page.keyboard.press("Escape")
            break

def upload_video(video_path: Path, caption: str, dry_run: bool = False):
    print("=======================================================")
    print(f"🚀 INICIANDO SUBIDA A TIKTOK STUDIO: {video_path.name}")
    print(f"   Tamaño: {video_path.stat().st_size / (1024*1024):.2f} MB")
    print(f"   Modo Dry Run: {dry_run}")
    print("=======================================================")

    if not SESSION_FILE.exists():
        print(f"❌ Error: No se encontró {SESSION_FILE}")
        return False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 900}
        )
        page = context.new_page()

        print("[*] Navegando a TikTok Studio Upload...")
        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)
        page.mouse.click(600, 200)
        time.sleep(1)

        file_input = page.locator("input[type='file']").first
        file_input.set_input_files(str(video_path))

        print("[*] Subiendo archivo y esperando procesamiento...")
        time.sleep(30)
        dismiss_modals(page)

        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)

        # Inset caption
        editor = page.locator("div.public-DraftEditor-content, div[contenteditable='true']").first
        try:
            editor.click(force=True, timeout=5000)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            time.sleep(0.5)
            page.keyboard.type(caption, delay=15)
            time.sleep(2)
        except Exception:
            page.evaluate(f"""() => {{
                const el = document.querySelector("div.public-DraftEditor-content, div[contenteditable='true']");
                if (el) {{
                    el.innerText = `{caption}`;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}""")
            time.sleep(2)

        dismiss_modals(page)
        time.sleep(2)

        screenshot_ready = SCRATCH_DIR / f"ready_to_post_{video_path.stem}.png"
        page.screenshot(path=str(screenshot_ready))
        print(f"[*] Screenshot capturado: {screenshot_ready}")

        if dry_run:
            print("🛑 Modo Dry Run activo: No se hace clic en Publicar.")
            browser.close()
            return True

        # Scroll to bottom to reveal Post button
        print("[*] Haciendo scroll al final del formulario...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        dismiss_modals(page)

        post_btn = page.locator("div.btn-post button, button:has-text('Publicar'), button:has-text('Post')").last
        if post_btn.is_visible():
            post_btn.click(force=True)
            print("[+] ¡Clic en Publicar realizado con éxito!")
            time.sleep(3)
        else:
            print("[-] Intentando selector alternativo de publicación...")
            btn_alt = page.locator("button[data-e2e='post_video_button'], button.btn-post").first
            if btn_alt.is_visible():
                btn_alt.click(force=True)
                print("[+] ¡Clic en Publicar alternativo realizado!")
                time.sleep(3)

        # Manejar modal de confirmación ("Continue to post? We're still checking..." -> "Post now")
        for attempt in range(8):
            post_now = page.locator("button:has-text('Post now'), button:has-text('Publicar ahora')").first
            if post_now.count() > 0 and post_now.is_visible():
                print("[+] Detectado modal 'Post now'. Confirmando publicación inmediata...")
                post_now.click(force=True)
                time.sleep(3)
                break
            time.sleep(1)

        print("[*] Esperando a que TikTok procese la publicación...")
        time.sleep(10)
        screenshot_after = SCRATCH_DIR / f"after_post_{video_path.stem}.png"
        page.screenshot(path=str(screenshot_after))
        print(f"[*] Screenshot tras publicación: {screenshot_after}")
        browser.close()
        print("✓ Sesión de subida completada.")
        return True

def main():
    parser = argparse.ArgumentParser(description="TikTok Studio Video Uploader")
    parser.add_argument("--video", required=True, help="Ruta al video MP4")
    parser.add_argument("--caption", required=True, help="Caption del post")
    parser.add_argument("--dry-run", action="store_true", help="Detenerse antes de pulsar Publicar")
    args = parser.parse_args()

    video_path = Path(args.video)
    if not video_path.is_absolute():
        video_path = BASE_DIR / video_path

    if not video_path.exists():
        print(f"❌ Error: El archivo {video_path} no existe.")
        sys.exit(1)

    success = upload_video(video_path, args.caption, dry_run=args.dry_run)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
