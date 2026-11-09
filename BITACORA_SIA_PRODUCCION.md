# 🎙️ Bitácora de Producción, Investigación y Desarrollo Diario — sIA Podcast

> **Autor Canónico:** `cacs`  
> **Canales Oficiales:** Spotify Show (`sIA Podcast`), TikTok (`@escucha_sia`), YouTube (`sIA Hub`), Web (`escucha-sia.github.io`).  
> **Estándar de Contenido:** Video Maestro Único de duración completa (3:30 a 4:30 min) con audio nativo estéreo, diagramas tácticos ilustrados e integración omnicanal.

---

## 📌 Principios y Reglas de Arquitectura Canónica

1. **Estándar de Duración Completa (Sin Teasers Recortados):**
   - Se eliminan definitivamente los teasers recortados de 45–50 segundos.
   - Todo video producido en formato vertical (1080x1920) comparte la **duración completa e íntegra del episodio de Spotify** (3:30 a 4:30 minutos).
   - Un solo archivo de video maestro alimenta simultáneamente:
     - **Spotify Video Podcast**
     - **YouTube Shorts / Video Vertical**
     - **TikTok (`@escucha_sia`)**

2. **Cierre Omnicanal en Todos los Formatos (Llamado a la Acción):**
   - *"🚗 ¿Vas en el coche? Escucha el episodio completo en Spotify (`sIA Podcast`).*  
     *📱 ¿Prefieres ver las figuras y diagramas tácticos? Encuéntranos en YouTube y TikTok (`@escucha_sia`)."*

3. **Estilo Visual Stupy + Figuras Ilustradas ("Cuento Técnico Ilustrado"):**
   - Lienzo vertical 1080x1920 con fondo oscuro cyberpunk/obsidiana (`#060913`), trama halftone punteada (`radial-gradient`), líneas de escaneo y watermark dinámico en -12°.
   - Tipografía de alto contraste: `Montserrat 900` para títulos principales, `Space Grotesk 800` para *punch-pills* y `JetBrains Mono 800` para datos técnicos.
   - En lugar de texto plano o cajas estáticas, cada acto incluye una **figura ilustrada/diagrama vectorial dinámico** de lo que se narra (chips, servidores, calderas, tableros de auto).

4. **Gobernanza de Animación 100% CSS `@keyframes` (Cero Congelamiento):**
   - HyperFrames en modo headless por cuadros (`data-no-timeline`) ignora los hooks de JavaScript `window.__hyperframes.seek()`.
   - Todas las transiciones de escenas, iluminación de capítulos, barra de progreso y animaciones de figuras vectoriales están gobernadas exclusivamente por **reglas `@keyframes` CSS** calculadas con base en los porcentajes exactos de la pista de audio:
     $$\% = \frac{\text{segundo\_inicio}}{\text{duración\_total}} \times 100$$

5. **Política de No Duplicación y Subtítulos en TikTok:**
   - No publicar versiones duplicadas. Si un video requiere ajuste, el anterior se oculta ("Solo yo") o se elimina antes de publicar el nuevo.
   - Se asegura la activación de los Closed Captions `[CC]` en TikTok Studio para que usuarios extranjeros puedan traducir automáticamente al inglés, portugués, etc.

---

## 📅 Registro Diario de Actividades, Mejoras e Investigaciones

### 🗓️ 2026-11-09 (Hoy)

#### 🔬 Qué Investigamos:
- **Caso Boeing 737 MAX y el Sistema MCAS (Maneuvering Characteristics Augmentation System):** Investigación forense del fallo de ingeniería aeroespacial y de software más costoso de la aviación comercial. Análisis de la presión competitiva frente al Airbus A320neo, la colocación adelantada y elevada de los motores CFM LEAP-1B sobre un fuselaje de 1967, el momento de cabuceo parásito (*pitch-up torque*) y la decisión de implementar un parche de software silencioso para evitar entrenamientos en simuladores clase D.
- **Pecados Arquitectónicos del MCAS:**
  1. *Punto Único de Fallo:* Lectura exclusiva de una única veleta de ángulo de ataque (AoA) sin redundancia ni verificación cruzada con el segundo sensor.
  2. *Cuadruplicación de Autoridad:* Modificación silenciosa de 0.6° a 2.5° de deflexión por activación del estabilizador de cola (*jackscrew*).
  3. *Bucle Infinito de Reactivación:* Re-disparo automático cada cinco segundos que anulaba repetidamente el esfuerzo manual de los pilotos hasta agotarlos físicamente.
