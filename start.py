import os
import shutil
import urllib.request
import zipfile

ZIP_URL = "https://github.com/TAMAGO55123/SOB/releases/latest/download/sob.zip"
NOTUPDATE_URL = "https://github.com/TAMAGO55123/SOB/releases/latest/download/notupdate.txt"

TEMP_DIR = "_update_temp"

print("Downloading latest SOB...")
urllib.request.urlretrieve(ZIP_URL, "sob.zip")

print("Downloading notupdate list...")
urllib.request.urlretrieve(NOTUPDATE_URL, "notupdate.txt")

print("Reading exclude list...")
exclude = []
with open("notupdate.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            exclude.append(line.rstrip("/"))

print("Extracting ZIP to temp folder...")
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)
os.makedirs(TEMP_DIR, exist_ok=True)

with zipfile.ZipFile("sob.zip", "r") as z:
    z.extractall(TEMP_DIR)

# ZIP の中のフォルダ名を自動検出
root_folder = os.listdir(TEMP_DIR)[0]
root_path = os.path.join(TEMP_DIR, root_folder)

print("Copying files (excluding listed files)...")

for root, dirs, files in os.walk(root_path):
    rel = os.path.relpath(root, root_path)
    if rel == ".":
        rel = ""

    # フォルダ除外（前方一致）
    if any(rel.startswith(ex) for ex in exclude):
        continue

    target_dir = os.path.join(".", rel)
    os.makedirs(target_dir, exist_ok=True)

    for file in files:
        rel_file = os.path.join(rel, file)

        # ファイル除外（前方一致）
        if any(rel_file.startswith(ex) for ex in exclude):
            continue

        src = os.path.join(root, file)
        dst = os.path.join(".", rel_file)

        shutil.copy2(src, dst)

print("Cleaning temp folder...")
shutil.rmtree(TEMP_DIR)

print("Starting bot...")
os.system("python3 main.py")
