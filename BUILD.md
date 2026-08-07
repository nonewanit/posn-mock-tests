# คู่มือการคอมไพล์ — POSN Mock Tests

## ภาพรวม

โปรเจกต์นี้ใช้ **XeLaTeX** ในการคอมไพล์ (ไม่ใช่ pdfLaTeX) เนื่องจากใช้ `fontspec` สำหรับฟอนต์ภาษาไทย ระบบบิลด์ใช้สองขั้นตอน: XeLaTeX สร้าง `.xdv` → `xdvipdfmx` แปลงเป็น `.pdf`

สามารถใช้ `latexmk` เพื่อจัดการการคอมไพล์อัตโนมัติ รวมถึงโหมด live preview ที่คอมไพล์ใหม่ทุกครั้งเมื่อเซฟไฟล์

## สิ่งที่ต้องมี

| ซอฟต์แวร์ | เวอร์ชัน | หมายเหตุ |
|---|---|---|
| XeLaTeX | TeX Live 2025+ | ติดตั้งด้วย `apt install texlive-xetex` |
| xdvipdfmx | มาพร้อม TeX Live | ใช้แปลง `.xdv` → `.pdf` |
| latexmk | 4.87+ | ใช้สำหรับ live preview |
| Python 3 | 3.8+ | ใช้รัน `generate_main.py` |
| TH Sarabun New | bundled ใน `fonts/THSarabunNew/` | ฟอนต์ภาษาไทยสำหรับข้อสอบ |

## ฟอนต์

### การติดตั้ง

ฟอนต์ TH Sarabun New ถูกจัดเก็บไว้ใน `fonts/THSarabunNew/` จำนวน 4 ไฟล์:

- `THSarabunNew.ttf` (ปกติ)
- `THSarabunNew Bold.ttf` (ตัวหนา)
- `THSarabunNew Italic.ttf` (ตัวเอียง)
- `THSarabunNew BoldItalic.ttf` (หนา+เอียง)

**ติดตั้งบน Linux:**
```bash
cp fonts/THSarabunNew/*.ttf ~/.fonts/
fc-cache -fv ~/.fonts/
```

**บน Windows/Mac:** ดับเบิลคลิกที่ไฟล์ `.ttf` แล้วกด "Install"

### หากไม่พบฟอนต์

หากขึ้น error `! Package fontspec Error: The font "TH Sarabun New" cannot be found`:

1. ตรวจสอบว่าติดตั้งฟอนต์แล้วหรือยัง
2. ลองรัน `fc-cache -fv ~/.fonts/` (Linux)
3. รีสตาร์ตโปรแกรมที่ใช้เปิด PDF

### ฟอนต์สำรอง

หากไม่ต้องการใช้ TH Sarabun New สามารถแก้ไข `preamble.tex` บรรทัดที่ 6 เปลี่ยนเป็นฟอนต์ภาษาไทยอื่นที่มีในระบบ เช่น `\setmainfont{Sarabun}[Scale=1.5]`

## การคอมไพล์

### ขั้นตอนที่ 1: สร้าง main.tex

```bash
# สร้าง main.tex จากไฟล์โจทย์ใน problems/
python3 generate_main.py --test-dir mock-test-1 --seed 42
```

สคริปต์นี้จะ:
- สแกนโฟลเดอร์ `problems/ton1/`, `ton2/`, `ton3/` หาไฟล์ `.tex` ทั้งหมด
- นับจำนวนข้อแต่ละตอนและคำนวณช่วงเลขข้อ
- สุ่มลำดับข้อ (ตาม seed ที่กำหนด — seed เดิมให้ลำดับเดิมเสมอ)
- สร้าง `main.tex` พร้อม section headers และ `\input{}` ข้อทุกข้อ

### ขั้นตอนที่ 2: คอมไพล์ด้วย latexmk (แนะนำ)

```bash
cd mock-test-1

# คอมไพล์ครั้งเดียว
latexmk main.tex

# Live preview — คอมไพล์ใหม่ทุกครั้งเมื่อเซฟ
latexmk -pvc main.tex
```

### ขั้นตอนที่ 2 (ทางเลือก): คอมไพล์เองทีละขั้น

```bash
cd mock-test-1
xelatex -no-pdf -interaction=nonstopmode main.tex
xdvipdfmx main.xdv
# → main.pdf
```

## การตั้งค่า latexmk

ไฟล์ `.latexmkrc` ที่ root ของโปรเจกต์กำหนดค่า:

```perl
$pdf_mode = 5;                                           # XeLaTeX → xdvipdfmx
$xelatex = 'xelatex -no-pdf -interaction=nonstopmode %O %S';
$pdf_previewer = 'none';                                  # ไม่ต้องเปิด PDF viewer
```

ทุกครั้งที่รัน `generate_main.py` จะสร้าง symlink `.latexmkrc` → `../.latexmkrc` ในไดเรกทอรีของข้อสอบนั้น ๆ โดยอัตโนมัติ

