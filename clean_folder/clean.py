import shutil
import sys
import re
from pathlib import Path
from random import randint, choice, choices
import numpy
from PIL import Image
import os

MESSAGE = "Hello, Привіт"

def get_random_filename():
    random_value = (
        "()+,-0123456789;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz"
        "{}~абвгдеєжзиіїйклмнопрстуфхцчшщьюяАБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
    )
    return "".join(choices(random_value, k=8))

def generate_text_files(path):
    documents = ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX")
    with open(path / f"{get_random_filename()}.{choice(documents).lower()}", "wb") as f:
        f.write(MESSAGE.encode())

def generate_archive_files(path):
    archive = ("ZIP", "GZTAR", "TAR")
    shutil.make_archive(f"{path}/{get_random_filename()}", f"{choice(archive).lower()}", path)

def generate_image(path):
    images = ("JPEG", "PNG", "JPG")
    image_array = numpy.random.rand(100, 100, 3) * 255
    image = Image.fromarray(image_array.astype("uint8"))
    image.save(f"{path}/{get_random_filename()}.{choice(images).lower()}")

def generate_folders(path):
    folder_name = [
        "temp",
        "folder",
        "dir",
        "tmp",
        "OMG",
        "is_it_true",
        "no_way",
        "find_it",
    ]
    folder_path = Path(
        f"{path}/"
        + "/".join(
            choices(
                folder_name,
                weights=[10, 10, 1, 1, 1, 1, 1, 1],
                k=randint(5, len(folder_name)),
            )
        )
    )
    folder_path.mkdir(parents=True, exist_ok=True)

def generate_folder_forest(path):
    for i in range(0, randint(2, 5)):
        generate_folders(path)

def generate_random_files(path):
    for i in range(3, randint(5, 7)):
        function_list = [generate_text_files, generate_archive_files, generate_image]
        choice(function_list)(path)

def parse_folder_recursion(path):
    for elements in path.iterdir():
        if elements.is_dir():
            generate_random_files(path)
            parse_folder_recursion(elements)

def exist_parent_folder(path):
    path.mkdir(parents=True, exist_ok=True)

def file_generator(path):
    exist_parent_folder(path)
    generate_folder_forest(path)
    parse_folder_recursion(path)

if __name__ == "__main__":
    parent_folder_path = Path("Temp")
    file_generator(parent_folder_path)

def move_image_file(file, root_folder):
    image_folder = root_folder / "images"
    image_folder.mkdir(exist_ok=True)
    new_name = normalize.normalize(file.name)
    new_path = image_folder / new_name
    file.rename(new_path)

def move_document_file(file, root_folder):
    document_folder = root_folder / "documents"
    document_folder.mkdir(exist_ok=True)
    new_name = normalize.normalize(file.name)
    new_path = document_folder / new_name
    file.rename(new_path)

def move_audio_file(file, root_folder):
    audio_folder = root_folder / "audio"
    audio_folder.mkdir(exist_ok=True)
    new_name = normalize.normalize(file.name)
    new_path = audio_folder / new_name
    file.rename(new_path)

def move_video_file(file, root_folder):
    video_folder = root_folder / "video"
    video_folder.mkdir(exist_ok=True)
    new_name = normalize.normalize(file.name)
    new_path = video_folder / new_name
    file.rename(new_path)

def main(folder_path):
    scan.scan(folder_path)

    for file in scan.jpeg_files:
        move_image_file(file, folder_path)

    for file in scan.jpg_files:
        move_image_file(file, folder_path)

    for file in scan.png_files:
        move_image_file(file, folder_path)

    for file in scan.txt_files:
        move_document_file(file, folder_path)

    for file in scan.docx_files:
        move_document_file(file, folder_path)

    for file in scan.audio_files:
        move_audio_file(file, folder_path)

    for file in scan.video_files:
        move_video_file(file, folder_path)

def remove_empty_folders(root_folder):
    for folder in root_folder.iterdir():
        if folder.is_dir():
            try:
                folder.rmdir()
                print(f"Удалена пустая папка: {folder}")
            except OSError as e:
                print(f"Ошибка при удалении пустой папки: {folder}, {e}")

if __name__ == "__main__":
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    main(arg.resolve())

    remove_empty_folders(arg.resolve())

UKRAINIAN_SYMBOLS = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "je",
    "zh",
    "z",
    "y",
    "i",
    "ji",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "ju",
    "ja",
)

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(name):
    name, *extension = name.split(".")
    new_name = name.translate(TRANS)
    new_name = re.sub(r"\W", "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"

import sys
from pathlib import Path

jpeg_files = list()
png_files = list()
jpg_files = list()
txt_files = list()
docx_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    "JPEG": jpeg_files,
    "PNG": png_files,
    "JPG": jpg_files,
    "TXT": txt_files,
    "DOCX": docx_files,
    "ZIP": archives,
}

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in (
                "JPEG",
                "JPG",
                "PNG",
                "TXT",
                "DOCX",
                "OTHER",
                "ARCHIVE",
            ):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder / item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)

if __name__ == "__main__":
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

    print(f"jpeg: {jpeg_files}\n")
    print(f"jpg: {jpg_files}\n")
    print(f"png: {png_files}\n")
    print(f"txt: {txt_files}\n")
    print(f"docx: {docx_files}\n")
    print(f"archive: {archives}\n")
    print(f"unknown: {others}\n")
    print(f"All extensions: {extensions}\n")
    print(f"Unknown extensions: {unknown}\n")
