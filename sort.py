import os
import shutil
import sys
import re


def normalize(filename):
    translit_table = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "h",
        "ґ": "g",
        "д": "d",
        "е": "e",
        "є": "ie",
        "ж": "zh",
        "з": "z",
        "и": "y",
        "і": "i",
        "ї": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ь": "",
        "ю": "iu",
        "я": "ia",
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "H",
        "Ґ": "G",
        "Д": "D",
        "Е": "E",
        "Є": "Ye",
        "Ж": "Zh",
        "З": "Z",
        "И": "Y",
        "І": "I",
        "Ї": "Yi",
        "Й": "Y",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "Kh",
        "Ц": "Ts",
        "Ч": "Ch",
        "Ш": "Sh",
        "Щ": "Shch",
        "Ь": "",
        "Ю": "Yu",
        "Я": "Ya",
    }

    filename = re.sub(r"[^\w\s-]", "", filename)
    filename = re.sub(r"[-\s]+", "_", filename)

    return "".join(translit_table.get(c, c) for c in filename)


def process_file(file_path, target_dir):
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1][1:].upper()

    new_file_name = normalize(file_name)
    new_file_path = os.path.join(target_dir, new_file_name)

    shutil.move(file_path, new_file_path)

    return file_extension, new_file_name


def sort_folder(folder_path):
    file_extensions = {
        "images": ("JPEG", "PNG", "JPG", "SVG"),
        "videos": ("AVI", "MP4", "MOV", "MKV"),
        "documents": ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"),
        "music": ("MP3", "OGG", "WAV", "AMR"),
        "archives": ("ZIP", "GZ", "TAR"),
    }

    result = {
        "images": [],
        "videos": [],
        "documents": [],
        "music": [],
        "archives": [],
        "known_extensions": set(),
    }

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension, new_file_name = process_file(file_path, folder_path)

            if file_extension in file_extensions["images"]:
                result["images"].append(new_file_name)
            elif file_extension in file_extensions["videos"]:
                result["videos"].append(new_file_name)
            elif file_extension in file_extensions["documents"]:
                result["documents"].append(new_file_name)
            elif file_extension in file_extensions["music"]:
                result["music"].append(new_file_name)
            elif file_extension in file_extensions["archives"]:
                result["archives"].append(new_file_name)

            result["known_extensions"].add(file_extension)

    return result


if len(sys.argv) < 2:
    print("Usage: python sort.py <folder_path>")
else:
    folder_path = sys.argv[1]
    result = sort_folder(folder_path)
    print("Images:", result["images"])
    print("Videos:", result["videos"])
    print("Documents:", result["documents"])
    print("Music:", result["music"])
    print("Archives:", result["archives"])
    print("Known Extensions:", result["known_extensions"])
