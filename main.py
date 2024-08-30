from src.tgdownloader import TGDownloader
from src.utils import *
from src.menu import Menu
from dotenv import load_dotenv
import os
import sys

load_dotenv()

def create_tgd() -> TGDownloader:

    api_id = os.getenv('API_ID') or ''
    api_hash = os.getenv('API_HASH') or ''
    database_encryption_key = os.getenv('DATABASE_ENCRYPTION_KEY') or ''
    phone = os.getenv('PHONE') or ''
    files_directory = os.getenv('FILES_DIRECTORY') or f"./files/{phone}"

    tgd = TGDownloader(
        api_id=api_id, 
        api_hash=api_hash, 
        database_encryption_key=database_encryption_key, 
        phone=phone,
        files_directory=files_directory)
    
    return tgd

def run():
    try:
        tgd = create_tgd()
        tgd.login()

        chat_list = tgd.get_chats()

        chats = [chat.title for chat in chat_list] + ["Exit"]

        menu = Menu(chats)
        selected_chat = None
        while selected_chat is None:
            selected_chat, _ = menu.start_menu()

        chat = [chat for chat in chat_list if chat.title == selected_chat][0]

        file_list: list | None = None

        chat_name = f'{selected_chat}.txt'.replace('/', '')

        files_from_chat = tgd.get_files_from_chat(chat)

        try:
            file_list = get_file_list_from_file(chat_name)
            print(f"\nGetting files from {chat_name}...")
        except FileNotFoundError:
            print("\nGetting files from chat...")

            file_list = [file.file_name for file in files_from_chat]
            store_files_file_in_file(chat_name, file_list)

            print("\nList of files: ")
            for file in file_list:
                print(f'\t- {file}')

            print(f"\nYou can find the list of files here: {chat_name}")
            print("And select which files you want to download")

            return
        except Exception as e:
            raise e

        to_download = sorted([file for file in files_from_chat if file.file_name in file_list],
                            key=lambda x: file_list.index(x.file_name))

        for file in to_download:
            while not file.is_downloaded:
                go_back_n_lines(1)
                file.download()
                print_progress_bar(
                    file.file_name, file.download_percentage, len(file.file_name))

            print("\n")

    except KeyboardInterrupt:  # pragma: no cover
        pass
    except Exception as e:
        sys.stderr.write(f"\033[31m{e}\033[0m")
    finally:
        tgd.stop()
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

if __name__ == '__main__': # pragma: no cover
    run()
            