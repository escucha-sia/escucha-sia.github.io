"""
sIA TikTok Cookies Tester & Validator
Verifica que el archivo cookies.txt sea valido y permita acceder
a los perfiles privados de TikTok (@charly_corona y @x41338).
"""

import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
COOKIES_FILE = BASE_DIR / "cookies.txt"
VENV_PYTHON = BASE_DIR / "venv" / "Scripts" / "python.exe"

def test_cookies():
    print("=" * 60)
    print("VALIDADOR DE COOKIES DE TIKTOK PARA sIA")
    print("=" * 60)

    if not COOKIES_FILE.exists():
        print(f"\n[ALERTA] No se encontró el archivo de cookies en:")
        print(f" -> {COOKIES_FILE}")
        print("\nPara generarlo en 30 segundos:")
        print("1. Abre Chrome o Edge.")
        print("2. Instala la extensión 'Get cookies.txt LOCALLY' o 'Cookie-Editor'.")
        print("3. Entra a www.tiktok.com con tu sesión iniciada.")
        print("4. Haz clic en la extensión y pulsa 'Export' (formato Netscape).")
        print(f"5. Guarda el archivo como 'cookies.txt' en:")
        print(f"   {COOKIES_FILE}")
        return False

    size = COOKIES_FILE.stat().st_size
    print(f"\n[OK] Archivo 'cookies.txt' detectado ({size} bytes).")

    # Probar con @charly_corona y @x41338
    for handle in ["@charly_corona", "@x41338"]:
        url = f"https://www.tiktok.com/{handle}"
        print(f"\n[TEST] Probando acceso autenticado a {handle}...")
        cmd = [
            str(BASE_DIR / "venv" / "Scripts" / "yt-dlp.exe"),
            "--cookies", str(COOKIES_FILE),
            "--dump-json",
            "--playlist-items", "1",
            url
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        if "This user's account is private" in res.stderr:
            print(f"[ERROR] TikTok sigue marcando {handle} como privado. Asegúrate de exportar las cookies con la sesión que tiene acceso.")
        elif res.returncode == 0 or "playlist" in res.stdout or "id" in res.stdout:
            print(f"[ÉXITO] ¡Acceso autenticado conseguido para {handle}!")
        else:
            print(f"[INFO] Resultado:\n{res.stderr[:200]}")

if __name__ == '__main__':
    test_cookies()