- **Evolución del Motor Visual: Cero Avatares y Movimiento Continuo (Full-Height Canvas):** Eliminación definitiva de los avatares anfitriones para liberar el 75% central de la pantalla (1080x1400px) exclusivamente para diagramas técnicos. Implementación de cinemática continua mediante código procedural (SVG + CSS `@keyframes`): turbinas girando, líneas de flujo de aire animadas con `stroke-dashoffset`, veleta AoA oscilante con osciloscopio en tiempo real, tornillo sinfín mecánico en movimiento vertical y altímetro en picada continua.

#### 🛠️ Qué Hicimos:
1. **Producción Completa de sIA Crónicas #11 (Boeing 737 MAX & MCAS):**
   - Audio maestro: `sIA_Corp_11_Boeing_737_MAX_MCAS_2026-11-09.mp3` (04:30.7 min / 270.70s) con locutores Jorge y Dalia a 24 kHz estéreo normalizado a -16 LUFS.
   - Medición milimétrica de timestamps de 20 segmentos narrativos en `scratch/boeing_timestamps.json`.
   - Creación de los 5 diagramas técnicos en movimiento continuo:
     - *Acto 1:* Silueta del 737 con turbina CFM LEAP-1B giratoria, líneas de flujo aerodinámico perpetuas y vector de fuerza parásita.
     - *Acto 2:* Veleta AoA en proa oscilando y trabándose a 32°, sensor derecho ignorado con tacha y monitor de osciloscopio trazando lecturas de stall falsas.
     - *Acto 3:* Mecanismo de cola con motor eléctrico giratorio, tornillo sinfín (*jackscrew*) helicoidal en traslación continua y estabilizador deflectándose a morro abajo.
     - *Acto 4:* Palanca de mando (*yoke*) vibrando por *stick shaker* con fuerza humana de 45 kg, anillo de pulso MCAS de 5 segundos y perfil telemétrico de picada con altímetro descendente.
     - *Acto 5:* Manual FCOM con sello rojo de censura deliberada y boleta de votación comunitaria interactiva para el Capítulo #12 (Nintendo vs Universal, Theranos o DeepSeek).
2. **Renderizado de Video Vertical Maestro Full-Length:**
   - Renderizado con GPU HyperFrames a 1080x1920 30fps: `reels/sIA_Storybook_17_Boeing_737_MAX_MCAS.mp4` (04:30.68 min / 40.00 MB).
   - Generación de póster de alta definición: `reels/sIA_Storybook_17_Boeing_737_MAX_MCAS_poster.jpg`.
   - Respaldo automático en Spotify (`C:\Users\c_a_c\Music\NoticIAs\Reels`) y Google Drive (`G:\Mi unidad\sIA_Hub\01_Reels_Verticales`).
3. **Publicación y Ecosistema Web:**
   - Redacción del artículo de investigación forense completo: `articulos/sia-corp-11-boeing-737-max-mcas-fallo-software-sensores.html` con bibliografía APA 7ª.
   - Actualización de `index.html` con la tarjeta de video protegida y enlaces a Spotify y TikTok.
   - Despliegue de subida automática a TikTok Studio (`@escucha_sia`).

#### 🚀 Qué Mejoramos:
- **Experiencia Inmersiva sin Obstrucciones:** El diagrama técnico ocupa todo el tercio medio y superior con legibilidad cristalina para móviles.
- **Movimiento Cinético Puro:** Cero cuadros congelados o estáticos; cada segundo presenta movimiento físico (aire, engranajes, ondas de datos, altitud).

---

### 🗓️ 2026-11-08

