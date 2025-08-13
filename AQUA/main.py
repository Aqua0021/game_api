from tkinter import*
from PIL import ImageTk,Image
import tkinter.messagebox as mb
import random
import pygame
import time
import os
import psycopg
from urllib.parse import urlparse

DATABASE_URL = os.getenv("DATABASE_URL")
mydb = psycopg.connect(DATABASE_URL)


def intro():
    root_login.destroy()
    root=Tk()
    root.geometry("300x300")
    img=Image.open('assets/car1.png')
    phot=img.resize((100,100))
    photo=ImageTk.PhotoImage(phot)
    Label(root,text="GAMES WITH AQUA",font=("arial",30,'bold')).pack()
    Button(root,image=photo,width=100,height=100).place(x=500,y=250)
    root.mainloop()
    
def login():
    global login1,E01,E02
    try:
        login2.destroy()
    except:
        try:
            root_login.destroy()
        except:
            pass
    login1=Tk()
    login1.geometry("250x280")
    login1.resizable(width=False,height=False)
    img1=Image.open('assets/signin.png')
    phot1=img1.resize((250,280))
    photo1=ImageTk.PhotoImage(phot1)
    Label(login1,image=photo1).place(x=0,y=0)
    Label(login1,text='LOGIN HERE',bg='#BBCBC8',font=('algerian',30)).pack()
    Label(login1,text='USERNAME:',bg='#BBCBC8',font=('bell mt',15)).place(x=10,y=80)
    Label(login1,text='PASSWORD:',bg='#BBCBC8',font=('bell mt',15)).place(x=10,y=140)
    E01=Entry(login1,font=('bell mt',10),bd=2)
    E1=E01.place(x=10,y=105)
    E02=Entry(login1,font=('bell mt',10),bd=2,show=('*'))
    E2=E02.place(x=10,y=165)
    Button(login1,text='BACK',fg="white",bg="#00173A",width=15,height=2,command=log).place(x=10,y=200)
    Button(login1,text='CONFIRM',fg="white",bg="#00173A",width=15,height=2,command=confirm2).place(x=130,y=200)
    root_login.mainloop()


def confirm2():
    global Uname
    Uname=E01.get()
    E2=E02.get()
    c=mydb.cursor()
    c.execute('select user_name from main_game')
    c2=c.fetchall()
    c=mydb.cursor()
    c.execute('select password from main_game where user_name ='+'"'+Uname+'"')
    c1=c.fetchone()
    L=[]
    for i in c2:
        L.append(i[0].lower())
    if Uname.lower() not in L:
        mb.showerror('Oppppps','User name or Password in incorrect')
    elif E2!=c1[0]:
        mb.showerror('Oppppps','User name or Password in incorrect')
    else:
        INTRO()

def confirm1():
    e1=e01.get()
    e2=e02.get()
    e3=e03.get()
    try:
        L=[]
        c=mydb.cursor()
        c.execute('select user_name from main_game')
        c1=c.fetchall()
        for i in c1:
            L.append(i[0].lower())
        if e1.lower() not in L:
            if e2==e3 and e2!='':
                c=mydb.cursor()
                c.execute("insert into main_game(user_name,password) values(%s,%s)",(e1,e2))
                mydb.commit()
                if mb.askyesno('sucessfull','you are sucessfully registered now go to login')==True:
                    login()
            else:
                mb.showerror('ERROR','PASSWORD are not same')
        else:
            mb.showinfo("",'USERNAME is already taken')
    except:
        pass

