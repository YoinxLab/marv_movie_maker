import os
from pathlib import Path

# === CONFIGURATION ===
SOURCE_DIRS = [
    os.path.join(os.environ['LOCALAPPDATA'], "Overwolf", "Log", "Apps", "Outplayed"),
    "./log/raw/backup"
]
TARGET_DIR = "./log/raw"
ARCHIVE_FILE = os.path.join(TARGET_DIR, "1_op_full_raw.log")

# === LOAD EXISTING ARCHIVED LINES INTO MEMORY ===
def load_existing_lines(archive_path):
    if not os.path.exists(archive_path):
        return set()
    with open(archive_path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

# === PROCESS ALL SOURCE FILES ===
def backup_new_lines():
    existing_lines = load_existing_lines(ARCHIVE_FILE)
    total_new_lines = 0

    with open(ARCHIVE_FILE, "a", encoding="utf-8") as archive:
        for src_dir in SOURCE_DIRS:
            for root, _, files in os.walk(src_dir):
                for fname in files:
                    if fname.startswith("background"):
                        src_path = os.path.join(root, fname)
                        with open(src_path, "r", encoding="utf-8", errors="ignore") as src_file:
                            for line in src_file:
                                line_clean = line.strip()
                                if line_clean and line_clean not in existing_lines:
                                    archive.write(line)
                                    existing_lines.add(line_clean)
                                    total_new_lines += 1

    print(f"Backup complete. {total_new_lines} new lines added.")

# === RUN ===
if __name__ == "__main__":
    Path(TARGET_DIR).mkdir(parents=True, exist_ok=True)
    backup_new_lines()
