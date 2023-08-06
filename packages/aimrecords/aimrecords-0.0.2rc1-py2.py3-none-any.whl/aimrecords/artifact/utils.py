import os


def get_storage_name(path: str) -> str:
    return os.path.join(path, '.aimrecords_storage')
