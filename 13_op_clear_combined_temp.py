import os

# MODIFY THIS PATH BEFORE RUNNING
TARGET_DIR = "./json/combined_temp"

def delete_all_files_in_directory(directory):
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    deleted_count = 0
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            try:
                os.remove(filepath)
                deleted_count += 1
                print(f"Deleted: {filepath}")
            except Exception as e:
                print(f"Failed to delete {filepath}: {e}")

    print(f"\nDone. Deleted {deleted_count} file(s).")

if __name__ == "__main__":
    delete_all_files_in_directory(TARGET_DIR)
