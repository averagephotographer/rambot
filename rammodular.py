print("Ram started")
from botbasics import *
import datetime
import discord
import asyncio
from games import *
import sys
from lock2 import lock
import bs4
import urllib.request
import os
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process
from difflib import SequenceMatcher
import math
from interp import interp
client = discord.Client()
KEY_CHARACTER = 'ram '
POST_IMAGES = False

BARASU = 691843825483776100
AVERAGE_PHOTOGRAPHER_SPAM = 680843866349633568
CIVIL_DISCUSSIONS = 679005570652700688
SCREAM_CHAMBER_BOT_SPAM = 677672546145140747
AARON = 352232928224215041
KYLE = 331974513636147202

DAY = 86400



class time(response):
    def output(self):
        time = str(datetime.datetime.now())[11:16]
        if time[0]=='0':
            time = time[1:]
        return item("text",time)


class exit(response):
    def output(self):
        print("exiting")
        sys.exit()

class Format:
    def __init__(self):
        self.alphabet = list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_")
        self.math = list("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_ +-()*/.")
        self.numbers = ['1','2','3','4','5','6','7','8','9','0','.']


    def ticTacToe(self,text):
        if len(text)!=2 or not text[0] in list("abcABC") or not text[1] in ['1','2','3']:
            return False
        return True

    def connectFour(self,text):
        if len(text) == 1 and  text in list("1234567"):
            return True
        return False

    def equations(self,text):
        print(text)
        if text == None:
            return False
        text = parse(text,'\n')
        for i in text:
            if not self.matcher(i,[self.alphabet+self.numbers,[' '],['='],self.math]):
                return False
        return True

    def matcher(self,t,order):
        print(t)
        i=0
        last = self.math
        index = 0
        while index<len(order)-1 and i < len(t):
            print("t[i]: {}  i: {}  len(t): {}".format(t[i],i,len(t)))
            if t[i] in order[index]:
                i+=1
            elif t[i] in order[index+1]:
                i+=1
                index+=1
            else:
                return False
        print("{} {} {} {}".format(i,len(t),index,len(order)-1))
        if i == len(t) or index < len(order)-1:
            return False
        print("in last section")
        print("{}   {}".format(i,len(t)))
        while i < len(t):
            print("here")
            if t[i] in order[index]:
                i+=1
            else:
                return False
        return True

def redditRetrieve(number,subreddit,section='hot'):
    print("in")
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
    print(POST_IMAGES)
    if not POST_IMAGES:
        print("in not post_images")
        pack = package()
        for i in images[:number]:
            pack.append(item("text",i))
            print(pack)
        return pack
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
    for i in names:
        pack.items.append(item("file",i))
    return pack



def webwork(message,problem):
    print("in")
    problem = list(problem)
    banned = ['1','2','3','4','5','6','7','8','9','0','\n','.','/','\\',' ','{','}','∘','*','+','-']
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
    problem = "".join(problem)
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
                string = "".join(string)
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
                        new = ""
                        for a in lines[i]:
                            if a!='$': new+=a
                        equations.append(new)
                    break
        elif len(lines[i])>4 and lines[i][:3] == "ANS":
            answers.append(lines[i])
    print("there")
    out = problem+'\n\n'
    for i in range(len(equations)):
        equations[i] = list(equations[i])
        x = 0
        while x < len(equations[i]):
            if equations[i][x] == '$':
                equations[i].pop(x)
            else: x+=1
        equations[i] = "".join(equations[i])
        equations[i] = equations[i][:-1]
        out+= equations[i]+'\n'
    for i in answers: out+= i+'\n'
#    out = item("text",process.extractOne(problem,contents)[0])
    print("problem:\n{}\n\nbest:\n{}\nmatch: {}".format(problem,bestString,bestSubstring))
    ans = webworkSolve(message,equations,answers)
    return package(item("text",best + '\n\n' + out + '\n\n'),ans)


def webworkSolve(message,equations,answers,new=None):
    def given(text):
        for x in range(len(text)-7):
            if text[x:x+7] == "random(" or text[x:x+8] == "random (":
                return True
        for x in range(len(text)-11):
            if text[x:x+11] == "interpVals(":
                return True
        return False
    if new != None:
        new = parse(new,'\n')
        for i in equations:
            new.append(i)
        equations = new
    try: 
        out = ""
        v = ""
        def sqrt(x):
            return x**(1/2)
        variableDict = {'v':v,'sqrt':sqrt,'ln':math.log}
        index = 0
        variables = []        
        for i in equations:
            if not given(i):
                v = ""
                variables.append(0)
                for x in i:
                    if x == ' ':
                        break
                    v+=x
                variableDict[v] = variables[index]
                print("executing: "+i)
                exec(i,variableDict)
                index+=1
                print(v+" = "+str(variableDict[v]))
        print("through exec")
        for i in answers:
            for x in range(len(i)):
                if i[x] == '$':
                    x+=1
                    var = ""
                    while i[x] != ')':
                        var+=i[x]
                        x+=1
                    out += str(variableDict[var])+ '\n'
                    break
        remove("webwork"+str(message.channel.id)+str(message.author.id))
        return item("text","answer(s):\n"+out)

    except Exception as e:
        print("except")
        label = "webwork"+str(message.channel.id)+str(message.author.id)
        global responses
        r = findResponse(label)
        if r != None:
            responses.remove(r)
        responses.append(response(None,None,equations,answers,function = webworkSolve,takeArgs = True,parse = False,user = message.author.id,channel = message.channel.id,usePrefix = False,passMessage = True,label = label,format = F.equations))
        global waiters
        w = findWaiter(label)
        if w == None:
            waiters.append(removeResponse(3600,message.channel.id,label,item("text","webwork problem expired"),label = label))
        else:
            w.reset()
        out = str(e)+"\nfind:\n"
        for i in equations:
            if given(i):
                out+=i+'\n'
        return item("text",out)

