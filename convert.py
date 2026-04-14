import os
import sys
import shutil

targetDir = sys.argv[1]
outDir = f"{targetDir}_out"
EDIT_FILE = "files.txt"
if os.path.exists(EDIT_FILE):
    os.makedirs(outDir, exist_ok=True)
    filenames = open(EDIT_FILE, encoding="utf8").readlines()
    for index, filename in enumerate(os.listdir(targetDir)):
        shutil.copyfile(
            f"{targetDir}/{filename.strip()}",
            f"{outDir}/{filenames[index].strip()}",
        )
    os.remove(EDIT_FILE)
    print("converted.")
else:
    filenames = open(EDIT_FILE, "w", encoding="utf8")
    for f in os.listdir(targetDir):
        filenames.write(f"{f}\n")
    print(EDIT_FILE)
