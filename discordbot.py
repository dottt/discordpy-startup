import discord
from discord.ext import commands
import asyncio
import os
import datetime
from datetime import datetime, timedelta, timezone
from discord.utils import get

JST = timezone(timedelta(hours=+9), 'JST')

client = commands.Bot(command_prefix='!')
token = os.environ['DISCORD_BOT_TOKEN']
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command()
async def rect(ctx, about = "募集", cnt = 4, settime = 10800.0):
    cnt, settime = int(cnt), float(settime)
    max_cnt = cnt;
    now = datetime.now(JST)
    end_at = now + timedelta(seconds=settime)

    reaction_member = [">>>"]
    test = discord.Embed(title=about,colour=0x1e90ff)
    test.add_field(name=f"あと{cnt}人 募集中 {end_at.strftime('%H:%M:%S')}まで\n", value=None, inline=True)
    msg = await ctx.send(embed=test)
    
    leader = ctx.author.name
    reaction_member.append(leader)
    cnt -= 1
    test = discord.Embed(title=about,colour=0x1e90ff)
    test.add_field(name=f"あと__{cnt}__人 募集中 {end_at.strftime('%H:%M:%S')}まで\n", value='\n'.join(reaction_member), inline=True)
    await msg.edit(embed=test)
    
    #投票の欄
    sanka = get(client.emojis, name='sanka')
    await msg.add_reaction(sanka)
    husanka = get(client.emojis, name='husanka')
    await msg.add_reaction(husanka)

    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji == '✖' or emoji == str(sanka) or emoji == str(husanka)

    while len(reaction_member)-1 <= max_cnt:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=settime, check=check)
        except asyncio.TimeoutError:
            # await ctx.send('残念、人が足りなかったようだ...')
            test = discord.Embed(title=about,colour=0x1e90ff)
            test.add_field(name=f"募集期限が切れました\n", value='\n'.join(reaction_member), inline=True)
            await msg.edit(embed=test)
            break
        else:
            if str(reaction.emoji) == str(sanka):
                if user.name in reaction_member:
                    pass
                else:
                  reaction_member.append(user.name)
                  cnt -= 1
                  test = discord.Embed(title=about,colour=0x1e90ff)
                  test.add_field(name=f"あと__{cnt}__人 募集中 {end_at.strftime('%H:%M:%S')}まで\n", value='\n'.join(reaction_member), inline=True)
                  await msg.edit(embed=test)
                  await msg.remove_reaction(str(husanka), user)
                    
                if cnt == 0:
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__{cnt}__人 募集中 {end_at.strftime('%H:%M:%S')}まで\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                    finish = discord.Embed(title=about,colour=0x1e90ff)
                    finish.add_field(name="おっと、メンバーがきまったようだ",value='\n'.join(reaction_member), inline=True)
                    await ctx.send(embed=finish)

            elif str(reaction.emoji) == '✖':
                if user.name == leader:
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"募集主が募集をやめました\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                    break
                if user.name in reaction_member:
                    reaction_member.remove(user.name)
                    cnt += 1
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__{cnt}__人 募集中 {end_at.strftime('%H:%M:%S')}まで\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                else:
                    pass
            elif str(reaction.emoji) == str(husanka):
                if user.name == leader:
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"募集主が募集をやめました\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                    break
                if user.name in reaction_member:
                    reaction_member.remove(user.name)
                    cnt += 1
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__{cnt}__人 募集中 {end_at.strftime('%H:%M:%S')}まで\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                else:
                    continue
        # リアクション消す。メッセージ管理権限がないとForbidden:エラーが出ます。
        await msg.remove_reaction(str(reaction.emoji), user)

client.run(token)
