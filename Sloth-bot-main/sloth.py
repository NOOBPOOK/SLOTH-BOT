import wikipedia
import nextcord
from nextcord.ui import Button, View, Select 
from nextcord.utils import get
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import smtplib
import datetime
import webbrowser
import youtube_dl
import humanfriendly
import time
import random
import asyncio
import asyncpraw
import youtube_dl
from youtubesearchpython.__future__ import VideosSearch

reddit = asyncpraw.Reddit(client_id= "rlxZ8ONX4K12gG28bslAQw",
                     client_secret = "SeclhK30B2TG7ndn7V4gRB6yQs5bmg",
                     username = "Advanced_Daikon756",
                     password = "#noobpookveduki1234",
                     user_agent = "scrbot")
                     
intents=nextcord.Intents(messages = True, message_content=True, guilds = True, voice_states = True, members=True)
client = commands.Bot(command_prefix="$", help_command=None, intents=intents)
board = []
music = []
queue = []
dur = []
que_time = 0
gameOver = True
cricket_p1 = ""
cricket_p2 = ""
winningConditions = [
    [ 0, 1, 2],
    [ 3, 4, 5],
    [ 6, 7, 8],
    [ 0, 3, 6],
    [ 1, 4, 7],
    [ 2, 5, 8],
    [ 0, 4, 8],
    [ 2, 4, 6]
]

#Music related functions   
@client.command()
async def join(ctx):
    if ctx.voice_client == None:
        if (ctx.author.voice):
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.reply("Bot connected to play music!🎶")
        else:
            await ctx.reply("You're not in a Voice Channel!🎶")
    else:
        await ctx.reply("The Bot is already connected to a Voice Channel!")
            
@client.command()
async def leave(ctx):
    if ctx.voice_client:
        global music
        global queue
        global dur
        global que_time
        await ctx.voice_client.disconnect()
        await ctx.reply("Disconnected from Voice channel!")
        music = []
        queue = []
        dura = []
        que_time = 0
    else:
        await ctx.reply("The Bot is not connected to any Voice Channel!")
    
@client.command()
async def play(ctx,* ,arg):
    if ctx.voice_client:
        if ctx.author.voice:
            global music
            global queue
            global dur
            global que_time
            video = VideosSearch(str(arg),limit=1)
            vid = await video.next()
            url =(vid['result'][0]['link'])
            name = (vid['result'][0]['title'])
            dura = (vid['result'][0]['duration'])
            if len(music) != 0:
                music.append(url)
                queue.append(name)
                dur.append(dura)
                x = dura.split(":")
                dt = int(x[0])*60 + int(x[1])
                que_time+=dt
                await ctx.message.delete()
                await ctx.send(f"**{name}** has been added to the queue\n**Expexted time:- **{int(que_time/60)}:{int(que_time%60)}!")
            else:
                music.append(url)
                queue.append(name)
                dur.append(dura)
                x = dura.split(":")
                dt = int(x[0])*60 + int(x[1])
                que_time+=dt
                await qplay(ctx, url)
        else:
            await ctx.reply("You are not connected to Voice Channel!")
    else:
        await ctx.reply(f"The Bot is not connected to any Voice Channel!")

@client.command()
async def q(ctx):
    global queue
    global dur
    global que_time
    if len(queue)>1:
        mins = int(que_time/60)
        sec = int(que_time%60)
        quebed = nextcord.Embed(title = f"MUSIC QUEUE🎶", description=('\n\n'.join(map(str,queue))) ,color=0x3498db)
        quebed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2018/09/17/14/27/headphones-3683983_960_720.jpg")
        quebed.set_footer(text = f"Time for the whole queue {mins}mins {sec}seconds!")
        await ctx.reply(embed = quebed)
    else:
        await ctx.reply("No Queue Exits!")
    
@client.command()
async def qremove(ctx, n:int):
    global music
    global dur
    global queue
    global que_time
    if n<=(len(music)+1) and n !=0:
        await ctx.reply(f"{queue[n-1]} has been removed from the queue!\nQueue Updated!")
        del music[n-1]
        x = dur[n-1].split(":")
        dt = int(x[0])*60 + int(x[1])
        que_time-=dt
        del dur[n-1]
        del queue[n-1]
    else:
        await ctx.reply("Song doesn't exist at this Position!")

async def qplay(ctx,url):
    global music
    global queue
    global dur
    FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format':'bestaudio'}
    vc = ctx.voice_client
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url , download = False)
        try:
            await ctx.message.delete()
        except:
            print("Not Available!")
           
        url2 = info['formats'][0]['url']
        music_bed = nextcord.Embed(title = f"Music World!", description=f"{info['title']}", color=0x3498db)
        music_bed.set_image(url = f"{info['thumbnails'][3]['url']}")
        music_bed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2018/09/17/14/27/headphones-3683983_960_720.jpg")
        music_bed.set_footer(text = f"Length of the song >>> {dur[0]}")
        await ctx.send(embed = music_bed)
        vc.play(await nextcord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS))
        await music_but(ctx)
               
