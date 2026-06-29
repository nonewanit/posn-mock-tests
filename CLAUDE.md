# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build

```bash
xelatex -no-pdf -interaction=nonstopmode main.tex
xdvipdfmx main.xdv
```

XeLaTeX is required (not pdfLaTeX) because `fontspec` is used for Thai font support. The document uses **TH Sarabun New** font, which must be installed on the system. On Overleaf, the font file needs to be uploaded into the project.

Build outputs: `.aux`, `.log`, `.pdf`, `.xdv` — these are generated files, never commit them.

## Architecture

Multi-file LaTeX project for Thai-language POSN (Promotion of Science and Mathematics Talented) 1st Qualification exam papers. Each problem lives in its own file, included via `\input{}` into `main.tex`.

```
main.tex              — document skeleton (documentclass, \begin{document}, sections, \input calls, \end{document})
preamble.tex          — shared packages, fonts, geometry, header config, custom commands
problems/
  ton1/               — Part 1: Math (multiple choice, 4 choices per question)
    01.tex .. 03.tex
  ton2/               — Part 2: Computer Science (multiple choice)
    04.tex .. 06.tex
  ton3/               — Part 3: Computer Science (written/fill-in, no choices)
    07.tex .. 08.tex
```

To add a new question: create `problems/tonX/NN.tex` with just the `\question` body and `\choices*` call, then add `\input{problems/tonX/NN.tex}` in `main.tex` under the right section.

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
