import os
from datetime import datetime

# === CONFIGURATION ===
input_log_file = "./log/raw/2_op_full_raw_reordered.log"
output_dir = "./log/raw/matches/temp"

# === SCRIPT START ===
os.makedirs(output_dir, exist_ok=True)

writing = False
log_counter = 1
out_file = None

with open(input_log_file, 'r', encoding='utf-8-sig') as infile:
    for line in infile:
        # Start of new match block
        if "Got Info Update:" in line and '"game_mode":"' in line:
            if out_file:
                out_file.close()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"match_log_{log_counter:03}_{timestamp}.log"
            out_path = os.path.join(output_dir, filename)
            out_file = open(out_path, 'w', encoding='utf-8')
            writing = True
            log_counter += 1
            out_file.write(line)
        elif writing:
            out_file.write(line)
            if "Creating new dummy match" in line:
                out_file.close()
                out_file = None
                writing = False

# Final safeguard
if out_file:
    out_file.close()

print(f"✅ Done. {log_counter - 1} match log(s) written to: {output_dir}")
