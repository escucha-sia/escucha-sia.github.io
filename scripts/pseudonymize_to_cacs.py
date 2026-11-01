import re
from pathlib import Path
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")

def replace_in_file(path: Path, patterns: list):
    if not path.exists():
        return 0
    content = path.read_text(encoding='utf-8')
    orig = content
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    if content != orig:
        path.write_text(content, encoding='utf-8')
        return 1
    return 0

def main():
    print("[*] INICIANDO SANITIZACION DE PRIVACIDAD: Reemplazo a 'cacs'")
    
    PATTERNS = [
        (r'\bCarlos Corona \(sIA\)\b', 'cacs (sIA)'),
        (r'\bCarlos Corona\b', 'cacs'),
        (r'\bCorona, C\., & sIA Editora\b', 'cacs, & sIA Editora'),
        (r'\bCorona, C\.\b', 'cacs'),
    ]
    
    # 1. Archivos principales
    main_files = [
        BASE_DIR / "links.html",
        BASE_DIR / "podcast.xml",
        BASE_DIR / "audio" / "podcast.xml",
        BASE_DIR / "build_magazine.py",
        BASE_DIR / "produce_episode_ninera_prompts.py",
        BASE_DIR / "produce_episode_bambu_reprap.py",
        BASE_DIR / "produce_episode_mullenweg_wpengine.py",
        BASE_DIR / "produce_episode_lakehouse_datamesh.py",
    ]
    
    modified_count = 0
    for f in main_files:
        if replace_in_file(f, PATTERNS):
            print(f"  [+] Sanitizado: {f.name}")
            modified_count += 1
            
    # 2. Vault Obsidian y notas de Reels
    vault_dirs = [
        BASE_DIR / "02_Reels_Shorts",
        Path(r"G:\Mi unidad\sIA_Hub\03_Obsidian_Vault\02_Reels_Shorts")
    ]
    for vd in vault_dirs:
        if vd.exists():
            for md_file in vd.glob("*.md"):
                if replace_in_file(md_file, PATTERNS):
                    print(f"  [+] Sanitizada nota Markdown: {md_file.name}")
                    modified_count += 1

    print(f"\n[OK] Total archivos principales actualizados: {modified_count}")
    
    # 3. Recompilar la revista para propagar a todos los artículos HTML e index.html
    print("\n[*] Recompilando sIA Journal (index.html + articulos/*.html)...")
    res = subprocess.run([sys.executable, str(BASE_DIR / "build_magazine.py")], capture_output=True, text=True)
    if res.returncode == 0:
        print("[OK] Revista sIA Journal e index.html recompilados con autor 'cacs'.")
    else:
        print(f"[!] Error al recompilar revista: {res.stderr}")

if __name__ == "__main__":
    main()
