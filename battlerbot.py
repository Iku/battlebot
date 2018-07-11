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
async def on_message(message):
    if message.content.startswith('!battle'):


        if len(message.mentions) < 2:
            await client.send_message(message.channel, "Please mention the 2 users battling.")
            return
        

        flip = random.randint(0,1)
        if flip == 0:
            firstturn = message.mentions[0] 
            secondturn = message.mentions[1]
        else:
            firstturn = message.mentions[1] 
            secondturn = message.mentions[0]
        
        
        embed = discord.Embed(
            title=f"{firstturn.display_name} goes first",
            type='rich',
            url=None,
            colour=16007856
            )
        embed.add_field(name=f'TIME', value=f'1:30')
        embed.set_thumbnail(url=f"{firstturn.avatar_url}")
        embed.set_footer(
            text=f'BattleBot By mango#0001',
            icon_url='https://i.imgur.com/HVNFdu6.jpg') 
        msg1 = await client.send_message(message.channel, None, embed=embed)

        await asyncio.sleep(90)

        await client.delete_message(msg1)

        embedtime1 = discord.Embed(
            title=f"TIMES UP ",
            type='rich',
            url=None,
            colour=16007856
            )
        embed.set_thumbnail(url=f"{firstturn.avatar_url}")
        embedtime1.set_footer(
            text=f'BattleBot By mango#0001',
            icon_url='https://i.imgur.com/HVNFdu6.jpg') 
        timesup1 = await client.send_message(message.channel, None, embed=embedtime1)
 
        await asyncio.sleep(5)

        await client.delete_message(timesup1)

        embedt2 = discord.Embed(
            title=f"{secondturn.display_name} you're up!",
            type='rich',
            url=None,
            colour=16007856
            )
        embedt2.set_thumbnail(url=f"{secondturn.avatar_url}")
        embedt2.add_field(name=f'TIME', value=f'1:30')
        embedt2.set_footer(
            text=f'BattleBot By mango#0001',
            icon_url='https://i.imgur.com/HVNFdu6.jpg') 
        secondmsg = await client.send_message(message.channel, None, embed=embedt2)

        await asyncio.sleep(90)

        await client.delete_message(secondmsg)

        embedtime2 = discord.Embed(
            title=f"TIMES UP ",
            type='rich',
            url=None,
            colour=16007856
            )
        embedtime2.set_thumbnail(url=f"{secondturn.avatar_url}")
        embedtime2.add_field(name=f'TIME', value=f'1:30')
        embedtime2.set_footer(
            text=f'BattleBot By mango#0001',
            icon_url='https://i.imgur.com/HVNFdu6.jpg') 
        timesup2 = await client.send_message(message.channel, None, embed=embedtime1)
 
        await asyncio.sleep(5)

        await client.delete_message(timesup2)


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
            icon_url='https://i.imgur.com/HVNFdu6.jpg')
    
        #send off first embed
        msg2 = await client.send_message(message.channel, None, embed=embed2)
        #add reactions to message
        react1 = await client.add_reaction(msg2, '🇦')
        react2 = await client.add_reaction(msg2, '🅱')
        
        #sleep for 1 second due to a bug in discord.py
        await asyncio.sleep(1)
       
        #create variables for tallying
        vote1 = 0
        vote2 = 0
        
        #create a list of users who have voted and add the bot before hand
        voters = [client.user.id]

        #get current time
        currenttime = time.time()
        
        def check(reaction, user):
            e = str(reaction.emoji)
            return e.startswith(('🇦', '🅱'))

        #run a 15 second loop tracking reactions made
        while (time.time() - currenttime < 15):
            res = await client.wait_for_reaction(['🇦', '🅱'], message=msg2, timeout=15, check=check)
            #if theres no votes, break the loop so it doesn't hang
            if res is None:
                break
            #if the user id isn't in the voter list, add thier reaction to the tally
            if res.user.id not in voters and str(res.reaction.emoji) == '🇦':
                vote1 += 1
            if res.user.id not in voters and str(res.reaction.emoji) == '🅱':
                vote2 += 1
            #add thier user id to the voter list so they can't vote multiple times
            voters.append(res.user.id)
        
        #delete msg and tally votes
        await client.delete_message(msg2)
        
        if vote1 > vote2:
            winner = f"{message.mentions[0].display_name} is the winner of this battle"
            winavi = message.mentions[0].avatar_url
        elif vote1 < vote2:
            winner = f"{message.mentions[1].display_name} is the winner of this battle"
            winavi = message.mentions[1].avatar_url
        elif vote1 == vote2:
            winner = "It's a tie"
            winavi = "https://i.imgur.com/DjyaJaK.png"

        winnerembed = discord.Embed(
            title=f"{winner}",
            type='rich',
            url=None,
            colour=16007856
            )
        winnerembed.set_thumbnail(url=f"{winavi}")
        winnerembed.add_field(name=f"The results were", value=f"{message.mentions[0].display_name}: {vote1} votes"   \
                                                              f" | {message.mentions[1].display_name}: {vote2} votes")
        winnerembed.set_footer(
            text=f'BattleBot By mango#0001',
            icon_url='https://i.imgur.com/HVNFdu6.jpg')
        
        await client.send_message(message.channel, None, embed=winnerembed)

client.run('token')
