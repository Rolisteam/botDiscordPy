from discord.ext.commands import Bot
from subprocess import run,Popen, PIPE
import logging
from threading import Timer,Thread,Event
from cogs import api
from threading import Thread
class DiceBot(Thread):
    def __init__(self, id, shardCount, alias, macro, prefix):
        super(DiceBot, self).__init__()
        self.id = id
        self.shardCount = shardCount
        self.alias = alias
        self.macro = macro
        self.prefix= prefix

        self.bot = Bot(shard_id=self.id,shard_count=self.shardCount,command_prefix='')
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(filename='/opt/document/log/discord.log', encoding='utf-8', mode='a')
        self.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)
        self.bot.add_listener(self.on_ready)
        self.bot.add_listener(self.on_read)
        self.bot.add_listener(self.on_message)


    def run(self):
        # debug
        self.bot.run("MzkxMzAxNDU2MjMxMTM3Mjky.DRWrew.1LjVb2w702Mtu9fURpU64yGlTyM")
        # production
        # self.bot.run("Mjc5NzIyMzY5MjYwNDUzODg4.DzBGCA.QjJAGewTZr7eVovN18Gxvu2QnAM")


    ## Callback
    async def on_ready():
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')
        print('id: {} count: {}'.format(self.id,self.shardCount))
        await self.bot.change_presence(game=discord.Game(name = '!support !help !vote'))
        api.setup(self.bot, self.id, self.shardCount)
        logger.info("#### Server count (shard "+str(self.id)+"): "+str(len(list(self.bot.servers))))
        #t.start()

    async def on_read():
        print("Client logged in")

    async def on_message(message):
        idServer=""
        if(message.server is not None):
            idServer = str(message.server.id)
            prefix = self.getPrefix(idServer)
            textmsg = message.content
            if textmsg.startswith(prefix) and message.author != self.bot.user:
                textmsg= textmsg[len(prefix):].strip()
                if textmsg.startswith('play') or textmsg.startswith('skip') or textmsg.startswith('stop'):
                    return
                if textmsg.startswith('alias'):
                    self.logger.info("alias")
                    await self.manageAlias(message,textmsg)
                if textmsg.startswith('macro'):
                    self.logger.info("macro")
                    await self.manageMacro(message,textmsg,self.bot)
                if textmsg.startswith('support'):
                    self.logger.info("Support asked")
                    await self.manageSupport(message, self.bot)
                if textmsg.startswith('vote'):
                    self.logger.info("vote asked")
                    await self.manageVote(message, self.bot)
                if textmsg.startswith('prefix'):
                    self.logger.info("Confix prefix")
                    await self.managePrefix(idServer,textmsg,message,self.bot)
                else:
                    command = textmsg
                    normalCmd=True
                    if(len(idServer) >0 and idServer in self.alias):
                        val = self.alias[idServer]
                        if(command in val):
                            cmds=val[command]
                            for line in cmds:
                                if(line.startswith('!')):
                                    line = line[1:]
                                self.logger.info("Saved Command: "+line)
                                normalCmd=False
                                await self.rollDice(line,message,my_bot)
                    if(normalCmd):
                        await self.rollDice(command,message,my_bot)


    def getPrefix(serverId):
        if(serverId in PrefixByServer):
            return PrefixByServer[serverId]
        return "!"

    async def managePrefix(idserver, textmsg, message, bot ):
        # !prefix set roll
        try:
            array=textmsg.split(' ')
            print(array)
            if(len(array)==3):
                if(array[0] == "prefix"):
                    if(array[1] == "set"):
                        self.prefix[idserver]=array[2]


            with open(prefixFile, 'w') as outfile:
                json.dump(PrefixByServer,outfile,indent=4)
            await self.bot.send_message(message.channel, "[Prefix]New prefix definition is done!")
        except:
            await self.bot.send_message(message.channel, "[Prefix]Something goes wrong")


    async def manageAdsMessage(message):
        if (message.channel.id in channels):
            channels[message.channel.id] += 1
            if(channels[message.channel.id] == 1000):
                index = random.randint(0,len(messages)-1)
                ads = messages[index]
                self.logger.info("Ads:"+ads+" channel:"+message.channel.name)
                await self.bot.send_message(message.channel, ads)
                channels[message.channel.id] = 0
        else :
            channels[message.channel.id] = 0

    async def sendImageMessage(bot,message,data):
        decodedData=base64.b64decode(data,validate=True)
        f = io.BytesIO(decodedData)
        self.logger.info("data: "+data)
        await self.bot.send_file(message.channel, f, filename="result.png",content="")


    async def manageMacro(message,textmsg,bot):
        idServer=str(message.server.id)
        macroPattern=""
        macroCmd=""
        filename = "{}macro_{}.json".format(macroFileName,idServer)
        macros = []
        if os.path.isfile(filename):
            with open(filename) as f:
                macros = json.load(f)
        macroRegExp=False
        addMacro=False
        removeMacro=False
        showlistMacro = False
        idToRemove=-1


        tab=textmsg.split(' ')
        if(not addMacro and not removeMacro):
           if(tab[0] == "macro"):
               if(tab[1] == "rm"):
                   removeMacro=True
                   idToRemove=tab[2]
               elif(tab[1] == "list"):
                   showlistMacro=True
               else:
                   addMacro=True
                   size=len(tab)
                   macroName=tab[1]

                   try:
                       macroRegExp=False
                       if(int(tab[size-1])==1):
                           macroRegExp=True
                           size-=1
                       elif(int(tab[size-1])==0):
                           size-=1
                   except IndexError:
                        macroRegExp=False


                   try:
                       macroCmd=""
                       for i in range(2, size):
                           macroCmd += " "+tab[i]
                           print("macro:"+macroCmd)
                       macroCmd=macroCmd.strip()
                   except IndexError:
                       addMacro=False
                       await bot.send_message(message.channel, "Error in your add Macro Command: no command")


        if(addMacro):
            macro = {}
            macro["pattern"]=macroName
            macro["cmd"]=macroCmd
            macro["regexp"]=macroRegExp
            macro["comment"]=""
            macros.append(macro)

        if(showlistMacro):
            lines="```"
            id = 0
            for i in macros:
                lines+="id: {} Pattern: {} Command: {} Regexp: {}\n\n".format(id,i["pattern"],i["cmd"],i["regexp"])
                id+=1
            lines+="```"
            if(id>0):
                await bot.send_message(message.channel, lines)
            else:
                await bot.send_message(message.channel, "No recorded macro for this server")


        if(removeMacro):
            try:
                del macros[int(idToRemove)]
            except IndexError:
                await bot.send_message(message.channel, "Error in your remove Macro Command")


        if(removeMacro or addMacro):
            with open(filename, 'w') as outfile:
                json.dump(macros,outfile,indent=4)
                AllMacro[idServer]="macro_{}.json".format(idServer)


    async def manageAlias(message,textmsg):
        idServer=str(message.server.id)
        aliases={}
        commands=[]
        aliasName=""
        addAlias=False
        showlistAlias=False
        removeAlias=False
        firstLine=True
        for line in textmsg.splitlines():
            tab=line.split(' ')
            if(not addAlias and not removeAlias and firstLine):
                if(tab[0] == "alias"):
                    if(tab[1] == "rm"):
                        removeAlias=True
                        try:
                            aliasName=tab[2]
                        except IndexError:
                            print("error index in alias")
                    elif(tab[1] == "list"):
                        showlistAlias=True
                    else:
                        addAlias=True
                        aliasName=tab[1]
            if(addAlias):
                if(firstLine):
                    cmd=""
                    for i in range(2,len(tab)):
                        if(i!=tab[0]):
                            cmd+=str(tab[i])+" "
                    if(len(cmd)>0):
                        commands.append(cmd)
                else:
                    commands.append(line)
            firstLine=False

        if(showlistAlias):
            lines="```"
            id = 0
            val = AllAliases[idServer]
            for i in val:
                lines+="id: {} Pattern: {}\nCommand:\n{}\n\n".format(id,i,"\n".join(val[i]))
                id+=1
            lines+="```"
            if(id>0):
                await bot.send_message(message.channel, lines)
            else:
                await bot.send_message(message.channel, "No recorded macro for this server")
            return

        if( idServer not in AllAliases):
            AllAliases.update({str(idServer):{}})

        val = AllAliases[idServer]
        if(addAlias):
            val.update({str(aliasName):commands})
        elif(removeAlias):
            del val[aliasName]

        with open(filename, 'w') as outfile:
            json.dump(AllAliases,outfile,indent=4)


    async def rollDice(command,message,bot):
        idServer=str(message.server.id)
        logger = logging.getLogger('discord')
        kill = lambda process: process.kill()
        cmd = ['dice','-b',command]
        if idServer in AllMacro:
            cmd.append('-a');
            cmd.append("{}{}".format(macroFileName,AllMacro[idServer]));
        roll = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        my_timer = Timer(5, roll.kill)
        try:
            my_timer.start()
            stdout, stderr = roll.communicate()
            print(stdout)
            print(stderr)
            rc = roll.returncode
            if (rc == 0):
                logger.info("cmd: "+str(command))
                if(stdout.endswith("```")):
                    await bot.send_message(message.channel, stdout)
                else:
                    await sendImageMessage(bot,message,stdout)
                await manageAdsMessage(message)
            elif(rc != 1):
                logger.info("command FAIL: "+str(command)+" returncode:"+str(rc))
        except OSError as inst:
            logger.info(type(inst))    # the exception instance
            logger.info(inst)          # __str__ allows args to be printed directly,
            logger.info("OSError error: "+str(sys.exc_info()[0])+" cmd:"+str(command))
            #await my_bot.send_message(message.channel, "Error: your command took too much time")
        except:
            msgError = sys.exc_info()
            logger.info("Unexpected error:"+str(msgError[0])+""+str(msgError[1])+""+str(msgError[2])+" cmd:"+str(command))
        finally:
            my_timer.cancel()

    async def manageSupport(message, bot):
        await bot.send_message(message.channel, "You want to help ? go to: https://liberapay.com/obiwankennedy/donate and support my developer")

    async def manageVote(message, bot):
        await bot.send_message(message.channel, "Vote for Diceparser! go to: https://discordbots.org/bot/279722369260453888/vote")
