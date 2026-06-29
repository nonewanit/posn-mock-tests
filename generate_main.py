#!/usr/bin/env python3
"""
generate_main.py — Generate main.tex from problem files in problems/ directory.

Scans problems/ton1/, problems/ton2/, problems/ton3/ recursively for .tex files.
Each .tex file must have a "% topic: <key>" comment on its first line.
Questions within each ton are randomly shuffled using a fixed seed for reproducibility.

Usage:
    python generate_main.py              # Generate main.tex with default seed
    python generate_main.py --seed 123   # Use a different seed
    python generate_main.py -h           # Show help
"""

import sys
import random
from pathlib import Path

# =============================================================================
# CONFIGURATION — Edit these values as needed
# =============================================================================

# Random seed: change this to get a different shuffle.
# The same seed always produces the same question order.
SEED = 42

# Directory containing problem files
PROBLEMS_DIR = Path("problems")

# Output file
OUTPUT_FILE = Path("main.tex")

# Section configuration per ton (in order they appear in the exam)
# {count}, {start}, {end} are filled in automatically from the actual file counts.
TON_SECTIONS = [
    {
        "ton": "ton1",
        "header": "ตอนที่ 1 คณิตศาสตร์ จำนวน {count} ข้อ (ข้อ {start}--{end}) ข้อละ 1 คะแนน",
    },
    {
        "ton": "ton2",
        "header": "ตอนที่ 2 วิทยาการคำนวณ จำนวน {count} ข้อ (ข้อ {start}--{end}) ข้อละ 1 คะแนน",
    },
    {
        "ton": "ton3",
        "header": "ตอนที่ 3 วิทยาการคำนวณ แบบอัตนัย (เติมคำตอบ) จำนวน {count} ข้อ (ข้อ {start}--{end}) ข้อละ 2 คะแนน",
    },
]


# =============================================================================
# Core logic
# =============================================================================

def find_problem_files(problems_dir):
    """
    Scan problems/ directory recursively for .tex files.
    Returns: dict mapping ton_name -> list of (topic, filepath)
    """
    problems = {}
    for ton_dir in sorted(problems_dir.iterdir()):
        if not ton_dir.is_dir():
            continue
        ton = ton_dir.name
        problems[ton] = []

        for tex_file in sorted(ton_dir.rglob("*.tex")):
            topic = read_topic(tex_file)
            problems[ton].append((topic, tex_file))

    return problems


def read_topic(filepath):
    """
    Read the % topic: marker from the first line of a .tex file.
    Returns the topic key string, or "unknown" if no marker found.
    """
    with open(filepath, "r", encoding="utf-8-sig") as f:
        first_line = f.readline().strip()
    if first_line.startswith("% topic:"):
        return first_line[len("% topic:"):].strip()
    return "unknown"


def generate_main_tex(problems, output_file, seed):
    """
    Generate main.tex from collected problem files.

    For each ton, questions are randomly shuffled using the given seed.
    Same-topic questions may appear consecutively — pure random shuffle within each ton.
    """
    rng = random.Random(seed)

    lines = []
    lines.append("\\documentclass[16pt,a4paper]{article} % ใช้ขนาดฟอนต์ 16pt ตามมาตรฐานข้อสอบไทย")
    lines.append("\\input{preamble.tex}")
    lines.append("")
    lines.append("\\begin{document}")

    question_start = 1

    for section in TON_SECTIONS:
        ton = section["ton"]
        if ton not in problems or not problems[ton]:
            continue

        # Collect all file paths for this ton and shuffle
        file_paths = [fp for _, fp in problems[ton]]
        rng.shuffle(file_paths)

        count = len(file_paths)
        question_end = question_start + count - 1

        # Section header with computed question range
        header = section["header"].format(
            count=count,
            start=question_start,
            end=question_end,
        )

        lines.append("")
        lines.append(f"% ========= {ton} ============")
        lines.append(f"\\examsection{{{header}}}")
        lines.append("")

        # Input each shuffled problem
        for fp in file_paths:
            rel_path = str(fp).replace("\\", "/")
            lines.append(f"\\input{{{rel_path}}}")
            lines.append("")

        lines.append("\\pagebreak")

        question_start = question_end + 1

    lines.append("\\end{document}")
    lines.append("")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return lines


def print_summary(problems):
    """Print a summary of found problems grouped by ton and topic."""
    for ton in sorted(problems.keys()):
        topics = {}
        for topic, fp in problems[ton]:
            topics.setdefault(topic, []).append(fp.name)

        print(f"\n{ton}: {len(problems[ton])} questions")
        for topic, files in sorted(topics.items()):
            print(f"  {topic}: {len(files)} file(s) — {', '.join(files)}")


def main():
    global SEED

    # Parse command-line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--seed" and len(sys.argv) > 2:
            SEED = int(sys.argv[2])
        elif sys.argv[1] in ("-h", "--help"):
            print(__doc__)
            return

    print(f"Using seed: {SEED}")

    problems = find_problem_files(PROBLEMS_DIR)
    print_summary(problems)

    generate_main_tex(problems, OUTPUT_FILE, SEED)
    print(f"\nGenerated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
