import shutil
import sys
from pathlib import Path

result = {
    "files": [],
    "unknown_ext": [],
    "extensions": []
}
FOLDER_LIST = ["images", "documents", "audio", "archives", "video", "other"]
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def create_folders(path):
    path = Path(path)
    for folder in FOLDER_LIST:
        (path / folder).mkdir(exist_ok=True)


def normalize(name):
    parts = name.split('.')
    symbol_for_change = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '`',
                         '.', '-', '{', '}', '|', '"', '№', ';', '%', ':', '?', '=', " "]
    new_name = parts[0].translate(TRANS)
    for symbol in symbol_for_change:
        new_name = new_name.replace(symbol, "_")
    return '.'.join([new_name, parts[-1]])


def move_to_folder(item, new_name, source_path, folder_name):
    global result
    result['extensions'].append(item.suffix)
    file_path = str(source_path / folder_name / new_name)
    result['files'].append(file_path)
    shutil.move(str(item), file_path)


def sort_files_and_folders(path):
    global result
    source_path = Path(source)
    path = Path(path)
    for item in path.glob("*"):
        if item.is_file():
            extension = item.suffix.lower()
            new_name = normalize(item.name)
            if extension in (".jpg", ".jpeg", ".png", ".gif", ".bmp"):
                move_to_folder(item, new_name, source_path, "images")
            elif extension in (".avi", ".mp4", ".mov", ".mkv"):
                move_to_folder(item, new_name, source_path, "video")
            elif extension in (".doc", ".docx", ".txt", ".pdf", ".xls", ".pptx"):
                move_to_folder(item, new_name, source_path, "documents")
            elif extension in (".mp3", ".ogg", ".wav", ".amr"):
                move_to_folder(item, new_name, source_path, "audio")
            elif extension in (".zip", ".gz", ".tar"):
                archive_path = source_path / "archives" / item.stem
                archive_path.mkdir(parents=True, exist_ok=True)
                shutil.unpack_archive(str(item), str(archive_path))
                move_to_folder(item, new_name, source_path, "archives")
            else:
                result['unknown_ext'].append(item.suffix)
                file_path = str(source_path / "other" / new_name)
                result['files'].append(file_path)
                shutil.move(str(item), file_path)
        elif item.is_dir():
            if item.name not in FOLDER_LIST:
                sort_files_and_folders(item)
                item.rmdir()


if __name__ == '__main__':
    try:
        source = sys.argv[1]
    except IndexError:
        print("Source path is not specified.")
        exit(0)
    create_folders(source)
    sort_files_and_folders(source)
    print(result)
