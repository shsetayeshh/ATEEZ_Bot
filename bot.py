import requests
import time
import html
import traceback

with open("token.txt", "r", encoding="utf-8") as file:
    token = file.read().strip()

base_url = f"https://api.telegram.org/bot{token}/"
offset=0
pending_media = {}

def send_message(chat_id,text,reply_markup=None):
    url=base_url+"sendMessage"
    data={
        "chat_id":chat_id,
        "text":text
    }
    if reply_markup is not None:
        data['reply_markup']=reply_markup

    response=requests.post(url,json=data,timeout=15)
    response.raise_for_status()
    result=response.json()
    return result

def answer_callback_query(callback_query_id):
    response = requests.post(
        base_url + "answerCallbackQuery",
        json={"callback_query_id": callback_query_id},
        timeout=15
    )
    response.raise_for_status()


hashtags = [
    "#TikTok", "#Comeback",
    "#Show", "#Concert",
    "#Live", "#Fromm",
    "#IG", "#Music",
    "#YouTube", "#Mv",
    "#Twitter", "#FanSign",
    "#FanMeeting", "#Solo",
    "#Vid", "#Pic",
    "#Mag", "#Cut",
    "#News", "#Charts"
]

def make_hashtag_keyboard():
    keyboard = []

    for i in range(0, len(hashtags), 2):
        row = [
            {
                "text": hashtags[i],
                "callback_data": f"tag:{hashtags[i]}"
            },
            {
                "text": hashtags[i + 1],
                "callback_data": f"tag:{hashtags[i + 1]}"
            }
        ]
        keyboard.append(row)
    return {"inline_keyboard": keyboard}

members = [
    "Hongjoong", "Seonghwa",
    "Yunho", "Yeosang",
    "San", "Mingi",
    "Wooyoung", "Jongho"
]
def make_member_keyboard():
    keyboard = []

    for i in range(0, len(members), 2):
        row = [
            {
                "text": members[i],
                "callback_data": f"member:{members[i]}"
            },
            {
                "text": members[i + 1],
                "callback_data": f"member:{members[i + 1]}"
            }
        ]

        keyboard.append(row)

    keyboard.append([
        {
            "text": "No Name",
            "callback_data": "member:none"
        }
    ])

    return {"inline_keyboard": keyboard}


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_message(
            chat_id,
            "Welcome To The ATEEZ Assistant Bot!"
        )

    elif text == "/help":
        send_message(
            chat_id,
            "Send me a Photo, Video, or Text to Get Started."
        )

    elif "photo" in message:
        photo = message["photo"][-1]
        file_id = photo["file_id"]
        caption = message.get("caption", "")

        pending_media[chat_id] = {
            "type": "photo",
            "file_id": file_id,
            "caption": caption
        }

        send_message(
            chat_id,
            "Choose Hashtag:",
            reply_markup=make_hashtag_keyboard()
        )

    elif "video" in message:
        video = message["video"]
        file_id = video["file_id"]
        caption = message.get("caption", "")

        pending_media[chat_id] = {
            "type": "video",
            "file_id": file_id,
            "caption": caption
        }

        send_message(
            chat_id,
            "Choose Hashtag:",
            reply_markup=make_hashtag_keyboard()
        )

    elif text:
        # ذخیره متن ترجمه برای ادامه فرایند
        pending_media[chat_id] = {
            "type": "text",
            "text": text
        }

        send_message(
            chat_id,
            "Choose Hashtag:",
            reply_markup=make_hashtag_keyboard()
        )



def handle_callback(callback_query):
    callback_id = callback_query["id"]
    data = callback_query.get("data", "")

    message = callback_query.get("message")

    answer_callback_query(callback_id)

    if not message:
        return

    chat_id = message["chat"]["id"]

    if chat_id not in pending_media:
        send_message(
        chat_id,
        "Your message was not found. Please send your text, photo, or video again."
    )
        return

    if data.startswith("tag:"):
        hashtag = data.split(":", 1)[1]

        pending_media[chat_id]["hashtag"] = hashtag

        send_message(
            chat_id,
            "Choose an ATEEZ member:",
            reply_markup=make_member_keyboard()
        )

    elif data.startswith("member:"):
        member = data.split(":", 1)[1]
        pending = pending_media[chat_id]

        if "hashtag" not in pending:
            send_message(
                chat_id,
                "Please choose a hashtag first."
            )
            return

       
        hashtag = pending["hashtag"]

        # ساخت قالب نهایی
        if member == "none":
            template = (
                f"⤞{hashtag}\n"
                f'⤞<a href="https://t.me/ateez_upd">Join</a>'
            )
        else:
            template = (
                f"⤞{hashtag} ~ {member}\n"
                f'⤞<a href="https://t.me/ateez_upd">Join</a>'
            )

        media_type = pending["type"]

        # حالت متن
        if media_type == "text":
            original_text = pending["text"]

            final_text = (
                html.escape(original_text)
                + "\n\n"
                + template
            )

            response = requests.post(
                base_url + "sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": final_text,
                    "parse_mode": "HTML"
                },
                timeout=30
            )

        # حالت عکس و ویدئو
        else:
            original_caption = pending.get("caption", "")

            if original_caption:
                final_caption = (
                    html.escape(original_caption)
                    + "\n\n"
                    + template
                )
            else:
                final_caption = template

            if media_type == "photo":
                endpoint = "sendPhoto"
                media_key = "photo"
            else:
                endpoint = "sendVideo"
                media_key = "video"

            response = requests.post(
                base_url + endpoint,
                json={
                    "chat_id": chat_id,
                    media_key: pending["file_id"],
                    "caption": final_caption,
                    "parse_mode": "HTML"
                },
                timeout=30
            )

        response.raise_for_status()

        del pending_media[chat_id]



print("ATEEZ Bot is Running...")

while True:
    try:
        response = requests.get(
            base_url + "getUpdates",
            params={"offset": offset, "timeout": 20},
            timeout=30
        )

        response.raise_for_status()
        updates = response.json()["result"]

        for update in updates:
            offset = update["update_id"] + 1

            try:
                callback_query = update.get("callback_query")

                if callback_query:
                    handle_callback(callback_query)

                message = update.get("message")

                if message:
                    handle_message(message)

            except Exception as error:
                print(
                    f"Error processing update "
                    f"{update.get('update_id')}: {error}"
                )
                traceback.print_exc()

    except requests.exceptions.RequestException as error:
        print("Connection error:", error)
        time.sleep(3)
