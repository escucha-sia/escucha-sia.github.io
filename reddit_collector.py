"""
sIA Personal Reddit Collector & Trend Analyzer
Lee el feed RSS privado de Carlos (Unhappy-Thought-4502),
extrae discusiones activas, las clasifica por bloques temáticos
y detecta novedades para el podcast diario de 1 hora.
"""

import sys
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
PROFILE_FILE = BASE_DIR / "user_profile.json"
VAULT_FILE = BASE_DIR / "news_vault.json"

def load_user_profile():
    if PROFILE_FILE.exists():
        return json.loads(PROFILE_FILE.read_text(encoding='utf-8'))
    return {}

def load_news_vault():
    if VAULT_FILE.exists():
        return json.loads(VAULT_FILE.read_text(encoding='utf-8'))
    return {"covered_items": [], "last_run": None}

def save_news_vault(vault):
    VAULT_FILE.write_text(json.dumps(vault, indent=2, ensure_ascii=False), encoding='utf-8')

def fetch_reddit_feed():
    profile = load_user_profile()
    feed_url = profile.get("reddit_feed_url")
    if not feed_url:
        print("[ERR] No se encontró 'reddit_feed_url' en user_profile.json")
        return []

    req = urllib.request.Request(
        feed_url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            xml_data = resp.read()
    except Exception as e:
        print(f"[ERR] Error al conectar con Reddit: {e}")
        return []

    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = root.findall('atom:entry', ns)
    
    vault = load_news_vault()
    already_covered_titles = {item["title"].lower() for item in vault.get("covered_items", [])}
    
    candidates = []
    
    for e in entries:
        title_el = e.find('atom:title', ns)
        cat_el = e.find('atom:category', ns)
        link_el = e.find('atom:link', ns)
        updated_el = e.find('atom:updated', ns)
        
        title = title_el.text.strip() if title_el is not None else ""
        sub = cat_el.get('label') or cat_el.get('term') if cat_el is not None else ""
        link = link_el.get('href') if link_el is not None else ""
        updated = updated_el.text if updated_el is not None else ""
        
        # Check deduplication
        if title.lower() in already_covered_titles:
            continue
            
        # Classify by block
        sub_lower = sub.lower()
        title_lower = title.lower()
        
        category = "general"
        if any(k in sub_lower for k in ["antigravity", "bard", "notebooklm", "artificial", "localllama"]) or any(k in title_lower for k in ["gemini", "llm", "claude", "gpt"]):
            category = "ai_and_agents"
        elif any(k in sub_lower for k in ["sql", "dataengineering", "bigquery", "dbt"]) or any(k in title_lower for k in ["query", "database", "join"]):
            category = "data_engineering"
        elif any(k in sub_lower for k in ["smartglasses", "eink", "calibre", "samsung", "dex", "dreame", "toyota"]):
            category = "hardware_and_wearables"
        elif any(k in sub_lower for k in ["3dprinting", "bambulab", "orcaslicer"]):
            category = "maker_3d"
        elif any(k in sub_lower for k in ["anime", "manhwa", "horrorlit", "j_horror", "swordartonline"]):
            category = "geek_culture"
            
        candidates.append({
            "title": title,
            "subreddit": sub,
            "link": link,
            "category": category,
            "updated": updated
        })
        
    return candidates

def generate_daily_lineup():
    print("=" * 60)
    print("ANALIZANDO FEED PERSONAL DE CARLOS & ARQUITECTANDO PARRILLA")
    print("=" * 60)
    
    candidates = fetch_reddit_feed()
    print(f"\n[OK] Candidatos frescos recolectados de Reddit: {len(candidates)}")
    
    grouped = {}
    for c in candidates:
        cat = c["category"]
        grouped.setdefault(cat, []).append(c)
        
    for cat, items in grouped.items():
        print(f"\n--- Categoría: {cat.upper()} ({len(items)} noticias) ---")
        for it in items[:3]:
            print(f"  • [{it['subreddit']}] {it['title']}")
            
    return grouped

if __name__ == '__main__':
    generate_daily_lineup()
