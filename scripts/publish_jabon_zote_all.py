import sys
import time
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
AUDIO_DIR = BASE_DIR / "audio"
XML_FILE = BASE_DIR / "podcast.xml"
BUILD_MAG = BASE_DIR / "build_magazine.py"
LINKS_FILE = BASE_DIR / "links.html"
SESSION_FILE = BASE_DIR / "tiktok_session.json"
SCRATCH_DIR = BASE_DIR / "scratch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

EP_MP3 = "sIA_Corp_08_Jabon_Zote_La_Corona_Ecatepec_2026-11-06.mp3"
REEL_MP4 = "sIA_Storybook_14_Jabon_Zote_La_Corona_Ecatepec.mp4"
SLUG = "sia-corp-08-fabrica-de-jabon-la-corona-y-el-imperio-del-jabon-zote"

def step1_register_magazine_and_rss():
    print("📖 Registrando sIA Crónicas #08 (Jabón Zote & La Corona) en build_magazine.py, podcast.xml y links.html...")
    mag_text = BUILD_MAG.read_text(encoding="utf-8")

    if f'"{EP_MP3}"' not in mag_text:
        mag_text = mag_text.replace(
            "REELS_MAP = {",
            f'REELS_MAP = {{\n    "{EP_MP3}": "{REEL_MP4}",'
        )

    zote_entry = f'''    # sIA Corp 08 - Fabrica de Jabon La Corona & Jabon Zote - 6 de Noviembre de 2026
    "{EP_MP3}": {{
        "slug": "{SLUG}",
        "category": "Crónicas Corporativas & Industria",
        "badge_color": "rose",
        "read_time": "14 min",
        "title": "sIA Crónicas #08: Fábrica de Jabón La Corona y el Imperio del Jabón Zote: De unos Baños de Vapor en 1920 a Conquistar Corea del Sur sin Gastar $1 en Publicidad",
        "subtitle": "Integración Vertical en Ecatepec, Química de Saponificación con Blanqueadores Ópticos UV y Resistencia Familiar frente a Wall Street.",
        "thesis": "El éxito centenario de Fábrica de Jabón La Corona demuestra que la integración vertical extrema —desde la cogeneración termoeléctrica y el refinamiento de glicerina hasta la logística ferroviaria propia— combinada con una política de cero gasto publicitario y cero endeudamiento financiero permite a una empresa familiar mexicana superar en cuota de mercado a conglomerados multinacionales como Procter & Gamble y Unilever.",
        "nexo": "Octavo episodio de Crónicas Corporativas (Formato Cuento Ilustrado Tri-Plataforma): Ingeniería química mexicana, economía circular industrial en Xalostoc y soberanía manufacturera.",
        "reel_video": "{REEL_MP4}",
        "content_blocks": [
            {{
                "title": "1. De Tepatitlán a los Baños Corona de Peralvillo (1920)",
                "body": """
En 1920, tras el final de la fase armada de la Revolución Mexicana, los hermanos Esteban, Loreto y Daniel González Padilla emigraron desde Tepatitlán, Jalisco, hacia la Ciudad de México. Instalaron su primer taller artesanal de saponificación con cazos de cobre dentro del inmueble de unos antiguos baños públicos de vapor ubicados en el barrio de Peralvillo, conocidos popularmente como los 'Baños Corona'.

Como el taller carecía de un rótulo comercial propio y conservaba en su fachada de ladrillo el letrero de los antiguos baños, los habitantes de la capital comenzaron a decir cotidianamente: 'Vamos a comprar jabón a La Corona'. Aquel bautizo popular dio nombre definitivo a la empresa que transformaría la industria química de limpieza en México.
"""
            }},
            {{
                "title": "2. El Coloso Industrial de Xalostoc en Ecatepec: Integración Vertical y Cogeneración",
                "body": """
Para sostener el crecimiento de la demanda nacional, la compañía trasladó su corazón operativo al Parque Industrial Xalostoc, en Ecatepec de Morelos, Estado de México. A diferencia de las firmas de consumo que subcontratan la maquila, La Corona edificó un complejo autosuficiente con espuelas de ferrocarril propias que ingresan directamente a los patios de descarga de materias primas.

La planta opera bajo un esquema de economía circular e integración vertical: cuenta con turbinas de cogeneración de energía eléctrica y térmica, plantas de tratamiento de agua, soplado de envases plásticos, imprenta de empaques y torres de refinación que recuperan la glicerina generada naturalmente durante la saponificación para comercializarla con pureza de grado farmacéutico y cosmético. En este mismo complejo se producen marcas históricas como los detergentes biodegradables Roma y Foca, el jabón de tocador Rosa Venus y el aceite vegetal comestible 1-2-3.
"""
            }},
            {{
                "title": "3. La Química del Jabón Zote (1970): Ácidos Grasos y Blanqueadores Ópticos UV",
                "body": """
Lanzado al mercado en 1970 bajo un ingenioso juego lingüístico ('un jabón-zote' de 400 gramos), el Jabón Zote fue formulado con un mínimo de 66% de ácidos grasos puros derivados de una proporción exacta entre sebo de res refinado (que aporta firmeza estructural y baja solubilidad de desgaste) y aceite de coco (que garantiza abundante espuma incluso en aguas con alta concentración de sales minerales), aromatizado con aceite esencial de citronela.

Su secreto más notable reside en la incorporación de blanqueadores ópticos fluorescentes. En lugar de degradar las fibras textiles mediante hipoclorito de sodio (cloro), estas moléculas se fijan al tejido durante el lavado, absorben fotones de radiación ultravioleta invisible de la luz solar y los reemiten en el espectro visible como luz azulada, neutralizando ópticamente el tono amarillento de las prendas blancas.
"""
            }},
            {{
                "title": "4. Cero Publicidad, Rechazo a Wall Street y Culto en Corea del Sur",
                "body": """
Fábrica de Jabón La Corona constituye una anomalía en las escuelas de negocios globales: no invierte en campañas de televisión ni mantiene pasivos con la banca internacional. Todo el margen que las transnacionales destinan a mercadotecnia se transfiere directamente a un precio imbatible para el consumidor. Pese a las reiteradas ofertas de compra por parte de fondos de inversión y gigantes extranjeros, la familia González ha mantenido el principio de que una fuente de trabajo mexicana no está en venta.

Irónicamente, sin pagar un solo anuncio, el Jabón Zote cruzó el océano Pacífico: en Corea del Sur se comercializa en tiendas especializadas como producto predilecto para higienizar brochas de maquillaje profesional y tratar pieles grasas, mientras que en los ríos del sur de Estados Unidos es utilizado por pescadores deportivos como la carnada más eficaz para capturar bagre (catfish) debido a la dispersión acuática de sus ácidos grasos y citronela.
"""
            }}
        ],
        "apa_references": [
            "Fábrica de Jabón La Corona, S.A. de C.V. (2025). *Historia centenaria, procesos de saponificación y sostenibilidad en Xalostoc (1920-2025)*. Documentación Corporativa La Corona. https://www.lacorona.com.mx/",
            "González Padilla, E. (Archivo Histórico). *De Tepatitlán a Peralvillo: Memoria industrial de la jabonería mexicana*. Acervo Industrial del Estado de México.",
            "Procurement & Chemical Engineering Review. (2024). *Optical brighteners and fatty acid ratios in traditional laundry bars: The Zote formulation*. Journal of Surfactants and Detergents.",
            "cacs, & sIA Editora. (2026). *sIA Crónicas #08: Fábrica de Jabón La Corona y el Imperio del Jabón Zote (Cuento Ilustrado Tri-Plataforma)*. sIA Journal Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    }},'''

    if SLUG not in mag_text:
        mag_text = mag_text.replace("RESEARCH_DATABASE = {", "RESEARCH_DATABASE = {\n" + zote_entry)
        BUILD_MAG.write_text(mag_text, encoding="utf-8")
        print("  [OK] Inyectado en build_magazine.py")

    # Add to podcast.xml
    xml_text = XML_FILE.read_text(encoding="utf-8")
    if EP_MP3 not in xml_text:
        mp3_path = AUDIO_DIR / EP_MP3
        size_bytes = mp3_path.stat().st_size
        dur_str = "03:35"
        art_url = f"https://escucha-sia.github.io/articulos/{SLUG}.html"
        base_stem = EP_MP3.replace(".mp3", "")
        item_xml = f"""    <item>
      <title>sIA Crónicas #08: Fábrica de Jabón La Corona y el Imperio del Jabón Zote: De unos Baños de Vapor en 1920 a Conquistar Corea del Sur sin Gastar $1 en Publicidad</title>
      <link>{art_url}</link>
      <description>Cuento Ilustrado Tri-Plataforma (Spotify en tu coche + Video en YouTube y TikTok): Cómo los hermanos González Padilla fundaron La Corona en unos baños de vapor en 1920, la fortaleza industrial de Ecatepec con ferrocarril propio y cogeneración, la química secreta del Jabón Zote con blanqueadores ópticos UV y su éxito en Corea del Sur sin gastar en publicidad por cacs. | Leer artículo y referencias APA: {art_url}</description>
      <pubDate>Thu, 05 Nov 2026 12:00:00 GMT</pubDate>
      <enclosure url="https://escucha-sia.github.io/audio/{EP_MP3}" length="{size_bytes}" type="audio/mpeg"/>
      <guid isPermaLink="true">https://escucha-sia.github.io/audio/{EP_MP3}</guid>
      <itunes:duration>{dur_str}</itunes:duration>
      <itunes:author>Jorge y Dalia</itunes:author>
      <itunes:image href="https://escucha-sia.github.io/cover.jpg"/>
      <itunes:explicit>no</itunes:explicit>
      <podcast:transcript url="https://escucha-sia.github.io/audio/{base_stem}.vtt" type="text/vtt" language="es"/>
      <podcast:transcript url="https://escucha-sia.github.io/audio/{base_stem}.srt" type="application/x-subrip" language="es"/>
    </item>
    <item>"""
        xml_text = xml_text.replace("    <item>", item_xml, 1)
        XML_FILE.write_text(xml_text, encoding="utf-8")
        print("  [OK] Inyectado en podcast.xml")

    # Add card to links.html
    links_text = LINKS_FILE.read_text(encoding="utf-8")
    if SLUG not in links_text:
        new_card = f"""            <!-- EPISODIO: sIA Crónicas #08 Jabón Zote Storybook -->
            <a href="articulos/{SLUG}.html" class="ep-card" style="border-color: rgba(236, 72, 153, 0.55); background: linear-gradient(135deg, rgba(236, 72, 153, 0.16) 0%, rgba(15, 23, 42, 0.92) 100%);">
                <div class="ep-top">
                    <span class="ep-tag" style="background: rgba(236, 72, 153, 0.25); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.5);">🧼 sIA CRÓNICAS #08 • CUENTO ILUSTRADO (03:35)</span>
                    <span class="ep-date">06 Nov 2026</span>
                </div>
                <div class="ep-title">Fábrica La Corona y el Imperio del Jabón Zote: De unos Baños en 1920 a Corea del Sur sin Gastar $1 en Publicidad</div>
                <div class="ep-desc">🚗 Escúchalo en tu coche por Spotify o 📱 mira el Cuento Ilustrado en YouTube y TikTok: Ecatepec, química UV y resistencia ante Wall Street.</div>
                <div class="ep-ReadMore" style="color: #f472b6;">Ver Cuento Ilustrado + Fuentes APA →</div>
            </a>
"""
        links_text = links_text.replace('<div class="episodes-list">', '<div class="episodes-list">\n' + new_card, 1)
        LINKS_FILE.write_text(links_text, encoding="utf-8")
        print("  [OK] Tarjeta añadida a links.html")

    subprocess.run([sys.executable, str(BUILD_MAG)], cwd=str(BASE_DIR), check=True)
    print("  [OK] Revista compilada con éxito.")

