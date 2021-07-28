from botbasics import *
DAY = 86400

def gameInit(message,board,inputFormat):
    if len(message.mentions)!=1:
        return item("text","@ one person to play with")
    board = board(message.author.id,message.mentions[0].id)
    label = board.title+str(message.author.id+message.mentions[0].id)+str(message.channel.id)
    if findResponse(label)!=None:
        return item("text","game with "+message.mentions[0].display_name+" active, send 'ram cancel' on your turn to cancel the game")
    print("set the board")
    global responses
    responses.append(response("",None,message.author,board,inputFormat,function = game,usePrefix = False,takeArgs = True, parse = False,channel = message.channel.id,user = message.mentions[0].id,passMessage = True,format = inputFormat,label = label))
    global waiters
    waiters.append(removeResponse(board.expiration,message.channel.id,label,item("text",board.title+" game between {} and {} has expired".format(message.author.display_name,message.mentions[0].display_name)),label = label))
    return package(board.initalMessage,board.out())

def game(message,opponent,board,inputFormat,move):
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
        r = findResponse(label)
        responses.remove(r)
        responses.append(response("",None,message.author,board,inputFormat,function = game,usePrefix = False,takeArgs = True, parse = False,channel = message.channel.id,user = opponent.id,passMessage = True,format = inputFormat,label = label))
        outputBoard = board.out()
        return package(item("text",opponent.mention+" your move"),outputBoard)
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
        self.expiration = DAY
        
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
        self.initalMessage = item("text","Welcome to Connect Four beta\n to move, type a number 1 through 7")
        self.p1 = player1
        self.p2 = player2
        self.board = []
        for i in range(7):
            self.board.append([])
            for x in range(6):
                self.board[i].append("   ")
        self.expiration = DAY*7

    def out(self):
        print("making output")
        b = []
        for i in range(5,-1,-1):
            for x in range(7):
                b.append(self.board[x][i])
        b = tuple(b)
        print("made tuple len: "+ str(len(b)))
        return item("text","\
.  1    2    3    4   5    6    7\n\
| {} | {} | {} | {} | {} | {} | {} |\n\
| {} | {} | {} | {} | {} | {} | {} |\n\
| {} | {} | {} | {} | {} | {} | {} |\n\
| {} | {} | {} | {} | {} | {} | {} |\n\
| {} | {} | {} | {} | {} | {} | {} |\n\
| {} | {} | {} | {} | {} | {} | {} |\n\
|================|\n\
|                                          |".format(*b))

    def isLegal(self,player,move):
        if self.board[int(move)-1][5] == "   ":
            return True
        return False

    def move(self,player,move):
        for i in range(6):
            if self.board[int(move)-1][i] == "   ":
                if player == self.p1:
                    self.board[int(move)-1][i] = 'O'
                else:
                    self.board[int(move)-1][i] = 'X'
                break

    def gameOver(self):
        def winner(c):
            if c == 'O':
                return self.p1
            return self.p2
        b = self.board
        for i in b:
            for x in range(3):
                if "   "!=i[x]==i[x+1]==i[x+2]==i[x+3]:
                    return winner(i[x])
        for i in range(6):
            for x in range(4):
                if "   "!=b[x][i]==b[x+1][i]==b[x+2][i]==b[x+3][i]:
                    return winner(b[x][i])
        for  i in range(4):
            for x in range(3):
                if "   "!=b[x][i]==b[x+1][i+1]==b[x+2][i+2]==b[x+3][i+3]:
                    return winner(b[x][i])
                if "   "!=b[x+3][i]==b[x+2][i+1]==b[x+1][i+2]==b[x][i+3]:
                    return winner(b[x+3][i])
        return None