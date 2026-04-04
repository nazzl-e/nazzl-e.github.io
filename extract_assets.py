# extract_assets.py
import re, os, shutil
from pathlib import Path

HTML_FILE = "index.html"
OUTPUT_DIR = "extracted_assets"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

patterns = [
    r'src=["\']([^"\']+)["\']',
    r'href=["\']([^"\'http][^"\']+)["\']',
    r'url\(["\']?([^"\')\s]+)["\']?\)',
    r"src:\s*['\"]([^'\"]+)['\"]",        # JS object src:
    r"videoSrc:\s*['\"]([^'\"]+)['\"]",   # JS videoSrc:
    r"poster=['\"]([^'\"]+)['\"]",        # poster attributes
    r"poster:\s*['\"]([^'\"]+)['\"]",     # JS poster:
    r"img:\s*['\"]([^'\"]+)['\"]",        # JS img:
]

found = set()
for pattern in patterns:
    found.update(re.findall(pattern, html))

local_files = [
    f for f in found
    if not f.startswith(("http", "data:", "#", "//", "mailto"))
]

print(f"\n📋 Found {len(local_files)} local asset references:\n")
for f in sorted(local_files):
    exists = "✅" if Path(f).exists() else "❌ MISSING"
    print(f"  {exists}  {f}")

os.makedirs(OUTPUT_DIR, exist_ok=True)
copied, missing = [], []

for path in sorted(local_files):
    src = Path(path)
    if src.exists():
        dest = Path(OUTPUT_DIR) / src
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied.append(str(src))
    else:
        missing.append(str(src))

print(f"\n✅ Copied {len(copied)} files to '{OUTPUT_DIR}/'")
if missing:
    print(f"\n⚠️  {len(missing)} files not found:")
    for m in missing:
        print(f"   - {m}")