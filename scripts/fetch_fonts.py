"""Install the real fonts used by the original report into fonts/.

    python scripts/fetch_fonts.py

The original PDF uses three fonts: Arial, Arial Bold and Arial Narrow Bold.

* Arial / Arial Bold: the genuine Microsoft TrueType files, taken from Microsoft's
  freely distributed "core fonts for the web" package (arial32.exe). Needs `cabextract`.
* Arial Narrow Bold: not freely downloadable. If it is installed on the system
  (e.g. Windows/Office), copy it to fonts/ArialNarrow-Bold.ttf. Otherwise the real
  Arial Narrow Bold glyphs embedded in reference/original.pdf are extracted. These cover
  every character the report prints in that font (TOTAL, COMPENTENCY LEVEL, the
  "Grade X (...)" labels).
* Any character missing from those falls back to Liberation Sans Narrow Bold
  (metric-compatible, bundled in fonts/fallback/). That is the only substitute.

The Microsoft files are not committed to git (licence); run this script instead.
"""

import io
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"
COREFONTS_URL = "https://downloads.sourceforge.net/corefonts/arial32.exe"


def fetch_arial():
    if (FONTS / "arial.ttf").exists() and (FONTS / "arialbd.ttf").exists():
        print("Arial, Arial Bold: already present")
        return
    if not shutil.which("cabextract"):
        sys.exit("cabextract is required (apt install cabextract / dnf install cabextract)")
    with tempfile.TemporaryDirectory() as tmp:
        exe = Path(tmp) / "arial32.exe"
        print("downloading", COREFONTS_URL)
        with urllib.request.urlopen(COREFONTS_URL) as r:
            exe.write_bytes(r.read())
        subprocess.run(["cabextract", "-q", "-L", "-d", tmp, str(exe)], check=True)
        for name in ("arial.ttf", "arialbd.ttf"):
            shutil.copy(Path(tmp) / name, FONTS / name)
    print("Arial, Arial Bold: installed from Microsoft core fonts")


def fetch_arial_narrow_bold():
    target = FONTS / "ArialNarrow-Bold.ttf"
    if target.exists():
        print("Arial Narrow Bold: already present")
        return
    # 1) a real installed copy
    try:
        out = subprocess.run(["fc-match", "-f", "%{file}|%{fullname}", "Arial Narrow:bold"],
                             capture_output=True, text=True).stdout
        path, _, full = out.partition("|")
        if "Arial Narrow Bold" in full and Path(path).exists():
            shutil.copy(path, target)
            print("Arial Narrow Bold: copied from system", path)
            return
    except FileNotFoundError:
        pass
    # 2) the real glyphs embedded in the original PDF
    original = ROOT / "reference" / "original.pdf"
    if not original.exists():
        print("Arial Narrow Bold: not found; the fallback (Liberation Sans Narrow Bold) will be used")
        return
    import pypdf
    from fontTools.ttLib import TTFont

    for page in pypdf.PdfReader(original).pages:
        for font in page["/Resources"]["/Font"].values():
            desc = font.get_object()["/DescendantFonts"][0].get_object()["/FontDescriptor"].get_object()
            if "/FontFile2" not in desc:
                continue
            data = desc["/FontFile2"].get_object().get_data()
            if TTFont(io.BytesIO(data))["name"].getDebugName(4) == "Arial Narrow Bold":
                target.write_bytes(data)
                print("Arial Narrow Bold: extracted from", original.relative_to(ROOT))
                return
    print("Arial Narrow Bold: not embedded in original; fallback will be used")


if __name__ == "__main__":
    FONTS.mkdir(exist_ok=True)
    fetch_arial()
    fetch_arial_narrow_bold()
