from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN
import requests
from bs4 import BeautifulSoup

app = Client(
    "ig_stalk_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# /start handler
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply(
        "Hi, saya adalah bot untuk melihat profil Instagram yang dibuat oleh Razer.\n\n"
        "Ketik `/stalk username_ig` untuk mulai stalking."
    )

# Fungsi untuk mengambil info IG dari picuki
def get_ig_info(username: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.picuki.com/profile/{username.strip('@')}"
    r = requests.get(url, headers=headers)

    if "Page not found" in r.text or r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    try:
        profile_pic = soup.find("img", {"class": "profile-avatar"})["src"]
        fullname = soup.find("div", class_="profile-title").text.strip()
        bio = soup.find("div", class_="profile-description").text.strip()
        stats = soup.find_all("span", class_="info-box-number")
        posts, followers, following = [s.text.strip() for s in stats[:3]]

        return {
            "name": fullname,
            "bio": bio,
            "posts": posts,
            "followers": followers,
            "following": following,
            "pfp": profile_pic
        }
    except Exception:
        return None

# /stalk handler
@app.on_message(filters.command("stalk") & filters.private)
async def stalk_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Gunakan perintah: `/stalk username_ig`", quote=True)

    username = message.command[1]
    wait_msg = await message.reply("Mencari data...")

    result = get_ig_info(username)
    if not result:
        return await wait_msg.edit("Gagal mengambil data. Username salah atau akun mungkin privat.")

    caption = (
        f"**Nama:** {result['name']}\n"
        f"**Bio:** {result['bio']}\n\n"
        f"**Postingan:** {result['posts']}\n"
        f"**Followers:** {result['followers']}\n"
        f"**Following:** {result['following']}"
    )

    await message.reply_photo(photo=result['pfp'], caption=caption)
    await wait_msg.delete()

# Menjalankan bot
app.run()
