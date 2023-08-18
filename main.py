from src.envtool import EnvTool
from src.models.chat import Chat
from src.tgdownloader import TGDownloader
from src.utils import print_progress_bar, go_back_n_lines, go_forward_n_lines
from src.menu import Menu
import sys

def create_tgd() -> TGDownloader:
    env = EnvTool()
    env.set_env_vars_from_file('.env')

    api_id = env.get_env_var('API_ID')
    api_hash = env.get_env_var('API_HASH')
    database_encryption_key = env.get_env_var('DATABASE_ENCRYPTION_KEY')
    phone = env.get_env_var('PHONE')

    tgd = TGDownloader(
        api_id=api_id, 
        api_hash=api_hash, 
        database_encryption_key=database_encryption_key, 
        phone=phone,
        files_directory=f'./files/{phone}')
    
    return tgd

def download_files_from_chat(tgd: TGDownloader, chat: Chat):
    files = tgd.get_files_from_chat(chat.id, limit=100, from_message_id=chat.last_message_id)

    longest_file_name = len(max([file.file_name for file in files], key=len))

    go_forward_n_lines(len(files))
    
    while len([file for file in files if file.is_downloaded == False]) > 0:
        go_back_n_lines(len(files))

        for file in files:
            if not file.is_downloaded:
                file.download()
            print_progress_bar(file.file_name, file.download_percentage, longest_file_name)

    print("Download completed!")

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

        download_files_from_chat(tgd, chat)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.stderr.write(f"\033[31m{e}\033[0m")
    finally:
        tgd.stop()
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

if __name__ == '__main__': # pragma: no cover
    run()
            