import os
import json

# ======= GLOBAL SETTINGS =======
INPUT_DIR = "./log/raw/matches/updated"
OUTPUT_DIR = "./json/parsed_match_kills_temp"
MATCH_KEY = "Match was added to session"
os.makedirs(OUTPUT_DIR, exist_ok=True)
# ===============================

def parse_kill_data_from_line(line, existing_keys):
    kills = []

    try:
        json_part = line[line.find("{"):]
        data = json.loads(json_part)

        match_start = data["startTime"]
        match_end = data["endTime"]

        for clip_index, media in enumerate(data["medias"]):
            clip_start = media["startTime"]
            clip_end = media["endTime"]
            video_id = media["id"]
            video_path = media["path"]

            for kill_index, event in enumerate(media["events"]):
                kill_id = event["data"]
                kill_time = event["time"]
                timing = event.get("timing", {})

                key = (kill_id, video_id)
                if key in existing_keys:
                    continue

                structured = {
                    "kill_id": kill_id,
                    "video_clip_id": video_id,
                    "video_path": video_path,
                    "clip_index": clip_index,
                    "kill_order_within_clip": kill_index + 1,
                }

                kills.append((key, structured))
    except Exception as e:
        print(f"Error parsing line:\n{line}\nError: {e}")

    return kills

# ===== MAIN EXECUTION =====
for filename in os.listdir(INPUT_DIR):
    if not filename.endswith(".log"):
        continue

    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename.replace(".log", ".json"))

    # Load existing kills (if any)
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_keys = {(k["kill_id"], k["video_clip_id"]) for k in existing_data}
    new_data = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            if MATCH_KEY not in line:
                continue
            new_kills = parse_kill_data_from_line(line, existing_keys)
            for key, obj in new_kills:
                existing_keys.add(key)
                new_data.append(obj)

    if new_data:
        final_data = existing_data + new_data
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=2)
        print(f"✓ {filename}: {len(new_data)} new kills saved to {output_path}")
    else:
        print(f"- {filename}: No new kills found.")
