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
import math
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

class item():
    def __init__(self,type=None,content=None):
        self.type = type
        self.content = content

    def __str__(self):
        return "{0.type} Item: {0.content}".format(self)

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
        elif self.type == None:
            pass


class package():
    def __init__(self,*args):
        self.items = list(args)

    def __str__(self):
        out = "["
        for i in self.items:
            out+=str(i) + ' , '
        out = out[:-3]+']'
        return out

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
    def __init__(self,textIn=None,content = None,*args,**kwargs):
        if textIn == None: textIn = ""
        self.label = "normal"
        self.inn = textIn
        self.args = args
        self.usePrefix = True
        self.user = None
        self.channel = None
        self.function = None
        self.locked = False
        self.parse = True
        self.argsOut = args
        self.takeArgs = False
        self.error = False
        self.passMessage = False
        self.format = None
        for name,value in kwargs.items():
            if name == "label":
                self.label = value
            elif name == "usePrefix":
                self.usePrefix = value
            elif name == "user":
                self.user = value
            elif name == "channel":
                self.channel = value
            elif name == "function":
                self.function = value
            elif name == "locked":
                self.locked = value
            elif name == "takeArgs":
                self.takeArgs = value
            elif name == "parse":
                self.parse = value
            elif name == "passMessage":
                self.passMessage = value
            elif name == "format":
                self.format = value
            else: print("bad kwarg")
        if isinstance(content,str):
            self.out = item("text",content)
        elif isinstance(content,list):
            for i in range(len(content)):
                if isinstance(content[i],str):
                    content[i] = item("text",content[i])
            self.out = content
        else:
            self.out = content

    def messageIn(self,message):
        text = message.content
        if self.usePrefix:
            if text[:len(KEY_CHARACTER)].lower() == KEY_CHARACTER.lower():
                text = text[len(KEY_CHARACTER):]
            else:
                return False
        if self.user != None and message.author.id != self.user: return False
        if self.channel != None and message.channel.id != self.channel: return False
        if self.locked:
            if text[-5:] == lock():
                text = text[:-6]
            else: 
                return False
        if self.passMessage:
            args = (message,) + self.args
        else:
            args = self.args
        if self.takeArgs:
            if not isinstance(self.inn,list):
                self.inn = [self.inn]
            for i in self.inn:
                if i.lower() == text.lower()[:len(i)]:
                    try:
                        if i == "":
                            text = text[len(i):]
                        else:
                            text = text[len(i)+1:]
                        if self.format != None and not self.format(text): return False
                        if self.parse:
                            args = list(args)
                            for x in parse(text):
                                args.append(x)
                            self.argsOut = tuple(args)
                        else:
                            self.argsOut = args + (text,)
                    except Exception as e:
                        print(e)
                        self.out = item("text","error in response.messageIn:" + str(e))
                        self.error = True 
                    return True
            return False
        else:
            self.argsOut = args
            if self.inn == None: return True
            if isinstance(self.inn,list):
                for i in self.inn:
                    if i.lower() == text.lower()[:len(i)]:
                        return True
                return False
            return self.inn.lower() == text.lower()[:len(self.inn)]

    def output(self):
        if isinstance(self.out,list):
            return self.out[randint(0,len(self.out)-1)]
        elif self.function != None and self.error == False:
            return self.function(*self.argsOut)
        return self.out

    def help(self):
        return "Figure it out" 


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
    def __init__(self,time,place,content,repeat = 0,**kwargs):
        self.label = "normal"
        self.time = time
        self.place = place
        if isinstance(content,str):
            self.content = item("text",content)
        else:
            self.content = content
        self.repeat = repeat
        self.endtime = self.setEndtime()
        for name,value in kwargs.items():
            if name == "label":
                self.label = value
            else:
                print("bad kwarg in waiter")

    def setEndtime(self):
        return datetime.timedelta(seconds = self.time) + datetime.datetime.now()

    def reset(self):
        self.endtime = self.setEndtime()

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
    def __init__(self,time,place,content,repeat = -1,**kwargs):
        waiter.__init__(self,time,place,content,repeat,**kwargs)

    def setEndtime(self):
        today = datetime.date.today()
        return datetime.datetime.combine(today,self.time) + datetime.timedelta(days=1)


class randDailyPoster(dailyPoster):
    def __init__(self,content,repeat = -1,**kwargs):
        dailyPoster.__init__(self,0,content,repeat,**kwargs)
        
    def setEndtime(self):
        today = datetime.date.today()
        return datetime.datetime.combine(today,datetime.time(hour = randint(0,23), minute = randint(0,59),second = randint(0,59)))+datetime.timedelta(days=1)

