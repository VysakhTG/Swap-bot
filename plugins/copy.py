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
        xd = await USER.copy_message(chat_id=CHANNEL, from_chat_id=chat_ed, message_id=msg_id)
        if xd:
            await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=int(xd.id))
            await xd.delete()
            await ms.delete()
    file = getattr(owe, owe.media.value)
    if owe.photo:
        photo_file_path = f"downloads/{msg_id}.png"
        await USER.download_media(message=file, file_name=photo_file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time()))
        f = await USER.send_photo(chat_id=CHANNEL, photo=photo_file_path, caption=owe.caption)  # Send the sticker as a file 
        await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
        os.remove(photo_file_path)
        await f.delete()      
        await ms.delete()  # Delete the "" message
        return
    new_filename = file.file_name
    file_path = f"downloads/{new_filename}"
    duration = 0
    if owe.sticker:
        sticker_file_path = f"downloads/{msg_id}.webp"  
        await USER.download_media(message=file, file_name=sticker_file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time()))
        f = await USER.send_sticker(chat_id=CHANNEL, sticker=sticker_file_path)  # Send the sticker as a file 
        await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
        os.remove(sticker_file_path)
        await f.delete()      
        await ms.delete()  # Delete the "Sending the sticker" message
        return

    elif owe.document or owe.video:
        try:
            await ms.edit("Downloading....")
            await USER.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())) 
        except Exception as e:
            await ms.edit(str(e))
            return
        try:
            os.remove(file.thumbs[0].file_id)
        except:
            pass
        caption = f"**{owe.caption}**" if not None else ''
        try:
            metadata = extractMetadata(createParser(file_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except:
                pass
        await ms.edit("Uploading....")
        try:
            if owe.video:
                thump = await USER.get_messages(CHANNEL, int(344))
                thumb = getattr(thump, thump.media.value)
                ph_path = await USER.download_media(thumb.file_id)
                img = Image.open(ph_path).convert("RGB")  # Added conversion to RGB
                img.thumbnail((320, 320))
                img.save(ph_path, "JPEG")
                f = await USER.send_video(
                    CHANNEL,
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())
                )
                await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                await f.delete()
                await ms.delete()
                os.remove(file_path)
                if ph_path:
                    os.remove(ph_path)
            if owe.document:
                thump = await USER.get_messages(CHANNEL, int(344))
                thumb = getattr(thump, thump.media.value)
                ph_path = await USER.download_media(thumb.file_id)
                img = Image.open(ph_path).convert("RGB")  # Added conversion to RGB
                img.thumbnail((320, 320))
                img.save(ph_path, "JPEG")
                f = await USER.send_document(
                    CHANNEL,
                    document=file_path,
                    caption=caption,
                    thumb=ph_path,
                    progress=progress_for_pyrogram,
                    progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())
                )
                await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                await f.delete()
                await ms.delete()
                os.remove(file_path)
                if ph_path:
                    os.remove(ph_path)

        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            return await ms.edit(f"Error: {e}")
    
