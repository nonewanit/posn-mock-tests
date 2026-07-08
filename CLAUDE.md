# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build

Each mock test builds independently from its own directory:

```bash
cd mock-test-1
xelatex -no-pdf -interaction=nonstopmode main.tex
xdvipdfmx main.xdv
```

The shared `preamble.tex` is referenced via `\input{../preamble.tex}` from each mock test's `main.tex`.

XeLaTeX is required (not pdfLaTeX) because `fontspec` is used for Thai font support. The document uses **TH Sarabun New** font, which must be installed on the system. On Overleaf, the font file needs to be uploaded into the project.

Build outputs: `.aux`, `.log`, `.pdf`, `.xdv` — these are generated files, never commit them.

## Architecture

Multi-file LaTeX project for Thai-language POSN (Promotion of Science and Mathematics Talented) 1st Qualification exam papers. The repo supports multiple mock tests, each in its own self-contained folder sharing a common `preamble.tex`.

```
preamble.tex          — shared packages, fonts, geometry, header config, custom commands (used by all mock tests)
.gitignore            — ignores LaTeX build artifacts (*.aux, *.log, *.xdv, *.synctex.gz, etc.)

mock-test-1/          — Mock Test 1 (60 questions: 30 math + 25 CS MCQ + 5 CS written)
  main.tex            — document skeleton for this mock test
  images/             — images for this mock test, named as tonX-category-NN.ext
  problems/
    ton1/             — Part 1: Math (multiple choice, 4 choices per question)
      01.tex .. 30.tex (across subfolders: counting, equations, functions, geometry, logic, number-theory, real-numbers, sequences, sets)
    ton2/             — Part 2: Computer Science (multiple choice)
      01.tex .. 25.tex (across subfolders: algorithms, programming)
    ton3/             — Part 3: Computer Science (written/fill-in, no choices)
      01.tex .. 05.tex

mock-test-2/          — Mock Test 2 (future), same structure
  main.tex
  images/
  problems/
    ton1/
    ton2/
    ton3/
```

To add a new question to a mock test: create `mock-test-N/problems/tonX/category/NN.tex` with just the `\question` body and `\choices*` call, then add `\input{problems/tonX/category/NN.tex}` in that test's `main.tex` under the right section.

To create a new mock test: copy the `mock-test-1/` folder structure (excluding problems), update `main.tex` to include new problem files.

### Custom LaTeX commands (defined in preamble.tex)

| Command | Purpose |
|---|---|
| `\question` | Auto-incremented question counter. Renders bold number with `\theqnum.` |
| `\examsection{title}` | Section header with spacing (large bold title) |
| `\choiceshorizontal{a}{b}{c}{d}` | 4 choices inline, one row (for short numeric answers) |
| `\choicesgrid{a}{b}{c}{d}` | 4 choices in a 2×2 table (ก/ค top row, ข/ง bottom row) — default for most questions |
| `\choicesvertical{a}{b}{c}{d}` | 4 choices stacked vertically (for long sentence answers) |

### Question formatting patterns

Three content layout patterns are demonstrated in `problems/ton2/`:
1. **Verbatim code block + choices** (`04.tex`) — code snippet in `\begin{verbatim}...\end{verbatim}` then choices
2. **Centered image + choices** (`05.tex`) — image/placeholder in `\begin{center}...\end{center}` then choices
3. **Side-by-side image and text** (`06.tex`) — uses `minipage` environments: text on left (0.55\textwidth), image placeholder on right (0.38\textwidth)

Image placeholders use `\framebox` — replace with `\includegraphics[width=...]{filename.png}` when real images are available.

### Document settings

- A4 paper, 16pt base font, 2.5cm top/bottom, 2.2cm left/right margins
- Line spread 1.25 for Thai diacritic readability
- Page number in header, right-aligned, 12pt
- Sections currently separated by `\pagebreak` between parts
