from os import getenv, listdir
from os.path import isdir, join, dirname
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.app_commands import default_permissions
from func.dc import Bot
from func.log import get_log, stream_handler
from asyncio import create_task, run
from tags_collection.func.tools import tc_ob
load_dotenv()

async def main(bot: Bot):
    log = get_log("Main")
    @bot.event
    async def on_ready():
        log.info(f"{bot.user.name}としてログインしました")
    
    @bot.event
    async def setup_hook():
        try:
            log.info("通常Cog読み込み")
            for cog in listdir("cogs"):
                if cog.endswith(".py"):
                    await bot.load_extension(f"cogs.{cog[:-3]}")
            if isdir("tags_collection"):
                API_URL = getenv("API_URL") == None
                API_KEY = getenv("API_KEY") == None
                if API_URL or API_KEY:
                    log.warn(f"{'API_URL' if API_URL else ''}{'、' if API_URL and API_KEY else ''}{'API_KEY' if API_KEY else ''}が.env(環境変数)に指定されていません。\nこの機能を使用するには指定してください。")
                log.info("Tags Collection Cog読み込み")
                for cog in listdir("tags_collection"):
                    if cog.endswith(".py"):
                        await bot.load_extension(f"tags_collection.{cog[:-3]}")
            synced = await bot.tree.sync()
            log.info(f"{len(synced)}個のコマンドを同期しました。")
            if isdir("tags_collection"):
                tc_synced = await bot.tree.sync(guild=tc_ob)
                log.info(f"Tags Collectionサーバーに{len(tc_synced)}個のコマンドを同期しました。")
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
    
    @bot.event
    async def on_message(message:discord.Message):
        if message.guild:
            if message.guild.id == 1484823783817613352:
                #print(message.content)
                if "@everyone" in message.content:
                    with open(join(dirname(__file__), "emoji/noeveryone.png"), "rb") as f:
                        bt = f.read()
                    webhook = await message.channel.create_webhook(
                        name="everyoneすんな",
                        avatar=bt
                    )
                    await webhook.send(
                        content="https://cdn.discordapp.com/emojis/1485589494127398985.webp?size=240"
                    )
                    await webhook.delete()
            await bot.process_commands(message)
    
    await bot.start(getenv("TOKEN"))

if __name__ == "__main__":
    intents = discord.Intents.all()
    bot = Bot(command_prefix="s!", intents=intents)
    discord.utils.setup_logging(handler=stream_handler)
    run(main(bot))