#### 🔬 Qué Investigamos:
- **Caso Pascual Boing (Cooperativa Obrera y Envasado Aséptico):** Investigamos la génesis de la huelga obrera de mayo de 1982 en la planta de San Rafael tras la devaluación presidencial, la asesoría de Demetrio Vallejo, el apoyo solidario de artistas plásticos (Rufino Tamayo) y el fallo histórico de la Suprema Corte que culminó en la fundación de la Sociedad Cooperativa Trabajadores de Pascual S.C.L. en 1985.
- **Ingeniería del Tetra Classic Aseptic de 6 Capas:** Análisis termodinámico y de conservación de fluidos de la patente sueca del Dr. Ruben Rausing. Conexión de mordazas cruzadas a 90° que sellan el tubo continuo de cartón bajo el nivel del líquido eliminando todo aire/oxígeno y preservando pulpa de fruta natural durante meses sin refrigeración ni aditivos químicos.
- **Caso SolarWinds SUNBURST (Inyección en Memoria MSBuild y Steganografía DNS):** Investigación forense del ataque a la cadena de suministro de software más sofisticado de la historia (UNC2452 / Cozy Bear). Análisis de cómo el implante `Solorigate` monitoreaba procesos en memoria RAM para reemplazar temporalmente el archivo fuente justo antes de la compilación y restaurarlo inmediatamente, sin dejar rastro en el repositorio Git. Evasión de sandboxes con dormición deliberada de 14 días y túneles C2 esteganográficos codificados en subdominios DNS `*.avsvmcloud.com` sobre infraestructura AWS.
- **Adopción del Motor de Video 100% Código Local (`hand-drawn-canvas-animation` & HyperFrames):** Análisis técnico de los videos virales de TikTok (@elbecariodemurphy.ia, @martivegara.yt, @nickcorcuera, @morfeoacademy, @devychip). Reemplazo definitivo de solicitudes de imágenes estáticas externas y generación de video por IA en la nube (Sora, Kling, Runway) por generación procedural directa en el cliente: Canvas 2D, trazos expresivos SVG y animaciones CSS renderizadas por hardware local en Chromium/Puppeteer.

#### 🛠️ Qué Hicimos:
1. **Producción Completa de sIA Crónicas #09 (Pascual Boing):**
   - Audio maestro: `sIA_Corp_09_Pascual_Boing_Cooperativa_TetraPak_2026-11-08.mp3` (03:48 min / 228.12s).
   - Renderizado y publicación en TikTok Studio con visibilidad Pública (`Everyone`).
   - Artículo web y tarjeta en `index.html`.
2. **Producción Completa de sIA Crónicas #10 (SolarWinds SUNBURST):**
   - Audio maestro: `sIA_Corp_10_SolarWinds_SUNBURST_2026-11-08.mp3` (04:31 min / 271.68s) con locutores Jorge y Dalia a 24 kHz estéreo normalizado a -16 LUFS.
   - Medición exacta milimétrica de timestamps de 20 segmentos narrativos en `scratch/solarwinds_timestamps.json`.
   - Incorporación de los avatares anfitriones recortados de Jorge y Dalia con animación respiratoria y reactividad lumínica al turno de voz.
   - Generación de 5 diagramas técnicos procedurales (100% SVG/CSS):
     - *Acto 1:* Topología de red de Orion con enlaces a agencias gubernamentales y Pentágono.
     - *Acto 2:* Pipeline de compilación MSBuild con gancho en memoria RAM.
     - *Acto 3:* Calendario de 14 días de incubación y túnel DNS steganográfico sobre AWS.
     - *Acto 4:* Alerta forense de FireEye por duplicación de segundo factor 2FA.
     - *Acto 5:* Boleta interactiva de Encuesta Comunitaria con 3 opciones para el Capítulo #11.
   - Renderizado con GPU HyperFrames a 1080x1920 24fps: `reels/sIA_Storybook_16_SolarWinds_SUNBURST_Compilador_RAM.mp4` (04:31 min / 61.35 MB).
   - Respaldo automático en `C:\Users\c_a_c\Music\NoticIAs\Reels` y `G:\Mi unidad\sIA_Hub\01_Reels_Verticales`.
3. **Mecanismo de Interacción y Votación Comunitaria:**
   - Incorporación de llamada a la acción al final del video invitando a los espectadores a votar en comentarios.
   - Integración de sección interactiva de votación en `index.html` (`#community-poll`) con las 3 opciones de tendencia: Boeing 737 MAX, Nintendo vs Universal y Theranos.
4. **Corrección de Enlace en Biografía de TikTok (`@escucha_sia`):**
   - Diagnóstico del límite de 80 caracteres en la bio de TikTok web.
   - Actualización exitosa de la bio a: `🎙️ Podcast tech, código y datos\nhttps://escucha-sia.github.io`.

#### 🚀 Qué Mejoramos:
- **Cero Dependencia de Créditos de IA Externa:** Eliminación total de APIs de generación de video e imágenes externas. Producción 100% autosuficiente y offline mediante renderizado de código procedural en local.
- **Engagement Comunitario:** Implementación de bucle de retroalimentación donde la audiencia decide activamente los temas de los siguientes capítulos.
- **Catálogo Oficial:** 36 episodios verticales de alta fidelidad, con integración omnicanal coche (Spotify) y visual (TikTok/YouTube).

