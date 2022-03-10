
import discord,time,pprint,os,sys,random
from discord.ext import commands
from discord import utils
import json,pprint
print("bop")
os.chdir('C:\\Users\\Parker\\Documents\\wordle bot')

file=open("TOKEN1.txt","r")
TOKEN=file.readline()
file.close()
 
intents = discord.Intents.all()
bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='?',help_command=None)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


def contains(lists,name):

    for i in lists:
        if i.startswith(name):
            return i
        else:
            pass
    return False

def valid(arg1):
    File=open("words.txt",'r')
    possib=File.readlines()
    File.close()

    newlist=[]

    for i in possib:
        i = i.rstrip("\n")
        newlist.append(i)

    if len(arg1)!=5:
        return False
    elif arg1.isalpha==False:
        return False 

    elif arg1 not in newlist:
        return False

    return True

def tofile(lines):
    newprog="".join(lines)

    File=open("Progress.txt","w")
    File.write(newprog)
    File.close()

def evalues(data,answer,embed):

    File=open('C:\\Users\\Parker\\Documents\\wordle bot\\get\\%s.json'%(answer),'r')
    y=json.load(File)
    File.close()
    string=""
    letters=['q','w',"e","r",'t','y','u','i','o','p','\n\n','a','s','d','f','g','h','j','k','l','\n\n','z','x','c','v','b','n','m']

    File=open('emotes.txt','r')
    lines=File.readlines()
    File.close()

    for l in letters:
        if l=='\n\n':
            pass
        else:
            linevalue=ord(l)-97+78
            letters[letters.index(l)]=getevalue(linevalue,lines)

    for i in data:
        values=y[i]

        stuff=assign(values,letters)
        letters=stuff[1]
        tup=stuff[0]

        for m in values:
            if m[0].upper() in letters:
                letters.remove(m[0].upper())

        string+='%s %s %s %s %s\n\n'%(tup[0],tup[1],tup[2],tup[3],tup[4])


    embed.add_field(name='Progress:', value=string+'\n----------------------------------------',inline=False)
    embed.add_field(name='Remaining:',value=' '.join(letters),inline=False)

    return embed

def assign(values,letters):

    tup=list()

    File=open('emotes.txt','r')
    lines=File.readlines()
    File.close()

    lit=list()
    temp=['q','w',"e","r",'t','y','u','i','o','p','\n\n','a','s','d','f','g','h','j','k','l','\n\n','z','x','c','v','b','n','m']

    for i in range(5):

        char=values[i][0]
        color=values[i][1]

        linevalue=ord(char)-97

        if 'open' in letters[temp.index(char)]:
            if color=='b':
                letters[temp.index(char)]=getevalue(linevalue+52,lines)

            elif color=='y':
                letters[temp.index(char)]=getevalue(linevalue+26,lines)
            else:
                letters[temp.index(char)]=getevalue(linevalue,lines)

        elif color=='g':
            letters[temp.index(char)]=getevalue(linevalue,lines)
        
        elif color=='y':
            if letters[temp.index(char)][1]=='b':
                letters[temp.index(char)]=getevalue(linevalue+26,lines)

        if color=='b':
            linevalue+=52
        elif color=='y':
            linevalue+=26
        else:
            pass

        tup.append(getevalue(linevalue,lines))

    lit.append(tup)
    lit.append(letters)

    return lit

def getevalue(lval,lines):
        emote=lines[lval]
        emote= emote.rstrip("\n")

        evalue="%s"%(emote)
        return evalue
        

@bot.command()
async def wordle(ctx):

    File=open("Progress.txt",'r')
    player=ctx.author

    contain=contains(File.readlines(),str(player)) #if player has an active game

    Stats=open('Stats.txt','r')
    stat=contains(Stats.readlines(),str(player))
    Stats.close()
    
    if stat:
        pass
    else:
        Stats=open('Stats.txt','a')
        Stats.write('%s,0,0,0,0,0,0,0,0,\n'%(player))
        Stats.close()
    
    Stats.close()
    
    File.close()

    if contain!=False:
        await ctx.channel.send("you are already in a wordle, ?progress to see your progress")
        return
    else:

        File=open("answers.txt","r")
        answer= random.choice(File.read().splitlines())     #select a random answer
        File.close()

        File=open("Progress.txt","a")
        File.write("%s,%s,0,,\n"%(player,answer))

    embed=discord.Embed(title='%s Wordle'%(str(player)[0:-5]),colour=discord.Colour.blue(),)
    embed.set_footer(text="play: ?guess [word]")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/513864352663863328/947958181596909608/unknown.png")
    await ctx.channel.send(embed=embed)

@bot.command()
async def progress(ctx):
    
    File=open("Progress.txt",'r')
    player=ctx.author

    contain=contains(File.readlines(),str(player))

    File.close()

    if contain==False:
        await ctx.channel.send("you are not currently in a wordle game, ?wordle to start one")
        return

    else:
        data=contain.split(',')
        embed=discord.Embed(title='%s Wordle'%(str(player)[0:-5]),colour=discord.Colour.blue(),)

        if data[3]=="":

            embed.add_field(name='Progress:', value='you have not made any guesses yet\n\nplay: ?guess [word]', inline=False)

        else:
            answer=data[1]
            data=data[3].split('|')
            data.pop(-1)

            embed=evalues(data,answer,embed)

            embed.set_footer(text="play: ?guess [word]")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/513864352663863328/947958181596909608/unknown.png")
        await ctx.channel.send(embed=embed)


