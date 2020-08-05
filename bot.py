#imports################################################################################################################################################
import time
#starts timer for connection time
t = time.process_time()

import json
import discord
#variables bruv you blind?##############################################################################################################################
#global author
author = ""
#global waiting_for_registration
waiting_for_registration = False
#global registration_code
registration_code = 0
#global region
region = ""
#global username
username = ""

data = {}
#FUNCTIONS##############################################################################################################################################

#unix convert to seconds
def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    if hour == 0:
        return "%02d:%02d" % (minutes, seconds)
    else:
        return "%d:%02d:%02d" % (hour, minutes, seconds)

#adding to dictionary
def append(userid, region, username, name):
    data[userid] = []
    data[userid].append({
        'region': region,
        'username': username,
        'name': name
})

#MAIN###################################################################################################################################################

#establishes client
client = discord.Client()


#use client.event for async events as they come in
@client.event
async def on_ready():
    elapsed_time = time.process_time() - t
    print("Bot initialised")
    print("Connection took",elapsed_time,"seconds")
    print("##########################")
    
#messageevent ,could have used a client.command thing but cba and also just scanning messages is easier to do instead of detecting commands plus i dont have to use the command key dont @ me
@client.event
async def on_message(message):
#####ignore messages from the bot
    if message.author == client.user:     
        return

#####hello
    if message.content.startswith('hello'):     
        await message.channel.send('Hi there!')


#####funny poo poo stinky haha
    if message.content == 'poo':
        await message.channel.send('Rude...')
        print(message.guild)
        
        
#####list online users
    if message.content == "!list":    #list command

        x = message.guild.members
        for member in x:   #iterates through server members
            #print(member.name)   #troubleshooting ;)
            #print(type(member.activity))
            #print(member.activity)
            if type(member.activity) == discord.activity.Activity and member.activity.name == "League of Legends":   #for some reason it's not activity.Game and i got stuck on this for ages
                if member.activity.details == None and member.activity.state == None: #if you're streaming league sometimes it says you're playing it but things like mode are set to None
                    await message.channel.send("%s is currently not in a lobby or game" % member) 
                    
                if member.activity.state == "In Game": #displays the character being played if you're in a game (character name is only shown in the image when you click on profile weirdly
                    gametime = convert((time.time() - ((member.activity.timestamps["start"])/1000)))
                    await message.channel.send("%s is playing %s (%s %s) as %s" % (member, member.activity.details, member.activity.state, gametime, member.activity.large_image_text))

                else:
                    if member.activity.details == None:    #for some reason practice tool doesn't have its own details section, but everything else does
                        member.activity.details = "Practice Tool"
                    await message.channel.send("%s is playing %s (%s)" % (member, member.activity.details, member.activity.state)) #Member is playing Mode (in game or in lobby)



#####registration
    if message.content == "!register": #register for op.gg    #move to command maybe? #nah lol

        global author
        author = message.author.id
        global waiting_for_registration
        waiting_for_registration = True
        global registration_code
        registration_code = 0
        #await message.channel.send("Please check DMs for registration")
        await message.channel.send("Please type your league username: ")
        return


#####stats
    if message.content.startswith("!stats"):
        file = open('usernames.txt', 'r')
        filedata = json.load(file)
        #await message.channel.send("command receieved")
        if message.content == "!stats":                 #no mentioned users
            if str(message.author.id) in filedata:
                #await message.channel.send("id in json")
                url = ("https://%s.op.gg/summoner/userName=%s" % (filedata[str(message.author.id)][0]['region'], filedata[str(message.author.id)][0]['username']))
                await message.channel.send(url)
            else:
                await message.channel.send("User not found. Please use !register")
                
        if len(message.mentions) != 0:
            #print((message.mentions[0]).id)

            if len(message.mentions) == 1:
                if str((message.mentions[0]).id) in filedata:
                    url = ("https://%s.op.gg/summoner/userName=%s" % (filedata[str((message.mentions[0]).id)][0]['region'], filedata[str((message.mentions[0]).id)][0]['username']))
                    await message.channel.send(url)
                else:
                    await message.channel.send("No information found for this user, please ask them to register using !register")


                        
            else:
                await message.channel.send("Please only mention one user")
                return
            
        else:
            return

#####wol
    if message.content.startswith("!wol"):
        file = open('usernames.txt', 'r')
        filedata = json.load(file)
        
        if len(message.mentions) == 0:
            await message.channel.send("No mentioned user")
            return

        if len(message.mentions) == 1:
            if str((message.mentions[0]).id) in filedata:
                url = "https://wol.gg/stats/%s/%s/" % (filedata[str((message.mentions[0]).id)][0]['region'], filedata[str((message.mentions[0]).id)][0]['username'])
                await message.channel.send(url)
                return
            else:
                await message.channel.send("No information found for this user,please ask them to register using !register")
                return

        else:
            await message.channel.send("Please only mention one user")
            return
        


#####about
    if message.content == "!about":
        await message.channel.send('''who's playing league bot by Wimble#8807
------------------------------------------------
created 01/08/20 using discord.py

please report any bugs to Wimble#8807''')
                                               

