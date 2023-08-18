import sys

def print_progress_bar(file_name: str, percentage: float, name_size: int, bar_length: int = 60):
    if not (0 <= percentage <= 100):
        raise ValueError("Percentage must be between 0 and 100")

    completed_length = int(percentage / 100 * bar_length)
    remaining_length = bar_length - completed_length

    colored_bar = f"\033[42m{' ' * completed_length}\033[0m{'-' * remaining_length}"
    sys.stdout.write("\033[?25l")
    sys.stdout.write(f"\033[K {file_name[:name_size] + ' ' * (name_size - len(file_name))}\t")
    print(f"[{colored_bar}] {f'{percentage:.2f}'}%")
    sys.stdout.flush()