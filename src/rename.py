import os


def rename_with_index(order: list[str], pad: int = 3):
    for i, file_name in enumerate(order):
        path, old_file_name = os.path.split(file_name)
        new_file_name = f'{(i+1):0{pad}d}_{old_file_name}'
        new_file_path = os.path.join(path, new_file_name)
        os.rename(file_name, new_file_path)
        pass


def remove_index(path: str):
    files = [os.path.join(path, file) for file in sorted(os.listdir(
        path)) if file != '.DS_Store' and os.path.isfile(os.path.join(path, file))]

    for _, file in enumerate(files):
        path, file_name = os.path.split(file)
        new_file_name = file_name[4:]
        new_file_path = os.path.join(path, new_file_name)
        os.rename(file, new_file_path)


if __name__ == "__main__":  # pragma: no cover
    files_container = '/<path_to>/files/<phone_number>/files/videos'
    file_list = [os.path.join(files_container, file)
                 for file in os.listdir(files_container)]

    ordered_file_list = []

    with open('/<path_to>/<file_list>.txt', 'r') as f:
        ordered_file_list = [os.path.join(
            files_container, file.strip()) for file in f.readlines()]

    rename_with_index(ordered_file_list)
