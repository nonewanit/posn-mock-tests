#!/usr/bin/env python3
"""
Generate answer-sheet.tex for a mock test directory.
Compile with XeLaTeX to produce a 1-page Thai answer sheet PDF.

Usage:
    python3 generate_answer_sheet.py --test-dir mock-test-1
    python3 generate_answer_sheet.py --test-dir mock-test-1 --mc-total 55 --fillin-count 5
"""

import argparse
from pathlib import Path


# ── configurable defaults ──────────────────────────────────────────────
DEFAULT_CONFIG = {
    "mc_total": 55,        # total multiple-choice questions
    "mc_part1_end": 30,    # last question of part 1 (คณิตศาสตร์)
    "mc_cols": 5,          # columns for MC layout
    "fillin_start": 56,    # first fill-in question number
    "fillin_count": 5,     # number of fill-in questions
    "fillin_digits": 4,    # digits per fill-in answer
}


# ── LaTeX preamble ──────────────────────────────────────────────────────
def latex_preamble():
    return r"""% !TEX program = xelatex
\documentclass[12pt,a4paper]{article}
\usepackage{geometry}
\geometry{top=0.8cm, bottom=0.5cm, left=0.8cm, right=0.8cm}
\usepackage{fontspec}
\setmainfont{TH Sarabun New}[Scale=1.4]
\usepackage{tikz}
\usepackage{multirow}
\usepackage{array}
\usepackage{hhline}

% --- MC bubble with label inside ---
\newcommand{\mcbubble}[2]{%
  \begin{tikzpicture}[scale=1.0]
    \draw[thick] (0,0) circle (3.8pt);
    \node at (0,0.02) {\fontsize{6.5pt}{7pt}\selectfont #1};
  \end{tikzpicture}%
}

% --- MC question: number + 4 inline bubbles ---
\newcommand{\mcquestion}[1]{%
  \fontsize{8pt}{9pt}\selectfont #1.\hspace{1pt}%
  \mcbubble{ก}{}\hspace{1pt}%
  \mcbubble{ข}{}\hspace{1pt}%
  \mcbubble{ค}{}\hspace{1pt}%
  \mcbubble{ง}{}%
}

% --- digit column (0-9) ---
\newcommand{\digitcol}[1]{%
  \begin{tikzpicture}[scale=1.0]
    \foreach \y/\n in {0/9, 0.48/8, 0.96/7, 1.44/6, 1.92/5, 2.40/4, 2.88/3, 3.36/2, 3.84/1, 4.32/0} {
      \draw[thick] (0,\y) circle (3.8pt);
      \node at (0,\y) {\fontsize{7pt}{8pt}\selectfont \n};
    }
  \end{tikzpicture}%
}

% --- fill-in question: 4-column table ---
\newcommand{\fillinquestion}[2]{%
  \fontsize{10pt}{12pt}\selectfont \textbf{ข้อ #1} \\[0.5mm]
  \begin{tabular}{|c|c|c|c|}
  \hline
  \multicolumn{1}{|c|}{\fontsize{8pt}{9pt}\selectfont หลักพัน} &
  \multicolumn{1}{c|}{\fontsize{8pt}{9pt}\selectfont หลักร้อย} &
  \multicolumn{1}{c|}{\fontsize{8pt}{9pt}\selectfont หลักสิบ} &
  \multicolumn{1}{c|}{\fontsize{8pt}{9pt}\selectfont หลักหน่วย} \\
  \hline
  \digitcol{0} & \digitcol{1} & \digitcol{2} & \digitcol{3} \\
  \hline
  \end{tabular}%
}

\begin{document}
\pagestyle{empty}
"""


# ── LaTeX body generators ───────────────────────────────────────────────
def body_header():
    return r"""
% --- title ---
\begin{center}
{\fontsize{16pt}{18pt}\selectfont \textbf{กระดาษคำตอบ}}
\end{center}
\vspace{1mm}

% --- student info ---
\noindent
{\fontsize{10pt}{12pt}\selectfont
\textbf{ชื่อ-นามสกุล} \dotfill \hspace{1cm}
\textbf{ชั้น} \dotfill \hspace{1cm}
\textbf{ชื่อเล่น} \dotfill
}
\vspace{1mm}
"""


def mc_section_header(mc_first, mc_last):
    return rf"""
% --- multiple choice section ---
\noindent
{{\fontsize{{11pt}}{{13pt}}\selectfont \textbf{{ตอนที่ 1--2 ปรนัย (ข้อ {mc_first}--{mc_last})}}}} \hfill
{{\fontsize{{8pt}}{{9pt}}\selectfont \textbf{{คำเตือน:}} ระบายตัวเลือก \textbf{{เพียงข้อเดียว}} ในแต่ละข้อ ถ้าต้องการเปลี่ยนคำตอบ ให้ลบข้อเดิมออกก่อน}}

\vspace{{2mm}}
"""


def mc_part_header(part_label):
    return fr"""
\noindent
{{\fontsize{{10pt}}{{12pt}}\selectfont \textbf{{{part_label}}}}}
\vspace{{1mm}}
"""