async def music_but(ctx):
    global button1
    global button2
    global mus_but
    global view
    global but1
    global but2
    but1 = 0
    but2 = 0
    button1 = Button(label="Resume", style=nextcord.ButtonStyle.green, emoji="▶️")
    button2 = Button(label="Pause", style=nextcord.ButtonStyle.blurple, emoji="⏸")
    button3 = Button(label="Skip/Next", style=nextcord.ButtonStyle.danger, emoji="⏭️")
    view = View(timeout=500)
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    mus_but = await ctx.send(view = view)
    async def button_callback(interaction):
        global button2
        global mus_but
        global view
        global but2
        global but1
        if but2 == 1:
            button2.disabled = False
        ctx.voice_client.resume()
        button1.disabled = True
        await mus_but.edit(view = view)
        but1 = 1
    button1.callback = button_callback
    async def button_callback(interaction):
        global button1
        global mus_but
        global view
        global but2
        global but1
        if but1 == 1:
            button1.disabled = False
        ctx.voice_client.pause()
        button2.disabled = True
        await mus_but.edit(view = view)
        but2 = 1
    button2.callback = button_callback
    async def button_callback(interaction):
        global button1
        global button2
        global view
        global mus_but
        global music
        global queue
        global dur
        global que_time
        ctx.voice_client.stop()
        button1.disabled = True
        button2.disabled = True
        button3.disabled = True
        await mus_but.edit(view = view)
        del music[0]
        del queue[0]
        x = dur[0].split(":")
        dt = int(x[0])*60 + int(x[1])
        que_time-=dt
        del dur[0]
        try:
            url = music[0]
            await qplay(ctx, url)
        except:
            await ctx.send("Queue Ended 🎧!")
    button3.callback = button_callback

#Other commands        
@client.event
async def on_ready():
    print("Bot just landed on the server!")
    
@client.command()
async def private(ctx):
    myEmbed = nextcord.Embed(title = "Video Games Chat🎮", description=f"Hello there In Private! **{ctx.author}**\nHow may I help you?", color=0xffff00)
    myEmbed.set_author(name="SLOTH BOT#4310")
    await ctx.author.send(embed=myEmbed)
    
@client.command()
async def wiki(ctx, *, arg):
    mes_1 = await ctx.reply("Searching Google!")
    try:
        results = wikipedia.page(arg)
        url = results.url
        content = results.content
        await mes_1.edit(content=f"According to CCC, {url}")
    except Exception as e:
        await mes_1.edit(content="Could not get what you were looking for!")
        
@client.command()
async def luckyroles(ctx, give_rol:nextcord.Role):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=983357105417367612)#Admin Role
    user2_rol = get(user_give.guild.roles, id=983357284660957244)#Modeartor role
    if user_rol in user_give.roles or user2_rol in user_give.roles or user_give == await client.fetch_user(763676643356835840):
        giveaway_mem = random.choice(user_give.guild.members)
        try:
            await giveaway_mem.add_roles(give_rol)
            give_embed = nextcord.Embed(title="Video Games Chat🎮", description = f"**{giveaway_mem}** \n You have just won the giveaway held by **{ctx.author}**\n You have got the **{give_rol}** !🎆🎊🎉*", color=0xffff00)
            give_embed.set_thumbnail(url = giveaway_mem.display_avatar)
            await ctx.reply(embed=give_embed)
            try:
                await giveaway_mem.send(embed=give_embed)
            except:
                await ctx.author.send("Cannot send message to the user who won the giveaway!")
        except Exception as e:
            print(e)
            await ctx.send("Above mentioned role doesn't exist or either the bot is unable to give the Role due to less permissions!")
    else:
        await ctx.send(f"You don't have the necessary role to perrform a giveaway!\n You should have **{user_rol}** or **{user2_rol}** to perform giveaway in the server!")
        
@client.command()
async def admin(ctx, pas:int , chn_id:int, *, arg):
    if pas == 2333:
        try:
            chn = client.get_channel(chn_id)
            admin_ctx = await ctx.author.send("Sending your message!")
            await chn.send(arg)
            await admin_ctx.edit(content=f"Your message has been sent successfully to this channel {chn.mention}")
        except Exception as e:
            await admin_ctx.edit(content=f"Your message could not be delivered to the channel!\n Here is why {e}")
    else:
        await ctx.send(f"The above password is Wrong {ctx.author.mention}!\nTry again!")

