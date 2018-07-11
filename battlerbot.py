import discord
import asyncio
import time
import random

#basic discord shit
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
    if message.content.startswith('!battle'):

        if len(message.mentions) < 2:
            await client.send_message(message.channel, "please mention the 2 people battling.")
        
        #create first embed
        embed2 = discord.Embed(
            title=f"Voting for battle between {message.mentions[0].display_name} & {message.mentions[1].display_name}",
            type='rich',
            url=None,
            colour=16007856
            )
        embed2.add_field(name=f'React with :regional_indicator_a: for', value=f"{message.mentions[0].display_name}")
        embed2.add_field(name=f'React with :b: for', value=f"{message.mentions[1].display_name}")
        embed2.set_footer(
            text=f'BattleBot By mango#0001',
            icon_url='https://i.imgur.com/k7aARj9.jpg')
    
        #send off first embed
        msg2 = await client.send_message(message.channel, None, embed=embed2)
        react1 = await client.add_reaction(msg2, '🇦')
        react2 = await client.add_reaction(msg2, '🅱')
        
        await asyncio.sleep(1)

        vote1 = 0
        vote2 = 0
        
        currenttime = time.time()
        #wait 15 seconds for votes
        while (time.time() - currenttime < 5):
            res = await client.wait_for_reaction(['🇦', '🅱'], message=msg2, timeout=10.0)
            if res is None:
                break
            if str(res.reaction.emoji) == '🇦':
                vote1 += 1
            if str(res.reaction.emoji) == '🅱':
                vote2 += 1

        #delete msg and tally votes
        await client.delete_message(msg2)
        
        if vote1 > vote2:
            winner = message.mentions[0]
        else:
            winner = message.mentions[1]

        winnerembed = discord.Embed(
            title=f"{winner.display_name} is the winner of this battle",
            type='rich',
            url=None,
            colour=16007856
            )
        winnerembed.set_thumbnail(url=winner.avatar_url)
        winnerembed.add_field(name=f"The results were", value=f"{message.mentions[0].display_name}: {vote1} votes"   \
                                                              f" | {message.mentions[1].display_name}: {vote2} votes")
        winnerembed.set_footer(
            text=f'BattleBot By mango#0001',
            icon_url='https://i.imgur.com/k7aARj9.jpg')
        
        await client.send_message(message.channel, None, embed=winnerembed)

client.run('token')
