import sys
import urllib.request
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    ("elbecario", "https://vt.tiktok.com/ZSpSqj168/"),
    ("estilomovimiento", "https://vt.tiktok.com/ZSpSHo4kK/")
]

for tag, u in urls:
    print(f"\nResolviendo {tag}: {u}")
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            resolved = resp.geturl()
            print("  Resolved:", resolved)
    except Exception as e:
        print("  Error:", e)
