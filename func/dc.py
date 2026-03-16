from discord.ext import commands
class Bot(commands.Bot):
    def __init__(self, *args, **kwrds):
        super().__init__(*args, **kwrds)