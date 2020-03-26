#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import requests
import MySQLdb
import linecache
import random,os
import webbrowser
from operator import itemgetter
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
import colfilalgo

def on_click():
    keywords='通信' ### 查询的主题 
    keywords=entry.get()
    n=0
    num=150 #n为搜索的文献数，num为参考文献字符串长度
    impact=0.8#影响因子
    score=10#总分为10构建打分矩阵
    target='http://search.cnki.net/search.aspx?q='+str(keywords)+'&rank=relevant&cluster=all&val=CJFDTOTAL&p={}'#知网检索
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    headers = {'User-Agent':user_agent}
    myfile=open('sourcedata.txt','w',encoding='utf-8')
    outfile=open('resultdata.txt','w',encoding='utf-8')
    for i in range(10):
        i=i*15
        target=target.format(i)
        req=requests.get(url=target)
        html=req.text
        html=html.replace('<br>',' ').replace('<br/>',' ').replace('/>','>')
        bf=BeautifulSoup(html,"html.parser")
        texts=bf.find('div',class_='articles')
        texts_div=texts.find_all('div',class_='wz_content')
        for item in texts_div:
            item_name=item.find('a').text
            item_href=item.find('a')['href']
            req2=requests.get(url=item_href)
            html2=req2.text
            html2=html2.replace('<br>',' ').replace('<br/>',' ').replace('/>','>')
            bf2=BeautifulSoup(html2,"html.parser")
            text2=bf2.find('div',class_='node_item')
            item_refer=item.find_all('td',style_='line-height:1.8em')
            c=''
            for j in item_refer:
                item_min=j.find('a').text
                if item_min==item_name:
                    c+='1'
                else:
                    c+='0'
            xnum=random.randint(1,num/5)
            a = [0 for x in range(num-xnum)]+[1 for x in range(xnum)]
            random.shuffle(a)
            for j in range(len(a)):
                if j==n:
                    c+='0'
                    continue
                if a[j]==1:c+='1'
                if a[j]==0:c+='0'
            item_refer2=item.find('span',class_='count').text
            num1=item_refer2[item_refer2.find('（')+1:item_refer2.find('）')]
            if num1=='':num1='0'
            num2=item_refer2[item_refer2.rfind('（')+1:item_refer2.rfind('）')]
            if num2=='':num2='0'
            print('{} {} {}\n'.format(item_name,item_href,item_refer2))
            myfile.write(str(n)+' '+item_name+' '+num1+' '+num2+' '+ c + ' ' + item_href + '\n')
            n+=1
    myfile.close()
    content=linecache.getlines('sourcedata.txt')
    listt=[["","","","","","",""]for i in range(n)]
    colfilalgo.cff=str(listt)
    for i in range(n):
        string=content[i]
        a1=string.find(' ')#序号
        listt[i][0]=string[:a1]
        string=string[a1+1:]
        a2=string.find(' ')#名字
        listt[i][1]=string[:a2]
        string=string[a2+1:]
        a3=string.find(' ')#总下载次数
        listt[i][2]=int(string[:a3])
        string=string[a3+1:]
        a4=string.find(' ')#总引用次数
        listt[i][3]=int(string[:a4])
        string=string[a4+1:]
        a5=string.find(' ')#参考文献字符串
        listt[i][4]=string[:a5]
        listt[i][5]=string[a5+1:]#href地址
        listt[i][6]=score-float(1/(0.2*(listt[i][2]+1))+1/((impact-0.2)*(listt[i][3]+1)))#可控制下载矩阵和引用矩阵的影响因子
    content2=sorted(listt,key=(lambda x:x[6]),reverse=True)
    #print(content2)
    outfile.write(str(content2))
    outfile.close()
    message['text']='论文推荐：\n'
    global var,label12,label22,label32,label42,label52,label62,label72,label82,label92,label102
    var=StringVar()
    r1 = Radiobutton(root, text='1.', variable=var, value='1').place(x=30,y=80)
    label11 = Label(root,text=content2[0][1]).place(x=80,y=82)
    label12 = Label(root,text=content2[0][5])
    r2 = Radiobutton(root, text='2.', variable=var, value='2').place(x=30,y=100)
    label21 = Label(root,text=content2[1][1]).place(x=80,y=101)
    label22 = Label(root,text=content2[1][5])
    r3 = Radiobutton(root, text='3.', variable=var, value='3').place(x=30,y=120)
    label31 = Label(root,text=content2[2][1]).place(x=80,y=121)
    label32 = Label(root,text=content2[2][5])
    r4 = Radiobutton(root, text='4.', variable=var, value='4').place(x=30,y=140)
    label41 = Label(root,text=content2[3][1]).place(x=80,y=141)
    label42 = Label(root,text=content2[3][5])
    r5 = Radiobutton(root, text='5.', variable=var, value='5').place(x=30,y=160)
    label51 = Label(root,text=content2[4][1]).place(x=80,y=161)
    label52 = Label(root,text=content2[4][5])
    r6 = Radiobutton(root, text='6.', variable=var, value='6').place(x=30,y=180)
    label61 = Label(root,text=content2[5][1]).place(x=80,y=181)
    label62 = Label(root,text=content2[5][5])
    r7 = Radiobutton(root, text='7.', variable=var, value='7').place(x=30,y=200)
    label71 = Label(root,text=content2[6][1]).place(x=80,y=201)
    label72 = Label(root,text=content2[6][5])
    r8 = Radiobutton(root, text='8.', variable=var, value='8').place(x=30,y=220)
    label81 = Label(root,text=content2[7][1]).place(x=80,y=221)
    label82 = Label(root,text=content2[7][5])
    r9 = Radiobutton(root, text='9.', variable=var, value='9').place(x=30,y=240)
    label91 = Label(root,text=content2[8][1]).place(x=80,y=241)
    label92 = Label(root,text=content2[8][5])
    r10 = Radiobutton(root, text='10.', variable=var, value='10').place(x=30,y=260)
    label101 = Label(root,text=content2[9][1]).place(x=80,y=261)
    label102 = Label(root,text=content2[9][5])
    button2 = Button(root,text='查看原文地址',command=do_job7).place(x=360,y=280)
   

    #os.system("mysql.py")
    print("论文总数为：%d"%n)