**สำคัญ:** ต้องมี `.latexmkrc` ในไดเรกทอรีที่รัน `latexmk` เพราะระบบ `/etc/LatexMk` ตั้งค่า default เป็น LuaLaTeX (`$pdf_mode = 4`) ซึ่งไม่รองรับ `\XeTeXlinebreaklocale`

## การแก้ปัญหา

### พบ "th" ปรากฏใน PDF

เกิดจาก `latexmk` ใช้ LuaLaTeX แทน XeLaTeX ตรวจสอบว่า `.latexmkrc` (symlink) มีอยู่ในไดเรกทอรีข้อสอบ:

```bash
ls -la mock-test-1/.latexmkrc   # ต้องมีไฟล์นี้
```

หากไม่มี ให้รัน `generate_main.py` ใหม่ หรือสร้าง symlink เอง:
```bash
cd mock-test-1
ln -sf ../.latexmkrc .latexmkrc
```

### ข้อความล้นขอบกระดาษด้านขวา (overfull hbox)

`preamble.tex` ตั้งค่า `\emergencystretch=1em`, `\tolerance=1000`, `\hfuzz=3pt` ไว้เพื่อจัดการข้อความภาษาไทย หากยังพบปัญหา เพิ่มค่าเหล่านี้ใน `preamble.tex`

### ทำความสะอาดไฟล์ชั่วคราว

```bash
cd mock-test-1
latexmk -C    # ลบ .aux, .log, .xdv, .pdf, .fls, .fdb_latexmk ทั้งหมด
```

หรือลบด้วยมือ:
```bash
rm -f main.aux main.log main.xdv main.pdf main.fls main.fdb_latexmk
```

### คอมไพล์ไม่ผ่านหลังจากแก้ preamble.tex

preamble ที่เปลี่ยนอาจไม่เข้ากันกับ `.aux` เก่า ให้ล้างก่อน:
```bash
latexmk -C && latexmk
```

### ข้อผิดพลาด "There's no line here to end"

เกิดจากการใช้ `\newline` ในตำแหน่งที่ไม่มีบรรทัด (เช่น หลัง `\end{itemize}` โดยไม่มีข้อความ) แก้โดยเปลี่ยน `\newline` เป็น `\par\medskip` หรือลบออก

## กระดาษคำตอบ

แต่ละชุดข้อสอบมีกระดาษคำตอบ (answer sheet) แยกไว้สำหรับนักเรียนระบายคำตอบ

### การสร้างกระดาษคำตอบ

```bash
python3 generate_answer_sheet.py --test-dir mock-test-1
cd mock-test-1
latexmk answer-sheet.tex
# → answer-sheet.pdf
```

### การปรับแต่ง

```bash
# เปลี่ยนจำนวนข้อปรนัย/อัตนัย
python3 generate_answer_sheet.py --test-dir mock-test-1 \
    --mc-total 60 --mc-part1-end 30 \
    --fillin-start 61 --fillin-count 8 --fillin-digits 4

# เปลี่ยนจำนวนคอลัมน์ (default 5)
python3 generate_answer_sheet.py --test-dir mock-test-1 --mc-cols 6
```

| ตัวเลือก | ค่าเริ่มต้น | คำอธิบาย |
|---|---|---|
| `--mc-total` | 55 | จำนวนข้อปรนัยทั้งหมด |
| `--mc-part1-end` | 30 | ข้อสุดท้ายของตอนที่ 1 (คณิตศาสตร์) |
| `--mc-cols` | 5 | จำนวนคอลัมน์ในส่วนปรนัย |
| `--fillin-start` | 56 | เลขข้อแรกของอัตนัย |
| `--fillin-count` | 5 | จำนวนข้ออัตนัย |
| `--fillin-digits` | 4 | จำนวนหลักต่อข้ออัตนัย |

## หมายเหตุสำหรับผู้พัฒนา

- `main.tex` ถูกสร้างโดย `generate_main.py` — **ห้ามแก้ไขด้วยมือ** (จะถูกเขียนทับเมื่อรันสคริปต์ครั้งต่อไป)
- ไฟล์ `main.tex` ที่ generate แล้วขึ้นต้นด้วย `% !TEX program = xelatex` เพื่อบอก latexmk ให้ใช้ XeLaTeX
- การแก้ไข preamble (`preamble.tex`) มีผลกับข้อสอบทุกชุดทันที
- ไฟล์ `.aux`, `.log`, `.xdv`, `.pdf`, `.fls`, `.fdb_latexmk` ถูกละเว้นโดย `.gitignore` — ไม่ต้อง commit
- ฟอนต์ `/fonts` เคยอยู่ใน `.gitignore` แต่ถูกนำออกแล้ว — ตอนนี้ถูก track ใน git เพื่อให้โปรเจกต์สมบูรณ์ในตัวเอง
