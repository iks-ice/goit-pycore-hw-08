from pathlib import Path

def get_path(main_file, *path_parts):
    file_path = Path(main_file).resolve().parent.joinpath(*path_parts)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)
    return file_path
