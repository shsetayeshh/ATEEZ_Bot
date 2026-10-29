# ATEEZ Assistant Bot

A Telegram bot built with Python to help organize ATEEZ-related media and text posts by adding hashtags and member tags.

## Features

- **Media Support:** Accepts photos, videos, and text messages.
- **Hashtag Selection:** Provides 20 hashtag options through inline keyboard buttons.
- **Member Selection:** Allows users to select an ATEEZ member or choose `No Name`.
- **Automatic Caption Formatting:** Appends a consistent template to the original caption or text.
- **Original Content:** Keeps the original text or media caption and adds the selected tags.
- **Join Link:** Automatically adds a link to the ATEEZ update channel.
- **Long Polling:** Receives Telegram updates using the Telegram Bot API.
- **Error Handling:** Handles connection errors and logs unexpected errors during update processing.

## Available Hashtags

`#TikTok` · `#Comeback` · `#Show` · `#Concert` · `#Live` · `#Fromm` · `#IG` · `#Music` · `#YouTube` · `#Mv` · `#Twitter` · `#FanSign` · `#FanMeeting` · `#Solo` · `#Vid` · `#Pic` · `#Mag` · `#Cut` · `#News` · `#Charts`

## How It Works

1. Send a photo, video, or text message to the bot.
2. Choose a hashtag from the inline keyboard.
3. Select an ATEEZ member or choose `No Name`.
4. The bot sends the content back with the formatted tag and channel link.

### Example Output

For a selected member:

`⤞#TikTok ~ San`

For no member selected:

`⤞#TikTok`

Both formats include a link to the ATEEZ update channel


## Technologies

- Python
- [Requests](https://requests.readthedocs.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## Project Structure

```text
ATEEZBot/
├── bot.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/shsetayeshh/ATEEZ_Bot.git
cd ATEEZBot
```


### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your bot token

Create a file named `token.txt` in the project directory and place your Telegram bot token inside it.

The file should contain only the token, without additional text.

**Security note:** Never upload `token.txt` or share your bot token publicly. The `.gitignore` file excludes `token.txt` from Git.

### 4. Run the bot

```bash
python bot.py
```

The bot will start polling Telegram for updates.

## Deployment

This bot can run on a hosting service that supports Python applications and continuous long polling. It is currently designed to use a local `token.txt` file for its bot token.

## Limitations

- Pending selections are stored in memory and are lost when the application restarts.
- The bot requires an active connection to the Telegram Bot API.
- Continuous availability depends on the hosting environment.

## Disclaimer

This is an independent fan-made project and is not officially affiliated with, endorsed by, or sponsored by ATEEZ or KQ Entertainment.
