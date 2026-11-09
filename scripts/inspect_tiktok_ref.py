import sys
import json
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
SCRATCH_DIR = BASE_DIR / "scratch" / "tiktok_ref_ZSp6Gk34F"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://vt.tiktok.com/ZSp6Gk34F/"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        print(f"Navigating to {URL}...")
        page.goto(URL, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(5000)
        final_url = page.url
        print("Final URL:", final_url)
        title = page.title()
        print("Page title:", title)

        # Extract meta tags and text
        desc = page.evaluate("""() => {
            const metas = Array.from(document.querySelectorAll('meta')).map(m => ({name: m.name || m.getAttribute('property'), content: m.content}));
            const h1 = document.querySelector('[data-e2e="browse-video-desc"], [data-e2e="video-desc"], h1')?.innerText || '';
            const author = document.querySelector('[data-e2e="browse-username"], [data-e2e="video-author-uniqueid"]')?.innerText || '';
            return {metas: metas.filter(m => m.name && m.content), h1, author, bodyText: document.body.innerText.slice(0, 3000)};
        }""")
        print("Author:", desc.get("author"))
        print("H1/Desc:", desc.get("h1"))
        for m in desc.get("metas", []):
            if any(k in str(m["name"]).lower() for k in ["title", "desc", "og:", "twitter:"]):
                print(f"  META {m['name']}: {m['content']}")

        page.screenshot(path=str(SCRATCH_DIR / "page_view.png"))
        browser.close()

    # Also try yt-dlp to download the video and extract frames!
    out_mp4 = SCRATCH_DIR / "ref_video.mp4"
    res = subprocess.run([
        sys.executable, "-m", "yt_dlp",
        "-o", str(out_mp4),
        URL
    ], capture_output=True, text=True)
    print("yt-dlp returncode:", res.returncode)
    if out_mp4.exists():
        print("Downloaded video:", out_mp4, out_mp4.stat().st_size)
        # Extract 6 frames across the video
        for i, sec in enumerate([1, 5, 12, 20, 30, 40]):
            frame_path = SCRATCH_DIR / f"frame_{i+1}_{sec}s.jpg"
            subprocess.run([
                "ffmpeg", "-y", "-ss", str(sec), "-i", str(out_mp4),
                "-vframes", "1", "-q:v", "2", str(frame_path)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    main()