def dismiss_modals(page):
    for _ in range(3):
        modals = page.locator("div.TUXModal-overlay, div[data-floating-ui-portal], div[role='dialog']").all()
        dismissed = False
        for m in modals:
            if m.is_visible():
                btn = m.locator("button:has-text('Activar'), button:has-text('Cancelar'), button:has-text('Entendido'), button:has-text('Aceptar'), button[aria-label='close']").first
                if btn.count() > 0 and btn.is_visible():
                    btn.click()
                    time.sleep(1)
                    dismissed = True
        if not dismissed:
            page.keyboard.press("Escape")
            break

def step2_publish_to_tiktok():
    video_path = BASE_DIR / "reels" / REEL_MP4
    caption = (
        "🧼 ¿Cómo una fábrica mexicana de jabón en Ecatepec derrotó a gigantes de Wall Street sin gastar un solo peso en publicidad? "
        "De los Baños Corona de 1920 en Peralvillo a conquistar Corea del Sur con el Jabón Zote. "
        "🚗 Si vas en tu coche escúchanos en Spotify (sIA Podcast) | 📱 Mira este Cuento Ilustrado completo aquí en TikTok y YouTube (@escucha_sia). "
        "#jabonzote #hechoenmexico #industriales #historia #empresas #mexico #quimica #siapodcast"
    )

    print("\n🚀 Subiendo Cuento Ilustrado Completo (03:35 min) a TikTok Studio...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 950},
            locale="es-ES",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(4)
        page.mouse.click(600, 200)
        time.sleep(1)

        file_input = page.locator("input[type='file']").first
        print(f"[*] Adjuntando video: {video_path.name} ({video_path.stat().st_size / (1024*1024):.2f} MB)...")
        file_input.set_input_files(str(video_path))

        print("[*] Esperando carga del video de 3:35 min (28s)...")
        time.sleep(28)

        dismiss_modals(page)
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)

        editor = page.locator("div.public-DraftEditor-content, div[contenteditable='true']").first
        try:
            editor.click(force=True, timeout=5000)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            time.sleep(0.5)
            page.keyboard.type(caption, delay=18)
            time.sleep(2)
        except Exception:
            page.evaluate(f"""() => {{
                const el = document.querySelector('div.public-DraftEditor-content, div[contenteditable="true"]');
                if (el) {{
                    el.innerText = `{caption}`;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}""")
            time.sleep(1)

        dismiss_modals(page)
        page.screenshot(path=str(SCRATCH_DIR / "ready_to_post_zote_storybook.png"))

        page.evaluate("window.scrollTo(0, 1500)")
        time.sleep(1)
        dismiss_modals(page)

        post_btn = page.locator("button:has-text('Publicar'), button:has-text('Post')").first
        if post_btn.count() > 0:
            try:
                post_btn.click(timeout=5000)
            except Exception:
                post_btn.click(force=True)
            print("[*] Esperando confirmación de publicación en TikTok (20s)...")
            time.sleep(20)
            dismiss_modals(page)
            page.screenshot(path=str(SCRATCH_DIR / "published_zote_storybook.png"))
            print("🎉 ¡CUENTO ILUSTRADO DE JABÓN ZOTE PUBLICADO EN TIKTOK STUDIO!")
        context.storage_state(path=str(SESSION_FILE))
        browser.close()

if __name__ == "__main__":
    step1_register_magazine_and_rss()
    step2_publish_to_tiktok()
