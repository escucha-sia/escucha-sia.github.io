import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Carlos\noticias_podcast")
src_reel = BASE_DIR / "reels" / "sIA_Terror_01_Las_Escaleras_Reel.mp4"
dst1 = Path(r"C:\Users\c_a_c\Music\NoticIAs\Reels") / src_reel.name
dst2 = Path(r"G:\Mi unidad\sIA_Hub\01_Reels_Verticales") / src_reel.name

shutil.copy2(src_reel, dst1)
print(f"[OK] Copied to Music: {dst1.exists()} ({dst1.stat().st_size} bytes)")

if dst2.parent.exists():
    shutil.copy2(src_reel, dst2)
    print(f"[OK] Copied to Google Drive: {dst2.exists()} ({dst2.stat().st_size} bytes)")
else:
    print("[!] Google Drive directory not accessible")
