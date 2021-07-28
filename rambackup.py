print("Ram started")
import discord
from random import randint
import datetime
import sys
import asyncio
from lock import lock
import bs4
import urllib.request
import os
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process
from difflib import SequenceMatcher
client = discord.Client()
KEY_CHARACTER = 'ram '

BARASU = 691843825483776100
AVERAGE_PHOTOGRAPHER_SPAM = 680843866349633568
MY_DMS = 692949833316565046
CIVIL_DISCUSSIONS = 679005570652700688
OWO_SPAM = 677672546145140747
KYLE = 331974513636147202


class item():
    def __init__(self,type,content):
        self.type = type
        self.content = content

    async def send(self,place):
        if self.type == "text":
            while len(self.content)>1999:
                await place.send(self.content[:2000])
                self.content = self.content[2000:]
            await place.send(self.content)
        elif self.type == "file":
            await place.send(file=discord.File(self.content))
        elif self.type == "reaction":
            pass


class package():
    def __init__(self,items=[]):
        if isinstance(items,list):
            self.items = items
        else:
            self.items = [items]

    def append(self,newItem):
        self.items.append(newItem)

    async def send(self,place):
        for i in self.items:
            await i.send(place)

class runAtSend():
    def __init__(self,function,*args):
        self.function = function
        self.args = args

    async def send(self,place):
        await self.function(*self.args).send(place)

class response:
    def __init__(self,textIn=0,content = 0,label = "normal"):
        self.inn = textIn
        self.label = label
        if isinstance(content,str):
            self.out = item("text",content)
        else:
            self.out = content

    def textIn(self,text):
        if text[:len(KEY_CHARACTER)].lower() == KEY_CHARACTER.lower():
            text = text[len(KEY_CHARACTER):]
        else:
            return False
        if isinstance(self.inn,list):
            for i in self.inn:
                if i.lower() == text.lower():
                    return True
            return False
        return self.inn.lower() == text.lower()

    def output(self):
        return self.out

    def help(self):
        return "Figure it out" 


class rawResponse(response):
    def textIn(self,text):
        return text.lower() == self.inn.lower() 


class lockedResponse(response):
    def textIn(self,text):
        if text[-5:] == lock():
            return response.textIn(self,text[:-6])
        return False


class randResponse(response):
    def output(self):
        return item("text",self.out[randint(0,len(self.out)-1)])


class argResponse(response): 
    def __init__(self,inn,function,parse = True,*args):
        response.__init__(self,inn)
        self.function = function
        self.parse = parse
        self.error = False
        self.args = args

    def textIn(self,text):
        if text[:len(KEY_CHARACTER)].lower() == KEY_CHARACTER.lower():
            text = text[len(KEY_CHARACTER):]
        else:
            return False
        if not isinstance(self.inn,list):
            self.inn = [self.inn]
        for i in self.inn:
            if i.lower() == text.lower()[:len(i)]:
                try:
                    text = text[len(i)+1:]
                    if self.parse:
                        args = list(self.args)
                        for x in parse(text):
                            args.append(x)
                        self.argsOut = tuple(args)
                    else:
                        self.argsOut = self.args + (text,)
                except Exception as e: 
                    print("no arguements")
                    self.out = item("text","error:\n" + str(e))
                    self.error = True
                return True
        return False

    def output(self):
        if not self.error: 
            self.out = self.function(*self.argsOut)
            del self.argsOut
        return response.output(self) 


class time(response):
    def output(self):
        time = str(datetime.datetime.now())[11:16]
        if time[0]=='0':
            time = time[1:]
        return item("text",time)


class holdup(response):
    def output(self):
        raw_input()
        return item("text","done waiting")

class exit(response):
    def output(self):
        print("exiting")
        sys.exit()


class waiter():
    def __init__(self,time,place,content,repeat = 0):
        self.time = time
        self.place = place
        if isinstance(content,str):
            self.content = item("text",content)
        else:
            self.content = content
        self.repeat = repeat
        self.endtime = self.setEndtime()

    def setEndtime(self):
        return datetime.timedelta(seconds = self.time) + datetime.datetime.now()

    def ready(self):
#        print(str(self.endtime))
#        print(str(datetime.datetime.now()))
#        print(self.endtime<datetime.datetime.now())
        return self.endtime<datetime.datetime.now()

    async def go(self):
        await self.content.send(client.get_channel(self.place))
        self.endtime = self.setEndtime()

    def keep(self):
        if self.repeat==0:
            return False
        if self.repeat>0:
            self.repeat = self.repeat-1
        return True


class dailyPoster(waiter): 
    def __init__(self,time,place,content,repeat = -1):
        waiter.__init__(self,time,place,content,repeat)

    def setEndtime(self):
        today = datetime.date.today() 
        return datetime.datetime.combine(today,self.time) + datetime.timedelta(days=1)