@client.command()
async def addrole(ctx, mem: nextcord.Member, rol: nextcord.Role):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=929020271954907218)#Host Chat Role
    user2_rol = get(user_give.guild.roles, id=929076788309680178)#Assiatant role
    if user_rol in user_give.roles or user2_rol in user_give.roles or user_give == await client.fetch_user(763676643356835840):
        try:
            await mem.add_roles(rol)
            rol_emb = nextcord.Embed(title="ROLE UPDATED🔃", description=f"**{rol}** has been given to **{mem}**", color = 0x7289da)
            rol_emb.set_thumbnail(url = mem.display_avatar)
            await ctx.reply(embed = rol_emb)
        except:
            await ctx.reply(f"Something Went Wrong❌,\nCannot give {rol} to {mem}!")
    else:
        await ctx.reply(f"You don't have the necessary permissions!\nOnly {user_rol} and {user2_rol} can use this!")

@client.command()
async def remrole(ctx, mem: nextcord.Member, rol: nextcord.Role):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=929020271954907218)#Host Chat Role
    user2_rol = get(user_give.guild.roles, id=929076788309680178)#Assistant role
    if user_rol in user_give.roles or user2_rol in user_give.roles or user_give == await client.fetch_user(763676643356835840):
        try:
            await mem.remove_roles(rol)
            rol_emb = nextcord.Embed(title="Role Updated🔃", description=f"**{rol}** has been removed from **{mem}**!", color=0x7289da)
            rol_emb.set_thumbnail(url = mem.display_avatar)
            await ctx.reply(embed = rol_emb)
        except Exception as e:
            print(e)
            await ctx.reply(f"Something Went Wrong❌,\nCannot remove {rol} from {mem}!")
    else:
        await ctx.reply(f"You don't have the necessary permissions!\nOnly {user_rol} and {user2_rol} can use this!")

@client.command()
async def timeout(ctx, mem: nextcord.Member, time:int, *, arg):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=929020271954907218)#Host Caht Role
    user2_rol = get(user_give.guild.roles, id=929076788309680178)#Assistant role
    if user_rol in user_give.roles or user2_rol in user_give.roles or user_give == await client.fetch_user(763676643356835840):
        try:
            await mem.edit(timeout = nextcord.utils.utcnow() + datetime.timedelta(seconds=(time*60)), reason=arg)
            time_emb = nextcord.Embed(title="TIMEOUT❌", description=f"**{mem.mention}** is in timeout for **{time}** minute\n**REASON**:*{arg}*", color=0xe74c3c)
            time_emb.set_footer(text = f"{ctx.author} used this command!")
            time_emb.set_thumbnail(url = mem.display_avatar)
            await ctx.reply(embed = time_emb)
        except Exception as e:
            print(e)
            await ctx.reply(f"Cannot timeout {mem}!")
    else:
        await ctx.reply(f"You don't have the necessary permissions!\nOnly {user_rol} and {user2_rol} can use this!")

@client.command()
async def kick(ctx, mem:nextcord.Member, *, arg=None):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=929020271954907218)#Host Caht Role
    user2_rol = get(user_give.guild.roles, id=929076788309680178)#Assistant role
    if user_rol in user_give.roles or user2_rol in user_give.roles or user_give == await client.fetch_user(763676643356835840):
        if arg==None:
            arg="Confidential"
        try:
            url = mem.display_avatar
            await mem.kick(reason=arg)
            mem_emb = nextcord.Embed(title="⭐Kermy's Village⭐", description=f"{mem.mention} was kicked out of the server by {ctx.author}\n**REASON**:*{arg}*", color=0xe74c3c)
            mem_emb.set_thumbnail(url = url)
            await ctx.reply(embed = mem_emb)
        except Exception as e:
            print(e)
            await ctx.reply(f"Cannot kick {mem}!")
    else:
        await ctx.reply(f"You don't have the necessary permissions!\nOnly {user_rol} and {user2_rol} can use this!")

@client.command()
async def pfp(ctx, mem:nextcord.Member):
    mem_emb = nextcord.Embed(title = "PROFIE PICTURE📸", description=f"Here is the pfp of **{mem}**!", color=0x5865F2)
    mem_emb.set_image(url = mem.display_avatar)
    mem_emb.set_footer(text = f"This cmd was used by {ctx.author}")
    await ctx.reply(embed = mem_emb)

@client.command()
async def selfrole(ctx):
    select = MySelect(placeholder="Choose a Role wisely as you can only get one!",
                        options=[nextcord.SelectOption(label="Gamer", emoji="🎮", description="All time Gaming🤙", value="ax_1"),#951940676449349643
                            nextcord.SelectOption(label="Xbox Gamer", emoji="❎", description="The Rich Gamer💲", value="ax_2"),#951942632081334302
                            nextcord.SelectOption(label="YT-Channel", emoji="🎥", description="Has a youtube channel", value="ax_3"),#952330588034056222
                            nextcord.SelectOption(label="Cute People PFP", emoji="📸", description="Are you sure you are cute?", value="ax_4"),#945657244211621888
                            nextcord.SelectOption(label="Popular Mushroom", emoji="🍄", description="Hehe, You are a Mushroom", value="ax_5")#975433260312166411
                            ])
    view = View()
    view.add_item(select)
    await ctx.reply(view = view)