@Client.on_message(filters.private & filters.user(ADMINS) & filters.regex(pm_pattern))
async def pm_save(client, message):
    try:
        bot_id, ms_id = re.search(r"user_id=(\d+)&message_id=(\d+)", message.text).groups()
        # Fetch the raw message using 'app.get_messages'
        username = await client.ask(identifier = (message.chat.id, message.from_user.id, None), text="<b>Send this Bot username without @</b>")
        raw = await USER.get_messages(username.text, int(ms_id))
        await username.request.delete()
        ms = await message.reply("Please wait.....")
        if not raw.media:
            await client.send_message(message.from_user.id, raw.text)
            await ms.delete()
            return
        file = getattr(raw, raw.media.value)
        if raw.photo:
            photo_file_path = f"downloads/{ms_id}.png"
            await USER.download_media(message=file, file_name=photo_file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time()))
            f = await USER.send_photo(chat_id=CHANNEL, photo=photo_file_path, caption=raw.caption)  # Send the sticker as a file 
            await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
            os.remove(photo_file_path)
            await f.delete()      
            await ms.delete()  # Delete the "" message
            return
        new_filename = file.file_name
        file_path = f"downloads/{new_filename}"
        duration = 0
        if raw.sticker:
            sticker_file_path = f"downloads/{ms_id}.webp"  
            await USER.download_media(message=file, file_name=sticker_file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time()))
            f = await USER.send_sticker(chat_id=CHANNEL, sticker=sticker_file_path)  # Send the sticker as a file 
            await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
            os.remove(sticker_file_path)
            await f.delete()      
            await ms.delete()  # Delete the "Sending the sticker" message
            return

        elif raw.document or raw.video:
            try:
                await ms.edit("Downloading....")
                await USER.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())) 
            except Exception as e:
                await ms.edit(str(e))
                return
            try:
                metadata = extractMetadata(createParser(file_path))
                if metadata.has("duration"):
                    duration = metadata.get('duration').seconds
            except:
                pass
            try:
                os.remove(file.thumbs[0].file_id)
            except:
                pass
            caption = f"**{raw.caption}**"

            await ms.edit("Uploading....")
            try:
                if raw.video:
                    thump = await USER.get_messages(CHANNEL, int(288))
                    thumb = getattr(thump, thump.media.value)
                    ph_path = await USER.download_media(thumb.file_id)
                    img = Image.open(ph_path).convert("RGB")  # Added conversion to RGB
                    img.thumbnail((320, 320))
                    img.save(ph_path, "JPEG")
                    f = await USER.send_video(
                        CHANNEL,
                        video=file_path,
                        caption=caption,
                        thumb=ph_path,
                        duration=duration,
                        progress=progress_for_pyrogram,
                        progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())
                    )
                    await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                    await f.delete()
                    await ms.delete()
                    os.remove(file_path)
                    if ph_path:
                        os.remove(ph_path)
                
                if raw.document:
                    thump = await USER.get_messages(CHANNEL, int(344))
                    thumb = getattr(thump, thump.media.value)
                    ph_path = await USER.download_media(thumb.file_id)
                    img = Image.open(ph_path).convert("RGB")  # Added conversion to RGB
                    img.thumbnail((320, 320))
                    img.save(ph_path, "JPEG")
                    f = await USER.send_document(
                        CHANNEL,
                        document=file_path,
                        caption=caption,
                        thumb=ph_path,
                        progress=progress_for_pyrogram,
                        progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())
                    )
                    await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                    await f.delete()
                    await ms.delete()
                    os.remove(file_path)
                    if ph_path:
                        os.remove(ph_path)
            except Exception as e:
                os.remove(file_path)
                if ph_path:
                    os.remove(ph_path)
                return await ms.edit(f"Error: {e}")
    except Exception as e:
        await ms.edit(f"Error: {e}")


