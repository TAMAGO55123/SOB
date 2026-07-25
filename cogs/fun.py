import discord
from discord.ext import commands
from discord import app_commands
from func.dc import Bot
from func.log import get_log
from func.tools import convert_size
import datetime
import aiohttp
import jpholiday
from random import randint
import io
import re

class FunCog(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        self.log = get_log(self.__class__.__name__)
    @commands.Cog.listener()
    async def on_ready(self):
        self.log.info(f"{self.__class__.__name__}が読み込まれました！")

    class Fun(app_commands.Group):
        pass

    fun = Fun(name="fun", description="娯楽用コマンド")

    @fun.command(name="aniv", description="記念日を取得します。")
    async def aniv(self, interaction:discord.Interaction, year:int = None, month:int = None, day:int = None):
        await interaction.response.defer(thinking=True)
        is_today = year == None or month == None and day == None
        if is_today is False:
            d = f"{str(month).zfill(2)}{str(day).zfill(2)}"
            date = datetime.date(year=year, month=month, day=day)
        else:
            d = datetime.date.today().strftime("%m%d")
            date = datetime.date.today()
        async with aiohttp.ClientSession() as session:
            # powered by whatistodayAPI | https://note.com/sooz/n/naffb68c7f53b
            async with session.get(f"https://api.whatistoday.cyou/index.cgi/v3/anniv/{d}") as resp:
                data = await resp.json()
        self.log.debug(data)
        holiday = jpholiday.is_holiday_name(date=date)
        anniv = []
        anniv.append(data["anniv1"])
        if data["anniv2"] != "":
            anniv.append(data["anniv2"])
        if data["anniv3"] != "":
            anniv.append(data["anniv3"])
        if data["anniv4"] != "":
            anniv.append(data["anniv4"])
        if data["anniv5"] != "":
            anniv.append(data["anniv5"])
        await interaction.followup.send(
            embed=discord.Embed(
                title=f"{"今日" if is_today else date.strftime("%Y/%m/%d")}は何の日?",
                description=f"{f"今日は祝日です！\n- {holiday}\n" if holiday else ""}- {"\n- ".join(anniv)}",
                colour=discord.Colour.green()
            )
            .set_footer(text="powered by whatistodayAPI")
        )

    @fun.command(name="dice", description="ダイスを振ります。")
    @app_commands.describe(
        dice="〇d〇の形式で指定してください(例:1d100)"
    )
    async def manydice(self, interaction: discord.Interaction, dice: str):
        try:
            m = re.search(r"(\d+)d(\d+)", dice)
            a = m.group(1)
            b = m.group(2)
    
            await interaction.response.defer()
            res = [randint(1, int(b)) for i in range(int(a))]
    
            MAX_BYTES = 5 * 1024 * 1024  # 5MB
    
            sres = ",\n".join(map(str, res))
            all = sum(res)
            encoded = sres.encode("utf-8")
    
            is_compressed = False
            byte = len(encoded)
            # 5MBを超える場合は切り詰める
            if len(encoded) > MAX_BYTES:
                is_compressed = True
                encoded = encoded[:MAX_BYTES]
                sres = encoded.decode("utf-8", errors="ignore")
            print(all)
    
            em_output = f"{dice}\n-> (計算結果はファイル){f"(結果が大きいため、一部切り捨てられました。元:{convert_size(byte)})" if is_compressed else ""}\n-> {all}"
            fileio = io.StringIO()
            fileio.write(sres)
            fileio.seek(0)
            file = discord.File(fileio, filename="result.txt")
    
            embed = discord.Embed(
                title="結果",
                description=em_output[:4000],
                colour=discord.Colour.green()
            )
    
            await interaction.followup.send(
                embed=embed,
                file=file
            )
        except Exception as e:
            await interaction.followup.send("計算に失敗しました", embed=discord.Embed(description=f"```{e}```"))
            self.log.error(e)

async def setup(bot):
    await bot.add_cog(FunCog(bot))