class MySelect(Select):
    async def callback(self, interaction):
        auth = interaction.user
        rol1 = get(auth.guild.roles, id=951940676449349643)#gamer role
        rol2 = get(auth.guild.roles, id=951942632081334302)#xbox gamer role
        rol3 = get(auth.guild.roles, id=952330588034056222)#ytchannel role
        rol4 = get(auth.guild.roles, id=945657244211621888)#cutepfp role
        rol5 = get(auth.guild.roles, id=975433260312166411)#popular mushroom role
        rol_list = [rol1,rol2,rol3,rol4,rol5]
        for rol in rol_list:
            await interaction.user.remove_roles(rol)
            
        self.disabled = True
        view = View()
        view.add_item(self)
        await interaction.response.edit_message(view = view)
            
        if self.values[0] == "ax_1":
            await interaction.user.add_roles(rol1)
            new_emb = nextcord.Embed(title="Role Updated🔃", description=f"{interaction.user.mention} choose the **{rol1}**!", color=0xf1c40f)
            new_emb.set_thumbnail(url=interaction.user.display_avatar)
            await interaction.followup.send(embed = new_emb)
        elif self.values[0] == "ax_2":            
            await interaction.user.add_roles(rol2)
            new_emb = nextcord.Embed(title="Role Updated🔃", description=f"{interaction.user.mention} choose the **{rol2}**!", color=0xf1c40f)
            new_emb.set_thumbnail(url=interaction.user.display_avatar)
            await interaction.followup.send(embed = new_emb)
        elif self.values[0] == "ax_3":  
            await interaction.user.add_roles(rol3)
            new_emb = nextcord.Embed(title="Role Updated🔃", description=f"{interaction.user.mention} choose the **{rol3}**!", color=0xf1c40f)
            new_emb.set_thumbnail(url=interaction.user.display_avatar)
            await interaction.followup.send(embed = new_emb)
        elif self.values[0] == "ax_4":
            await interaction.user.add_roles(rol4)
            new_emb = nextcord.Embed(title="Role Updated🔃", description=f"{interaction.user.mention} choose the **{rol4}**!", color=0xf1c40f)
            new_emb.set_thumbnail(url=interaction.user.display_avatar)
            await interaction.followup.send(embed = new_emb)
        elif self.values[0] == "ax_5":
            await interaction.user.add_roles(rol5)
            new_emb = nextcord.Embed(title="Role Updated🔃", description=f"{interaction.user.mention} choose the **{rol5}**!", color=0xf1c40f)
            new_emb.set_thumbnail(url=interaction.user.display_avatar)
            await interaction.followup.send(embed = new_emb)

#Meme realted functions        
@client.command()
async def meme(ctx):
    all_subs = []
    subreddit = await reddit.subreddit("memes")
    top_red = subreddit.top("day", limit=50)
    async for top_hot in top_red:
        all_subs.append(top_hot)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    memEmbed = nextcord.Embed(title= name)
    memEmbed.set_thumbnail(url = "https://static-prod.adweek.com/wp-content/uploads/2021/06/Reddit-Avatar-Builder-Hero-1280x680.png")
    memEmbed.set_image(url = url)
    ctx_mem = await ctx.reply(embed = memEmbed)
    await meme_but(ctx,ctx_mem)
        
async def meme_but(ctx,ctx_mem):
    button = Button(label="Another One!", style=nextcord.ButtonStyle.blurple, emoji="🤚")
    view = View(timeout=100)
    view.add_item(button)
    async def button_callback(interaction):
        await mem_rep(ctx,ctx_mem)
    button.callback = button_callback
    await ctx.reply(view = view)

#All in one help cmd!       
async def mem_rep(ctx,ctx_mem):
    all_subs = []
    subreddit = await reddit.subreddit("memes")
    top_red = subreddit.top("day", limit=50)
    async for top_hot in top_red:
        all_subs.append(top_hot)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    memEmbed = nextcord.Embed(title= name)
    memEmbed.set_thumbnail(url = "https://static-prod.adweek.com/wp-content/uploads/2021/06/Reddit-Avatar-Builder-Hero-1280x680.png")
    memEmbed.set_image(url = url)
    await ctx_mem.edit(embed = memEmbed)
            
