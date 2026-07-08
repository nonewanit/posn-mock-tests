import re
import sys
import os

def main():
    # Accept mock test directory as argument, default to mock-test-1
    test_dir = sys.argv[1] if len(sys.argv) > 1 else 'mock-test-1'
    main_tex = os.path.join(test_dir, 'main.tex')
    key_file = os.path.join(test_dir, 'key.txt')

    # Step 1: Parse main.tex to get the question order as seen in the PDF
    with open(main_tex, 'r', encoding='utf-8') as f:
        main_content = f.read()

    # Extract all \input{problems/...} paths in order
    input_pattern = r'\\input\{(problems/[^}]+)\}'
    input_paths = re.findall(input_pattern, main_content)

    # Step 2: Read the answer from each file (paths relative to test_dir)
    with open(key_file, 'w', encoding='utf-8') as key_f:
        for i, rel_path in enumerate(input_paths, start=1):
            full_path = os.path.join(test_dir, rel_path)
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract the % answer: line
            match = re.search(r'^% answer:\s*(.+)', content, flags=re.MULTILINE)
            answer = match.group(1).strip() if match else 'N/A'

            key_f.write(f"{i}. {answer}\n")

    print(f"Done! Answer key written to: {key_file}")
    print(f"Total questions (in PDF order): {len(input_paths)}")

if __name__ == '__main__':
    main()
