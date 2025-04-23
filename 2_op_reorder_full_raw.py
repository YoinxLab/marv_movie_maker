import re
from datetime import datetime

INPUT_LOG_FILE = './log/raw/1_op_full_raw.log'
OUTPUT_LOG_FILE = './log/raw/2_op_full_raw_reordered.log'

# Define the timestamp regex pattern (still matching from the beginning)
TIMESTAMP_PATTERN = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}'

def extract_timestamp(line):
    # Strip Byte Order Mark (BOM) and leading whitespace
    cleaned_line = line.lstrip('\ufeff').lstrip()
    match = re.match(TIMESTAMP_PATTERN, cleaned_line)
    if match:
        try:
            return datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S,%f')
        except ValueError:
            return None
    return None

def sort_log_by_timestamp(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    timestamped_lines = []
    for line in lines:
        timestamp = extract_timestamp(line)
        if timestamp:
            timestamped_lines.append((timestamp, line))
        else:
            print(f"Warning: Skipping line with no valid timestamp: {line.strip()}")

    timestamped_lines.sort(key=lambda x: x[0])

    with open(output_path, 'w', encoding='utf-8') as f:
        for _, line in timestamped_lines:
            f.write(line)

if __name__ == '__main__':
    sort_log_by_timestamp(INPUT_LOG_FILE, OUTPUT_LOG_FILE)
    print(f"Sorted log written to: {OUTPUT_LOG_FILE}")