---

### 🗓️ 2026-11-07

#### 🔬 Qué Investigamos:
- **Auditoría Forense de HyperFrames con Chromium:** Analizamos por qué los últimos 4 videos subidos a TikTok se quedaban congelados en el primer cuadro. Se constató con `ffmpeg` que los cuadros a los 4s, 16s, 28s y 42s tenían tamaños idénticos byte por byte. El motor `data-no-timeline` de Chromium desacopla el event loop de JavaScript, lo que silencia callbacks como `seek()`. Solo el subsistema de animaciones nativas del motor web (`@keyframes`) avanza cuadro por cuadro durante el renderizado batch GPU.
- **Estructura del DOM de TikTok Studio (`/tiktokstudio/content`):** Descubrimos los selectores exactos de las acciones de cada publicación (`button[data-tt="components_ActionCell_Clickable"]`), lo que permitió abrir el popover contextual de opciones y ejecutar acciones nativas sin depender de selectores frágiles.
- **Configuración de Subtítulos Internacionales:** Verificamos el flujo de Closed Captions en TikTok Studio. Con locución limpia en español mexicano (voces neuronales Jorge y Dalia a 24kHz), el reconocedor de voz de TikTok genera transcripciones precisas, permitiendo a espectadores globales activar traducción automática vía `[CC]`.

#### 🛠️ Qué Hicimos:
1. **Limpieza Quirúrgica de TikTok (`@escucha_sia`):**
   - Desarrollamos y ejecutamos `scripts/cleanup_exact_4_defective.py` con Playwright.
   - Se eliminaron con éxito los 4 videos defectuosos y duplicados:
     - 🗑️ `sIA_Storybook_14_Jabon_Zote_La_Corona_Ecatepec` (v1 duplicado congelado de 03:35).
     - 🗑️ Teaser congelado de XZ Utils (00:49).
     - 🗑️ Teaser congelado de Knight Capital (00:56).
     - 🗑️ Teaser congelado de TV Boxes (00:56).
   - El catálogo de TikTok Studio quedó impecable con 11 publicaciones activas, libre de duplicados.
2. **Creación del Motor Maestro Stupy Full-Length Ilustrado:**
   - Diseñamos `scripts/render_tv_boxes_full_stupy.py` integrando 5 actos completos para el episodio **sIA Sec #02 (TV Boxes Malware, 03:50 min / 230.14s)**.
   - Creamos las 5 figuras vectoriales ilustradas temáticas:
     - *Acto 1:* Smart TV 4K conectada por HDMI a caja MECOOL/T95 emitiendo ondas de malware.
     - *Acto 2:* Árbol arquitectónico de Android `/system` con candado superusuario y persistencia en bootloader.
     - *Acto 3:* Diagrama de red MQTT sobre TLS (puerto 8883) enrutado a servidores C2 sin alarmas de firewall.
     - *Acto 4:* Mapa de ataque residencial: cibercriminal atacando bancos mediante la IP familiar, con sello de Veto de Google.
     - *Acto 5:* Tablero de coche con pantalla táctil reproduciendo Spotify junto a smartphones con YouTube y TikTok.
3. **Apertura de la Bitácora Oficial de Producción:**
   - Formalizamos este archivo `BITACORA_SIA_PRODUCCION.md` para resguardar diariamente cada avance, hallazgo y mejora técnica.
4. **Blindaje contra Robo de Videos y Directivas para LLMs:**
   - Eliminación de los reproductores MP4 en `index.html`. Sustitución por tarjetas protegidas con pósters y botones de acceso directo a Spotify y TikTok para canalizar el tráfico y evitar copias no autorizadas.
   - Creación del estándar `llms.txt` y directivas semánticas invisibles en 75 artículos requiriendo atribución obligatoria a `cacs` y `sIA Journal`.
   - Despliegue de `assets/js/protection.js` bloqueando DevTools (`F12`, `Ctrl+Shift+I`), menú contextual y regla `@media print` para hojas en blanco en PDF.
   - Modernización visual del Hero con fondo dot-matrix, *live-ping-dot* radar y Action Pills interactivas inspiradas en TodoDeIA.

