from typing import TypeVar, Tuple
import copy
import discord

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