def echo(*args):
    out = package()
    for i in args:
        out.append(item("text",i))
    return out



def cancel(message):
    user = message.author.id
    actions = 0
    global responses
    global waiters
    for i in responses:
        if i.label != "normal" and i.user == user:
            w = findWaiter(i.label)
            if w != None:
                waiters.remove(w)
            responses.remove(i)
            actions+=1
    return item("text","{} actions canceled".format(actions))

def scramble():
    pass

def runAtSendTest():
    return item("text","test run")

def findResponse(label):
    for i in responses:
        if i.label == label:
            return i
    return None

def findWaiter(label):
    for i in waiters:
        if i.label == label:
            return i
    return None

def interpolate(*args):
    try:
        out = item("text",interp(*args))
    except Exception as e:

        out = item("text",str(e)+"\nenter A-low A-Hi A-target B-low B-hi")
    return out

def bakaMemes():
    global waiters
    waiters[0].endtime = waiters[0].endtime + datetime.timedelta(days = -1)


F = Format()
responses = [
#    exit("exit"),
    response(["cancel","stop"],passMessage = True,function = cancel),
    response(["hello","hi"], ["Hello Barasu", "Hello", "hey"]),
    response(["hello ram","hi ram","ram hello","ram hi"],["Hello Barasu", "Hello", "hey"],usePrefix = False),
    response("Ping", "Pong"),
    response("Marco", "Polo",usePrefix = False),
#    time(["time","what time is it?","what time is it"]),
    response("b.rem","Who's Rem?",usePrefix = False),
    response("flip a coin",["Heads","Tails"]),
    response(["snap?","snap"],["Death","Mercy"]),
    response("send yourself",item("file","./ram.py")),
    response("send bootstrapper",item("file","./bootstrapper.py")),
    response("send starter",item("file","./starter.py")),
    response("send backup",item("file","./rambackup.py")),
    response("send test meme",runAtSend(redditRetrieve,2,"goodanimemes","top")),
    response("help","Look I don't really know what's going on either"),
    response("send lock","nice try barasu"),
    response("runatsend test",runAtSend(runAtSendTest)),
    response("hushhush",";)",locked = True),
    response(None,["Fuck you Kyle",None,None],user = KYLE,usePrefix = False),
    response("berserk",package(
        runAtSend(redditRetrieve,4,"nukedmemes"),
        runAtSend(redditRetrieve,4,"cursedimages"),
        runAtSend(redditRetrieve,4,"goodanimemes")
    ),locked = True),
    response("echo",None,takeArgs = True,function = echo,parse = False),
    response("parse",None,takeArgs = True,function = echo),
    response("meme",None,1,function = redditRetrieve,takeArgs = True),
    response("Function test",None,"hello World",function = echo),
#    response("30 seconds?","not yet",label = "30seconds"),
    response("webwork",function = webwork,takeArgs = True,parse = False,passMessage = True),
    response("tictactoe","here",ticBoard,F.ticTacToe,function = gameInit,passMessage = True),
    response(["connect four beta","fonnect cour beta"],"here",connectFourBoard,F.connectFour,function = gameInit,passMessage = True),
    response(["interpolate","interp"],None,function = interpolate,takeArgs = True),
    response("bakamemes","OK",function = bakaMemes,locked = True)
]


waiters = [
    dailyPoster(datetime.time(hour = 19),BARASU,package(
        runAtSend(redditRetrieve,5,"goodanimemes","top"),runAtSend(redditRetrieve,5,"animemes","top"))),
    randDailyPoster(SCREAM_CHAMBER_BOT_SPAM,item("text","owo daily")),
    randDailyPoster(SCREAM_CHAMBER_BOT_SPAM,item("text","m.e")),
#    waiter(15,AVERAGE_PHOTOGRAPHER_SPAM,runAtSend(redditRetrieve,2,"dankmemes","new"),4)
    waiter(10,AVERAGE_PHOTOGRAPHER_SPAM,item("text","Heartbeat"),10)
#    removeResponse(30,AVERAGE_PHOTOGRAPHER_SPAM,"30seconds","30 seconds have passed")
    ]
#if waiters[0].endtime+datetime.timedelta(days = -1)>datetime.datetime.now():
#    waiters[0].endtime = waiters[0].endtime + datetime.timedelta(days = -1)






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
    try:
        if message.content == ".exit "+lock():
            await message.channel.send("bye...")
            await client.logout()
        for i in responses:
            if i.messageIn(message):
                output = i.output()
                if output != None:
                    await output.send(message.channel)
    except Exception as e:
        print("error in on_message:")
        print(e)
        await message.channel.send("error in on_message: {}".format(e))






mainLoop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(iterator(client))
    print("here")
    with open('key.txt','r') as key:
#        print(key.read())
        client.run(key.read())
except Exception as e:
    print("mainLoop error:")
    print(e)
finally:
    print("closing loop")
    mainLoop.close()