def login02():
    global login2,e01,e02,e03
    root_login.destroy()
    login2=Tk()
    login2.geometry("250x300")
    login2.resizable(width=False,height=False)
    img1=Image.open('assets/signin.png')
    phot1=img1.resize((250,300))
    photo1=ImageTk.PhotoImage(phot1)
    Label(login2,image=photo1).place(x=0,y=0)
    Label(login2,text='REGISTER HERE',bg='#BBCBC8',font=('algerian',25)).pack()
    Label(login2,text='USERNAME:',bg='#BBCBC8',font=('bell mt',15)).place(x=10,y=80)
    Label(login2,text='PASSWORD:',bg='#BBCBC8',font=('bell mt',15)).place(x=10,y=140)
    Label(login2,text='CONFIRM PASSWORD:',bg='#BBCBC8',font=('bell mt',10)).place(x=10,y=200)
    e01=Entry(login2,font=('bell mt',10),bd=2)
    e1=e01.place(x=10,y=105)
    e02=Entry(login2,font=('bell mt',10),bd=2,show=('*'))
    e2=e02.place(x=10,y=165)
    e03=Entry(login2,font=('bell mt',10),bd=2,show=('*'))
    e3=e03.place(x=10,y=220)
    Button(login2,text='BACK',fg="white",bg="#00173A",width=15,height=2,command=log).place(x=10,y=250)
    Button(login2,text='CONFIRM',fg="white",bg="#00173A",width=15,height=2,command=confirm1).place(x=130,y=250)
    
    root_login.mainloop()
    
def log():
    try:
        login1.destroy()
    except:
        try:
            login2.destroy()
        except:
            pass
    global root_login
    root_login=Tk()
    root_login.geometry("500x250")
    root_login.resizable(width=False,height=False)
    img=Image.open('assets/login.png')
    phot=img.resize((500,250))
    photo=ImageTk.PhotoImage(phot)
    Label(root_login,image=photo).place(x=0,y=0)
    Label(root_login,text="GAMES WITH AQUA",font=("algerian",30,'bold')).pack()
    Button(root_login,text='login',fg="white",bg="#00173A",width=15,height=2,command=login).place(x=309,y=107)
    Button(root_login,text='register',fg="white",bg="#00173A",width=15,height=2,command=login02).place(x=85,y=107)
    root_login.mainloop()

def INTRO():
    global Intro
    try:
        login1.destroy()
    except:
        pass
    Intro=Tk()
    Intro.geometry("500x250")
    Intro.resizable(width=False,height=False)
    img=Image.open('assets/Intro.png')
    phot=img.resize((500,250))
    photo=ImageTk.PhotoImage(phot)
    img1=Image.open('assets/car1.png')
    phot1=img1.resize((50,50))
    photo1=ImageTk.PhotoImage(phot1)
    img2=Image.open('assets/background2.png')
    phot2=img2.resize((50,50))
    photo2=ImageTk.PhotoImage(phot2)
    Label(Intro,image=photo).place(x=0,y=0)
    Label(Intro,text="GAMES WITH AQUA",font=("algerian",30,'bold')).pack()
    Button(Intro,image=photo1,fg="white",bg="#00173A",width=50,height=50,command=car_game).place(x=85,y=107)
    Button(Intro,image=photo2,fg="white",bg="#00173A",width=50,height=50,command=snake_game).place(x=300,y=107)
    Intro.mainloop()
    
