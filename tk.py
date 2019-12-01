import time
from builtins import range, open
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
import sqlite3
from pygame import mixer
import datetime
import random

# creat window -----------------------------------------
windo = Tk()
windo.title("Link Game")
Question = PhotoImage(file="ques.png")
buttonImag = PhotoImage(file='rrr.png')

w = 1050
h = 700
windo.geometry("%dx%d+50+30" % (w, h))

windo.resizable(0, 0)  # to can not change the size of the window

mixer.init()
mixer.music.load('music.wav')

mixer.music.play()
HELPM = StringVar()


def stop_():
    if HELPM.get() == "false":
        mixer.music.pause()
        HELPM.set("true")
    else:
        HELPM.set("false")
        mixer.music.unpause()


# ---------------------------------------------------------

def answers():
    list = random.sample(range(0, 101), 15)
    file = open("answers.txt", "r")
    string_word = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    stre = file.readlines()
    for i in range(15):
        string_word[i] = stre[list[i]]
    file.close()
    return string_word


# ---------------------------------------------------------
def Database():
    global conn, cursor
    conn = sqlite3.connect("players.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `members` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, age TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `players` ( username TEXT,score INTEGER)")


HELPM.set("false")
USERNAME = StringVar()
PASSWORD = StringVar()
AGE = StringVar()
PLAYER1 = StringVar()
PLAYER2 = StringVar()
PLAYER3 = StringVar()
COLORH = StringVar()
COLORH.set("light green")


# ***********************************************************************************************************************

def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(windo)
    LoginFrame.pack(side=TOP, pady=80)

    menubar = Menu(LoginFrame)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=Exit)
    menubar.add_cascade(label="File", menu=filemenu)
    windo.config(menu=menubar)

    lbl_username = Label(LoginFrame, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=1)

    lbl_password = Label(LoginFrame, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)

    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)

    username = Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)

    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)

    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=Login)
    btn_login.grid(row=4, columnspan=2, pady=20)

    lbl_register = Label(LoginFrame, text="Register", fg="Blue", font=('arial', 12))
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)


# ***********************************************************************************************************************

def RegisterForm():
    global RegisterFrame, lbl_result2

    RegisterFrame = Frame(windo)
    RegisterFrame.pack(side=TOP, pady=40)

    lbl_username = Label(RegisterFrame, text="Username:", font=('arial', 18), bd=18)
    lbl_username.grid(row=1)

    lbl_password = Label(RegisterFrame, text="Password:", font=('arial', 18), bd=18)
    lbl_password.grid(row=2)

    lbl_age = Label(RegisterFrame, text="Age:", font=('arial', 18), bd=18)
    lbl_age.grid(row=3)

    lbl_result2 = Label(RegisterFrame, text="", font=('arial', 18))
    lbl_result2.grid(row=5, columnspan=2)

    username = Entry(RegisterFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)

    password = Entry(RegisterFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)

    age = Entry(RegisterFrame, font=('arial', 20), textvariable=AGE, width=15)
    age.grid(row=3, column=1)

    btn_login = Button(RegisterFrame, text="Register", font=('arial', 18), width=35, command=Register)
    btn_login.grid(row=6, columnspan=2, pady=20)

    lbl_login = Label(RegisterFrame, text="Login", fg="Blue", font=('arial', 12))
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)


