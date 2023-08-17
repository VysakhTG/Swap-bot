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


      