############################################################
#car game
def car_game():
    c=mydb.cursor()
    c.execute('select hard_car_high_score,easy_car_high_score from main_game where user_name='+'"'+Uname+'"')
    global h_score_e,h_score_h,sc
    sc=c.fetchall()
    if sc[0][0]==None and sc[0][1]==None:
        c.execute('update main_game set hard_car_high_score=0,easy_car_high_score=0 where user_name='+'"'+Uname+'"')
        mydb.commit()
        c.execute('select hard_car_high_score,easy_car_high_score from main_game where user_name='+'"'+Uname+'"')
        sc=c.fetchall()
    Intro.destroy()
    pygame.init()
    clock=pygame.time.Clock()
    #leader board
    def leader_board():
        c.execute('select user_name,hard_car_high_score from main_game order by hard_car_high_score desc')
        lb1=c.fetchall()
        c.execute('select user_name,easy_car_high_score from main_game order by easy_car_high_score desc')
        lb2=c.fetchall()
        while True:
            gd.fill(gray)
            Message(50,"EASY",50,0)
            Message(50,"HARD",550,0)
            for i in range(1,21):
                try:
                    Message(30,str(lb1[i-1][0]),500,i*25)
                    Message(30,str(lb1[i-1][1]),700,i*25)
                    Message(30,str(lb2[i-1][0]),0,i*25)
                    Message(30,str(lb2[i-1][1]),200,i*25)
                    button(350,400,'BACK')
                except:
                    pass
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.update()
    #display surface
    gd=pygame.display.set_mode((800,600))
    white=(255,255,255)
    black=(0,0,0)
    red=(255,0,0)
    green=(0,255,0)
    light_green=(0,200,0)
    gray=(119,118,110) 
    blue=(0,0,255)
    h_score_e=sc[0][0]
    h_score_h=sc[0][1]
    #image
    car_img=pygame.image.load('assets/car2.png')
    car_img=pygame.transform.scale(car_img,(100,100))
    car_im=pygame.image.load('assets/car3.png')
    car_im=pygame.transform.scale(car_im,(100,100))
    background=pygame.image.load('assets/background.jpg')
    grass=pygame.image.load('assets/grass.jpg')
    #message\text
    def Message(size,mess,x_pos,y_pos):
        font=pygame.font.SysFont(None,size)
        render=font.render(mess,True,white)
        gd.blit(render,(x_pos,y_pos))


    #car
    def car(x,y):
        gd.blit(car_img,(x,y))
        gd.blit(grass,(0,0))
        gd.blit(grass,(700,0))
        (grass,(700,0))
        if 0<x<90 or 700<x+100:
            Message(100,"GAME OVER",200,200)
            pygame.display.update()
            clock.tick(1)
            game_intro()
    #enmy car
    def enmy_car(x_r,y_r):
        gd.blit(car_im,(x_r,y_r))

    #button
    def button(x_button,y_button,mess_b):
        pygame.draw.rect(gd,green,[x_button,y_button,100,30])
        Message(50,mess_b,x_button,y_button)
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        if x_button<mouse[0]<x_button+100 and y_button<mouse[1]<y_button+30:
            pygame.draw.rect(gd,light_green,[x_button,y_button,100,30])
            Message(50,mess_b,x_button,y_button)
            if click==(1,0,0) and mess_b=='EASY':
                pygame.draw.rect(gd,black,[350,350,50,50])
                Message(50,'3',360,350)
                pygame.display.update()
                time.sleep(1)
                pygame.draw.rect(gd,black,[350,350,50,50])
                Message(50,'2',360,350)
                pygame.display.update()
                time.sleep(1)
                pygame.draw.rect(gd,black,[350,350,50,50])
                Message(50,'1',360,350)
                pygame.display.update()
                time.sleep(1)
                Game_loop_easy()
            elif click==(1,0,0) and mess_b=='HARD':
                pygame.draw.rect(gd,black,[350,350,50,50])
                Message(50,'3',360,350)
                pygame.display.update()
                time.sleep(1)
                pygame.draw.rect(gd,black,[350,350,50,50])
                Message(50,'2',360,350)
                pygame.display.update()
                time.sleep(1)
                pygame.draw.rect(gd,black,[350,350,50,50])
                Message(50,'1',360,350)
                pygame.display.update()
                time.sleep(1)
                Game_loop_hard()
            elif click==(1,0,0) and mess_b=='RANK':
                leader_board()
            elif click==(1,0,0) and mess_b=='BACK':
                game_intro()
            elif click==(1,0,0) and mess_b=='QUIT':
                pygame.quit()
                INTRO()
    #car crash
    def car_crash(x,x_r,y,y_r):
        if x_r<x<x_r+75 and y_r<y<y_r+85 or x_r<x+75<x_r+75 and y_r<y<y_r+85:
            Message(50,"CRASHED!",200,200)
            pygame.display.update()
            time.sleep(1)
            game_intro()
            for event in pygame.event.get():
                if event.type==ptgame.QUIT:
                    pygame.quit()
    # score
    def score_easy(count):
        font=pygame.font.SysFont(None,30)
        screen_text=font.render('score:'+str(count),True,white)
        gd.blit(screen_text,(0,20))
        screen_text1=font.render('high_score:'+str(h_score_e),True,white)
        gd.blit(screen_text1,(0,0))
        c.execute('update main_game set easy_car_high_score='+str(h_score_e)+' where user_name='+'"'+Uname+'"')
        mydb.commit()
    def score_hard(count1):
        font=pygame.font.SysFont(None,30)
        screen_text=font.render('score:'+str(count1),True,white)
        gd.blit(screen_text,(0,20))
        screen_text1=font.render('high_score:'+str(h_score_h),True,white)
        gd.blit(screen_text1,(0,0))
        c.execute('update main_game set hard_car_high_score='+str(h_score_h)+' where user_name='+'"'+Uname+'"')
        mydb.commit()
    #intro
    def game_intro():
        intro=False
        while intro==False:
            gd.blit(background,(0,0))
            button(100,300,'EASY')
            button(600,300,'HARD')
            button(100,400,'QUIT')
            button(600,400,'RANK')
            Message(25,'EASY_HIGH_SCORE:'+str(h_score_e),0,0)
            Message(25,'HARD_HIGH_SCORE:'+str(h_score_h),0,20)
            pygame.display.update()
            try:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()
            except:
                pass
            
    # gameloop/mainloop
    def Game_loop_easy():
        global h_score_e
        x=300
        count=0
        x_r=random.randrange(100,600)
        y_r=0
        y=490
        
        x_change=0
        
        game_over=False
        while game_over==False:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    game_over=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                        x_change=+10
                    elif event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                        x_change=-10
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT or event.key==pygame.K_d or event.key==pygame.K_a:
                        x_change=0
            gd.fill(gray)
            car(x,y)
            score_easy(count)
            if h_score_e<count:
                    h_score_e=count
                    
            enmy_car(x_r,y_r)
            y_r+=15
            if y_r==600:
                y_r=0
                x_r=random.randrange(100,600)
                count+=10
            car_crash(x,x_r,y,y_r)
            x=x-x_change
            clock.tick(40)
            pygame.display.update()
    def Game_loop_hard():
        global h_score_h
        x=300
        count1=0
        x_r=random.randrange(100,600)
        y_r=0
        y=490
        x_change=0
        game_over=False
        while game_over==False:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    game_over=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                        x_change=+10
                    elif event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                        x_change=-10
            gd.fill(gray)
            car(x,y)
            score_hard(count1)
            enmy_car(x_r,y_r)
            y_r+=15
            if y_r==600:
                y_r=0
                x_r=random.randrange(100,600)
                count1+=10
                if h_score_h<count1:
                    h_score_h=count1
            car_crash(x,x_r,y,y_r)
            x=x-x_change
            clock.tick(40)
            pygame.display.update()
    game_intro()
    pygame.display.update()
    pygame.quit()
    quit()
