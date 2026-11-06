import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
build_mag_path = BASE_DIR / "build_magazine.py"
content = build_mag_path.read_text(encoding="utf-8")

# 1. Ensure REELS_MAP has all 5 episodes
reels_additions = {
    "sIA_Dev_02_Code_Mode_vs_MCP_Cloudflare_Anthropic_2026-11-04.mp3": "sIA_Reel_Stupy_08_CodeMode_vs_MCP.mp4",
    "sIA_Maker_03_Biqu_Panda_Treat_FoodTech_2026-11-04.mp3": "sIA_Reel_Stupy_09_Biqu_Panda_Treat.mp4",
    "sIA_Sec_02_TV_Boxes_Malware_Fabrica_Videostrong_2026-11-04.mp3": "sIA_Reel_Stupy_11_TV_Boxes_Malware_Videostrong.mp4",
    "sIA_Corp_07_Knight_Capital_440_Millones_Flag_Reutilizado_2026-11-04.mp3": "sIA_Reel_Stupy_12_Knight_Capital_Bug_440M.mp4",
    "sIA_Sec_03_XZ_Utils_Backdoor_Andres_Freund_SSH_2026-11-04.mp3": "sIA_Reel_Stupy_13_XZ_Utils_Backdoor_500ms.mp4",
}

for ep, reel in reels_additions.items():
    if f'"{ep}"' not in content:
        content = content.replace(
            "REELS_MAP = {",
            f'REELS_MAP = {{\n    "{ep}": "{reel}",'
        )

