import os
import random
import shutil
from pathlib import Path

mapping = {
    "01": "Akhal-Teke",
    "02": "Appaloosa",
    "03": "Orlov-Trotter",
    "04": "Vladimir-Heavy-Draft",
    "05": "Percheron",
    "06": "Arabian",
    "07": "Friesian",
}

random.seed(42)
src = Path("data/raw_images")
dst = Path("horsebreed")
splits = {"train": 0.7, "val": 0.2, "test": 0.1}

# 預先建立目錄
for split in splits:
    for breed in mapping.values():
        (dst / split / breed).mkdir(parents=True, exist_ok=True)

for code, breed in mapping.items():
    files = sorted(src.glob(f"{code}_*.png"))
    random.shuffle(files)
    n = len(files)
    n_train = int(n * splits["train"])
    n_val = int(n * splits["val"])
    splits_idx = {
        "train": files[:n_train],
        "val": files[n_train:n_train + n_val],
        "test": files[n_train + n_val:]
    }
    for split, split_files in splits_idx.items():
        for f in split_files:
            shutil.copy2(f, dst / split / breed / f.name)
