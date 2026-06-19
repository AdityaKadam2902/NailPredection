#!/usr/bin/env python3
"""Rename dataset folders to match expected class names."""

import os
from pathlib import Path

FOLDER_MAP = {
    "aloperia areata": "Alopecia areata",
    "beau_s lines": "Beau's lines",
    "Darier_s disease": "Darier's disease",
    "Muehrck-e_s lines": "Muehrcke's lines",
    "onycholycis": "Onycholysis",
    "splinter hemmorrage": "Splinter hemorrhage",
    "terry_s_nail": "Terry's nail",
    "half and half nailes (Lindsay_s nails)": "Half and half nails (Lindsay's nails)",
}

def rename_folders(data_dir="data"):
    data_path = Path(data_dir)
    renamed = 0

    for split in ["train", "test"]:
        split_path = data_path / split
        if not split_path.exists():
            print(f"⚠ {split}/ not found")
            continue

        print(f"\nProcessing {split}/...")

        for old_name, new_name in FOLDER_MAP.items():
            old_path = split_path / old_name
            new_path = split_path / new_name

            if not old_path.exists():
                if new_path.exists():
                    print(f"  ✓ Already correct: {new_name}")
                continue

            if new_path.exists():
                print(f"  → Merging: {old_name} into {new_name}")
                import shutil
                for file in old_path.iterdir():
                    if file.is_file():
                        target = new_path / file.name
                        if target.exists():
                            target = new_path / f"merged_{file.name}"
                        shutil.move(str(file), str(target))
                shutil.rmtree(old_path)
                print(f"  ✓ Merged & removed: {old_name}")
            else:
                old_path.rename(new_path)
                print(f"  ✓ Renamed: {old_name} → {new_name}")

            renamed += 1

    print(f"\nDone! Renamed {renamed} folders")
    print("\nNext: python scripts/train.py")

if __name__ == "__main__":
    rename_folders()
