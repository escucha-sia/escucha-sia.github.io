import re

html_path = 'c:/Carlos/noticias_podcast/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Buscamos la sección de reels
start_tag = '<section class="container" id="reels-showcase"'
end_tag = '</section>'
start_idx = html.find(start_tag)
end_idx = html.find(end_tag, start_idx) + len(end_tag)

reels_section = html[start_idx:end_idx]

card_regex = re.compile(
    r'<div class="reel-home-card".*?'
    r'poster="(?P<poster>[^"]+)".*?'
    r'<div style="font-size: 0.75rem;[^>]*>(?P<cat>[^<]+)</div>.*?'
    r'<h4[^>]*>(?P<title>[^<]+)</h4>.*?'
    r'<a href="(?P<link>[^"]+)"',
    re.DOTALL
)

cards = list(card_regex.finditer(reels_section))
print(f"Cards encontradas: {len(cards)}")

new_cards_html = []
for c in cards:
    poster = c.group('poster')
    cat = c.group('cat').strip()
    title = c.group('title').strip()
    link = c.group('link').strip()
    
    card_html = f'''            <div class="video-hub-card">
                <div class="video-poster-box">
                    <img src="{poster}" alt="{title}" loading="lazy" />
                    <div class="video-badge-overlay">{cat}</div>
                </div>
                <h4 style="font-size: 0.95rem; color: #fff; line-height: 1.35; margin-bottom: 8px; font-weight: 700;">{title}</h4>
                <div class="video-actions-container">
                    <a href="https://www.tiktok.com/@escucha_sia" target="_blank" rel="noopener" class="btn-video-channel btn-video-tiktok">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64c.298-.002.595.042.88.13V9.4a6.33 6.33 0 0 0-1-.08A6.34 6.34 0 0 0 3 15.66a6.34 6.34 0 0 0 10.82 4.49 6.27 6.27 0 0 0 1.94-4.54V8.75a8.16 8.16 0 0 0 4.77 1.52V6.84a4.85 4.85 0 0 1-.94-.15z"/></svg>
                        Ver en TikTok (@escucha_sia)
                    </a>
                    <a href="https://open.spotify.com/show/3oNxteAETV5wvEIPN1KDVN" target="_blank" rel="noopener" class="btn-video-channel btn-video-spotify">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/></svg>
                        Escuchar en Spotify
                    </a>
                    <a href="{link}" style="margin-top: 6px; font-size: 0.8rem; color: #38bdf8; text-decoration: none; font-weight: 600; text-align: center;">
                        Leer artículo y bibliografía &rarr;
                    </a>
                </div>
            </div>'''
    new_cards_html.append(card_html)

new_reels_section = f'''    <section class="container" id="reels-showcase" style="margin-top: 2rem; margin-bottom: 2rem;">
        <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.7)); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 24px; padding: 24px 32px; backdrop-filter: blur(16px); box-shadow: 0 20px 50px rgba(0,0,0,0.6);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
                <div>
                    <span class="badge badge-purple" style="font-size: 0.75rem; letter-spacing: 0.05em;">TIKTOK & REELS (9:16) • HYPERFRAMES MASTER</span>
                    <h3 style="font-size: 1.5rem; color: #fff; margin-top: 6px;">🎬 Galería Oficial de Videos Verticales (TikTok & Spotify)</h3>
                    <p style="color: #94a3b8; font-size: 0.9rem;">Cápsulas de duración completa con diagramas técnicos vectoriales. Reproducción oficial protegida en canales autorizados.</p>
                </div>
                <div style="font-size: 0.85rem; color: #38bdf8; font-family: monospace; font-weight: 600;">{len(cards)} Episodios Disponibles</div>
            </div>
            <div style="display: flex; gap: 20px; overflow-x: auto; padding-bottom: 12px; scrollbar-width: thin;">
{chr(10).join(new_cards_html)}
            </div>
        </div>
    </section>'''

updated_html = html[:start_idx] + new_reels_section + html[end_idx:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("¡index.html actualizado exitosamente!")