# 2. Prepare entries in exact RESEARCH_DATABASE schema
NEW_ENTRIES = '''    # sIA Sec 03 - XZ Utils Backdoor Andres Freund - 4 de Noviembre de 2026
    "sIA_Sec_03_XZ_Utils_Backdoor_Andres_Freund_SSH_2026-11-04.mp3": {
        "slug": "sia-sec-03-el-backdoor-de-xz-utils-y-los-500ms-que-salvaron-internet",
        "category": "Ciberseguridad & Open Source",
        "badge_color": "emerald",
        "read_time": "15 min",
        "title": "sIA Sec #03: El Backdoor de XZ Utils: Cómo 500 Milisegundos de Lag Salvaron al Internet Entero",
        "subtitle": "Ingeniería Social de 2 Años, IFUNC Hooks en liblzma, Infiltración de OpenSSH y el Descubrimiento de Andrés Freund.",
        "thesis": "La crisis de seguridad de XZ Utils expone la vulnerabilidad estructural más crítica del ecosistema digital moderno: cómo actores estatales pueden invertir años de ingeniería social sobre mantenedores comunitarios agotados para inyectar vectores de ataque criptográficos indetectables que comprometen la totalidad de la infraestructura de servidores de producción.",
        "nexo": "Tercer episodio de Ciberseguridad: Espionaje cibernético tras CrowdStrike y Videostrong, arquitectura de OpenSSH, GNU IFUNC, micro-benchmarks y gobernanza de código abierto.",
        "reel_video": "sIA_Reel_Stupy_13_XZ_Utils_Backdoor_500ms.mp4",
        "content_blocks": [
            {
                "title": "1. 29 de Marzo de 2024: La Alerta que Paralizó al Mundo Tecnológico",
                "body": """
El viernes 29 de marzo de 2024, un mensaje publicado en la lista de correo de seguridad de código abierto oss-security hizo que los equipos de infraestructura de las principales empresas y gobiernos del planeta declararan estado de emergencia inmediata. Andrés Freund, un ingeniero de software de Microsoft especializado en bases de datos PostgreSQL, notificó la detección de un backdoor malicioso de ejecución remota de código inyectado en las versiones oficiales 5.6.0 y 5.6.1 de xz utils y liblzma, la librería estándar de compresión de datos del núcleo de Linux.

A diferencia de vulnerabilidades accidentales originadas por desbordamiento de búfer o punteros nulos, este incidente representaba la operación de espionaje e infiltración en la cadena de suministro más sofisticada y paciente jamás documentada en la historia de la informática.
"""
            },
            {
                "title": "2. La Operación Jia Tan: Dos Años Cultivando una Falsa Identidad",
                "body": """
La infiltración comenzó a finales de 2021. Un perfil bajo el seudónimo de 'Jia Tan' (JiaT75) comenzó a enviar parches menores y mejoras de compresión al repositorio de xz. El proyecto estaba mantenido por una sola persona: Lasse Collin, un voluntario finlandés que llevaba más de una década sosteniendo el software en su tiempo libre bajo un severo agotamiento mental.

Para acelerar la entrega de privilegios, una red coordinada de cuentas títere comenzó a presionar a Collin en foros públicos, recriminándole demoras en la integración de parches y sugiriendo agresivamente que cediera la gobernanza del código a Jia Tan. Agotado y confiando en la impecable trayectoria de Tan durante dos años, Collin le otorgó permisos de commit y control sobre los tarballs de distribución.
"""
            },
            {
                "title": "3. El Mecanismo Técnico: IFUNC Hooks y el Secuestro de OpenSSH",
                "body": """
Una vez al mando, Jia Tan diseñó un vector de inyección criptográfico de extraordinaria sofisticación. El código malicioso no se encontraba en el repositorio Git público, sino camuflado dentro de archivos binarios de prueba aparentemente corruptos ('bad-3-corrupt_lzma2.xz'). Durante el proceso de construcción mediante el sistema autotools (M4), scripts ofuscados extraían un archivo objeto (.o) que se vinculaba durante la compilación.

El payload aprovechaba las funciones indirectas de GNU (IFUNC) para interceptar la función 'RSA_public_decrypt' en el demonio sshd de OpenSSH (vía libsystemd). Si un atacante enviaba un certificado SSH firmado con su clave privada Ed448, el malware ejecutaba órdenes arbitrarias con privilegios de root antes de la fase de autenticación y sin dejar registros.
"""
            },
            {
                "title": "4. El Descubrimiento: 500 Milisegundos de Rigor Técnico",
                "body": """
Mientras realizaba micro-benchmarks para medir la latencia de conexiones en Debian sid, Andrés Freund detectó que los inicios de sesión por SSH consumían demasiada CPU y tardaban exactamente 500 milisegundos más de lo habitual. En lugar de ignorar ese medio segundo, Freund desensambló el binario con gdb y objdump, descubrió las tablas manipuladas y frenó la distribución horas antes de que llegara a Debian, Red Hat y Ubuntu estables.
"""
            }
        ],
        "apa_references": [
            "Freund, A. (2024). *Backdoor in upstream xz/liblzma leading to ssh server compromise*. Open Source Security (oss-security) Mailing List.",
            "Goodin, D. (2024). *What we know about the xz-utils backdoor that almost infected the world*. Ars Technica.",
            "CISA. (2024). *Supply Chain Compromise in XZ Utils (CVE-2024-3094)*. Cybersecurity and Infrastructure Security Agency.",
            "cacs, & sIA Editora. (2026). *sIA Sec #03: El Backdoor de XZ Utils y los 500ms que Salvaron Internet*. sIA Journal Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    },
    # sIA Corp 07 - Knight Capital $440M Bug - 4 de Noviembre de 2026
    "sIA_Corp_07_Knight_Capital_440_Millones_Flag_Reutilizado_2026-11-04.mp3": {
        "slug": "sia-corp-07-knight-capital-el-bug-de-440-millones-en-45-minutos",
        "category": "DevOps & Wall Street",
        "badge_color": "amber",
        "read_time": "14 min",
        "title": "sIA Corp #07: Knight Capital: $440 Millones Destruidos en 45 Minutos por Reutilizar un Flag Booleano",
        "subtitle": "El Mayor Desastre de DevOps en Wall Street: SMARS, Código Zombi PowerPeg, Despliegue Manual y la Caída de un Gigante Financiero.",
        "thesis": "La catástrofe de Knight Capital constituye el caso canónico de cómo la deuda técnica no gestionada, la reutilización imprudente de variables de configuración y la ausencia de despliegues automatizados e inmutables son capaces de aniquilar a un líder de mercado en menos de una hora.",
        "nexo": "Séptimo episodio de Crónicas Corporativas: Alta frecuencia, DevOps, SEC, feature flags, arquitectura financiera y circuit breakers.",
        "reel_video": "sIA_Reel_Stupy_12_Knight_Capital_Bug_440M.mp4",
        "content_blocks": [
            {
                "title": "1. 1 de Agosto de 2012: La Apertura del Abismo en Wall Street",
                "body": """
A las 9:30 AM del miércoles 1 de agosto de 2012, sonó la campana de apertura de la Bolsa de Valores de Nueva York (NYSE). En las pantallas de Knight Capital Group —el principal creador de mercado de Estados Unidos, responsable del 17% del volumen del NYSE y del NASDAQ— comenzó una cascada incomprensible de alertas.

En 45 minutos, el sistema SMARS ejecutó más de 4 millones de transacciones por 212 millones de acciones en 154 empresas, acumulando una pérdida neta de 440 millones de dólares: casi 10 millones de dólares destruidos por cada minuto de operación.
"""
            },
            {
                "title": "2. PowerPeg: El Código Zombi de 2003 que Nunca Fue Eliminado",
                "body": """
En 2003, los desarrolladores de Knight habían creado una función interna de prueba llamada 'PowerPeg', diseñada para comprar caro al Ask y vender barato al Bid en entornos de simulación para medir latencia sin verificar límites de precio. PowerPeg dejó de usarse hace casi una década, pero jamás fue borrado del código fuente en producción.
"""
            },
            {
                "title": "3. Reutilización del Flag y el Octavo Servidor Olvidado",
                "body": """
Para el lanzamiento del Retail Liquidity Program (RLP) de NYSE en 2012, los ingenieros reutilizaron la vieja bandera booleana que antes activaba PowerPeg. La noche previa, un técnico desplegó manualmente el nuevo software en el clúster de 8 servidores de SMARS, pero olvidó actualizar el octavo servidor.

Al abrir el mercado, el octavo servidor recibió el flag nuevo activado sobre el binario viejo de 2003, despertando a PowerPeg en un bucle infinito a mercado abierto que quebró a la compañía antes del mediodía.
"""
            }
        ],
        "apa_references": [
            "U.S. Securities and Exchange Commission (SEC). (2013). *In the Matter of Knight Capital Americas LLC (Release No. 70694)*. SEC Enforcement.",
            "Popper, N. (2012). *Knight Capital Says Trading Glitch Cost It $440 Million*. The New York Times.",
            "Nygard, M. T. (2018). *Release It!: Design and Deploy Production-Ready Software* (2nd ed.). Pragmatic Bookshelf.",
            "cacs, & sIA Editora. (2026). *sIA Corp #07: Knight Capital y el Bug de $440 Millones*. sIA Journal Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    },
    # sIA Sec 02 - TV Boxes Android Malware Videostrong - 4 de Noviembre de 2026
    "sIA_Sec_02_TV_Boxes_Malware_Fabrica_Videostrong_2026-11-04.mp3": {
        "slug": "sia-sec-02-el-caballo-de-troya-en-tu-sala-tv-boxes-android-malware-de-fabrica",
        "category": "Ciberseguridad & Hardware",
        "badge_color": "rose",
        "read_time": "12 min",
        "title": "sIA Sec #02: El Caballo de Troya en tu Sala: Cómo 1.3 Millones de TV Boxes Android Venían con Malware de Fábrica",
        "subtitle": "Supply-Chain Attacks en Hardware de Consumo: El Caso Videostrong, MECOOL, Proxies Residenciales y el Veto Histórico de Google.",
        "thesis": "La proliferación de dispositivos de streaming de bajo costo fabricados por ODMs sin auditoría de firmware demuestra que el eslabón más frágil de la seguridad doméstica reside en la cadena de suministro de hardware, donde componentes preinstalados con privilegios root convierten la red residencial en nodos de salida para el cibercrimen.",
        "nexo": "Segundo episodio de Ciberseguridad: Post-mortem tras CrowdStrike, supply chain attacks, protocolos MQTT, proxies residenciales y soberanía de red local.",
        "reel_video": "sIA_Reel_Stupy_11_TV_Boxes_Malware_Videostrong.mp4",
        "content_blocks": [
            {
                "title": "1. El Golpe de Google Threat Intelligence y la Botnet XCPE",
                "body": """
El Grupo de Inteligencia de Amenazas de Google (GTIG), junto con la Policía Nacional de Japón, HUMAN Security y Lumen, desmanteló una red global de más de 1.3 millones de decodificadores Android TV infectados desde la línea de ensamblaje. El fabricante señalado es Videostrong Technology Co., responsable de marcas populares como MECOOL y T95.
"""
            },
            {
                "title": "2. Persistencia en Bootloader y Comunicación MQTT",
                "body": """
El malware ('x.cpe' / 'com.oemservice') venía alojado en la partición '/system' con privilegios de superusuario ('android.uid.system'). Si el propietario ejecutaba un restablecimiento de fábrica, el bootloader volvía a inyectar el troyano en el siguiente arranque, desactivando Google Play Protect y comunicándose vía MQTT sobre TLS.
"""
            },
            {
                "title": "3. Tu Wi-Fi como Proxy Residencial para Cibercriminales y el Veto de Google",
                "body": """
La botnet alquilaba la conexión doméstica de las víctimas como proxy residencial para ataques DDoS, fraude publicitario invisible y robo de credenciales, haciendo que la dirección IP del hogar apareciera como autora de delitos informáticos. Google respondió vetando de por vida a Videostrong y revocando todas sus certificaciones de Android.
"""
            }
        ],
        "apa_references": [
            "Google Threat Intelligence Group (GTIG). (2026). *Technical Analysis and Global Takedown of the XCPE Android TV Botnet*. Google Security.",
            "HUMAN Security Research Team. (2026). *Badbox and Beyond: Supply-Chain Compromise of Consumer Android Devices*. HUMAN Satori.",
            "Márquez Flores, L. Á. (2026). *Un malware infectó a más de 1.3 millones de TV boxes Android*. Xataka México.",
            "cacs, & sIA Editora. (2026). *sIA Sec #02: El Caballo de Troya en tu Sala*. sIA Journal Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    },
    # sIA Maker 03 - BIQU Panda Treat - 4 de Noviembre de 2026
    "sIA_Maker_03_Biqu_Panda_Treat_FoodTech_2026-11-04.mp3": {
        "slug": "sia-maker-03-biqu-panda-treat-impresora-3d-confiteria-digital",
        "category": "Maker & FoodTech",
        "badge_color": "rose",
        "read_time": "12 min",
        "title": "sIA Maker #03: BIQU Panda Treat: Cómo una Impresora 3D de $200 Hackeó la Industria de la Confitería Digital",
        "subtitle": "De $5,000 a $330 USD: acoples modulares, química de tintas comestibles y la democratización del micro-baking artesanal.",
        "thesis": "La transformación de cinemáticas de impresión 3D de consumo en plataformas de manufactura alimentaria mediante cabezales térmicos intercambiables demuestra que la estandarización de movimientos de alta precisión es capaz de destruir monopolios de maquinaria industrial especializada.",
        "nexo": "Tercer episodio de Maker & 3D: Hardware abierto vs cerrado, ingeniería de alimentos, BIGTREETECH, química de formulaciones inocuas y microfabricación culinaria.",
        "reel_video": "sIA_Reel_Stupy_09_Biqu_Panda_Treat.mp4",
        "content_blocks": [
            {
                "title": "1. El Monopolio de la Confitería Digital y la Barrera de los Cinco Mil Dólares",
                "body": """
Durante más de una década, las impresoras directas sobre alimentos como la serie Eddie de Primera Technology exigían desembolsos de entre 3,000 y 8,000 dólares. Al combinar una Bambu Lab A1 Mini ($199 USD) con el cabezal modular BIQU Panda Treat ($130 USD), la barrera cae a $330 USD, reduciendo en un 93% el costo de entrada para reposterías artesanales.
"""
            },
            {
                "title": "2. Arquitectura de Acople Rápido e Inocuidad Alimentaria FDA",
                "body": """
El módulo Panda Treat sustituye el extrusor plástico por un cabezal de inyección térmica de tintas comestibles CMY formuladas con propilenglicol USP y glicerina vegetal certificadas por la FDA, Kosher y Halal, aislando la cama con tapetes de silicona curada al platino para decorar galletas y macarons en 20 segundos.
"""
            }
        ],
        "apa_references": [
            "BIGTREETECH & CMY Labs. (2026). *Panda Treat Food-Safe Inkjet Printing Module Specification*. BIQU Equipment.",
            "U.S. Food and Drug Administration. (2024). *Color additives approved for use in human food: 21 CFR*. FDA.",
            "cacs, & sIA Editora. (2026). *sIA Maker #03: BIQU Panda Treat y la Confitería Digital*. sIA Journal Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    },
    # sIA Dev 02 - Code Mode vs MCP - 4 de Noviembre de 2026
    "sIA_Dev_02_Code_Mode_vs_MCP_Cloudflare_Anthropic_2026-11-04.mp3": {
        "slug": "sia-dev-02-la-muerte-del-function-calling-code-mode-vs-mcp",
        "category": "Arquitectura de Agentes & IA",
        "badge_color": "blue",
        "read_time": "14 min",
        "title": "sIA Dev #02: La Muerte del Function Calling: Cómo Code Mode de Cloudflare y Anthropic Redujo MCP de 1.17M a 1,000 Tokens",
        "subtitle": "Por qué los LLMs son mediocres invocando herramientas JSON una por una, pero extraordinarios escribiendo código TypeScript en sandboxes V8.",
        "thesis": "La transición del paradigma de invocación secuencial de herramientas (JSON Tool Calling) hacia la síntesis programática de código ejecutable en sandboxes ligeros (Code Mode) elimina la inflación de contexto en servidores MCP masivos y reduce el consumo de tokens en un 99.9%.",
        "nexo": "Segundo episodio de sIA Dev: Evolución del protocolo MCP de Anthropic, V8 Isolates de Cloudflare, optimización de ventana de contexto y agentes autónomos.",
        "reel_video": "sIA_Reel_Stupy_08_CodeMode_vs_MCP.mp4",
        "content_blocks": [
            {
                "title": "1. La Crisis de Escalabilidad del Tool Calling Tradicional en MCP",
                "body": """
Cargar los esquemas JSON de los 2,500 endpoints de la API de Cloudflare en un servidor MCP tradicional consume 1.17 millones de tokens antes de que el usuario escriba su primera instrucción. Además, los modelos de lenguaje sufren degradación de razonamiento al encadenar decenas de llamadas JSON secuenciales (round-trips).
"""
            },
            {
                "title": "2. Code Mode y Sandboxes V8 Isolates: De 1.17 Millones a 1,000 Tokens",
                "body": """
En lugar de exponer miles de herramientas estáticas, Code Mode entrega al agente únicamente dos funciones: 'search()' y 'execute()'. El LLM consulta la documentación tipada bajo demanda y escribe un script completo en TypeScript que se ejecuta en milisegundos dentro de un Dynamic Worker V8 Isolate sin acceso a internet abierto, abatiendo el costo de contexto en un 99.9%.
"""
            }
        ],
        "apa_references": [
            "Cloudflare Engineering. (2026). *Code Mode: Executing MCP Servers in Dynamic Worker V8 Isolates*. Cloudflare Blog.",
            "Anthropic Research. (2026). *Scaling Model Context Protocol with Programmatic Code Execution*. Anthropic Publications.",
            "cacs, & sIA Editora. (2026). *sIA Dev #02: La Muerte del Function Calling (Code Mode vs MCP)*. sIA Journal Publications. / [escucha-sia](https://escucha-sia.github.io)"
        ]
    },'''

if "sia-sec-03-el-backdoor-de-xz-utils-y-los-500ms-que-salvaron-internet" not in content:
    content = content.replace("RESEARCH_DATABASE = {", "RESEARCH_DATABASE = {\n" + NEW_ENTRIES)
    build_mag_path.write_text(content, encoding="utf-8")
    print("[OK] Injected all 5 new episodes into RESEARCH_DATABASE in build_magazine.py")
else:
    print("[INFO] Entries already present in build_magazine.py")

subprocess.run([sys.executable, str(build_mag_path)], cwd=str(BASE_DIR), check=True)
print("[OK] Magazine rebuilt successfully!")
