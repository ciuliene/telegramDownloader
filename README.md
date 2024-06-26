# TelegramDownloader

[![Test](https://github.com/ciuliene/telegramDownloader/actions/workflows/python-app.yml/badge.svg)](https://github.com/ciuliene/telegramDownloader/actions/workflows/python-app.yml) [![codecov](https://codecov.io/gh/ciuliene/telegramDownloader/graph/badge.svg?token=02ZM98MDDM)](https://codecov.io/gh/ciuliene/telegramDownloader)

A python application to download video files from Telegram channel

## Requirements

Before starting, make sure you have:

- an active `Telegram` account
- `python@3`
- `openssl@1.1`

To use Telegram APIs you need to register an application from [here](https://my.telegram.org/). The data from the `App configuration` section will be used in the next step.

NOTE: The application will use your Telegram account so you must first join the channel containing the files you want to download

## Usage

First of all you need to create a .env file containing:

```sh
API_ID=<api_id> # From my.telegram.org
API_HASH=<api_hash> # From my.telegram.org
DATABASE_ENCRYPTION_KEY=<database_encryption_key> # what you want
PHONE=<phone_number> # Your phone number with country prefix
FILES_DIRECTORY=<files_directory> # Optional. Where you want to save the files
```

<span style="color:orange;">IMPORTANT</span>
For your security, **do not share or upload this file**.

NOTE: it is recommended to use the application in a virtual environment.

Then you can install the required packages with:

```sh
pip install -r requirements.txt
```

And run the application with:

```sh
python main.py
```

First usage will ask you to enter the code received on your Telegram account.
Once you have entered the code, the application will get the list of chats you are in and will ask you to select the one you want to download the files from.

Move up and down with the arrow keys and press enter to select the desired chat.

After that each file will be downloaded in the selected folder. The default folder is `./files/{PHONE}` but you can change it in the .env file.

### Step 1: List of available files

Once the chat is selected, the application checks if a file named <chat>.txt exists. This file contains the list of files to downloaded. If the file does not exist, it will be created and the application exits. You can edit this file to change the list of files to download. The order of the files determines the order in which they will be downloaded.

NOTE: the file is created in the same folder as the application.

### Step 2: Downloading files

If the file named <chat>.txt exists, the application will download them one by one. A progress bar will be shown for each file.

## Usage with Docker

If you have any problems using the application, you can use it with [Docker](https://www.docker.com/products/docker-desktop/). Make sure it is installed.

### Build

NOTE: Before creating the container, you need to create the .env file, as described above.

Build image using this command:

```sh
docker build -t telegram_downloader:latest .
```

### Create

Create container using this command:

```sh
docker create --name telegram_downloader -it telegram_downloader:latest
```

NOTE: this command create a 'non-daemon' container. This means that when you start the container, it runs on the local terminal where you executed the command.

### Start

Start container using this command:

```sh
docker start -i telegram_downloader
```

NOTES:

- `Interactive` mode (`-i`) is mandatory in order to enter the verification code (required at first run only) and select the chats.
- To edit the files with the list or to get downloaded videos, you can use the Docker Desktop (it's easier than attaching to the terminal where the container is)

## Disclaimer

This application is for educational purposes only. I am not responsible for any misuse of this application. Damages caused by this application are not my responsibility.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