def Admin_Form():
    global AdminFrame
    AdminFrame = Frame(windo)

    lbl_player1 = Label(AdminFrame, text="player 1:", font=('arial', 18))
    lbl_player1.grid(row=1, column=1)

    player1 = Entry(AdminFrame, font=('arial', 20), textvariable=PLAYER1, width=15)
    player1.grid(row=1, column=2)

    lbl_player2 = Label(AdminFrame, text="player 2:", font=('arial', 18))
    lbl_player2.grid(row=2, column=1)

    player2 = Entry(AdminFrame, font=('arial', 20), textvariable=PLAYER2, width=15)
    player2.grid(row=2, column=2)

    lbl_player3 = Label(AdminFrame, text="player 3:", font=('arial', 18))
    lbl_player3.grid(row=3, column=1)

    player3 = Entry(AdminFrame, font=('arial', 20), textvariable=PLAYER3, width=15)
    player3.grid(row=3, column=2)

    add_button = Button(AdminFrame, text='Add', width=19, command=Add_Players)
    add_button.grid(row=5, column=2)

    lbl_result = Label(AdminFrame, text="", font=('arial', 18))
    lbl_result.grid(row=6, columnspan=2)

    lbl_remmove = Label(AdminFrame, text="Remove Player:", font=('arial', 18))
    lbl_remmove.grid(row=20, column=1)

    remove_player = Entry(AdminFrame, font=('arial', 20), width=15)
    remove_player.grid(row=20, column=2)

    def Remove_player():  # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        Database()
        cursor.execute("SELECT * FROM players WHERE username =?", (remove_player.get(),))
        if cursor.fetchone() is not None:
            result = tkMessageBox.askquestion('System', 'Are you sure you want to remove the player', icon="warning")
            if result == 'yes':
                cursor.execute("delete from players where username= ?", (remove_player.get(),))


        else:
            print("no")

    remove_button = Button(AdminFrame, text='Remove', width=19, height=2, command=Remove_player)
    remove_button.grid(row=21, column=2)

    AdminFrame.pack()


def Add_Players():
    Database()
    Players_L = (PLAYER1, PLAYER2, PLAYER3)
    if PLAYER1.get() == "" or PLAYER2.get() == "" or PLAYER3.get() == "":
        lbl_result12 = Label(AdminFrame, text="Please complete the required field!", fg="orange")
        lbl_result12.grid(row=6, column=2, columnspan=2)

    else:
        for Player in Players_L:
            cursor.execute("SELECT * FROM players WHERE `username` = ?", (Player.get(),))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO  players (username,score) VALUES(?,?)", (str(Player.get()), 0))
                conn.commit()
        cursor.close()
        conn.close()
        ToggleTo__Menu()


def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        windo.destroy()
        exit()


def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()


def ToggleTo__Menu(event=None):
    AdminFrame.destroy()
    MenuForm()


def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()


def Register():
    Database()

    if USERNAME.get == "" or PASSWORD.get() == "" or AGE.get() == "":
        lbl_result2.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `members` WHERE `username` = ?", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Username is already taken", fg="red")
        else:
            cursor.execute("INSERT INTO `members` (username, password, age) VALUES(?, ?, ?)",
                           (str(USERNAME.get()), str(PASSWORD.get()), str(AGE.get())))
            conn.commit()
            USERNAME.set("")
            PASSWORD.set("")
            AGE.set("")
            lbl_result2.config(text="Successfully Created!", fg="black")
        cursor.close()
        conn.close()