def do_job1():
    #message['text'] = '1'
    os.system('sourcedata.txt')

def do_job2():
    #message['text'] = '2'
    os.system('resultdata.txt')

def do_job3():
    #message['text'] = '3'
    os.system('colfilalgo.py')

def do_job4():
    #message['text'] = '4'
    messagebox.showinfo(title='功能说明',message='1.该系统采用协同过滤算法处理数据集\n2.该系统可查看存储和评分源文件\n3.该系统可通过推荐论文直达页面')

def do_job5():
    #message['text'] = '5'
    messagebox.showinfo(title='数据集来源',message='数据集来源：中国知网\n通过默认浏览器打开该网页')
    webbrowser.open('http://search.cnki.net/Search.aspx?q=%E9%80%9A%E4%BF%A1')

def do_job6():
    #message['text'] = '6'
    messagebox.showinfo(title='版本说明',message='当前版本号:v3.1.2\n最后更新时间2019.5.27')

def do_job7():
    global var,label12
    urlm=''
    if var.get()=='1':urlm=label12['text']
    if var.get()=='2':urlm=label22['text']
    if var.get()=='3':urlm=label32['text']
    if var.get()=='4':urlm=label42['text']
    if var.get()=='5':urlm=label52['text']
    if var.get()=='6':urlm=label62['text']
    if var.get()=='7':urlm=label72['text']
    if var.get()=='8':urlm=label82['text']
    if var.get()=='9':urlm=label92['text']
    if var.get()=='10':urlm=label102['text']
    webbrowser.open(urlm)
    print(var.get())

if __name__=="__main__":
    root=Tk(className='论文推荐系统')
    root.geometry('800x400') 
    root.iconbitmap('推.ico')
    menu1=Menu(root)
    filemenu=Menu(menu1,tearoff=0)
    filemenu2=Menu(menu1,tearoff=0)
    menu1.add_cascade(label='→功能集合←',menu=filemenu)
    filemenu.add_command(label='存储数据源文件[r]', command=do_job1)
    filemenu.add_command(label='评分数据源文件[s]', command=do_job2)
    filemenu.add_command(label='协同过滤算法[c]', command=do_job3)
    filemenu.add_separator()    # 添加一条分隔线
    filemenu.add_command(label='退出程序[e]', command=root.quit) # 用tkinter里面自带的quit()函数
    menu1.add_cascade(label='→帮助←',menu=filemenu2)
    filemenu2.add_command(label='功能说明[m]', command=do_job4)
    filemenu2.add_command(label='数据集来源[n]', command=do_job5)
    filemenu2.add_separator()    # 添加一条分隔线
    filemenu2.add_command(label='版本[h]', command=do_job6) 
    root.config(menu=menu1)
    label=Label(root,text='请输入论文主题：',bg='orange')
    label.pack()
    message = Message(root,text='')
    message.place(x=60,y=60)
    entry=Entry(root)
    entry.pack()
    button = Button(root,text='查询',command=on_click)
    button.pack()
    mainloop()