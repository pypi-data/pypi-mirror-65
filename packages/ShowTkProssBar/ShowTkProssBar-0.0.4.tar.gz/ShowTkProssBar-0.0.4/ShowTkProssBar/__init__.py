
import tkinter
from tkinter import *
from tkinter import messagebox    #弹窗库
import time



'''===============================
这个类，显示在tkinter 中的一个进度条；
=================================='''
 
class ShowTkProssBar(): 
    def __init__(self, root,wd=400,hd=100,posx=80,posy=60,barwd = 20,step=1):
        self.i = 0
        self.step = step 
        self.wd = wd
        self.hd = hd
        self.posx = posx
        self.posy = posy
        self.barwd = barwd
        self.top = Toplevel(root)
        self.var_text = StringVar()
        self.initGUI(root)
 
    def loop(self):       
        self.i += self.step
        if 10*self.i <= self.wd - 20:
            self.rec = self.cv.create_rectangle(0,0,10*self.i,20,fill= 'blue')
            jd = 10*self.i/(self.wd -20)*100
            self.var_text.set('已完成:%.2f%%'%jd)
            self.top.after(500, self.loop)
        else:                      
            time.sleep(1)
            self.top.destroy()                        
            messagebox.showinfo(title='提示', message='任务完成！')     
 
    def initGUI(self, root): 
        #self.root = root
        self.top.title("任务进行中...")
        self.top.geometry("%dx%d+%d+%d"%(self.wd,self.hd,self.posx,self.posy))  
        
        self.top.resizable = False
        Label(self.top).pack()

        self.lb = Label(self.top,textvariable = self.var_text)
        self.var_text.set('进度显示')
        self.lb.pack( anchor ='w')
        self.cv = Canvas(self.top,width = self.wd - 20,height = self.barwd ,bg = 'white')
        self.cv.pack( anchor ='w')
        
        self.top.after(500, self.loop)
        #self.rec = self.cv.create_rectangle(0,0,0,20,fill= 'blue')
        #root.withdraw()
        self.top.update()

 
'''==========================
# 调用方法：
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    #top = Toplevel(root)
    SB = ShowTkProssBar(root,600,100,50,50,10,1)
    #root.withdraw()
    root.deiconify()
    #root.update()
    root.mainloop()
==============================''' 
