import os

def count_lines_of_code(directory, extensions):
    total_lines = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(extensions)):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    total_lines += len(lines)

    return total_lines

if __name__ == "__main__":
    path = "../../Cleave2.0"
    target_extensions = [".py", ".dart", ".md", '.html', '.qss']
    lines_of_code = count_lines_of_code(path, target_extensions)
    print(f"Total lines of code: {lines_of_code}")