############################################################
############################################################
#snake game
def snake_game():
    c=mydb.cursor()
    c.execute('select snake_high_score from main_game where user_name='+'"'+Uname+'"')
    global sc
    sc1=c.fetchall()
    if sc1[0][0]==None:
        c.execute('update main_game set snake_high_score=0 where user_name='+'"'+Uname+'"')
        mydb.commit()
        c.execute('select snake_high_score from main_game where user_name='+'"'+Uname+'"')
        sc1=c.fetchall()
    global high_score,snakelength
    Intro.destroy()
    pygame.init()
    clock=pygame.time.Clock()
    #display surface
    gd=pygame.display.set_mode((600,600))
    white=(255,255,255)
    black=(0,0,0)
    red=(255,0,0)
    green=(0,255,0)
    light_green=(0,200,0)
    gray=(119,118,110) 
    blue=(0,0,255)
    high_score=sc1[0][0]
    #image
    background=pygame.image.load('background2.png')
    background=pygame.transform.scale(background,(600,600))
    #message\text
    def Message(size,mess,x_po,y_po):
        font=pygame.font.SysFont(None,size)
        render=font.render(mess,True,white)
        gd.blit(render,(x_po,y_po))
    def button(x_button,y_button,mess_b):
        pygame.draw.rect(gd,(255,0,0),[x_button,y_button,100,30])
        Message(50,mess_b,x_button,y_button)
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        if x_button<mouse[0]<x_button+100 and y_button<mouse[1]<y_button+30:
            pygame.draw.rect(gd,(200,0,0),[x_button,y_button,100,30])
            Message(50,mess_b,x_button,y_button)
            if click==(1,0,0) and mess_b=='PLAY':
                game_loop()
            if click==(1,0,0) and mess_b=='RANK':
                leader_board()
            if click==(1,0,0) and mess_b=='BACK':
                snake_intro()
            elif click==(1,0,0) and mess_b=='QUIT':
                pygame.quit()
                INTRO()
    def leader_board():
        c.execute('select user_name,snake_high_score from main_game order by snake_high_score desc')
        lb1=c.fetchall()
        while True:
            gd.fill(black)
            Message(50,"RANKING",250,0)
            for i in range(1,21):
                try:
                    Message(30,str(lb1[i-1][0]),50,i*27)
                    Message(30,str(lb1[i-1][1]),500,i*27)
                    button(0,0,'BACK')
                except:
                    pass
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.update()
                
            
    def head(snakehead):
        global head2,body
        body=[]
        for x,y in snakehead:
            head2=pygame.Rect(x,y,10,10)
            pygame.draw.rect(gd,(0,255,0),head2)
            body.append(head2)
        body.pop(-1)


    def snake_intro():
        intro=False
        while intro==False:
            gd.blit(background,(0,0))
            Message(50,"HIGH SCORE: "+str(high_score),0,0)
            button(100,300,'PLAY')
            button(400,300,'RANK')
            button(250,300,'QUIT')
            pygame.display.update()
            try:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()
            except:
                pass
            
    def out(x_pos,y_pos):

        if x_pos>590 or x_pos<0 or y_pos>590 or y_pos<0:
            Message(100,"GAME OVER",100,200)
            pygame.display.update()
            clock.tick(1)
            snake_intro()
    def self():
        for i in body:
            if snakelength>1:
                if head2.colliderect(i):
                    Message(100,"GAME OVER",100,200)
                    pygame.display.update()
                    clock.tick(1)
                    snake_intro()
    def food(xr,yr):
        global food1
        food1=pygame.Rect(xr,yr,10,10)
        pygame.draw.ellipse(gd,red,food1)
    def game_loop():
        global snakelength,high_score,snakehead
        speed=15.00
        snakelength=1
        snakehead=[]
        count3=0
        x_pos=300
        y_pos=300
        x_change=0
        y_change=0
        xr=500
        yr=300
        game_over=False
        while game_over==False:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    game_over=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT and x_change!=-10 or event.key==pygame.K_a and x_change!=-10:
                        x_change=+10
                        y_change=0
                    elif event.key==pygame.K_RIGHT and x_change!=+10 or event.key==pygame.K_d and x_change!=+10:
                        x_change=-10
                        y_change=0
                    if event.key==pygame.K_DOWN and y_change!=+10 or event.key==pygame.K_s and y_change!=+10:
                        y_change=-10
                        x_change=0
                    elif event.key==pygame.K_UP and y_change!=-10 or event.key==pygame.K_w and y_change!=-10:
                        y_change=+10
                        x_change=0


            gd.fill(black)
            Message(20,'SCORE : '+str(count3),0,0)
            
            head1=[]
            head1.append(x_pos)
            head1.append(y_pos)
            snakehead.append(head1)
            head(snakehead)
            food(xr,yr)
            self()
            if head2.colliderect(food1):
                count3+=10
                speed+=0.3
                snakelength+=1
                xr=random.randint(0,59)*10
                yr=random.randint(0,59)*10
            if high_score<count3:
                high_score=count3
                c.execute('update main_game set snake_high_score='+str(high_score)+' where user_name='+'"'+Uname+'"')
                mydb.commit()
            if len(snakehead)>=snakelength:
                snakehead.pop(0)
            out(x_pos,y_pos)
            x_pos=x_pos-x_change
            y_pos=y_pos-y_change
            clock.tick(speed)
            pygame.display.update()
    snake_intro()

############################################################
    
log()

