from pathlib import Path

path = Path('.')

def walk(path):
    files = []
    for i in path.iterdir():
        if i.is_file():
            if i.suffix == '.py':
                files.append(i)
        if i.is_dir():
            files.extend(walk(i))
    return files

print(walk(path))