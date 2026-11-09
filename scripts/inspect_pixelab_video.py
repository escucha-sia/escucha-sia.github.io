import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def inspect_reference_video():
    url = "https://www.tiktok.com/@pixelabsolucionesc/video/7705832579525659905"
    out_dir = Path("c:/Carlos/noticias_podcast/scratch")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        print("Navegando al video de Pixelab:", url)
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=35000)
            await asyncio.sleep(5)
            
            # Tomar screenshot inicial
            await page.screenshot(path=str(out_dir / "pixelab_frame_1.png"))
            print("Capturado frame 1")
            
            # Esperar 4 segundos para capturar animación en movimiento
            await asyncio.sleep(4)
            await page.screenshot(path=str(out_dir / "pixelab_frame_2.png"))
            print("Capturado frame 2")
            
            title = await page.title()
            print("Título:", title)
        except Exception as e:
            print("Error inspeccionando:", e)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_reference_video())
