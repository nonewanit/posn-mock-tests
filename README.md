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
└── mock-test-2/              ← Mock Test #2 (ready for questions)
```

Each mock test is self-contained in its own folder. `preamble.tex` is shared across all tests.

## Build

Requires XeLaTeX and TH Sarabun New font (provided in `fonts/THSarabunNew/`).

### Step 1: Generate main.tex

```bash
python3 generate_main.py --test-dir mock-test-1 --seed 42
```

This scans `problems/` and auto-generates `main.tex` with all questions discovered.

### Step 2: Compile

```bash
cd mock-test-1
xelatex -no-pdf -interaction=nonstopmode main.tex
xdvipdfmx main.xdv
# Output: main.pdf
```

### Continuous preview (live update on save)

```bash
cd mock-test-1
latexmk -pvc main.tex
```

Watches all `.tex` files — rebuilds automatically when you save. Open the PDF in VS Code's viewer and it refreshes on each rebuild. Press `Ctrl+C` to stop.

### Creating a new mock test

```bash
mkdir -p mock-test-3/{problems/{ton1,ton2,ton3},images}
python3 generate_main.py --test-dir mock-test-3
```

## Answer Key

```bash
python randomize_answers.py mock-test-1    # writes key.txt into mock-test-1/
python randomize_answers.py mock-test-2    # for future tests
```

## License

This project is intended for educational use by POSN Computer students and instructors in Thailand.