@client.command()
async def help(ctx):
    help_embed = nextcord.Embed(title = "**Content Creator Community**", description = "Here are the various cmds to help you out!", color=0xffff00)
    help_embed.add_field(name="**🤖COMMANDS🤖**", value=f"1.**\$private**: Opens a dm with the user. \n2.**\$wiki [subject]**: Gives Information about the concerned subject. \n3.**\$luckyroles [role_id]**: Makes a giveaway of the mentioned role if the user has suitable permissions.\n4.**\$admin [password] [channel_id] [content]**: Sends the content matter to the described channel through the bot.\n5.**\$selfrole**: Send various options available for roles in the server.\n6.**\$meme**:Gives memes from reddit.\n7.**\$crickethelp**:Cricket instructions for the game!\n8.**\$tictactoehelp**:Tictactoe instructions for the game!",inline = True)
    help_embed.set_author(name = "SLOTH BOT#4310")
    await ctx.reply(embed = help_embed)

#Everrything related to Cricket game
@client.command()
async def cricket(ctx, p1:nextcord.Member, p2:nextcord.Member):
    global gameOver
    if gameOver:
        global cricket_p1
        global cricket_p2
        global runs1
        global runs2
        global wicket1
        global score1
        global balls1        
        global cricketp1_but
        global cricketp2_but
        global target
        global ingl
        global score_msg
        cricket_p1 = p1
        cricket_p2 = p2
        gameOver = False
        ingl = False
        runs1 = ""
        runs2 = ""
        score1 = 0
        score2 = 0
        target = 0
        wicket1 = 0
        wicket2 = 0
        balls1 = 0
        balls2 = 0
        toss = random.randint(1,2)
        if toss==1:
            cricket_p1 = p1
            cricket_p2 = p2
        else:
            cricket_p1 = p2
            cricket_p2 = p1
        wel_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} goes against {cricket_p2.mention} in Cricket!🏏", color = 0xffff00)
        wel_emb.add_field(name="RULES AND REGULATIONS", value=f"1.**{cricket_p1.mention}** will bat first.\n2.**{cricket_p2.mention}** will ball now.\n3.Don't cry for cheating!Accept your own luck!")
        wel_emb.set_thumbnail(url = "https://www.ballebaazi.com/blog/wp-content/uploads/2019/02/wc-history-e1550046374686.jpg")
        await ctx.send(embed = wel_emb)
        view = player1()
        cricketp1_but = await ctx.send(f"For **{cricket_p1}**!",view = view)
        score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} ⚔ {cricket_p2.mention}", color=0xffff00)
        score_emb.add_field(name="SCORECARD📟", value=f"{score1}/{wicket1} ({balls1} balls) \nCurrent Run Rate:0 \t Predicted Score:0")
        score_emb.set_thumbnail(url = cricket_p1.display_avatar)
        score_msg = await ctx.send(embed = score_emb)
        view = player2()
        cricketp2_but = await ctx.send(f"For **{cricket_p2}**!",view = view)
        await time(ctx)
        
async def time(ctx):
    global balls1
    balls1+=1
    await asyncio.sleep(7)
    await match(ctx)
    
class player1(View):
    @nextcord.ui.button(label="One", style=nextcord.ButtonStyle.green, emoji="1️⃣", custom_id="run_1")
    async def one_button_callback(self, button, interaction):
        global cricket_p1
        global runs1
        global score1
        if interaction.user == cricket_p1:
            runs1 = "One"
            score1+=1
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view = self)
            
    @nextcord.ui.button(label="Two", style=nextcord.ButtonStyle.green, emoji="2️⃣", custom_id="run_2")
    async def Two_button_callback(self, button, interaction):
        global cricket_p1
        global runs1
        global score1
        if interaction.user == cricket_p1:
            runs1 = "Two"
            score1+=2
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view = self)
            
    @nextcord.ui.button(label="Three", style=nextcord.ButtonStyle.blurple, emoji="3️⃣", custom_id="run_3")
    async def Three_button_callback(self, button, interaction):
        global cricket_p1
        global runs1
        global score1
        if interaction.user == cricket_p1:
            runs1 = "Three"
            score1+=3
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view = self)
            
    @nextcord.ui.button(label="Four", style=nextcord.ButtonStyle.blurple, emoji="4️⃣", custom_id="run_4")
    async def Four_button_callback(self, button, interaction):
        global cricket_p1
        global runs1
        global score1
        if interaction.user == cricket_p1:
            runs1 = "Four"
            score1+=4
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view = self)
     
    @nextcord.ui.button(label="Six", style=nextcord.ButtonStyle.danger, emoji="6️⃣", custom_id="run_6")
    async def Six_button_callback(self, button, interaction):
        global cricket_p1
        global runs1
        global score1
        if interaction.user == cricket_p1:
            runs1 = "Six"
            score1+=6
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view = self)

