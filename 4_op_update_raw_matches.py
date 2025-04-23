import os
import shutil

SOURCE_DIR = "./log/raw/matches/temp"
TARGET_DIR = "./log/raw/matches/updated"

def read_file_lines(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()

def are_files_identical(file1_lines, file2_lines):
    return file1_lines == file2_lines

def is_subset(smaller, larger):
    return all(line in larger for line in smaller)

def main():
    os.makedirs(TARGET_DIR, exist_ok=True)

    for src_filename in os.listdir(SOURCE_DIR):
        if not src_filename.endswith(".log"):
            continue

        src_path = os.path.join(SOURCE_DIR, src_filename)
        src_lines = read_file_lines(src_path)

        found_identical = False
        for tgt_filename in os.listdir(TARGET_DIR):
            if not tgt_filename.endswith(".log"):
                continue

            tgt_path = os.path.join(TARGET_DIR, tgt_filename)
            tgt_lines = read_file_lines(tgt_path)

            if are_files_identical(src_lines, tgt_lines):
                print(f"Skipping {src_filename} (identical to {tgt_filename})")
                found_identical = True
                break

            elif is_subset(tgt_lines, src_lines):
                print(f"Overwriting incomplete file {tgt_filename} with {src_filename}")
                shutil.copy2(src_path, tgt_path)
                found_identical = True
                break

        if not found_identical:
            dst_path = os.path.join(TARGET_DIR, src_filename)
            counter = 1
            while os.path.exists(dst_path):
                name, ext = os.path.splitext(src_filename)
                dst_path = os.path.join(TARGET_DIR, f"{name}_{counter}{ext}")
                counter += 1
            print(f"Copying new file: {src_filename}")
            shutil.copy2(src_path, dst_path)

if __name__ == "__main__":
    main()
