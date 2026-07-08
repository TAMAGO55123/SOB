import discord
from discord.ext import commands
from discord import app_commands
from func.dc import Bot
from func.log import get_log
from func.tools import is_bot_admin
import sys
import os

class AdminCog(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        self.log = get_log(self.__class__.__name__)
    @commands.Cog.listener()
    async def on_ready(self):
        self.log.info(f"{self.__class__.__name__}が読み込まれました！")
    
    class Admin(app_commands.Group):
        pass
    admin = Admin(name="admin", description="Bot管理者用コマンド", default_permissions=discord.Permissions(administrator=True))
    
    @admin.command(name="reload", description="再起動")
    async def reload2(self, interaction: discord.Interaction):
        if not is_bot_admin(interaction.user.id):
            await interaction.response.send_message("このコマンドはこのBOTの管理者のみが使用できます。", ephemeral=True)
            return
        
        try:
            await interaction.response.send_message("Botを再起動します...")
            os.execv(sys.executable, ['python'] + sys.argv)
            await interaction.response.edit_message("再起動しました。")
            await self.bot.close()

        except Exception as e:
            await interaction.response.send_message(f"リロードに失敗しました: {e}")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
