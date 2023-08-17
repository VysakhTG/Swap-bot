import os , time
import re
from user import User as USER
from pyrogram import Client, filters
from info import CHANNEL, ADMINS
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from utils import progress_for_pyrogram, convert, humanbytes

channel_pattern = "(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$"  # Capture the channel username
pm_pattern = r"tg:\/\/openmessage\?user_id=(\d+)&message_id=(\d+)"  # Capture user_id and message_id


@Client.on_message(filters.private & filters.user(ADMINS) & filters.regex(channel_pattern))
async def channel_save(client, message):
    ms = await message.reply("Please wait.....")
    regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
    match = regex.match(message.text)
    chat_id = match.group(4)
    msg_id = int(match.group(5))
    if chat_id.isnumeric():
        chat_id = int("-100" + chat_id)
    try:
        iwe = await USER.get_chat(chat_id)
    except ChannelInvalid:
        return await m.edit('This may be a private channel/group. Make me an admin over there to index the files.')
    except (UsernameInvalid, UsernameNotModified):
        return await m.edit('Invalid Link specified.')
    except Exception as e:
        logger.exception(e)
        return await m.edit(f'Errors - {e}')
    chat_ed = iwe.id
    owe = await USER.get_messages(chat_ed, msg_id)
    if not owe:
        return
    if not owe.media:
        return 

    file = getattr(owe, owe.media.value)
    new_filename = file.file_name
    file_path = f"downloads/{new_filename}"
    
    if owe.document or owe.video:
        try:
            await ms.edit("Downloading....")
            await USER.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())) 
        except Exception as e:
            await ms.edit(str(e))
            return
        
        try:
            caption = f"<code>{new_filename}</code>"
            thumbnail_path = await USER.download_media(file.thumbs[0].file_id)
            await ms.edit("Uploading....")
            thump = await USER.get_messages(int(-1001270936734), int(126))
            thumb = getattr(thump, thump.media.value)
            ph_path = await USER.download_media(thumb.file_id)
            img = Image.open(ph_path).convert("RGB")  # Added conversion to RGB
            img.thumbnail((320, 320))
            img.save(ph_path, "JPEG")
            try:
                f = await USER.send_document(
                    int(-1001837941527),
                    document=file_path,
                    caption=caption,
                    thumb=ph_path,
                    progress=progress_for_pyrogram,
                    progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())
                )
                
                await ms.delete()
                await owe.delete()
                os.remove(file_path)
                if ph_path:
                    os.remove(ph_path)
            except Exception as e:
                os.remove(file_path)
                if ph_path:
                    os.remove(ph_path)
            return await ms.edit(f"Error: {e}")
     
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            return await ms.edit(f"Error: {e}")
     