#####help
    if message.content == "!help":
        await message.channel.send('''Commands are:
!list        - lists all users currently in game or in lobby
!register  - register league name and region for op.gg !stats
!stats      - !stats for personal stats, !stats @user for user's stats
!online     - !online @user to see if user is online and what they are playing #WIP#
!wol        - !wol @user to see how much time user has wasted on league
!about      - bot information
!help       - you're looking at it :) ''')

    
    
#####json file stuff
    #this could go HORRIBLY wrong
    #^ 20 mins after this message i have come to terms with the fact i am about to spit in the face of god (codes for different possibilities is better than a tonne of global ifs right?)
    #^ 5 mins after this message i'm wondering how to handle dms with a user id EVERY TIME (does responding to a user work with message.channel.send() ?)
    #^ 5 mins after this message, it looks like it does... BUT WE SHALL SEE
        
    if waiting_for_registration == True and author == message.author.id:
        #global registration_code
        global username
        global region
        file = open('usernames.txt', 'r+')
        filedata = json.load(file)


        if registration_code == 0: #default
            username = message.content
            #await message.channel.send(username)
            registration_code = 1
        if registration_code == 1:
            #else:
            username = message.content
            await message.channel.send("Please enter a region (EUW,EUE,NA,OCE,BR,TR,RU,LAS,LAN,KR)")
            registration_code = 3 #TO REGION
            return
            

                        #prototype 3 option menu
##            if message.author.id in data:
##                await message.channel.send("There is already a username under this account. Would you like to view stored information(1), delete this information(2), or overwrite this information(3)? (Respond to this message with 1, 2 or 3")
##                registration_code = 2 #TO QUERY RESPONSE
##                username = message.content
##                return
##
##
##            #else:
##            username = message.content
##            await message.channel.send("Please enter a region (EUW,EUE,NA,OCE,BR,TR,RU,LAS,LAN,KR)")
##            registration_code = 3 #TO REGION
##            return
##            


        if registration_code == 2: #waiting for response to reg_code 1 query
            #making if statements for 1 2 3 
            if message.content == "1": #view
                await message.channel.send("%s %s" % (data[author][0]["username"], data[author][0]["region"]))
                await message.channel.send("If you wouldlike to select another option, send !register again")
                waiting_for_registration = False
                registration_code = 1 #BACK TO START
                return
                
            if message.content == "2": #delete
                #to do (delete)
                return
            if message.content == "3": #overwrite (looks like it can be done just with json update func, so i'll route to regular region bit)
                registration_code = 3
                await message.channel.send("Please enter a region (EUW,EUE,NA,OCE,BR,TR,RU,LAS,LAN,KR)")
                return
                
                               
        if registration_code == 3: #region
            valid_regions = ("euw","eue","na","oce","br","tr","ru","las","lan","kr")
            region = message.content
            region = region.lower()
            print(region)
            if region not in valid_regions:
                await message.channel.send("Region not valid. Send !register to try again")
                return
            else:
                await message.channel.send("%s %s. Is this correct? (Y or N)" % (username, region))
                registration_code = 4
                return
        if registration_code == 4: #confirmations and adding to json
            if message.content == "y" or message.content == "Y":
                #data = {}
                append(author,region,username,message.author.name)
                #print(filedata["245471571987267584"])
                #print(data)
                if str(author) in filedata:
                    filedata.pop(str(author))
                    #print(filedata)
                filedata.update(data)
                print(filedata)
                #file.seek(0)
                file = open('usernames.txt', 'w')
                json.dump(filedata, file)
                waiting_for_registration = False
                registration_code = 0
            else:
                await message.channel.send("Registration cancelled. Send !register to try again")
                waiting_for_registration = False
                registration_code = 0
                return

client.run('NzM4OTE2NTQxMDM4NDYwOTc5.XyS3pw.lEK0_tK75QQjweLz21AiZE4VxsA')


'''''
#####online
    if message.content.startswith("!online"):
        file = open('usernames.txt', 'r')
        filedata = json.load(file)
        if len(message.mentions) == 0:
            await message.channel.send("Please mention a user to see if they are online (e.g. !online @user")
            return
        if len(message.mentions) == 1:
            oluser = message.mentions
            print(oluser)
            if type(oluser.activity) == discord.activity.Activity and (oluser.activity.name) == "League of Legends":
                
                if oluser.activity.details == None and oluser.activity.state == None:
                    await message.channel.send("%s is currently not in a lobby or game" % member) 
                    
                if oluser.activity.state == "In Game": 
                    gametime = convert((time.time() - ((oluser.activity.timestamps["start"])/1000)))
                    await message.channel.send("%s is playing %s (%s %s) as %s" % (oluser, oluser.activity.details, oluser.activity.state, gametime, oluser.activity.large_image_text))

                else:
                    if oluser.activity.details == None:   
                        oluser.ractivity.details = "Practice Tool"
                    await message.channel.send("%s is playing %s (%s)" % (oluser, oluser.activity.details, oluser.activity.state))
            else:
                await message.channel.send("This user is not currently playing league")
            
'''''

#todo
#wol numbers                         
#check if user is online #CBA RN

#registration code key:
#0 default, first time through
#1
#2 waiting for response to reg_code 1 query
#3 region
