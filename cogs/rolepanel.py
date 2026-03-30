import discord
from discord.ext import commands
from discord import app_commands, ButtonStyle
from func.dc import Bot
from func.log import get_log
import json
from func.file import File
from func.tools import list_all, Mention_False
import asyncio
from func.dc import Bot

class RoleButton(discord.ui.Button):
    def __init__(self, *, role:discord.Role, style: discord.ButtonStyle = ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | discord.Emoji | discord.PartialEmoji | None = None, row: int | None = None, sku_id: int | None = None, id: int | None = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row, sku_id=sku_id, id=id)
        self.role = role
    async def callback(self, interaction: discord.Interaction):
        if self.role in interaction.user.roles:
            await interaction.user.remove_roles(self.role)
            await interaction.response.send_message(
                f"<@&{self.role.id}>を削除しました。",
                ephemeral=True,
                allowed_mentions=Mention_False
            )
        else:
            await interaction.user.add_roles(self.role)
            await interaction.response.send_message(
                f"<@&{self.role.id}>を付与しました。",
                ephemeral=True,
                allowed_mentions=Mention_False
            )

class MultiRolePanelView(discord.ui.LayoutView):
    def __init__(self, roles: list[discord.Role], message:int, description:dict[int, str], title:str):
        super().__init__(timeout=None)
        self.roles = roles
        self.container = discord.ui.Container()
        self.add_item(self.container)
        self.des = description
        self.title = title
        titleText = discord.ui.TextDisplay(f"## {title}")
        self.container.add_item(titleText)

        for role in roles:
            button = RoleButton(
                role=role,
                style=discord.ButtonStyle.secondary,
                label="取得",
                custom_id=f"{role.guild.id}_{message}_{role.id}"
            )
            section = discord.ui.Section(
                discord.ui.TextDisplay(
                    f'<@&{role.id}>\n{"\n".join([f"-# {i}" for i in (self.des[role.id] if role.id in self.des else "").splitlines()])}'
                ),
                accessory=button
            )
            self.container.add_item(section)

class RoleTitleModal(discord.ui.Modal):
    def __init__(self, roles:list[discord.Role], bot:Bot, file:File):
        super().__init__(title="情報を入力", timeout=None)
        self.roles = roles
        self.bot = bot
        self.file = file
        self.descriptions:dict[int, str] = []
        self.des_text:dict[int, discord.ui.Label] = {}
        self._title = discord.ui.Label(
            text="タイトル",
            component=discord.ui.TextInput(
                style=discord.TextStyle.short,
                placeholder="ロールパネル",
                required=False
            )
        )
        self.add_item(self._title)
        for role in roles:
            des = discord.ui.Label(
                text=f"ロール\"{role.name}\"の説明を入力",
                component=discord.ui.TextInput(
                    style=discord.TextStyle.paragraph,
                    required=False
                )
            )
            self.add_item(des)
            self.des_text.update({role.id: des})
    async def on_submit(self, interaction:discord.Interaction):
        des:dict[int, str] = {}
        for i in self.des_text:
            des[i] = self.des_text[i].component.value
        await interaction.response.send_message("待機...(うまくいかない場合は再実行してください)", ephemeral=True)
        mes = await interaction.channel.send(
            "作成待機中...",
            allowed_mentions=Mention_False
        )
        title = self._title.component.value if self._title.component.value != "" else "ロールパネル"
        view = MultiRolePanelView(
            self.roles,
            mes.id,
            des,
            title
        )
        await mes.edit(content=None, view=view, allowed_mentions=Mention_False)
        self.bot.add_view(view)
        self.file.set(
            f"{interaction.guild.id}_{mes.id}",
            {
                "roles": [i.id for i in self.roles],
                "title": title,
                "description": des
            }
        )
        await interaction.edit_original_response(content="作成しました。")


class RoleCog(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        self.log = get_log(self.__class__.__name__)
        self.file:File = None
    @commands.Cog.listener()
    async def on_ready(self):
        self.log.info(f"{self.__class__.__name__}が読み込まれました！")
        try:
            with open("role.json", mode="x") as f:
                f.write("{}")
            self.log.info(f"設定ファイルが生成されていなかったため、ファイルを作成しました。'role.json'")
        except FileExistsError:
            pass
        self.file = File("role.json")
        tasks = []
        f_d = self.file.get_all()
        for gm_id in f_d:
            datas = f_d[gm_id]
            role_ids = datas["roles"]
            title = datas["title"]
            description = datas["description"]
            guild_id, message_id = tuple(gm_id.split("_"))
            guild = self.bot.get_guild(int(guild_id))
            if guild:
                roles = [guild.get_role(role_id) for role_id in role_ids if guild.get_role(role_id)]
                if roles:
                    view = MultiRolePanelView(
                        roles,
                        message_id,
                        description,
                        title
                    )
                    self.bot.add_view(view)
                    print(f"ビューを再登録しました: {[role.name for role in roles]} (Guild ID: {guild_id}, Message ID: {message_id})")
                    tasks.append(asyncio.create_task(asyncio.sleep(0)))
        if tasks:
            await asyncio.gather(*tasks)
    
    @app_commands.command(name="rolepanel")
    @app_commands.default_permissions(manage_roles=True, manage_guild=True)
    async def rolepanel(
        self,
        interaction:discord.Interaction,
        role1:discord.Role,
        role2:discord.Role = None,
        role3:discord.Role = None,
        role4:discord.Role = None,
        role5:discord.Role = None,
        role6:discord.Role = None,
        role7:discord.Role = None,
        role8:discord.Role = None,
        role9:discord.Role = None,
        role10:discord.Role = None,
        ):
        roles:list[discord.Role] = list_all(
            role1,
            role2,
            role3,
            role4,
            role5,
            role6,
            role7,
            role8,
            role9,
            role10
        )
        await interaction.response.send_modal(
            RoleTitleModal(
                roles=roles,
                bot=self.bot,
                file=self.file
            )
        )

async def setup(bot):
    await bot.add_cog(RoleCog(bot))
