from pathlib import Path
from PIL import Image

# Paths are relative to the artifact root (the parent of python_codes).
REPO_ROOT = Path(__file__).resolve().parent.parent
# Place the original LivDet dataset under data/LivDet 2015, or change SRC_DIR.
SRC_DIR = REPO_ROOT / "data" / "LivDet 2015" / "Testing" / "Digital_Persona" / "Live"
DST_DIR = REPO_ROOT / "sourceafis-demo" / "livdet_preproc_png" / "Testing" / "Digital_Persona" / "Live"

DST_DIR.mkdir(parents=True, exist_ok=True)

png_files = sorted(SRC_DIR.glob("*.png"))

print(f"[i] Found {len(png_files)} png files")

for png_path in png_files:
    png_name = png_path.stem + ".png"
    dst_path = DST_DIR / png_name

    with Image.open(png_path) as img:
        img.save(dst_path, "PNG")

    print(f"[✓] {png_path.name} → {png_name}")

print("[✓] Conversion complete")