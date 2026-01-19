import json
import re
from pathlib import Path

INPUT_FILE = Path("input.json")
OUTPUT_FILE = Path("intput_merge.json")

def is_likely_hyphen_break(prev_text, next_text):
    if not prev_text or not next_text:
        return False
    prev_clean = prev_text.rstrip()
    if not prev_clean:
        return False
    last_char = prev_clean[-1]
    if last_char not in ('-', '\xad'):
        return False
    if len(prev_clean) < 2:
        return False
    if not prev_clean[-2].isalpha():
        return False
    if not next_text[0].islower():
        return False
    return True

def merge_hyphen_breaks(blocks):
    result = []
    i = 0
    merge_count = 0
    while i < len(blocks):
        current = blocks[i].copy()
        if i + 1 < len(blocks) and is_likely_hyphen_break(current["text"], blocks[i + 1]["text"]):
            next_block = blocks[i + 1]
            prev_clean = current["text"].rstrip(' -\xad\u200b\u200c\u200d')
            merged_text = prev_clean + next_block["text"]
            current["text"] = merged_text
            i += 2
            merge_count += 1
        else:
            i += 1
        result.append(current)
    print(f"Performed {merge_count} merges")
    return result

def main():
    print(f"Reading {INPUT_FILE}")
    blocks = []
    with INPUT_FILE.open(encoding="utf-8") as f:
        for line_nr, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                block = json.loads(line)
                if "text" not in block or not isinstance(block["text"], str):
                    continue
                blocks.append(block)
            except json.JSONDecodeError:
                print(f"JSON error on line {line_nr}")
                continue
    print(f"Loaded {len(blocks)} blocks")
    fixed_blocks = merge_hyphen_breaks(blocks)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for block in fixed_blocks:
            json.dump(block, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