def Login():
    Database()

    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `members` WHERE `username` = ? and `password` = ?",
                       (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            lbl_result1.config(text="You Successfully Login", fg="blue")
            LoginToAdmin()
        else:
            lbl_result1.config(text="Invalid Username or password", fg="red")


def MenuForm():
    global MenuFrame

    MenuFrame = Frame(windo)
    MenuFrame.pack(side=TOP, pady=80)
    btnStyle = ttk.Style()
    btnStyle.configure('TButton', height=40, width=40, font=('arial', 20))

    exit_btn = ttk.Button(MenuFrame, text='Exit', command=Exit, style='TButton')
    exit_btn.pack()

    play_btn = ttk.Button(MenuFrame, text='Play', command=ToggleToGame, style='TButton')
    play_btn.pack()

    credits_btn = ttk.Button(MenuFrame, text='Credits', style='TButton', command=MenuToCreadit)
    credits_btn.pack()

    sitting_btn = ttk.Button(MenuFrame, text='Sittings', command=ToggleToSitting, style='TButton')
    sitting_btn.pack()

    about_btn = ttk.Button(MenuFrame, text='Help', style='TButton', command=MenuToHelp)
    about_btn.pack()
    windo.configure(bg=COLORH.get())


def SittingsForm():
    global SittingsFrame

    SittingsFrame = Frame(windo)
    SittingsFrame.pack(side=TOP, pady=80)

    sound_btn = Button(SittingsFrame, text='Sound', font=('arial', 20), command=stop_)
    sound_btn.pack()

    back_btn = Button(SittingsFrame, text='Change Back-Ground', font=('arial', 20), command=ChangeBackGround)
    back_btn.pack()

    ret_btn = Button(SittingsFrame, text='Return To Menu', font=('arial', 20), command=RetMenu)
    ret_btn.pack()


def GameForm():
    global GameFrame
    GameFrame = Frame(windo)
    GameFrame.pack()
    start = datetime.datetime.now()

    def times():
        elapsed = datetime.datetime.now() - start

        lbl_time.config(text='Time is : '+ str(elapsed))
        lbl_time.after(1000, times)

    rre = 0

    def fun():
        nonlocal rre
        helpListPlayers = [list_player1, list_player2, list_player3]
        convert_answers(helpListPlayers[rre])
        rre += 1
    def round_change():
        nonlocal rre
        helpListPlayers=[list_player1,list_player2,list_player3]
        convert_answers(helpListPlayers[rre])
        rre+=1



    list_player1 = [' ', ' ', ' ', ' ', ' ']
    list_player2 = [' ', ' ', ' ', ' ', ' ']
    list_player3 = [' ', ' ', ' ', ' ', ' ']
    list = answers()

    for i in range(5):
        list_player1[i] = list[i]

    c = 0
    for i in range(5, 10):
        list_player2[c] = list[i]
        c += 1

    c = 0
    for i in range(10, 15):
        list_player3[c] = list[i]
        c = c + 1

    def convert_answers(list_):
        btn1.config(text=list_[0])
        btn2.config(text=list_[1])
        btn3.config(text=list_[2])
        btn4.config(text=list_[3])
        btn5.config(text=list_[4])

    menubar = Menu(GameFrame)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=Exit)
    menubar.add_cascade(label="File", menu=filemenu)
    windo.config(menu=menubar)

    lbl_time = Label(GameFrame, fg='red', font=('arial', 18))
    lbl_time.pack(side='top', pady=5, anchor='sw')

    lbl_ = Label(GameFrame, text='Score ' + USERNAME.get() + ' : ', fg='red', font=('arial', 18))
    lbl_.pack(side='top', pady=5, anchor='sw')

    lbl_1 = Label(GameFrame, text='Score ' + PLAYER1.get() + ' : ', fg='red', font=('arial', 18))
    lbl_1.pack(side='top', pady=5, anchor='sw')

    lbl_2 = Label(GameFrame, text='Score ' + PLAYER2.get() + ' : ', fg='red', font=('arial', 18))
    lbl_2.pack(side='top', pady=5, anchor='sw')

    lbl_3 = Label(GameFrame, text='Score ' + PLAYER3.get() + ' : ', fg='red', font=('arial', 18))
    lbl_3.pack(side='top', pady=5, anchor='sw')

    qes = Button(GameFrame, text="aa")
    qes.pack(side='top', padx=10, pady=5, anchor='s')
    qes.config(image=Question, compound='center', fg='red', font=('arial', 18))

    btn1 = Button(GameFrame, text="Click", command=fun)
    btn1.pack(side='left', padx=10, pady=5, anchor='sw')
    btn1.config(image=buttonImag, compound='center', fg='#ffffff', font=('arial', 18))

    btn2 = Button(GameFrame, text="Quit", command=fun)
    btn2.pack(side='left', pady=5, anchor='sw')
    btn2.config(image=buttonImag, compound='center', fg='#ffffff', font=('arial', 18))

    btn3 = Button(GameFrame, text="Click", command=fun)
    btn3.pack(side='left', padx=10, pady=5, anchor='sw')
    btn3.config(image=buttonImag, compound='center', fg='#ffffff', font=('arial', 18))

    btn4 = Button(GameFrame, text="Quit", command=fun)
    btn4.pack(side='left', pady=5, anchor='sw')
    btn4.config(image=buttonImag, compound='center', fg='#ffffff', font=('arial', 18))

    btn5 = Button(GameFrame, text="Quit", command=fun)
    btn5.pack(side='left', padx=10, pady=5, anchor='sw')
    btn5.config(image=buttonImag, compound='center', fg='#ffffff', font=('arial', 18))
    times()


