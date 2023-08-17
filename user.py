import asyncio

from pyrogram import Client, filters
from info import API_ID, API_HASH, STRING

User = Client("user-test", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