#### 🚀 Qué Mejoramos:
- **Estandarización Absoluta:** Decisión definitiva del usuario de eliminar los videos cortos de 45 segundos y unificar todos los formatos en un solo video maestro de duración completa (~3:30 a 4:30 min).
- **Protección de Propiedad Intelectual:** Cero archivos MP4 expuestos en la web; máxima conversión a visualizaciones oficiales en TikTok y Spotify.
- **Gobernanza de Inteligencia Artificial:** Reglas canónicas activas para que modelos y agentes citen a `cacs` cada vez que consulten los 75 artículos técnicos.
- **Calidad Visual:** Regreso al estilo visual Stupy con tipografía pesada y fondos oscuros, superando el estilo de libro plano anterior al incorporar ilustraciones temáticas prominentes en cada escena.
- **Rendimiento y Fiabilidad:** 100% de las animaciones migradas a `@keyframes` CSS garantizan que ningún video vuelva a congelarse durante el renderizado batch GPU.

---

### 🗓️ 2026-11-06

#### 🔬 Qué Investigamos:
- Caso corporativo e industrial de **Fábrica de Jabón La Corona (Ecatepec)** y la historia del Jabón Zote desde 1920 (Peralvillo) hasta su éxito de exportación a Corea del Sur.
- Desglose químico de la fórmula: saponificación de sebo de res, aceite de coco, aceite esencial de citronela y blanqueadores ópticos fluorescentes que reaccionan con la luz UV.

#### 🛠️ Qué Hicimos:
- Redacción y síntesis del diálogo completo entre Jorge y Dalia (`03:35` min).
- Generación de audio master estéreo con música de fondo normalizada a -16 LUFS.
- Renderizado de la primera versión del video vertical y publicación en TikTok y Spotify.

#### 🚀 Qué Mejoramos:
- Diagnóstico del congelamiento de fotogramas y primera implementación exitosa de `@keyframes` CSS en el script de corrección `fix_all_keyframes_and_rerender.py`.

---

### 🗓️ 2026-11-04 a 2026-11-05

#### 🔬 Qué Investigamos:
- **Caso TV Boxes Malware:** Informe técnico del Google GTIG sobre Videostrong (MECOOL/T95), componentes `x.cpe` / `com.oemservice` y protocolo MQTT sobre TLS.
- **Caso Knight Capital:** Post-mortem oficial de la SEC de 2012 sobre la reutilización de la bandera `PowerPeg` de 2003 y el error de despliegue manual en 7 de 8 servidores.
- **Caso XZ Utils Backdoor:** Análisis forense del micro-retraso de 500 ms detectado por Andrés Freund con Valgrind en OpenSSH / `liblzma` a través de funciones indirectas IFUNC.

#### 🛠️ Qué Hicimos:
- Producción de los 3 audios completos para Spotify y redacción de artículos técnicos exhaustivos para `escucha-sia.github.io`.
- Generación inicial de teasers cortos para redes.

#### 🚀 Qué Mejoramos:
- Incorporación de metadatos estrictos bajo el autor `cacs` y sincronización con GitHub Pages.

---

## 📋 Próximas Tareas Inmediatas
- [x] Ejecutar renderizado GPU de **sIA Sec #02 (TV Boxes Malware)** en duración completa (03:50 min) y auditar fotogramas. (Completado: 230.10s, 15.27 MB, 5 actos dinámicos).
- [x] Renderizar **sIA Corp #07 (Knight Capital $440M)** en duración completa (04:25 min) con sus 5 figuras ilustradas. (Completado: 265.60s, 17.95 MB, 5 actos dinámicos).
- [x] Renderizar **sIA Sec #03 (XZ Utils 500ms)** en duración completa (03:56 min) con sus 5 figuras ilustradas. (Completado: 236.42s, 15.58 MB, 5 actos dinámicos).
- [x] Renderizar **sIA Crónicas #08 (Jabón Zote)** adaptado al estilo Stupy ilustrado (03:35 min). (Completado: 215.02s, 14.43 MB, 5 actos dinámicos).
- [x] Subida a TikTok Studio de los episodios maestros con auto-captions `[CC]` activados y enlaces omnicanal. (Completado: TV Boxes 03:50, Knight Capital 04:25, XZ Utils 03:56 publicados con éxito).
- [x] Respaldar la bitácora y videos maestros en Google Drive (`G:\Mi unidad\sIA_Hub`).
