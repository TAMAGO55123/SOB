from typing import TypeVar, Tuple
import copy
import discord
from os import getenv
from dotenv import load_dotenv
load_dotenv()

T = TypeVar("T")

def list_all(*args:T) -> list[T]:
    r_l:list[T] = []
    for i in args:
        if i != None:
            r_l.append(i)
    return r_l

Mention_False:discord.AllowedMentions = discord.AllowedMentions(
    roles=False,
    users=False,
    replied_user=False,
    everyone=False
)

def is_bot_admin(id:int):
    bot_admins = [int(i) for i in getenv("ADMINID").split(",")]
    return id in bot_admins