@Client.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client, message):
    method = await client.ask(identifier=(message.chat.id, message.from_user.id, None),
                              text="<b>Send <code>True</code> if you are saving files from bot PM\n\nSend <code>False</code> if you are saving files from a channel</b>")
    
    if method.text.lower() == "true":
        f_link = await client.ask(identifier=(message.chat.id, message.from_user.id, None),
                                  text="<b>Send me the first message Link</b>")
        l_link = await client.ask(identifier=(message.chat.id, message.from_user.id, None),
                                  text="<b>Send me the last message Link</b>")
        
        f_match = re.match(pm_pattern, f_link.text)
        l_match = re.match(pm_pattern, l_link.text)
        
        if f_match and l_match:
            first_user_id = int(f_match.group(1))
            first_message_id = int(f_match.group(2))
            last_user_id = int(l_match.group(1))
            last_message_id = int(l_match.group(2))
            chat_id = message.chat.id
            if first_user_id != last_user_id:
                return await message.reply("Invalid link format. Please provide valid PM links.")
            username = await client.ask(identifier = (message.chat.id, message.from_user.id, None), text="<b>Send this Bot username without @</b>")
       
            for i in range(first_message_id, last_message_id + 1):
                await username.request.delete()
                ms = await message.reply("Please wait.....")
                raw = await USER.get_messages(username.text, i)
                if raw.empty:
                    continue
                if not raw.media:
                    owe = await USER.copy_message(chat_id=CHANNEL, from_chat_id=username.text, message_id=i)
                    await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=int(owe.id))
                    await ms.delete()
                    await owe.delete()
                    continue
                file = getattr(raw, raw.media.value)
                if raw.photo:
                    photo_file_path = f"downloads/{msg_id}.png"
                    await USER.download_media(message=file, file_name=photo_file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time()))
                    f = await USER.send_photo(chat_id=CHANNEL, photo=photo_file_path, caption=raw.caption)  # Send the sticker as a file 
                    await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                    os.remove(photo_file_path)
                    await f.delete()      
                    await ms.delete()  # Delete the "" message
                    continue
                new_filename = file.file_name
                file_path = f"downloads/{new_filename}"
                duration = 0
               
                if raw.sticker:
                    sticker_file_path = f"downloads/{i}.webp"  
                    await USER.download_media(message=file, file_name=sticker_file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time()))
                    f = await USER.send_sticker(chat_id=CHANNEL, sticker=sticker_file_path)  # Send the sticker as a file 
                    await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                    os.remove(sticker_file_path)
                    await f.delete()      
                    await ms.delete()  # Delete the "Sending the sticker" message
                    continue     
                elif raw.document or raw.video:
                    try:
                        await ms.edit("Downloading....")
                        await USER.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())) 
                    except Exception as e:
                        await ms.edit(str(e))
                        continue
                    try:
                        metadata = extractMetadata(createParser(file_path))
                        if metadata.has("duration"):
                            duration = metadata.get('duration').seconds
                    except:
                       pass
                    caption = f"{raw.caption}"
    
                    ph_path = None
         
                    await ms.edit("Uploading....")
                    try:
                        if raw.video:
                            thump = await USER.get_messages(CHANNEL, int(288))
                            thumb = getattr(thump, thump.media.value)
                            ph_path = await USER.download_media(thumb.file_id)
                            img = Image.open(ph_path).convert("RGB")  # Added conversion to RGB
                            img.thumbnail((320, 320))
                            img.save(ph_path, "JPEG")
                            f = await USER.send_video(
                                CHANNEL,
                                video=file_path,
                                caption=caption,
                                thumb=ph_path,
                                duration=duration,
                                progress=progress_for_pyrogram,
                                progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())
                            )
                            await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                            await f.delete()
                            await ms.delete()
                            os.remove(file_path)
                            if ph_path:
                               os.remove(ph_path)
                        if raw.document:
                            thump = await USER.get_messages(CHANNEL, int(287))
                            thumb = getattr(thump, thump.media.value)
                            ph_path = await USER.download_media(thumb.file_id)
                            img = Image.open(ph_path).convert("RGB")  # Added conversion to RGB
                            img.thumbnail((320, 320))
                            img.save(ph_path, "JPEG")
                            f = await USER.send_document(
                                CHANNEL,
                                document=file_path,
                                caption=caption,
                                thumb=ph_path,
                                progress=progress_for_pyrogram,
                                progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())
                            )
                            await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                            await f.delete()
                            await ms.delete()
                            os.remove(file_path)
                            if ph_path:
                                os.remove(ph_path)
                    except Exception as e:
                        os.remove(file_path)
                        if ph_path:
                            os.remove(ph_path)
                        return await ms.edit(f"Error: {e}") 
                
        else:
            await message.reply("Invalid link format. Please provide valid PM links.")
        
    elif method.text.lower() == "false":
        c_link = await client.ask(identifier=(message.chat.id, message.from_user.id, None),
                              text="<b>Send me the First message Link</b>")
        l_link = await client.ask(identifier=(message.chat.id, message.from_user.id, None),
                              text="<b>Send me the last message Link</b>")

        c_match = re.match(channel_pattern, c_link.text)  # Use channel_pattern for matching channel links
        l_match = re.match(channel_pattern, l_link.text)  # Use channel_pattern for matching last message link

        if c_match and l_match:
            r_chat_id = c_match.group(4)

            f_msg_id = int(c_match.group(5))
            l_msg_id = int(l_match.group(5))
            if r_chat_id.isnumeric():
                try:
                    iwe = await USER.get_chat(int("-100" + r_chat_id))
                except Exception as e:
                    return await message.reply(f'Errors - {e}')
            else:
                try:
                    iwe = await client.get_chat(r_chat_id)
                except Exception as e:
                    return await message.reply(f'Errors - {e}')
                r_chat_id = str(iwe.id)

            chat_ed = iwe.id if iwe else r_chat_id
            
            for msg_id in range(f_msg_id, l_msg_id + 1):
                
                owe = await USER.get_messages(chat_ed, msg_id)
                if owe.empty:
                    continue
                if not r_chat_id.isnumeric():
                    await client.copy_message(chat_id=message.from_user.id, from_chat_id=r_chat_id, message_id=msg_id)
                    continue
                if not owe.media:
                    await client.send_message(message.from_user.id, owe.text)
                    continue
                file = getattr(owe, owe.media.value)
                if owe.photo:
                    photo_file_path = f"downloads/{msg_id}.png"
                    await USER.download_media(message=file, file_name=photo_file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time()))
                    f = await USER.send_photo(chat_id=CHANNEL, photo=photo_file_path, caption=owe.caption)  # Send the sticker as a file 
                    await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                    os.remove(photo_file_path)
                    await f.delete()      
                    await ms.delete()  # Delete the "" message
                    continue
                new_filename = file.file_name
                file_path = f"downloads/{new_filename}"
                duration = 0
                ms = await message.reply("Please wait.....")
                
                if owe.sticker:
                    sticker_file_path = f"downloads/{msg_id}.webp"  
                    await USER.download_media(message=file, file_name=sticker_file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time()))
                    f = await USER.send_sticker(chat_id=CHANNEL, sticker=sticker_file_path)  # Send the sticker as a file 
                    await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                    os.remove(sticker_file_path)
                    await f.delete()      
                    await ms.delete()  # Delete the "Sending the sticker" message
                    continue

                elif owe.document or owe.video:
                    try:
                        await ms.edit("Downloading....")
                        await USER.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram,progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())) 
                    except Exception as e:
                        await ms.edit(str(e))
                        continue
                caption = f"**{owe.caption}**" if not None else ''
                try:
                    os.remove(file.thumbs[0].file_id)
                except:
                    pass
               
                try:
                    metadata = extractMetadata(createParser(file_path))
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                except:
                    pass
                await ms.edit("Uploading....")
                try:
                    if owe.video:
                        thump = await USER.get_messages(CHANNEL, int(288))
                        thumb = getattr(thump, thump.media.value)
                        ph_path = await USER.download_media(thumb.file_id)
                        img = Image.open(ph_path).convert("RGB")  # Added conversion to RGB
                        img.thumbnail((320, 320))
                        img.save(ph_path, "JPEG")
                        f = await USER.send_video(
                            CHANNEL,
                            video=file_path,
                            caption=caption,
                            thumb=ph_path,
                            duration=duration,
                            progress=progress_for_pyrogram,
                            progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())
                        )
                        await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                        await f.delete()
                        await ms.delete()
                        os.remove(file_path)
                        if ph_path:
                            os.remove(ph_path)
                    if owe.document:
                        thump = await USER.get_messages(CHANNEL, int(287))
                        thumb = getattr(thump, thump.media.value)
                        ph_path = await USER.download_media(thumb.file_id)
                        img = Image.open(ph_path).convert("RGB")  # Added conversion to RGB
                        img.thumbnail((320, 320))
                        img.save(ph_path, "JPEG")
                        f = await USER.send_document(
                            CHANNEL,
                            document=file_path,
                            caption=caption,
                            thumb=ph_path,
                            progress=progress_for_pyrogram,
                            progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time())
                        )
                        await client.copy_message(chat_id=message.from_user.id, from_chat_id=CHANNEL, message_id=f.id)
                        await f.delete()
                        await ms.delete()
                        os.remove(file_path)
                        if ph_path:
                            os.remove(ph_path)
                except Exception as e:
                   os.remove(file_path)
                   if ph_path:
                       os.remove(ph_path)
                   return await ms.edit(f"Error: {e}")
    
