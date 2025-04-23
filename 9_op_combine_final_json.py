import os
import json

parsed_json_dir = './json/parsed_match_kills_temp'
log_dir = './log/kills_temp'
output_dir = './json/combined_temp'
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(parsed_json_dir):
    if not filename.endswith('.json'):
        continue

    json_path = os.path.join(parsed_json_dir, filename)
    log_filename = os.path.splitext(filename)[0] + '.log'
    log_path = os.path.join(log_dir, log_filename)

    if not os.path.exists(log_path):
        print(f"Log file not found for {filename}")
        continue

    # Build kill_id -> character_name map
    kill_character_map = {}
    with open(log_path, 'r', encoding='utf-8') as log_file:
        for line in log_file:
            if '| kill_id:' in line and '| character:' in line:
                parts = line.split('|')
                kill_id = parts[1].strip().split(':')[1].strip()
                character_name = parts[2].strip().split(':')[1].strip()
                kill_character_map[kill_id] = character_name

    # Load JSON and update with character_name
    with open(json_path, 'r', encoding='utf-8') as jf:
        kills = json.load(jf)

    for kill in kills:
        kill_id = kill.get('kill_id')
        character_name = kill_character_map.get(kill_id)
        kill['character_name'] = character_name if character_name else "Unknown"

    # Write updated JSON
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w', encoding='utf-8') as out_file:
        json.dump(kills, out_file, indent=2)

    print(f"Processed and saved: {output_path}")