def fillin_header(fs, fe):
    return rf"""
\vspace{{2mm}}
\noindent
{{\fontsize{{11pt}}{{13pt}}\selectfont \textbf{{ตอนที่ 3 อัตนัย เติมคำตอบ (ข้อ {fs}--{fe})}}}}
\vspace{{2mm}}

\noindent
{{\fontsize{{8pt}}{{9pt}}\selectfont \textbf{{วิธีระบาย:}} แต่ละข้อมี 4 หลัก (พัน ร้อย สิบ หน่วย) ให้ระบายตัวเลข\textbf{{หนึ่งตัวต่อหนึ่งหลัก}} หากคำตอบมีค่าน้อยกว่า 4 หลัก ให้ระบาย \textbf{{0}} นำหน้าในหลักที่สูงกว่า (เช่น ตอบ 42 ให้ระบาย หลักพัน=0, หลักร้อย=0, หลักสิบ=4, หลักหน่วย=2)}}
\vspace{{3mm}}
"""


def latex_footer():
    return r"""
\vfill
\begin{center}
{\fontsize{8pt}{9pt}\selectfont จัดทำโดย พี่หยวน}
\end{center}
\end{document}
"""


# ── body builder ────────────────────────────────────────────────────────
def build_body(config):
    """Generate the body of the answer sheet."""
    mc_total = config["mc_total"]
    mc_part1_end = config["mc_part1_end"]
    mc_cols = config["mc_cols"]
    fs = config["fillin_start"]
    fc = config["fillin_count"]
    fd = config["fillin_digits"]

    parts = []

    # ── MC section ──────────────────────────────────────────────────
    parts.append(mc_section_header(1, mc_total))

    col_w = 1.0 / mc_cols

    def build_mc_grid(start_q, count):
        """Build a tabular grid of MC questions: count questions, mc_cols columns."""
        rows = (count + mc_cols - 1) // mc_cols
        grid = []
        grid.append(r"\noindent")
        grid.append(r"\begin{tabular}{%s}" % ("p{0.18\\textwidth}" * mc_cols))
        for r in range(rows):
            row_cells = []
            for c in range(mc_cols):
                q = start_q + r + c * rows
                if q < start_q + count:
                    row_cells.append(r"\mcquestion{%d}" % q)
                else:
                    row_cells.append("")
            grid.append(" & ".join(row_cells) + r" \\[1pt]")
        grid.append(r"\end{tabular}")
        return grid

    # Part 1: คณิตศาสตร์
    parts.append(mc_part_header(f"คณิตศาสตร์ (ข้อ 1–{mc_part1_end})"))
    parts.extend(build_mc_grid(1, mc_part1_end))

    parts.append(r"\vspace{2mm}")

    # Part 2: วิทยาการคำนวณ
    mc_part2_start = mc_part1_end + 1
    mc_part2_count = mc_total - mc_part1_end
    parts.append(mc_part_header(f"วิทยาการคำนวณ (ข้อ {mc_part2_start}–{mc_total})"))
    parts.extend(build_mc_grid(mc_part2_start, mc_part2_count))

    # ── fill-in section ─────────────────────────────────────────────
    fe = fs + fc - 1
    parts.append(fillin_header(fs, fe))

    # Lay out fill-in questions (3 per row)
    parts.append(r"\noindent\centering")
    fillin_qs = list(range(fs, fe + 1))
    fw = 0.32  # minipage width per fill-in question
    for i in range(0, len(fillin_qs), 3):
        row = []
        for j in range(3):
            if i + j < len(fillin_qs):
                q = fillin_qs[i + j]
                row.append(r"\fillinquestion{%d}{%d}" % (q, fd))
        for cell in row:
            parts.append(r"\begin{minipage}[t]{%0.2f\textwidth}\centering" % fw)
            parts.append(cell)
            parts.append(r"\end{minipage}")
        parts.append(r"\\[2mm]")

    return "\n".join(parts)


# ── main ─────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate answer-sheet.tex")
    parser.add_argument("--test-dir", default="mock-test-1")
    parser.add_argument("--mc-total", type=int, default=55)
    parser.add_argument("--mc-part1-end", type=int, default=30)
    parser.add_argument("--mc-cols", type=int, default=5)
    parser.add_argument("--fillin-start", type=int, default=56)
    parser.add_argument("--fillin-count", type=int, default=5)
    parser.add_argument("--fillin-digits", type=int, default=4)
    args = parser.parse_args()

    test_dir = Path(args.test_dir)
    output_file = test_dir / "answer-sheet.tex"

    config = {
        "mc_total": args.mc_total,
        "mc_part1_end": args.mc_part1_end,
        "mc_cols": args.mc_cols,
        "fillin_start": args.fillin_start,
        "fillin_count": args.fillin_count,
        "fillin_digits": args.fillin_digits,
    }

    body = build_body(config)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(latex_preamble())
        f.write(body_header())
        f.write(body)
        f.write(latex_footer())

    print(f"Generated: {output_file}")
    print(f"  MC: {config['mc_total']} questions ({config['mc_cols']} cols), "
          f"Fill-in: {config['fillin_count']} questions")


if __name__ == "__main__":
    main()
