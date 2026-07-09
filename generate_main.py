#!/usr/bin/env python3
"""
generate_main.py — Generate main.tex from problem files in problems/ directory.

Scans problems/ton1/, problems/ton2/, problems/ton3/ recursively for .tex files.
Each .tex file must have a "% topic: <key>" comment on its first line.
Questions within each ton are randomly shuffled using a fixed seed for reproducibility.

Usage:
    python generate_main.py --test-dir mock-test-1              # Generate for a specific mock test
    python generate_main.py --test-dir mock-test-1 --seed 123   # Use a different seed
    python generate_main.py -h                                  # Show help
"""

import sys
import argparse
import random
from pathlib import Path

# =============================================================================
# CONFIGURATION — Edit these values as needed
# =============================================================================

# Default random seed: change this to get a different shuffle.
# The same seed always produces the same question order.
DEFAULT_SEED = 42

# Default mock test directory
DEFAULT_TEST_DIR = "mock-test-1"

# Section configuration per ton (in order they appear in the exam)
# {count}, {start}, {end} are filled in automatically from the actual file counts.
# Set "shuffle": False to keep original file order (e.g. when difficulty increases per question).
TON_SECTIONS = [
    {
        "ton": "ton1",
        "header": "ตอนที่ 1 คณิตศาสตร์ จำนวน {count} ข้อ (ข้อ {start}--{end}) ข้อละ 1 คะแนน",
        "shuffle": True,
    },
    {
        "ton": "ton2",
        "header": "ตอนที่ 2 วิทยาการคำนวณ จำนวน {count} ข้อ (ข้อ {start}--{end}) ข้อละ 1 คะแนน",
        "shuffle": False,   # difficulty increases respectively — keep order
        "topic_order": {"programming": 0, "algorithms": 1},
    },
    {
        "ton": "ton3",
        "header": "ตอนที่ 3 วิทยาการคำนวณ แบบอัตนัย (เติมคำตอบ) จำนวน {count} ข้อ (ข้อ {start}--{end}) ข้อละ 2 คะแนน",
        "shuffle": True,
    },
]


# =============================================================================
# Core logic
# =============================================================================

def find_problem_files(problems_dir):
    """
    Scan problems/ directory recursively for .tex files.
    Returns: dict mapping ton_name -> list of (topic, filepath_relative_to_test_dir)
    """
    test_dir = problems_dir.parent
    problems = {}
    for ton_dir in sorted(problems_dir.iterdir()):
        if not ton_dir.is_dir():
            continue
        ton = ton_dir.name
        problems[ton] = []

        for tex_file in sorted(ton_dir.rglob("*.tex")):
            topic = read_topic(tex_file)
            # Store path relative to the test directory (e.g. mock-test-1)
            rel_path = tex_file.relative_to(test_dir)
            problems[ton].append((topic, rel_path))

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
    lines.append("% !TEX program = xelatex")
    lines.append("\\documentclass[16pt,a4paper]{article} % ใช้ขนาดฟอนต์ 16pt ตามมาตรฐานข้อสอบไทย")
    lines.append("\\input{../preamble.tex}")
    lines.append("")
    lines.append("\\begin{document}")

    question_start = 1

    for section in TON_SECTIONS:
        ton = section["ton"]
        if ton not in problems or not problems[ton]:
            continue

        # Collect all file paths for this ton
        file_paths = [fp for _, fp in problems[ton]]
        # Shuffle if enabled for this ton, otherwise keep numeric order
        if section.get("shuffle", True):
            rng.shuffle(file_paths)
        else:
            # Sort by (topic_order, stem): programming first, then algorithms
            topic_order = section.get("topic_order", {})
            file_paths.sort(key=lambda p: (
                topic_order.get(p.parent.name, 99),
                int(p.stem) if p.stem.isdigit() else p.stem
            ))

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

        # Input each problem (wrapped in samepage to prevent mid-question page breaks)
        for fp in file_paths:
            rel_path = str(fp).replace("\\", "/")
            lines.append("\\begin{samepage}")
            lines.append(f"\\input{{{rel_path}}}")
            lines.append("\\end{samepage}")
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
    parser = argparse.ArgumentParser(
        description="Generate main.tex from problem files in problems/ directory."
    )
    parser.add_argument(
        "--test-dir", default=DEFAULT_TEST_DIR,
        help=f"Mock test directory (default: {DEFAULT_TEST_DIR})",
    )
    parser.add_argument(
        "--seed", type=int, default=DEFAULT_SEED,
        help=f"Random seed for shuffling (default: {DEFAULT_SEED})",
    )
    args = parser.parse_args()

    test_dir = Path(args.test_dir)
    problems_dir = test_dir / "problems"
    output_file = test_dir / "main.tex"

    if not problems_dir.is_dir():
        print(f"Error: problems/ directory not found in {test_dir}")
        sys.exit(1)

    print(f"Test directory: {test_dir}")
    print(f"Using seed: {args.seed}")

    problems = find_problem_files(problems_dir)
    print_summary(problems)

    generate_main_tex(problems, output_file, args.seed)
    print(f"\nGenerated: {output_file}")

    # Ensure .latexmkrc symlink exists in the test directory
    latexmkrc = test_dir / ".latexmkrc"
    if not latexmkrc.exists():
        latexmkrc.symlink_to("../.latexmkrc")
        print(f"Created: {latexmkrc}")


if __name__ == "__main__":
    main()