class player2(View):
    @nextcord.ui.button(label="One", style=nextcord.ButtonStyle.green, emoji="1️⃣", custom_id="run_1")
    async def one_button_callback(self, button, interaction):
        global cricket_p2
        global runs2
        if interaction.user == cricket_p2:
            runs2 = "One"
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view = self)
            
    @nextcord.ui.button(label="Two", style=nextcord.ButtonStyle.green, emoji="2️⃣", custom_id="run_2")
    async def Two_button_callback(self, button, interaction):
        global cricket_p2
        global runs2
        if interaction.user == cricket_p2:
            runs2 = "Two"
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view = self)
            
    @nextcord.ui.button(label="Three", style=nextcord.ButtonStyle.blurple, emoji="3️⃣", custom_id="run_3")
    async def Three_button_callback(self, button, interaction):
        global cricket_p2
        global runs2
        if interaction.user == cricket_p2:
            runs2 = "Three"
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view = self)
            
    @nextcord.ui.button(label="Four", style=nextcord.ButtonStyle.blurple, emoji="4️⃣", custom_id="run_4")
    async def Four_button_callback(self, button, interaction):
        global cricket_p2
        global runs2
        if interaction.user == cricket_p2:
            runs2 = "Four"
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view = self)
            
    @nextcord.ui.button(label="Six", style=nextcord.ButtonStyle.danger, emoji="6️⃣", custom_id="run_6")
    async def Six_button_callback(self, button, interaction):
        global cricket_p2
        global runs2
        if interaction.user == cricket_p2:
            runs2 = "Six"
            buttons = [x for x in self.children]
            for v in buttons:
                v.disabled = True
            await interaction.response.edit_message(view = self)

async def match(ctx):
    global cricket_p1
    global cricket_p2
    global score1
    global runs1
    global runs2
    global balls1   
    global wicket1
    global score_msg
    if runs1 == "One" and runs2 == "One":
        wicket1+=1
        score1-=1
        score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} ⚔ {cricket_p2.mention}", color=0xffff00)
        score_emb.add_field(name="LAST BALL🥎", value=f"**WICKET**\n{cricket_p1.mention} got trapped in {cricket_p2.mention}'s Trap!")
        score_emb.add_field(name="SCORECARD📟", value=f"{score1}/{wicket1} ({balls1} balls) \nCurrent Run Rate:{round((score1/balls1), 2)} \t Predicted Score:{round((score1/balls1)*10, 2)}")
        score_emb.set_thumbnail(url = cricket_p1.display_avatar)
        await score_msg.edit(embed=score_emb)
    elif runs1 == "Two" and runs2 == "Two":
        wicket1+=1
        score1-=2
        score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} ⚔ {cricket_p2.mention}", color=0xffff00)
        score_emb.add_field(name="LAST BALL🥎", value=f"**WICKET**\n{cricket_p1.mention} got trapped in {cricket_p2.mention}'s Trap!")
        score_emb.add_field(name="SCORECARD📟", value=f"{score1}/{wicket1} ({balls1} balls) \nCurrent Run Rate:{round((score1/balls1), 2)} \t Predicted Score:{round((score1/balls1)*10, 2)}")
        score_emb.set_thumbnail(url = cricket_p1.display_avatar)
        await score_msg.edit(embed=score_emb)
    elif runs1 == "Three" and runs2 == "Three":
        wicket1+=1
        score1-=3
        score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} ⚔ {cricket_p2.mention}", color=0xffff00)
        score_emb.add_field(name="LAST BALL🥎", value=f"**WICKET**\n{cricket_p1.mention} got trapped in {cricket_p2.mention}'s Trap!")
        score_emb.add_field(name="SCORECARD📟", value=f"{score1}/{wicket1} ({balls1} balls) \nCurrent Run Rate:{round((score1/balls1), 2)} \t Predicted Score:{round((score1/balls1)*10, 2)}")
        score_emb.set_thumbnail(url = cricket_p1.display_avatar)
        await score_msg.edit(embed=score_emb)
    elif runs1 == "Four" and runs2 == "Four":
        wicket1+=1
        score1-=4
        score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} ⚔ {cricket_p2.mention}", color=0xffff00)
        score_emb.add_field(name="LAST BALL🥎", value=f"**WICKET**\n{cricket_p1.mention} got trapped in {cricket_p2.mention}'s Trap!")
        score_emb.add_field(name="SCORECARD📟", value=f"{score1}/{wicket1} ({balls1} balls) \nCurrent Run Rate:{round((score1/balls1), 2)} \t Predicted Score:{round((score1/balls1)*10, 2)}")
        score_emb.set_thumbnail(url = cricket_p1.display_avatar)
        await score_msg.edit(embed=score_emb)
    elif runs1 == "Six" and runs2 == "Six":
        wicket1+=1
        score1-=6
        score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} ⚔ {cricket_p2.mention}", color=0xffff00)
        score_emb.add_field(name="LAST BALL🥎", value=f"**WICKET**\n{cricket_p1.mention} got trapped in {cricket_p2.mention}'s Trap!")
        score_emb.add_field(name="SCORECARD📟", value=f"{score1}/{wicket1} ({balls1} balls) \nCurrent Run Rate:{round((score1/balls1), 2)} \t Predicted Score:{round((score1/balls1)*10, 2)}")
        score_emb.set_thumbnail(url = cricket_p1.display_avatar)
        await score_msg.edit(embed=score_emb)
    elif runs2 == "" or runs1 == "":
        score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} ⚔ {cricket_p2.mention}", color=0xffff00)
        score_emb.add_field(name="MISSED❌", value="Anyone one player didn't respond!")
        score_emb.add_field(name="SCORECARD📟", value=f"{score1}/{wicket1} ({balls1} balls) \nCurrent Run Rate:{round((score1/balls1), 2)} \t Predicted Score:{round((score1/balls1)*10, 2)}")
        score_emb.set_thumbnail(url = cricket_p1.display_avatar)
        await score_msg.edit(embed=score_emb)
    elif runs1 != runs2:
        score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} ⚔ {cricket_p2.mention}", color=0xffff00)
        score_emb.add_field(name="LAST BALL🥎", value=f"{cricket_p1.mention} did a **{runs1}** while {cricket_p2.mention} did a **{runs2}**")
        score_emb.add_field(name="SCORECARD📟", value=f"{score1}/{wicket1} ({balls1} balls) \nCurrent Run Rate:{round((score1/balls1), 2)} \t Predicted Score:{round((score1/balls1)*10, 2)}")
        score_emb.set_thumbnail(url = cricket_p1.display_avatar)
        await score_msg.edit(embed=score_emb)
    runs1 = ""
    runs2 = ""
    await pointcount(ctx)
  
