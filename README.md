# TelegramDownloader

[![Test](https://github.com/ciuliene/telegramDownloader/actions/workflows/python-app.yml/badge.svg)](https://github.com/ciuliene/telegramDownloader/actions/workflows/python-app.yml) [![codecov](https://codecov.io/gh/ciuliene/telegramDownloader/graph/badge.svg?token=02ZM98MDDM)](https://codecov.io/gh/ciuliene/telegramDownloader)

A python application to download video files from Telegram channel

## Requirements

Before starting, make sure you have an active `Telegram` account and that you have installed `python` (in my case I used version _3.11.4_).

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

The application will print the name of the file and a progress bar with the percentage of the download. You can stop the download at any time by pressing `CTRL+C`.

## Disclaimer

This application is for educational purposes only. I am not responsible for any misuse of this application. Damages caused by this application are not my responsibility.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
