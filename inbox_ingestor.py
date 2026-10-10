"""
sIA Inbox & Media Ingestor
Procesa enlaces de TikTok, GitHub, Reddit y artículos web.
Extrae transcripciones de audio, subtítulos y metadatos técnicos
para alimentar el podcast diario de 1 hora.
"""

import sys
import os
import json
import urllib.request
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
INBOX_FILE = BASE_DIR / "inbox_links.txt"
PROCESSED_FILE = BASE_DIR / "inbox_processed.json"

if not INBOX_FILE.exists():
    INBOX_FILE.write_text("# Pega aquí enlaces de TikTok, Reddit, GitHub o artículos web (uno por línea)\n", encoding='utf-8')

def ingest_url(url: str):
    url = url.strip()
    if not url or url.startswith("#"):
        return None

    print(f"\n[INGESTANDO] {url}...")
    
    # 1. TikTok
    if "tiktok.com" in url:
        try:
            import yt_dlp
            COOKIES_FILE = BASE_DIR / "cookies.txt"
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'extract_flat': False,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                    'Referer': 'https://www.tiktok.com/'
                }
            }
            if COOKIES_FILE.exists():
                ydl_opts['cookiefile'] = str(COOKIES_FILE)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "source": "tiktok",
                    "url": url,
                    "title": info.get("title") or info.get("description", "")[:100],
                    "description": info.get("description", ""),
                    "creator": info.get("uploader", ""),
                    "tags": info.get("tags", []),
                    "duration": info.get("duration", 0)
                }
        except Exception as e:
            print(f"[WARN] Error procesando TikTok con yt-dlp: {e}")
            return {"source": "tiktok", "url": url, "error": str(e)}

    # 2. GitHub
    elif "github.com" in url:
        try:
            parts = [p for p in url.split("/") if p]
            if len(parts) >= 4:
                owner, repo = parts[2], parts[3]
                api_url = f"https://api.github.com/repos/{owner}/{repo}"
                req = urllib.request.Request(api_url, headers={'User-Agent': 'sIA-Podcast-Agent'})
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    return {
                        "source": "github",
                        "url": url,
                        "title": f"Repo Open Source: {data.get('name')} ({data.get('full_name')})",
                        "description": data.get("description", ""),
                        "stars": data.get("stargazers_count", 0),
                        "language": data.get("language", "")
                    }
        except Exception as e:
            print(f"[WARN] Error procesando GitHub: {e}")

    # Fallback / General Web
    return {"source": "web", "url": url, "title": url}

def process_inbox():
    if not INBOX_FILE.exists():
        return []
    
    lines = INBOX_FILE.read_text(encoding='utf-8').splitlines()
    valid_urls = [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]
    
    results = []
    for u in valid_urls:
        res = ingest_url(u)
        if res:
            results.append(res)
            
    print(f"\n[OK] {len(results)} enlaces procesados del buzón inbox.")
    return results

if __name__ == '__main__':
    process_inbox()