async def pointcount(ctx):
    global balls1
    global wicket1
    global score1
    global score_msg
    global ingl
    global target
    global cricketp1_but
    global cricketp2_but
    global cricket_p1
    global cricket_p2
    global gameOver
    if ingl == False:
        if balls1==10 or wicket1==3:
            score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} scored {score1} in {balls1}!", color=0xffff00)
            score_emb.add_field(name="TARGET🎯", value=f"{cricket_p2.mention} needs to score {score1+1} runs in 10 balls with 3 wickets in hand!")
            score_emb.set_thumbnail(url = cricket_p1.display_avatar)
            await score_msg.edit(embed=score_emb)
            target = score1+1
            cricket_p1,cricket_p2 = cricket_p2,cricket_p1
            wicket1 = 0
            score1 = 0
            balls1 = 0
            ingl = True
            await asyncio.sleep(5)
            view = player1()
            await cricketp1_but.edit(f"For **{cricket_p1}**!",view = view)
            view = player2()
            await cricketp2_but.edit(f"For **{cricket_p2}**!",view = view)
            await time(ctx)
        else:
            view = player1()
            await cricketp1_but.edit(view = view)
            view = player2()
            await cricketp2_but.edit(view = view)
            await time(ctx)
    else:
        if score1>=target:
            score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} crushes {cricket_p2.mention} with {10-balls1} balls to spare and {3-wicket1} wickets in hand!", color=0xffff00)
            score_emb.set_thumbnail(url = cricket_p1.display_avatar)
            await score_msg.edit(embed=score_emb)
            gameOver = True
            
        elif balls1==10 or wicket1==3:
            score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p2.mention} crushes {cricket_p1.mention} by {target-score1} runs!", color=0xffff00)
            score_emb.set_thumbnail(url = cricket_p2.display_avatar)
            await score_msg.edit(embed=score_emb)
            gameOver = True
        else:
            view = player1()
            await cricketp1_but.edit(f"**{cricket_p1}** needs to score {target-score1} runs in {10-balls1} balls!",view = view)
            view = player2()
            await cricketp2_but.edit(view = view)
            await time(ctx)

@client.command()
async def gameover(ctx):
    global gameOver
    global cricket_p1
    global cricket_p2
    global cricketp1_but
    global cricketp2_but
    global score_msg
    if ctx.author==cricket_p1 or ctx.author==cricket_p2:
        gameOver = True
        await cricketp1_but.delete()
        await cricketp2_but.delete()
        winner = random.randint(1,2)
        if winner == 1:
            score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p1.mention} crushes {cricket_p2.mention} through toss!", color=0xffff00)
            score_emb.set_thumbnail(url = cricket_p1.display_avatar)
            await score_msg.edit(embed=score_emb)
        else:
            score_emb = nextcord.Embed(title="World ICC Tournament", description=f"{cricket_p2.mention} crushes {cricket_p1.mention} through toss!", color=0xffff00)
            score_emb.set_thumbnail(url = cricket_p2.display_avatar)
            await score_msg.edit(embed=score_emb)
    else:
        await ctx.reply(f"You can only end a game played by you!")
    