def ChangeBackGround():
    if COLORH.get() == "light green":
        COLORH.set("purple")
        windo.configure(bg="purple")
    else:
        COLORH.set("light green")
        windo.configure(bg="light green")


def ToggleToSitting(event=None):
    MenuFrame.destroy()
    SittingsForm()


def LoginToAdmin(event=None):
    LoginFrame.destroy()
    Admin_Form()


def RetMenu(event=None):
    SittingsFrame.destroy()
    MenuForm()


def Show_player_round(name):
    GameFrame.destroy()
    global Show_player_Frame
    Show_player_Frame = Frame(windo)
    Show_player_Frame.pack()
    lbl_game = Label(GameFrame, text=name, font=('arial', 50), bd=18)
    lbl_game.pack()
    for i in range(5, 0, -1):
        time.sleep(1)
    Show_player_Frame.destroy()
    GameForm()


def ToggleToMenu(event=None):
    LoginFrame.destroy()
    MenuForm()


def ToggleToGame(event=None):
    MenuFrame.destroy()
    GameForm()


def CreaditsForm():
    global CreaditsFrame
    CreaditsFrame = Frame(windo)
    CreaditsFrame.configure(bg='red')
    T = Text(CreaditsFrame, height=15, width=80, font=('arial', 14))
    T.pack()
    quote = """HAMLET: To be, or not to be--that is the question:
    Whether 'tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune
    Or to take arms against a sea of troubles
    And by opposing end them. To die, to sleep--
    No more--and by a sleep to say we end
    The heartache, and the thousand natural shocks
    That flesh is heir to. 'Tis a consummation
    Devoutly to be wished."""
    T.insert(END, quote)
    T.config(state=DISABLED)
    newbtb = Button(CreaditsFrame, text='Return To Menu', font=('arial', 20), command=CreaditToMenu)
    newbtb.pack()
    CreaditsFrame.pack()


def HelpForm():
    global HelpFrame
    HelpFrame = Frame(windo)
    HelpFrame.configure(bg='red')
    T = Text(HelpFrame, height=15, width=80, font=('arial', 14))
    T.pack()
    quote = """HAMLET: To be, or not to be--that is the question:
    Whether 'tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune
    Or to take arms against a sea of troubles
    And by opposing end them. To die, to sleep--
    No more--and by a sleep to say we end
    The heartache, and the thousand natural shocks
    That flesh is heir to. 'Tis a consummation
    Devoutly to be wished."""
    T.insert(END, quote)
    T.config(state=DISABLED)

    newbtb1 = Button(HelpFrame, text='Return To Menu', font=('arial', 20), command=HelpToMenu)
    newbtb1.pack()
    HelpFrame.pack()


def HelpToMenu(event=None):
    HelpFrame.destroy()
    MenuForm()


def MenuToHelp(event=None):
    MenuFrame.destroy()
    HelpForm()


def CreaditToMenu(event=None):
    CreaditsFrame.destroy()
    MenuForm()


def MenuToCreadit(event=None):
    MenuFrame.destroy()
    CreaditsForm()


LoginForm()

if __name__ == '__main__':
    windo.mainloop()