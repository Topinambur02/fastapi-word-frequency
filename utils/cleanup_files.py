import os


def cleanup_files(*filepaths):
    '''Удаляет временные файлы после успешной отдачи пользователю.'''
    for path in filepaths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f'Error when deleting a file {path}: {e}')