@client.command()
async def crickethelp(ctx):
    myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"Here are the various commands and rules in order to play this game!", color=0xffff00)
    myEmbed.set_thumbnail(url = ctx.author.display_avatar)
    myEmbed.add_field(name="Commands:-", value=f"1.**$cricket [player1] [player2] ** which starts the game.\n2.**$gameover** ends the current game and crowns one as the winner(Inorder to use this command, you should be the one who is playing the game).", inline=True)
    myEmbed.add_field(name="Rules:-", value=f"1.Both players should press the button only once.\n2.The one who will bat first will always get the message as interaction failed but don't worry as the response is noted.\n3.Both players should press the button within 5 seconds.\n4.If the bot gets stuck it may be an internal error and you may end the game and restart a new one.\n5.**Enjoy and have a Good Time!**", inline=False)
    myEmbed.set_author(name="SLOTH BOT#4310")
    await ctx.send(embed=myEmbed)

#Everything related to tictactoe!
@client.command()
async def tictactoe(ctx, p1 : nextcord.Member, p2 : nextcord.Member ):
    global player1
    global player2
    global turn
    global gameOver
    global count
    global tic_time    
    if gameOver and p1 != await client.fetch_user(949215188672974871) and p2 != await client.fetch_user(949215188672974871) :
        await tictactoeplay(ctx,p1,p2)
    else:
        await ctx.send("A game is already in progress! \n Finish it before starting a new one! \n You cannot play with the Bot itself!")       
        
async def tictactoeplay(ctx,p1,p2):        
        global player1
        global player2
        global turn
        global gameOver
        global count
        global tic_time
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0
        player1 = p1
        player2 = p2
        #print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]
                
        #determines who goes first!
        num =random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send(f"It is {player1.mention} turn!")
        elif num == 2:
            turn = player2
            await ctx.send(f"It is {player2.mention} turn!")
            
        #calculates time
        tic_time=0
        while True:
            if gameOver == False:
                await asyncio.sleep(1)
                tic_time+=1
            else:
                break
                   
@client.command()
async def place(ctx, pos : int):
    global turn
    global board
    global count
    global player1 
    global player2
    global gameOver
    global tic_time
    
    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0<pos<10 and board[pos - 1] == ":white_large_square:":
                board[pos-1] = mark
                count+=1
                
                #print board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]
                
                checkWinner(winningConditions, mark)
                if gameOver == True:
                    await asyncio.sleep(2)
                    if mark == ":regional_indicator_x:":
                        myEmbed = nextcord.Embed(title="TICTACTOE❌⭕", description=f"{player1.mention} :regional_indicator_x: Wins the Game!", color=0xffff00)
                        myEmbed.add_field(name="Game Stats!", value=f"Time taken:{tic_time} seconds\n Total Moves:{count}",inline = True)
                        myEmbed.set_author(name="M1ke Bot#7179")
                        await ctx.send(embed=myEmbed)
                        await playagain(ctx)
                    elif mark == ":o2:":
                        myEmbed = nextcord.Embed(title="TICTACTOE❌⭕", description=f"{player2.mention} :o2: Wins the Game in just {count} moves!", color=0xffff00)
                        myEmbed.add_field(name="Game Stats!", value=f"Time taken:{tic_time} seconds\n Total Moves:{count}",inline = True)
                        myEmbed.set_author(name="M1ke Bot#7179")
                        await ctx.send(embed=myEmbed)
                        await playagain(ctx)
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")
                    await playagain(ctx)
                
                #switch turns
                if turn == player1: 
                    turn = player2
                elif turn == player2:
                    turn = player1
                
            else:
                await ctx.send("Be sure to change an integer between 1 and 9 and an unmarked tile!")
        else:
            await ctx.send("It is not you turn!")
    else:
        await ctx.send("Please start a new game!")
       
@client.command()
async def clear(ctx):
    global player1
    global player2
    global gameOver
    if ctx.author == player1 or ctx.author == player2:
        num =random.randint(1, 2)
        if num == 1:
            await ctx.send(f"{player1.mention} Wins the Game By Random choice")
        else:
            await ctx.send(f"{player2.mention} Wins the Game By Random choice")
        gameOver = True
        await ctx.send("Game Over!")
    else:
        await ctx.send("You can only end the game played by you!")
            
def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@client.command()
async def tictactoehelp(ctx):
    embed = nextcord.Embed(title = "Video Games Chat", description = f"Everything you need to know about tictactoe", color = 0xffff00)
    embed.add_field(name = "**COMMANDS**", value = f"1.**\$tictactoe [player1] [player2]**: Creates a game between the two mentioned players.\n2.**\$place**: Places your sign on the desired block.\n3.**\&clear**:Ends the game ,*can only be used by players*", inline=True)
    embed.add_field(name = "**RULES**", value = f"1.There is no cheating involved in the game.\n2.Please only play your own turn.\n3.Play it with some sensible sense and don't cry later!", inline=True)
    embed.set_thumbnail(url = ctx.author.display_avatar)
    await ctx.reply(embed = embed)
    
client.run("******BOT-TOKEN******")
