from os import getenv, listdir
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.app_commands import default_permissions
from func.dc import Bot
from func.log import get_log, stream_handler
from asyncio import create_task, run
from web import web
load_dotenv()

async def main(bot: Bot):
    log = get_log("Main")
    @bot.event
    async def on_ready():
        log.info(f"{bot.user.name}としてログインしました")
        create_task(web())
    
    @bot.event
    async def setup_hook():
        try:
            for cog in listdir("cogs"):
                if cog.endswith(".py"):
                    await bot.load_extension(f"cogs.{cog[:-3]}")
            synced = await bot.tree.sync()
            log.info(f"{len(synced)}個のコマンドを同期しました。")
        except Exception as e:
            log.error(f"コマンドの同期中にエラーが発生しました。")
    
    class SendEmbedModal(discord.ui.Modal):
        def __init__(self, channel:discord.TextChannel, message:str):
            super().__init__(
                title="フォーム",
                timeout=None,
            )

            self.messages = discord.ui.TextInput(
                label="カラーコードを送信してください(例:5865f2)",
                style=discord.TextStyle.short,
                max_length=6,
                required=False,
            )
            self.add_item(self.messages)

            self.channel = channel
            self.message = message

        async def on_submit(self, interaction:discord.Interaction):
            if self.messages.value:
                a = int(f"0x{self.messages.value}", 16)
            else:
                a = None
            await self.channel.send(embed=discord.Embed(description=self.message, color=a))
            await interaction.response.send_message("sended.",ephemeral=True)

    @bot.tree.context_menu(name="メッセージを再送信")
    @default_permissions(administrator=True)
    async def message_re_send(interaction:discord.Interaction, message:discord.Message):
        await message.channel.send(content=message.content, embeds=message.embeds)
        await interaction.response.send_message(content="sended.",ephemeral=True)

    @bot.tree.context_menu(name="メッセージを埋め込みに変換")
    @default_permissions(administrator=True)
    async def message_send_embed(interaction:discord.Interaction, message:discord.Message):
        modal = SendEmbedModal(channel=message.channel, message=message.content)
        await interaction.response.send_modal(modal)
    
    @bot.tree.context_menu(name="埋め込みをメッセージに変換")
    @default_permissions(administrator=True)
    async def embed_send_message(interaction:discord.Interaction, message:discord.Message):
        a = ""
        for i in message.embeds:
            a = a + i.description
        await message.channel.send(content=a)
        await interaction.response.send_message("sended.", ephemeral=True)
    
    await bot.start(getenv("TOKEN"))

if __name__ == "__main__":
    intents = discord.Intents.all()
    bot = Bot(command_prefix="s!", intents=intents)
    discord.utils.setup_logging(handler=stream_handler)
    run(main(bot))
