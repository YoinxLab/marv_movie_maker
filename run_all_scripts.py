import subprocess
import time
from pathlib import Path

# === [ SCRIPT LIST - MODIFY THESE PATHS AS NEEDED ] ===
SCRIPT_PATHS = [
    "1_op_update_full_raw.py",
    "2_op_reorder_full_raw.py",
    "3_op_split_full_by_match.py",
    "4_op_update_raw_matches.py",
    "5_op_cleanup_temp_matches.py",
    "6_op_parse_match_kills.py",
    "7_op_parse_match_info.py",
    "8_op_parse_kill_lines.py",
    "9_op_combine_final_json.py",
    "10_op_clear_matchkills_temp.py",
    "11_op_clear_kills_temp.py",
    "12_op_update_kill_data.py",
    "13_op_clear_combined_temp.py"
]
# =======================================================

def run_script(script_path):
    if not Path(script_path).is_file():
        print(f"[SKIPPED] Script not found: {script_path}")
        return

    print(f"[RUNNING] {script_path}")
    try:
        result = subprocess.run(["python", script_path], check=True)
        print(f"[COMPLETED] {script_path} with return code {result.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {script_path} failed with return code {e.returncode}")
    except Exception as e:
        print(f"[EXCEPTION] {script_path} failed: {e}")

def main():
    for script in SCRIPT_PATHS:
        run_script(script)
        time.sleep(1)  # Optional delay between scripts

if __name__ == "__main__":
    main()