class removeResponse(waiter):
    def __init__(self,time,place,target,message=item(None,None),**kwargs):
        waiter.__init__(self,time,place,message,**kwargs)
        self.target = target

    async def go(self):
        await waiter.go(self)
        remove(self.target)


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

def game(message,opponent,board=None,move=None):
    #opponent doubles as the board class for first call
    if board == None:
        if len(message.mentions)!=1:
            return item("text","@ one person to play with")
        
        board = opponent(message.author.id,message.mentions[0].id)
        print("set the board")
        global responses
        label = board.title+str(message.author.id+message.mentions[0].id)+str(message.channel.id)
        responses.append(response("",None,message.author,board,function = game,usePrefix = False,takeArgs = True, parse = False,channel = message.channel.id,user = message.mentions[0].id,passMessage = True,format = F.ticTacToe,label = label))
        global waiters
        print("set response")
        waiters.append(removeResponse(DAY,message.channel.id,label,item("text",board.title+" game between {} and {} has expired".format(message.author.display_name,message.mentions[0].display_name)),label = label))
        print("set waiter")
        return package(board.initalMessage,board.out())
    else:
        move = move.lower()
        label = board.title+str(message.author.id+opponent.id)+str(message.channel.id)
        if board.isLegal(message.author.id,move):
            board.move(message.author.id,move)
            gg = board.gameOver()
            if gg != None:
                remove(label)
                if gg == "stalemate":
                    return package(item("text",opponent.mention+" It's a Stalemate"),board.out())
                elif gg == message.author.id:
                    winner = message.author.mention
                else:
                    winner = opponent.mention
                return package(item("text","Game over, the winner is "+winner),board.out())
            findWaiter(label).reset()
            global responses
            responses.remove(findResponse(label))
            responses.append(response("",None,message.author,board,function = game,usePrefix = False,takeArgs = True, parse = False,channel = message.channel.id,user = opponent.id,passMessage = True,format = F.ticTacToe,label = label))
            return package(item("text",opponent.mention+" your move"),board.out())
        else: 
            findWaiter(label).reset()
            return item("text","that is not a valid move")

class ticBoard:
    def __init__(self,player1,player2):
        print("in ticBoard.__init__()")
        self.key = {'a':0,'b':1,'c':2,'1':0,'2':1,'3':2}
        self.p1 = player1
        self.p2 = player2
        self.board = []
        for i in range(3): self.board.append(['  ','  ','  '])
        self.title = "Tictactoe"
        self.initalMessage = item("text","Welcome to tictactoe beta\nto move type [row][column] eg: a2")
        
    def out(self):
        print("in ticBoard.out()")
        out =  item("text",\
"  1    2    3\n\
a  {} |  {} | {}\n\
------------\n\
b  {} |  {} | {}\n\
------------\n\
c  {} |  {} | {}".format(self.board[0][0],self.board[0][1],self.board[0][2],self.board[1][0],self.board[1][1],self.board[1][2],self.board[2][0],self.board[2][1],self.board[2][2],))
        print("generated output")
        return out

    def isLegal(self,player,move):
        return self.board[self.key[move[0]]][self.key[move[1]]] == '  '

    def move(self,player,move): 
        if player == self.p1:
            self.board[self.key[move[0]]][self.key[move[1]]] = 'O'
        elif player == self.p2:
            self.board[self.key[move[0]]][self.key[move[1]]] = 'X'

    def gameOver(self):
        def winner(c):
            if c == 'O':
                return self.p1
            return self.p2
        for i in self.board:
            if '  ' != i[0] and i[0]==i[1] and i[1]==i[2]:
                return winner(i[0])
        for i in range(3): 
            if '  ' != self.board[0][i] and self.board[0][i]==self.board[1][i] and self.board[1][i]==self.board[2][i]:
                return winner(self.board[0][i])
        if '  ' != self.board[0][0] and self.board[0][0]==self.board[1][1] and self.board[1][1]==self.board[2][2]:
            return winner(self.board[0][0])
        if '  ' != self.board[0][2] and self.board[0][2]==self.board[1][1] and self.board[1][1]==self.board[2][0]:
            return winner(self.board[0][2])
        for i in self.board:
            for x in i:
                if x == '  ':
                    return None
        return "stalemate"