class randDailyPoster(dailyPoster):
    def __init__(self,content,repeat = -1):
        dailyPoster.__init__(self,0,content,repeat)
        
    def setEndtime(self):
        today = datetime.date.today()
        return datetime.datetime.combine(today,datetime.time(hour = randint(0,23), minute = randint(0,59),second = randint(0,59)))+datetime.timedelta(days=1)

class removeResponse(waiter):
    def __init__(self,time,place,label,message):
        waiter.__init__(self,time,place,message)
        self.label = label

    async def go(self):
        await waiter.go(self)
        global responses
        for i in responses:
            if i.label == self.label:
                responses.remove(i)
                break

                   
class addPersist(response):
    def __init__(self,textIn,persist):
        pass

class redditRunAtSend():
    def __init__(self,number,subreddit,section):
        self.number = number
        self.subreddit = subreddit
        self.section = section

    async def send(self,place):
        await redditRetrieve(self.number,self.subreddit,self.section).send(place)

def redditRetrieve(number,subreddit,section='hot'):
    req = urllib.request.Request("https://www.reddit.com/r/{}/{}".format(subreddit,section), headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req,None,5000) as page:
        soup = bs4.BeautifulSoup(page,features="lxml")
    images = soup.find_all('img')
    #print (images)
    i=0
    while i<len(images):
        if str(images[i]).startswith('<img alt="Post image"'):
            for x in range(len(str(images[i]))-5):
                if str(images[i])[x:x+8] == "redd.it/":
                    x+=8
                    image = "https://i.redd.it/"
                    for a in str(images[i])[x:]:
                        if a != '?' and a != '"':
                            image+=a
                        else: break
                    images[i] = image
            i+=1
        else:
            images.pop(i)
    if number>len(images): number=len(images)
    counter = 0
    names = []
    ext = ""
    for i in images[:number]:
        for x in range(len(i)-1,0,-1):
            if i[x] == '.':
                   ext = i[x:]
                   break
        try:
            urllib.request.urlretrieve(i,"./memes/"+str(counter)+ext)
        except:
            print("download error")
        names.append("./memes/"+str(counter)+ext)
        counter+=1
    pack = package()
    pack.items = []
    for i in names:
        pack.items.append(item("file",i))
    return pack


def webwork(problem):
    print("in")
    problem = list(problem)
    banned = ['1','2','3','4','5','6','7','8','9','0','\n','.','/','\\',' ','{','}']
    i=0
    while i<len(problem):
        if problem[i] in banned:
            problem.pop(i)
        else: i+=1
    for i in range(len(problem)):
        try:
            if problem[i] == '(':
                depth = 1
                while depth > 0:
                    problem.pop(i)
                    if problem[i] == '(':
                        depth+=1
                    elif problem[i] == ')':
                        depth-=1
                problem.pop(i)
        except: break
    problem = stringify(problem)
    print("here at 1")
    contents = []
    index = []
    for subdirs,dirs,files in os.walk("./webwork/webwork-open-problem-library/Contrib/LaTech"):
        for f in files:
            if f.endswith(".pg"):
                path = os.path.join(subdirs,f)
                with open(path,'r') as c:
                    string = c.read()
                start = 0
                end = 0
                for i in range(10,len(string)):
                    if string[i-10:i] == "BEGIN_TEXT":
                        start = i
                    elif string[i:i+8] == "END_TEXT":
                        end = i
                        break
                string = string[start:end]
                string = list(string)
                for i in range(len(string)):
                    try:
                        if string[i] == '$':
                            while (string[i] != ' ') and (string[i] != '\n'):
                                string.pop(i)
                        if string[i] == '(':
                            depth = 1
                            while depth > 0:
                                string.pop(i)
                                if string[i] == '(':
                                    depth+=1
                                elif string[i] == ')':
                                    depth-=1
                            string.pop(i)
                        if string[i] == '{':
                            while string[i] != '}':
                                string.pop(i)
                            string.pop(i)
                    except: break
                i=0
                while i<len(string):
                    if string[i] in banned:
                        string.pop(i)
                    else: i+=1
                string = stringify(string)
                contents.append(string)
                index.append(path)
    if contents == []:
        print("github files missing")
        return item("text","github files missing")
    best = 0
    bestScore = 0
    bestString = ""
    print(contents)
    for i in range(len(contents)):
        matcher = SequenceMatcher(None,problem,contents[i])
        match = matcher.find_longest_match(0,len(problem),0,len(contents[i]))
        longestSubstring = problem[match.a:match.a+match.size]
        score = match.size
        print("{}:  {}  {}".format(index[i],longestSubstring,score))
