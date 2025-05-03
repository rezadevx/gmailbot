
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN
import instaloader

app = Client(
    "ig_stalk_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


def login_to_instagram(username, password):
    L = instaloader.Instaloader()
    try:
        L.login(username, password)
        print("Login sukses!")
        return L
    except Exception as e:
        print(f"Gagal login: {e}")
        return None


def get_profile_info(L, profile_username):
    try:
        profile = instaloader.Profile.from_username(L.context, profile_username)
        return {
            "name": profile.full_name,
            "bio": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "profile_pic": profile.profile_pic_url
        }
    except Exception as e:
        print(f"Gagal mengambil data: {e}")
        return None


@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply(
        "Hi, saya adalah bot untuk melihat profil Instagram yang dibuat oleh reza.\n\n"
        "Ketik `/stalk username_ig` untuk mulai stalking."
    )


@app.on_message(filters.command("stalk") & filters.private)
async def stalk_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Gunakan perintah: `/stalk username_ig`", quote=True)

    username = message.command[1]
    wait_msg = await message.reply("Mencari data...")

    # Login ke Instagram
    L = login_to_instagram("indobot_stalker", "Piniaisyaa1")

    if L:
        result = get_profile_info(L, username)
        if not result:
            return await wait_msg.edit("Gagal mengambil data. Username salah atau akun mungkin privat.")

        caption = (
            f"**Nama:** {result['name']}\n"
            f"**Bio:** {result['bio']}\n\n"
            f"**Postingan:** {result['posts']}\n"
            f"**Followers:** {result['followers']}\n"
            f"**Following:** {result['following']}"
        )

        await message.reply_photo(photo=result['profile_pic'], caption=caption)
        await wait_msg.delete()

# Menjalankan bot
app.run()
