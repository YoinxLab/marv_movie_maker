import os
import json
import re

SOURCE_DIR = "./log/raw/matches/updated"
OUTPUT_DIR = "./log/kills_temp"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_inner_json(escaped_string):
    try:
        return json.loads(escaped_string)
    except json.JSONDecodeError as e:
        print(f"[!] Failed to parse inner JSON: {e}")
        return None

def process_file(file_path):
    kill_lines = []
    last_kill_count = 0  # start at 0, so we NEVER log kill_id 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if 'Got Info Update:' not in line or '"roster_' not in line:
                continue

            timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})', line)
            timestamp = timestamp_match.group(1) if timestamp_match else "UNKNOWN"

            try:
                json_chunk = re.search(r'Got Info Update: (.*)$', line).group(1)
                outer_json = json.loads(json_chunk)
            except Exception as e:
                print(f"[!] Failed to parse outer JSON: {e}")
                continue

            match_info = outer_json.get("info", {}).get("match_info", {})
            for key, value in match_info.items():
                if not key.startswith("roster_") or not isinstance(value, str):
                    continue

                inner = parse_inner_json(value)
                if not inner:
                    continue

                if inner.get("is_local") is True:
                    current_kills = int(inner.get("kills", 0))
                    character = inner.get("character_name", "UNKNOWN")

                    # ✅ Skip kill_id 0, only log kill_id > 0
                    if current_kills > last_kill_count and current_kills > 0:
                        for new_kill_id in range(last_kill_count + 1, current_kills + 1):
                            kill_lines.append(f"{timestamp} | kill_id: {new_kill_id} | character: {character}\n")
                        last_kill_count = current_kills

    return kill_lines

def main():
    for filename in os.listdir(SOURCE_DIR):
        if not filename.endswith(".log"):
            continue

        src_path = os.path.join(SOURCE_DIR, filename)
        out_path = os.path.join(OUTPUT_DIR, filename)

        print(f"Processing: {filename}")
        output_lines = process_file(src_path)

        if output_lines:
            with open(out_path, "w", encoding="utf-8") as f:
                f.writelines(output_lines)
            print(f"✅ {len(output_lines)} kills written to {out_path}")
        else:
            print(f"⚠️  No kills found in {filename}")

if __name__ == "__main__":
    main()
