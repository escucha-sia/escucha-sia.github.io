import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def main():
    url = "https://www.tiktok.com/@elbecariodemurphy.ia/video/7700662834274913558"
    out_dir = Path("c:/Carlos/noticias_podcast/scratch")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        print("Navegando a:", url)
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(4)
            
            title = await page.title()
            print("Titulo:", title)
            
            # Extraer texto de la descripción o caption
            caption_elem = await page.query_selector('h1, [data-e2e="browse-video-desc"], [data-e2e="video-desc"]')
            if caption_elem:
                text = await caption_elem.inner_text()
                print("Caption:", text)
                
            screenshot_path = out_dir / "elbecariodemurphy_video.png"
            await page.screenshot(path=str(screenshot_path))
            print(f"Screenshot guardado: {screenshot_path}")
            
        except Exception as e:
            print("Error durante inspección:", e)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
