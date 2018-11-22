import tkinter
#导入线程模块
import threading
import time
import random

root = tkinter.Tk()
root.title('大转盘')
root.minsize(300,300)

#摆放按钮
btn1 = tkinter.Button(root,text = '樱桃',bg = 'red')
btn1.place(x = 20,y = 20,width = 50,height = 50)

btn2 = tkinter.Button(root,text = '香蕉',bg = 'white')
btn2.place(x = 90,y = 20,width = 50,height = 50)

btn3 = tkinter.Button(root,text = '苹果',bg = 'white')
btn3.place(x = 160,y = 20,width = 50,height = 50)

btn4 = tkinter.Button(root,text = '西瓜',bg = 'white')
btn4.place(x = 230,y = 20,width = 50,height = 50)

btn5 = tkinter.Button(root,text = '鸭梨',bg = 'white')
btn5.place(x = 230,y = 90,width = 50,height = 50)

btn6 = tkinter.Button(root,text = '榴莲',bg = 'white')
btn6.place(x = 230,y = 160,width = 50,height = 50)

btn7 = tkinter.Button(root,text = '柚子',bg = 'white')
btn7.place(x = 230,y = 230,width = 50,height = 50)

btn8 = tkinter.Button(root,text = '葡萄',bg = 'white')
btn8.place(x = 160,y = 230,width = 50,height = 50)

btn9 = tkinter.Button(root,text = '草莓',bg = 'white')
btn9.place(x = 90,y = 230,width = 50,height = 50)

btn10 = tkinter.Button(root,text = '芒果',bg = 'white')
btn10.place(x = 20,y = 230,width = 50,height = 50)

btn11 = tkinter.Button(root,text = '荔枝',bg = 'white')
btn11.place(x = 20,y = 160,width = 50,height = 50)

btn12 = tkinter.Button(root,text = '甘蔗',bg = 'white')
btn12.place(x = 20,y = 90,width = 50,height = 50)

#将所有选项组成列表
fruitlists = [btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8,btn9,btn10,btn11,btn12]

#是否开启循环的标志
isloop = False
#是否停止标志
stopsign=False    #是否接收到 stop信号
#存储停止id------用于进行stop后的重新启动
stopid=None
def rounder():
    global isloop
    global stopid
    #判断是否开始循环
    if isloop == True:
        return
    i=1
    time_sleep = 0.02
    if isinstance(stopid,int):
        i=stopid
    while True:
        time_sleep *= random.randint(1001, 1020)/1000
        round(time_sleep, 8)
        if time_sleep > 0.08:
            time_sleep += 0.001
        print(time_sleep)
        time.sleep(time_sleep)
        for x in fruitlists:
            if time_sleep > 0.08:
                time_sleep += 0.001
            else:
                time_sleep += 0.00001
            x['bg'] = 'white'
        fruitlists[i]['bg'] = 'red'
        i += 1
        if i >= len(fruitlists):
            i = 0
        if stopsign == True or time_sleep > 0.3:
            isloop=False
            stopid =i
            break

def stop1():
    global stopsign

    if stopsign ==True:#当多接收stop1（）函数时 ，直接跳过
        return
    stopsign=True
#建立一个新线程的函数
def newtask():
    global isloop
    global stopsign
    #建立线程
    stopsign=False
    #print(stopsign)  #打印 点击开始时的stopsign
    t = threading.Thread(target = rounder)
    #开启线程运行
    t.start()
    # 设置循环开始标志
    isloop = True

btn_start = tkinter.Button(root,text = 'start',command = newtask)
btn_start.place(x = 90,y = 125,width = 50,height = 50)

btn_stop = tkinter.Button(root,text = 'stop',command=stop1)
btn_stop.place(x = 160,y = 125,width = 50,height = 50)

root.mainloop()