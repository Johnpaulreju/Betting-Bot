from tkinter import *
from tkinter import messagebox
import smtplib
import time
import pygame
from email.message import EmailMessage
import random
from functools import partial
from copy import deepcopy
from tkinter import ttk
from tkinter.font import Font
from twilio.rest import Client
####################################SMS SENDING#############################################
'''# verification code cf7lCDu02iyp6SbZKyddytgyBh06wmorlGcNRBTZ  
account_sid = 'AC96e4c1d4b2def1046a50ea8396942ffc'
auth_token = 'a1b4e5d55cd50649796487ca17997a6d'
client = Client(account_sid, auth_token)

message = client.messages.create(
         body='OTP for login - 8849',
         from_='+13344012740',
         to='+917742521023 '
     )

print(message.sid)'''
####################################TIC TAC TOE STARTS##########################################################
# sign variable to decide the turn of which player
sign = 0
button="global"
label="global"

# Creates an empty board
global board
board = [[" " for x in range(3)] for y in range(3)]
  
# Check l(O/X) won the match or not
# according to the rules of the game
def winner(b, l):
    return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
            (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
            (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
            (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
            (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
            (b[0][2] == l and b[1][1] == l and b[2][0] == l))
  
# Configure text on button while playing with another player
def get_text(i, j, gb, l1, l2):
    global sign
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    if winner(board, "X"):
        gb.destroy()
        box = messagebox.showinfo("Winner", "Player 1 won the match")
    elif winner(board, "O"):
        gb.destroy()
        box = messagebox.showinfo("Winner", "Player 2 won the match")
    elif(isfull()):
        gb.destroy()
        box = messagebox.showinfo("Tie Game", "Tie Game")
  
# Check if the player can push the button or not
def isfree(i, j):
    return board[i][j] == " "
  
# Check the board is full or not
def isfull():
    flag = True
    for i in board:
        if(i.count(' ') > 0):
            flag = False
    return flag
  
# Create the GUI of game board for play along with another player
def gameboard_pl(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3+i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()
  
# Decide the next move of system
def pc():
    possiblemove = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                possiblemove.append([i, j])
    move = []
    if possiblemove == []:
        return
    else:
        for let in ['O', 'X']:
            for i in possiblemove:
                boardcopy = deepcopy(board)
                boardcopy[i[0]][i[1]] = let
                if winner(boardcopy, let):
                    return i
        corner = []
        for i in possiblemove:
            if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                corner.append(i)
        if len(corner) > 0:
            move = random.randint(0, len(corner)-1)
            return corner[move]
        edge = []
        for i in possiblemove:
            if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                edge.append(i)
        if len(edge) > 0:
            move = random.randint(0, len(edge)-1)
            return edge[move]
  
# Configure text on button while playing with system
def get_text_pc(i, j, gb, l1, l2):
    global sign
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            button[i][j].config(state=ACTIVE)
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    x = True
    if winner(board, "X"):
        gb.destroy()
        x = False
        box = messagebox.showinfo("Winner", "Player won the match")
    elif winner(board, "O"):
        gb.destroy()
        x = False
        box = messagebox.showinfo("Winner", "Computer won the match")
    elif(isfull()):
        gb.destroy()
        x = False
        box = messagebox.showinfo("Tie Game", "Tie Game")
    if(x):
        if sign % 2 != 0:
            move = pc()
            button[move[0]][move[1]].config(state=DISABLED)
            get_text_pc(move[0], move[1], gb, l1, l2)
  
# Create the GUI of game board for play along with system
def gameboard_pc(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3+i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text_pc, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()
  
# Initialize the game board to play with system
def withpc(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text="Player : X", width=10)
    l1.grid(row=1, column=1)
    l2 = Button(game_board, text = "Computer : O",
                width = 10, state = DISABLED)
      
    l2.grid(row = 2, column = 1)
    gameboard_pc(game_board, l1, l2)
  
# Initialize the game board to play with another player
def withplayer(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text = "Player 1 : X", width = 10)
      
    l1.grid(row = 1, column = 1)
    l2 = Button(game_board, text = "Player 2 : O", 
                width = 10, state = DISABLED)
      
    l2.grid(row = 2, column = 1)
    gameboard_pl(game_board, l1, l2)
  
# main function
def play():
    menu = Tk()
    menu.geometry("350x210")
    menu.title("Tic Tac Toe")
    wpc = partial(withpc, menu)
    wpl = partial(withplayer, menu)
      
    head = Label(menu, text = "---Welcome to---\n---tic-tac-toe---",font=Font(family="Algerian",size=20,underline=0,overstrike=0),
                  activeforeground = 'red',
                  activebackground = "yellow", bg = "black", 
                  fg = "white", width = 500, bd = 5).pack(side="top")
      
    B1 = Button(menu, text = "Single Player", command = wpc, 
                activeforeground = 'red',
                activebackground = "yellow", bg = "red", 
                fg = "yellow", width = 500, font=Font(family="Algerian",size=15,underline=0,overstrike=0), bd = 5).pack(side="top")
      
    B2 = Button(menu, text = "Multi Player", command = wpl, activeforeground = 'red',
                activebackground = "yellow", bg = "red", fg = "yellow",
                width = 500,font=Font(family="Algerian",size=15,underline=0,overstrike=0), bd = 5).pack(side="top")
      
    B3 = Button(menu, text = "Exit", command = menu.quit, activeforeground = 'red',
                activebackground = "yellow", bg = "red", fg = "yellow",
                width = 500, font=Font(family="Algerian",size=15,underline=0,overstrike=0), bd = 5).pack(side="top")

###########################################Snake Games START##########################################################
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
dr_red = (139,0,0)
 
dis_width = 600
dis_height = 400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('RISKO Betting')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("algerian", 35)

 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, red)
    dis.blit(value, [0, 0])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, dr_red, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 
 
def gameLoop():
    messagebox.showinfo("Betting Info","5$ Deducted from your Account")
    
    game_over = False
    game_close = False
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
 
    while not game_over:
 
        while game_close == True:
            dis.fill(black)
            message("You Lost! Press SpaceBar to Play Again or Q to Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = False
                        game_close = True
                    if event.key == pygame.K_SPACE:
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            print(Length_of_snake-1)
            if (Length_of_snake-1) >5:
                messagebox.showinfo("RISKO Betting","Congrats! You Won 5$")
            else :
                messagebox.showinfo("RISKO Betting","Sorry! You Lost")
            collect()
            game_over = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()

###############################################Snake Game ENDS#############################################################

def deduct():
    email_alert("RISKO Account Message", "5$ has been deducted", str("johnpaul.19bcan039@jecrcu.edu.in"))

def message():
    messagebox.showinfo("Reward Collected","Your $50 Has Been Sent To \n Yur Account")

def verify():
    global otpentry
    global onetimepass
    otparea = str(otpentry.get())
    if otparea == onetimepass:
        messagebox.showinfo("OTP detail","Otp verified")
        newF()
        a.destroy()
    else:
        messagebox.showinfo("OTP detail","Otp not verified")
        frame2()

def collect():
    gm=Toplevel()
    gm.title("Chosse the game")
    gm.geometry('500x300')
    bg = PhotoImage(file="D:/jarvis/red.png")
    la = Label(gm, image = bg).place(x=0, y=0, relwidth=1, relheight=1)
    label_4 = Label(gm,text="RISKO \n Betting",font=Font(family="Algerian",size=30,weight="bold",slant="roman",underline=0,overstrike=0)).place(x=160,y=0)
    label_5= Label(gm,text="You have",font=Font(family="Arial",size=10,slant="roman",underline=0,overstrike=0)).place(x=380,y=20) 
    label_6= Label(gm,text="50$",font=Font(family="Arial",size=10,slant="roman",underline=0,overstrike=0)).place(x=440,y=20)  
    sent=Button(gm,text="Tic Tac Toe", command=lambda: [gm.destroy(),play()] ,font=Font(family="arial",size=15,weight="bold") ,activeforeground = 'red'
        ,activebackground = "yellow", bg = "white", fg = "red",width = 15, bd = 5).place(x=240,y=160)
    sent=Button(gm,text="Snake", command=lambda: [gm.destroy(),gameLoop()] ,font=Font(family="arial",size=15,weight="bold") ,activeforeground = 'red'
        ,activebackground = "yellow", bg = "white", fg = "red",width = 15, bd = 5).place(x=30,y=160)
    sent=Button(gm,text="Quit", command = gm.destroy ,font=Font(family="arial",size=15,weight="bold") ,activeforeground = 'red'
        ,activebackground = "yellow", bg = "white", fg = "red",width = 15, bd = 5).place(x=160,y=220)
    
    gm.mainloop()

def newF():  
    gam=Toplevel()
    gam.title("Collect Reward")
    gam.geometry('500x300')
    bg = PhotoImage(file="D:/jarvis/red.png")
    la = Label(gam, image = bg).place(x=0, y=0,
     relwidth=1, relheight=1)
    label_4 = Label(gam,text="RISKO \n Betting",font=Font(family="Algerian",size=30,weight="bold",slant="roman",underline=0,overstrike=0)).place(x=160,y=0) 
    messagebox.showinfo("Registration","Thanks For The Registration\n You Can Collect You reward of $50")
    label_1 = Label(gam,text="Collect Your Reward",font=Font(family="Arial",size=15,underline=0,overstrike=0)).place(x=160,y=135)
    
    sent=Button(gam,text="$50", command =lambda:[gam.destroy(),message(),collect()] ,font=Font(family="arial",size=15,weight="bold") ,activeforeground = 'red'
        ,activebackground = "yellow", bg = "white", fg = "red",width = 15, bd = 5).place(x=160,y=200)
    
    gam.mainloop()

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "bcaproject2k21@gmail.com"
    msg['from'] = user
    password = "sirrfnmvsmgyycsq"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

onetimepass = random.randint(1111,9999)

def otp():
    global EMAILID
    global onetimepass
    k = EMAILID.get()
    # verification code cf7lCDu02iyp6SbZKyddytgyBh06wmorlGcNRBTZ  
    account_sid = 'AC96e4c1d4b2def1046a50ea8396942ffc'
    auth_token = 'a1b4e5d55cd50649796487ca17997a6d'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
            body="To authenticate, please use the following One Time Password (OTP): "+str(onetimepass),
            from_='+13344012740',
            to='+91'+str(k)
        )
    print(message.sid)
    messagebox.showinfo('OTP Detail','OTP has been sent to your Phone Number')




def step():
    for x in range(4):
        progress['value'] +=25
        pro.update_idletasks()
        time.sleep(1)
        lab.config(text=(25+progress['value']))
        if progress['value'] == 100:
            lab.config(text="Completed!!")
            

def term():
    
    ter= Toplevel()
    ter.title("RISKO Betting")
    ter.geometry('560x250')
    bg = PhotoImage(file="D:/jarvis/red.png")
    lk = Label(ter, image = bg).place(x=0, y=0, relwidth=1, relheight=1)
    kr= Label(ter, text=" 11.1  EXCLUSION OF DAMAGES.EXCEPT AS OTHERWISE PROVIDED IN SECTION 11.3, IN \n NO EVENT WILL EITHER PARTY BE LIABLE UNDER OR IN CONNECTION WITH THE AGREEMENT OR ITS \nSUBJECT MATTER UNDER ANY LEGAL OR EQUITABLE THEORY, INCLUDING BREACH OF \nCONTRACT, TORT (INCLUDING NEGLIGENCE), STRICT LIABILITY AND OTHERWISE, \nFOR ANY: (a) LOSS OF PRODUCTION, USE, BUSINESS, REVENUE OR PROFIT; OR (b) IMPAIRMENT,\n INABILITY TO USE OR LOSS, INTERRUPTION OR DELAY OF THE SERVICES CONSEQUENTIAL,\n INCIDENTAL, INDIRECT, EXEMPLARY, SPECIAL, ENHANCED OR PUNITIVE DAMAGES, REGARDLESS \nOF WHETHER SUCH PERSONS WERE ADVISED OF THE POSSIBILITY OF SUCH LOSSES OR DAMAGES\n OR SUCH LOSSES OR DAMAGES WERE OTHERWISE FORESEEABLE, AND NOTWITHSTANDING \nTHE FAILURE OF ANY AGREED OR OTHER REMEDY OF ITS ESSENTIAL PURPOSE.\n")
    kr.pack(pady=20)
    exit=Button(ter,text="Exit",command=ter.destroy ,font=Font(family="arial",size=10,weight="bold") 
    ,activeforeground = 'red',activebackground = "yellow", bg = "white", fg = "red",width = 10, bd = 5).place(x=250,y=195)
    ter.mainloop()
'''
def frame3():
    
    acc= Toplevel()
    acc.title("Create Account")
    acc.geometry('500x300')
    bg = PhotoImage(file="D:/jarvis/red.png")
    la = Label(acc, image = bg).place(x=0, y=0, relwidth=1, relheight=1)
    label1 =Label(acc,text="Create Your Account",font=Font(family="Algerian",size=22,weight="bold",slant="roman",underline=0,overstrike=0)).place(x=160,y=0) 
    label_1 = Label(acc,text="Name",font=Font(family="Algerian",size=15,underline=0,overstrike=0)).place(x=25,y=105)
    entry_1 = Entry(acc,width=25,font=Font(family="times",size=15))
    entry_1.place(x=220,y=105)
    sent=Button(acc,text="Send OTP",command=otp ,font=Font(family="arial",size=15,weight="bold") ,activeforeground = 'red'
        ,activebackground = "yellow", bg = "white", fg = "red",width = 15, bd = 5).place(x=250,y=240)'''

def frame3():
    
    acc= Toplevel()
    acc.title("Create Account")
    acc.geometry('600x350')
    bg = PhotoImage(file="D:/jarvis/red.png")
    la = Label(acc, image = bg).place(x=0, y=0, relwidth=1, relheight=1)
    label1 =Label(acc,text="Create Your Account",font=Font(family="Algerian",size=22,weight="bold",slant="roman",underline=0,overstrike=0)).place(x=150,y=30) 
    label_1 = Label(acc,text="Name",font=Font(family="Algerian",size=15,underline=0,overstrike=0)).place(x=25,y=100)
    entry_4 = Entry(acc,width=25,font=Font(family="times",size=15))
    entry_4.place(x=100,y=100)
    genderlabel =Label(acc,text="Gender",font=Font(family="Algerian",size=15,underline=0,overstrike=0)).place(x=450,y=100)
    gender = Radiobutton(acc, text="Male").place(x=420,y=140)
    gender = Radiobutton(acc, text="Female").place(x=490,y=140)
    label_2 = Label(acc,text="Age",font=Font(family="Algerian",size=15,underline=0,overstrike=0)).place(x=25,y=140)
    entry_2 = Entry(acc,width=25,font=Font(family="times",size=15))
    entry_2.place(x=100,y=140)
    label_2 = Label(acc,text="***OTP will be sent\n to the given Email***",font=Font(family="Arial",size=10,underline=0,overstrike=0)).place(x=25,y=260)
    label_3 = Label(acc,text="Phone No.",font=Font(family="Algerian",size=15,underline=0,overstrike=0)).place(x=25,y=180)
    entry_3 = Entry(acc,width=25,font=Font(family="times",size=15))
    entry_3.place(x=140,y=180)
    label_3 = Label(acc,text="Email ID",font=Font(family="Algerian",size=15,underline=0,overstrike=0)).place(x=25,y=220)
    entry_1 = Entry(acc,width=25,font=Font(family="times",size=15))
    entry_1.place(x=140,y=220)
    sent=Button(acc,text="Send OTP" ,command=acc.destroy,font=Font(family="arial",size=15,weight="bold") ,activeforeground = 'red'
        ,activebackground = "yellow", bg = "white", fg = "red",width = 15, bd = 5).place(x=180,y=280)
    acc.mainloop()



def frame2():   
    a.mainloop()

if __name__ == "__main__" : 
    pro= Tk()
    pro.title("RISKO Betting")
    pro.geometry('500x200')
    '''dg = PhotoImage(file="D:/Project/black.png")
    la = Label(pro, image = dg).place(x=0, y=0, relwidth=1, relheight=1)'''
    progress = ttk.Progressbar(pro, orient=HORIZONTAL,length=400,mode='determinate')
    progress.pack(pady=20)
    lab=Label(pro, text="")
    lab.place(x=240,y=60)
    check=Checkbutton(pro,text="Accept The T&C")
    check.place(x=180,y=100)
    sent=Button(pro,text="Term & Condition",command=term ,font=Font(family="arial",size=15,weight="bold") 
        ,activeforeground = 'red',activebackground = "yellow", bg = "white", fg = "red",width = 15, bd = 5).place(x=250,y=130)
    sent=Button(pro,text="Login",command=lambda: [step(),pro.destroy(),frame2()],font=Font(family="arial",size=15,weight="bold") 
        ,activeforeground = 'red',activebackground = "yellow", bg = "white", fg = "red",width = 15, bd = 5).place(x=50,y=130)
    pro.mainloop()

###################    ANOTHER INTERFACE        ##############################     
    a= Tk()
    a.title("Login")
    a.geometry('500x300')
    bg = PhotoImage(file="D:/jarvis/red.png")
    ra = Label(a, image = bg).place(x=0, y=0, relwidth=1, relheight=1)
    label_4 = Label(a,text="RISKO \n Betting",font=Font(family="Algerian",size=30,weight="bold",slant="roman",underline=0,overstrike=0)).place(x=160,y=0) 
    label_1 = Label(a,text="Enter your Phone NO.",font=Font(family="Algerian",size=15,underline=0,overstrike=0)).place(x=25,y=105)
    EMAILID = Entry(a,width=25,font=Font(family="times",size=15))
    EMAILID.place(x=250,y=105)
    sent=Button(a,text="Send OTP",command=otp ,font=Font(family="arial",size=15,weight="bold") ,activeforeground = 'red'
        ,activebackground = "yellow", bg = "white", fg = "red",width = 15, bd = 5).place(x=250,y=240)
    label_2 = Label(a,text="Enter you OTP ",font=Font(family="Algerian",size=15,underline=0,overstrike=0)).place(x=25,y=160)
    otpentry = Entry(a,width=5,font=Font(family="times",size=15))
    otpentry.place(x=220,y=160)
    acc = Button(a,text="I Don't have Account ",command=frame3 ,font=Font(family="times",size=8,underline=0,overstrike=0),activeforeground = 'red'
        ,activebackground = "yellow", bg = "white", fg = "red",width = 20, bd = 5).place(x=180,y=200)
    verotp=Button(a,text="Verify",command=lambda: [verify()],font=Font(family="arial",size=15,weight="bold") ,activeforeground = 'red'
        ,activebackground = "yellow", bg = "white", fg = "red",width = 15, bd = 5).place(x=40,y=240)         
    print(onetimepass)



    pro.mainloop()
    