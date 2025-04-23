import os
import json
import re

LOG_DIR = './log/raw/matches/updated'
JSON_DIR = './json/parsed_match_kills_temp'

# Regex patterns
GAME_MODE_RE = re.compile(r'"game_mode":"(.*?)"')
GAME_TYPE_RE = re.compile(r'"game_type":"(.*?)"')
MAP_RE = re.compile(r'"map":"(.*?)"')

def extract_metadata(log_path):
    game_mode = game_type = map_name = "Unknown"
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            if game_mode == "Unknown" and (match := GAME_MODE_RE.search(line)):
                game_mode = match.group(1)
            elif game_type == "Unknown" and (match := GAME_TYPE_RE.search(line)):
                game_type = match.group(1)
            elif map_name == "Unknown" and (match := MAP_RE.search(line)):
                map_name = match.group(1)
            if game_mode != "Unknown" and game_type != "Unknown" and map_name != "Unknown":
                break
    return game_mode, game_type, map_name

def update_json(json_path, game_mode, game_type, map_name):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for kill in data:
        kill['game_mode'] = game_mode
        kill['game_type'] = game_type
        kill['map'] = map_name

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def main():
    for log_filename in os.listdir(LOG_DIR):
        if not log_filename.endswith('.log'):
            continue

        name_without_ext = os.path.splitext(log_filename)[0]
        log_path = os.path.join(LOG_DIR, log_filename)
        json_path = os.path.join(JSON_DIR, f'{name_without_ext}.json')

        if not os.path.exists(json_path):
            print(f'Skipping: No JSON file for {log_filename}')
            continue

        game_mode, game_type, map_name = extract_metadata(log_path)
        update_json(json_path, game_mode, game_type, map_name)
        print(f'Updated: {json_path} with metadata - Mode: {game_mode}, Type: {game_type}, Map: {map_name}')

if __name__ == '__main__':
    main()