class connectFourBoard:
    def __init__(self,player1,player2):
        print("starting connect 4")
        self.title = "Connect Four"
        self.initalMessage = "Welcome to Connect Four beta\n to move, type a number 1 through 7"
        self.p1 = player1
        self.p2 = player2
        self.board = []
        for i in range(7):
            self.board.append([])
            for x in range(6):
                self.board.append("  ")

    def out(self):
        b = []
        for i in range(6,-1,-1):
            for x in range(6):
                b = self.board[x][i]
        b = tuple(b)
        return item("text","\
|{}|{}|{}|{}|{}|{}|{}|\n\
|{}|{}|{}|{}|{}|{}|{}|\n\
|{}|{}|{}|{}|{}|{}|{}|\n\
|{}|{}|{}|{}|{}|{}|{}|\n\
|{}|{}|{}|{}|{}|{}|{}|\n\
|{}|{}|{}|{}|{}|{}|{}|\n\
|====================|\n\
|                    |".format(b))

    def islegal(self,player,move):
        if self.board[int(move)-1][5] == "  ":
            return True
        return False

    def move(self,player,move):
        for i in range(6):
            if self.board[int(move)-1][i] == "  ":
                if player == p1:
                    self.board[int(move)-1][i] = 'O'
                else:
                    self.board[int(move)-1][i] = 'X'
                return
        print("How did I get here?")

    def gameOver:
        return None



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
            if text[x:x+7] == "random(":
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


def parse(string=None,key=' '):
    out = []
    index = 0
    out.append("")
    foundOne = False
    for i in string:
        if i==key:
            foundOne = True
            index+=1
            out.append("")
        else:
            out[index]+=i
    if not foundOne:
        return [string]
    return out

def echo(*args):
    out = package()
    for i in args:
        out.append(item("text",i))
    return out

def remove(label):
    r = findResponse(label)
    if r != None:
        responses.remove(r)
    global waiters
    w = findWaiter(label)
    if w != None:
        waiters.remove(w)

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


F = Format()
responses = [
#    exit("exit"),
    response(["cancel","stop"],passMessage = True,function = cancel),
    response(["hello","hi"], ["Hello Barasu", "Hello", "hey"]),
    response(["hello ram","hi ram"],["Hello Barasu", "Hello", "hey"],usePrefix = False),
    response("Ping", "Pong"),
    response("Marco", "Polo",usePrefix = False),
#    time(["time","what time is it?","what time is it"]),
    response("b.rem","Who's Rem?",usePrefix = False),
#    holdup("holdup"),
    response("flip a coin",["Heads","Tails"]),
    response(["snap?","snap"],["Death","Mercy"]),
    response("send yourself",item("file","./ram.py")),
    response("send bootstrapper",item("file","./bootstrapper.py")),
    response("send starter",item("file","./starter.py")),
    response("send backup",item("file","./rambackup.py")),
    response("send test meme",runAtSend(redditRetrieve,2,"animemes","top")),
    response("help","Look I don't really know what's going on either"),
    response("send lock","nice try barasu"),
    response("runatsend test",runAtSend(runAtSendTest)),
    response("hushhush",";)",locked = True),
    response(None,["Fuck you Kyle",None,None],user = KYLE,usePrefix = False),
    response("berserk",package(
        runAtSend(redditRetrieve,4,"nukedmemes"),
        runAtSend(redditRetrieve,4,"cursedimages"),
        runAtSend(redditRetrieve,4,"animemes")
    ),locked = True),
    response("echo",None,takeArgs = True,function = echo,parse = False),
    response("parse",None,takeArgs = True,function = echo),
    response("meme",None,1,function = redditRetrieve,takeArgs = True),
    response("Function test",None,"hello World",function = echo),
#    response("30 seconds?","not yet",label = "30seconds"),
    response("webwork",function = webwork,takeArgs = True,parse = False,passMessage = True),
    response("tictactoe beta","here",ticBoard,function = game,passMessage = True)
]


waiters = [
    dailyPoster(datetime.time(hour = 18),BARASU,runAtSend(redditRetrieve,4,"animemes","top")),
    randDailyPoster(SCREAM_CHAMBER_BOT_SPAM,item("text","owo daily"))
#    waiter(15,AVERAGE_PHOTOGRAPHER_SPAM,runAtSend(redditRetrieve,2,"dankmemes","new"),4)
#    waiter(10,BARASU,"Heartbeat",-1)
#    removeResponse(30,AVERAGE_PHOTOGRAPHER_SPAM,"30seconds","30 seconds have passed")
    ]
if waiters[0].endtime+datetime.timedelta(days = -1)>datetime.datetime.now():
    waiters[0].endtime = waiters[0].endtime + datetime.timedelta(days = -1)




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





async def iterator():
    global waiters
    now = datetime.datetime.now()
    while True:
#        print("looping")
        await asyncio.sleep(1)
        for i in waiters:
            if i.ready():
#                print("go")
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