#        score = fuzz.ratio(problem,contents[i])
        if score > bestScore:
            best = index[i]
            bestScore = score
            bestString = contents[i]
            bestSubstring = longestSubstring
    print("problem:\n"+problem)
    print("best:\n{}   {}".format(best,score))
    print("here")
    with open(best,'r') as f:
        lines = parse(f.read(),'\n')
    problem = ""
    equations = []
    answers = []
    for i in range(len(lines)):
        if lines[i] == "BEGIN_TEXT":
            while lines[i] != "END_TEXT":
                problem+='\n'+lines[i]
                i+=1
        elif len(lines[i])>0 and lines[i][0] == '$':
            for x in range(len(lines[i])-1):
                if lines[i][x] == ' ':
                    if lines[i][x+1] == '=':
                        equations.append(lines[i])
                    break
        elif len(lines[i])>4 and lines[i][:3] == "ANS":
            answers.append(lines[i])
    print("there")
    out = problem+'\n\n'
    for i in equations: out+= i+'\n'
    for i in answers: out+= i+'\n'
#    out = item("text",process.extractOne(problem,contents)[0])
    print("problem:\n{}\n\nbest:\n{}\nmatch: {}".format(problem,bestString,bestSubstring))
    return item("text",best + '\n\n' + out)


def stringify(a):
    out = ""
    for i in a:
        out+=str(i)
    return out

def parse(string=None,key=' '):
    out = []
    index = 0
    out.append("")
    for i in string:
        if i==key:
            index+=1
            out.append("")
        else:
            out[index]+=i
    return out

def echo(*args):
    out = package([])
    for i in args:
        out.append(item("text",i))
    return out

def scramble():
    pass

def runAtSendTest():
    return item("text","test run")

responses = [
#    exit("exit"),
    randResponse(["hello","hi"], ["Hello Barasu", "Hello", "hey"]),
    response("Ping", "Pong"),
    rawResponse("Marco", "Polo"),
    time(["time","what time is it?","what time is it"]),
    rawResponse("b.rem","Who's Rem?"),
    holdup("holdup"),
    randResponse("flip a coin",["Heads","Tails"]),
    randResponse(["snap?","snap"],["Death","Mercy"]),
    response("send yourself",item("file","./ram.py")),
    response("send bootstrapper",item("file","./bootstrapper.py")),
    response("send starter",item("file","./starter.py")),
    response("send backup",item("file","./rambackup.py")),
#    response("send test meme",runAtSend(redditRetrieve,2,"animemes","top")),
    response("help","Look I don't really know what's going on either"),
    response("send lock","nice try barasu"),
    response("runatsend test",runAtSend(runAtSendTest)),
    lockedResponse("hushhush",";)"),
    lockedResponse("berserk",package([
        runAtSend(redditRetrieve,4,"nukedmemes"),
        runAtSend(redditRetrieve,4,"cursedimages"),
        runAtSend(redditRetrieve,4,"animemes")
    ])),
    argResponse("echo",echo,False),
    argResponse("parse",echo),
    argResponse("meme",redditRetrieve,True,1),
    response("30 seconds?","not yet","30seconds"),
    argResponse("webwork",webwork,False)
]


waiters = [
    dailyPoster(datetime.time(hour = 18),BARASU,runAtSend(redditRetrieve,4,"animemes","top")),
    randDailyPoster(OWO_SPAM,item("text","owo daily")),
#    waiter(15,AVERAGE_PHOTOGRAPHER_SPAM,runAtSend(redditRetrieve,2,"dankmemes","new"),4)
#    waiter(10,BARASU,"Heartbeat",-1)
    removeResponse(30,AVERAGE_PHOTOGRAPHER_SPAM,"30seconds","30 seconds have passed")
    ]
if waiters[0].endtime+datetime.timedelta(days = -1)>datetime.datetime.now():
    waiters[0].endtime = waiters[0].endtime + datetime.timedelta(days = -1)




persistent = []
@client.event
async def on_ready():
    print('Logged in as {}   {}'.format(client.user,str(datetime.datetime.now())))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == ".update "+lock():
        print("updating")
        await message.channel.send("saving file (live)")
        await message.attachments[0].save("ram.py")
    if message.author.id == KYLE:
        if randint(0,2) == 1:
            await message.channel.send("fuck you Kyle")
    try:
        if message.content == ".exit "+lock():
            await message.channel.send("bye...")
            await client.logout()
        for i in responses:
            if i.textIn(message.content):
                await i.output().send(message.channel)
    except Exception as e:
        print("error in on_message:")
        print(e)
        await message.channel.send("error in on_message: {}".format(e))





async def iterator():
    global waiters
    now = datetime.datetime.now()
    while True:
#        print("looping")
        await asyncio.sleep(1)
        for i in waiters:
            if i.ready():
                print("go")
                await i.go()
                if not i.keep():
                    waiters.remove(i)



mainLoop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(iterator())
    with open('key.txt','r') as key:
        client.run(key.read())
except Exception as e:
    print("mainLoop error:")
    print(e)
finally:
    print("closing loop")
    mainLoop.close()