@bot.command()
async def guess(ctx, arg1):

    arg1=str(arg1).lower()

    File=open("Progress.txt",'r')
    lines=File.readlines()
    File.close()

    player=ctx.author
    contain=contains(lines,str(player))

    if valid(arg1)==False:
        await ctx.channel.send('`not valid`')

    elif contain == False:
        await ctx.channel.send('`you are not in a game`')

    else:
        arg1=arg1.lower()
        ite=contain.split(',')

        ite[2]=str(int(ite[2])+1)
        ite[3]=ite[3]+arg1+"|"


        Stats=open('Stats.txt','r')
        stati=Stats.readlines()
        Stats.close()

        person=contains(stati,str(player))
        pos=stati.index(person)
        
        nums=person.split(',')

        attempts=ite[2] #attempts
        prog=ite[3] #progress
        answer=ite[1] #answer

        line=",".join(ite)

        lines[lines.index(contain)]=line

        embed=discord.Embed(title='%s Wordle'%(str(player)[0:-5]),colour=discord.Colour.blue())

        if arg1 == answer:

            data=prog.split('|')
            data.pop(-1)

            embed=evalues(data,answer,embed)

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/513864352663863328/947958181596909608/unknown.png")
            embed.set_footer(text='Correct! it took you %s guesses! - ?wordle to start a new game'%(attempts))

            nums[int(attempts)]=str(int(nums[int(attempts)])+1)
            nums[7]=str(int(nums[7])+1)

            Stats=open('Stats.txt','w')


            stati[pos]=','.join(nums)
            Stats.write(''.join(stati))
            Stats.close()

            lines.pop(lines.index(line))
            tofile(lines)

            await ctx.channel.send(embed=embed)

        else:
         
            data=prog.split('|')

            data.pop(-1)

            embed=evalues(data,answer,embed)

            if attempts=='6':
                embed.add_field(name='᲼᲼', value='youre out of guesses, the answer was : %s'%(answer), inline=False)
                lines.pop(lines.index(line))
                tofile(lines)

                Stats=open('Stats.txt','w')
                nums[8]=str(int(nums[8])+1)
                nums[7]=str(int(nums[7])+1)
                stati[pos]=','.join(nums)

                Stats.write(''.join(stati))
                Stats.close()

            else:
                embed.set_footer(text='number of guesses: %s'%(attempts))
                tofile(lines)

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/513864352663863328/947958181596909608/unknown.png")
            await ctx.channel.send(embed=embed)



@bot.command()
async def stats(ctx):
    player=ctx.author

    File=open('Stats.txt','r')
    lines=File.readlines()
    File.close()

    contain=contains(lines,str(player))

    if contain ==False:
        await ctx.channel.send("0 games played")

    else:
        line=contain.split(',')
        embed=discord.Embed(title='%s Wordle stats'%(str(player)[0:-5]),colour=discord.Colour.blue())    
       
        for i in range(1,7):
          embed.add_field(name='%s guess'%(i), value=line(i), inline=True)

        embed.add_field(name='played', value=line[7], inline=True)
        embed.add_field(name='Lost', value=line[8], inline=True)

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/513864352663863328/947958181596909608/unknown.png")
    await ctx.channel.send(embed=embed)
        


@bot.command()
async def leaderboard(ctx):

    Stats=open('Stats.txt','r')
    lines=Stats.readlines()
    Stats.close()

    top=[('none',0),('none',0),('none',0),('none',0),('none',0)]

    for i in lines:
        i=i.split(',')
        tup=(i[0],int(i[6])*1+int(i[5])*2+int(i[5])*2+int(i[4])*4+int(i[3])*8+int(i[2])*16+int(i[1])*32-int(i[8])*5)

        for l in range(5):
            if tup[1]<top[l][1]: 
                pass
            else:
                top.insert(l,tup)
                top.pop(-1)
                break

    embed=discord.Embed(title='Wordle Leaderboard',colour=discord.Colour.blue())
    
    for i in range(1,6):
      embed.add_field(name='%s'%(i), value='%s - %s'%(top[i-1][0][0:-5],str(top[i-1][1])), inline=False)

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/513864352663863328/947958181596909608/unknown.png")
    await ctx.channel.send(embed=embed)


@bot.command()
async def help(ctx):

    embed=discord.Embed(title='Wordle Leaderboard',colour=discord.Colour.blue())

    embed.add_field(name='Leaderboard',value='?wordle: start a game of wordle\n\n?guess [word]: guess a word\n\n?progress: see wordle game progress\n\n?stats: individual wordle stats\n\n?leaderboard: top 5 wordlers',inline=False)

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/513864352663863328/947958181596909608/unknown.png")
    await ctx.channel.send(embed=embed)

bot.run(TOKEN)
