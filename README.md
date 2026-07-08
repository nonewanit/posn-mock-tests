# POSN Computer Qualification Mock Tests

ข้อสอบจำลองสำหรับการสอบคัดเลือก (รอบแรก) สอวน. **วิชาคอมพิวเตอร์** 

## Structure

```
posn-mock-tests/
├── preamble.tex              ← shared LaTeX preamble (fonts, commands, layout)
├── generate_main.py          ← script to auto-generate main.tex with shuffled questions
├── randomize_answers.py      ← extract answer keys from problem files
│
├── mock-test-1/              ← Mock Test #1 (60 questions)
│   ├── main.tex
│   ├── images/
│   └── problems/
│       ├── ton1/             ← Part 1: Math basics (30 items, multiple choice)
│       ├── ton2/             ← Part 2: CS (25 items, multiple choice)
│       └── ton3/             ← Part 3: CS (5 items, written/fill-in)
│
└── mock-test-2/              ← Mock Test #2 (template — coming soon)
```

Each mock test is self-contained in its own folder. `preamble.tex` is shared across all tests.

## Build

Requires XeLaTeX and TH Sarabun New font.

```bash
cd mock-test-1
xelatex -no-pdf -interaction=nonstopmode main.tex
xdvipdfmx main.xdv
# Output: main.pdf
```

## Answer Key

```bash
python randomize_answers.py mock-test-1    # writes key.txt into mock-test-1/
python randomize_answers.py mock-test-2    # for future tests
```

## License

This project is intended for educational use by POSN Computer students and instructors in Thailand.
