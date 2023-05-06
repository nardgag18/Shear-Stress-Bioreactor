from tkinter import *
import tkinter as tk
import tkinter.messagebox as messagebox
# from tkinter.ttk import *
from ttkbootstrap import Style
import time
import threading
import traceback
from PIL import Image, ImageTk
from tkinter import filedialog
import csv
from readFile import checkFile


class gui():
    def __init__(self, root):
        self.hours = IntVar()
        self.minutes = IntVar()
        self.seconds = IntVar()
        self.stress = IntVar()
        self.c_hours = IntVar()
        self.c_minutes = IntVar()
        self.c_seconds = IntVar()
        self.flag = 1
        self.f = 1
        self.outOfTime = False
        self.advanced = False
        self.sysPrimed = False

        self.advanced_fileLength = IntVar()
        self.advanced_flowRateList = []
        self.advaced_shearStressList = []
        self.advanced_stressTimingList = []
        self.p1 = Image.open('1.png')
        self.p2 = Image.open('2.png')
        
        self.p_image1 = self.p1.resize((50, 50))
        self.p_image2 = self.p2.resize((50, 50))
        
        self.img1 = ImageTk.PhotoImage(self.p_image1)
        self.img2 = ImageTk.PhotoImage(self.p_image2)    

        self.ui_prime()
        self.ui1(root)


    def togglePump(self):
        if self.b2['text'] == "Turn pump off":
            print("Turn pump on")
            try:
                self.b2['text'] = "Turn pump on"
            except (Exception, BaseException) as e:
                exstr = traceback.format_exc()
                print(exstr)
        else:
            print("Turn pump off")
            try:
                self.b2['text'] = "Turn pump off"
            except (Exception, BaseException) as e:
                exstr = traceback.format_exc()
                print(exstr)

    def ui1(self, root):
        basic = Toplevel()
        basic.title('Basic Shear Stress')
        basic.geometry('551x325')

        if self.advanced == True:
            for options in self.advanced_flowRateList :
                inp = options.split(',')
                self.advaced_shearStressList.append(float(inp[0].strip()))
                stress = inp[0].strip()
                time = inp[1].strip()
                time = time.split(":")
                self.advanced_stressTimingList.append(time)
                print("{}, {}".format(stress, time))

            self.entry_boxes = []
            count = 0
            for i in range(0, self.advanced_fileLength):
                stress = StringVar()
                time = StringVar()
                op = StringVar()
                #line.set(self.advanced_flowRateList[count])

                stress.set(self.advaced_shearStressList[count])
                time.set(self.advanced_stressTimingList[count])

                op.set(self.advanced_flowRateList[count])  
                
                entry_box = tk.Label(basic, textvariable=str(op), font=('Times New Roman', 22)).pack()
                self.entry_boxes.append(entry_box)
                count += 1

        else:
        
            self.l1 = Label(basic, text='Time :', font=('Times New Roman', 22))
            self.h = Entry(basic, textvariable=self.hours, font=("Times New Roman", 11))
            self.h.configure(relief="groove")
            self.l2 = Label(basic, text='hours', font=("Times New Roman", 12, 'italic'), anchor='w')
            self.m = Entry(basic, textvariable=self.minutes, font=("Times New Roman", 11))
            self.m.configure(relief="groove")
            self.l3 = Label(basic, text='minutes', font=("Times New Roman", 12, 'italic'), anchor='w')
            self.s = Entry(basic, textvariable=self.seconds, font=("Times New Roman", 11))
            self.s.configure(relief="groove")
            self.l4 = Label(basic, text='seconds', font=("Times New Roman", 12, 'italic'), anchor='w')
            self.l5 = Label(basic, text='Shear Stress :', font=('Times New Roman', 20))
            self.str = Entry(basic, textvariable=self.stress, font=("Times New Roman", 12))
            self.str.configure(relief="groove")
            self.l6 = Label(basic, text='mPa', font=('Times New Roman', 20, 'italic'))
            self.bt1 = Button(basic, text='Start', font=("Times New Roman", 16, 'italic'), fg='black', command=self.time_confirm)
            self.bt2 = Button(basic, text='Advanced', font=("Times New Roman", 10, 'italic'), command=lambda: self.file_read(basic))
            self.bt3 = Button(basic, text='-', command=self.down_h, font=('Times New Roman', 20))
            self.bt4 = Button(basic, text='+', command=self.up_h, font=('Times New Roman', 20))
            self.bt5 = Button(basic, text='-', command=self.down_m, font=('Times New Roman', 20))
            self.bt6 = Button(basic, text='+', command=self.up_m, font=('Times New Roman', 20))
            self.bt7 = Button(basic, text='-', command=self.down_s, font=('Times New Roman', 20))
            self.bt8 = Button(basic, text='+', command=self.up_s, font=('Times New Roman', 20))
            self.l1.place(x=33, y=48, width=79, height=35)
            self.h.place(x=139, y=48, width=30, height=35)
            self.l2.place(x=177, y=48, width=76, height=35)
            self.m.place(x=263, y=48, width=30, height=35)
            self.l3.place(x=302, y=47, width=77, height=36)
            self.s.place(x=391, y=48, width=30, height=35)
            self.l4.place(x=432, y=47, width=77, height=36)
            self.l5.place(x=33, y=178, width=197, height=36)
            self.str.place(x=238, y=178, width=107, height=36)
            self.l6.place(x=355, y=176, width=36, height=38)
            self.bt1.place(x=217, y=251, width=115, height=35)
            self.bt2.place(x=432, y=258, width=100, height=28)
            self.bt3.place(x=138, y=88, width=28, height=28)
            self.bt4.place(x=138, y=12, width=28, height=28)
            self.bt5.place(x=264, y=88, width=28, height=28)
            self.bt6.place(x=264, y=12, width=28, height=28)
            self.bt7.place(x=391, y=88, width=28, height=28)
            self.bt8.place(x=391, y=12, width=28, height=28)

            pass        
    
    def ui2(self):
        win = Toplevel()
        win.title('Time Remaining')
        win.geometry('551x325')

        def ui_destroy():
            self.f = 0
            win.destroy()

        self.lable1 = Label(win, text='Time Remaining', font=('Times New Roman', 18))
        self.lable2 = Label(win, textvariable=self.c_hours, font=("Times New Roman", 11))
        self.lable2.configure(relief="groove")
        self.lable3 = Label(win, text='hours', font=("Times New Roman", 12, 'italic'), anchor='w')
        self.lable4 = Label(win, textvariable=self.c_minutes, font=("Times New Roman", 11))
        self.lable4.configure(relief="groove")
        self.lable5 = Label(win, text='minutes', font=("Times New Roman", 12, 'italic'), anchor='w')
        self.lable6 = Label(win, textvariable=self.c_seconds, font=("Times New Roman", 11))
        self.lable6.configure(relief="groove")
        self.lable7 = Label(win, text='seconds', font=("Times New Roman", 12, 'italic'), anchor='w')
        self.lable8 = Label(win, text='Time selected', font=('Times New Roman', 18))
        self.lable9 = Label(win, textvariable=self.hours, font=("Times New Roman", 11))
        self.lable9.configure(relief="groove")
        self.lable10 = Label(win, text='hours', font=("Times New Roman", 12, 'italic'), anchor='w')
        self.lable11 = Label(win, textvariable=self.minutes, font=("Times New Roman", 11))
        self.lable11.configure(relief="groove")
        self.lable12 = Label(win, text='minutes', font=("Times New Roman", 12, 'italic'), anchor='w')
        self.lable13 = Label(win, textvariable=self.seconds, font=("Times New Roman", 11))
        self.lable13.configure(relief="groove")
        self.lable14 = Label(win, text='seconds', font=("Times New Roman", 12, 'italic'), anchor='w')
        
        self.b1 = Button(win, text='Pause', image=self.img2, font=("Times New Roman", 16), command=self.p_r)
        self.b2 = Button(win, text='Stop', font=("Times New Roman", 22, 'italic'), command=ui_destroy)
        
        self.lable1.place(x=26, y=17, width=125, height=37)
        self.lable2.place(x=166, y=17, width=30, height=37)
        self.lable3.place(x=202, y=17, width=67, height=37)
        self.lable4.place(x=166, y=68, width=30, height=37)
        self.lable5.place(x=202, y=68, width=67, height=37)
        self.lable6.place(x=166, y=120, width=30, height=37)
        self.lable7.place(x=202, y=119, width=67, height=38)
        self.lable8.place(x=26, y=173, width=132, height=40)
        self.lable9.place(x=166, y=173, width=30, height=40)
        self.lable10.place(x=202, y=173, width=65, height=40)
        self.lable11.place(x=166, y=226, width=30, height=40)
        self.lable12.place(x=201, y=226, width=66, height=40)
        self.lable13.place(x=166, y=279, width=30, height=40)
        self.lable14.place(x=201, y=279, width=66, height=40)
        self.b1.place(x=450, y=29, width=80, height=90)
        self.b2.place(x=400, y=207, width=139, height=80)
        
        t = threading.Thread(target=self.set_time)
        t.setDaemon(True)
        t.start()
        win.protocol('WM_DELETE_WINDOW', ui_destroy)
        win.mainloop()

        pass
    
    '''
    def ui3(self):
        win = Toplevel()
        win.title('Prime Pump')
        win.geometry('551x325')
    '''

    def set_time(self):
        if self.sec >= 60:
            self.min += 1
            self.sec -= 60
            if self.min >= 60:
                self.hour += 1
                self.sec -= 60
        self.c_seconds.set(self.sec)
        self.c_minutes.set(self.min)
        self.c_hours.set(self.hour)
        while self.f == 1:
            if self.flag == 1:
                if self.sec > 0:
                    self.sec -= 1
                elif self.sec == 0:
                    if self.min > 0:
                        self.sec = 59
                        self.min -= 1
                    elif self.min == 0:
                        if self.hour == 0:
                            pass
                        else:
                            self.hour -= 1
                            self.min = 59
                            self.sec = 59

                time.sleep(1)
                self.c_seconds.set(self.sec)
                self.c_minutes.set(self.min)
                self.c_hours.set(self.hour)
        self.f = 1

    def time_confirm(self):
        #basicWin.update()
        self.sec = int(self.s.get())
        self.min = int(self.m.get())
        self.hour = int(self.h.get())

        if int(self.s.get()) < 0:
            self.seconds.set(0)
            messagebox.showwarning('Warning', 'check the second')
        if int(self.m.get()) < 0:
            self.minutes.set(0)
            messagebox.showwarning('Warning', 'check the minute')
        if int(self.h.get()) < 0:
            self.hours.set(0)
            messagebox.showwarning('Warning', 'check the hour')
        if self.sec != 0 or self.min != 0 or self.hour != 0:
            self.ui2()

    def up_s(self):
        if int(self.s.get()) < 59:
            self.seconds.set(int(self.s.get()) + 1)
        while int(self.s.get()) >= 59:
            self.seconds.set(int(self.s.get()) - 60)
            self.minutes.set(int(self.m.get()) + 1)

    def down_s(self):
        if int(self.s.get()) > 0:
            self.seconds.set(int(self.s.get()) - 1)

    def up_m(self):
        if int(self.m.get()) < 59:
            self.minutes.set(int(self.m.get()) + 1)
        while int(self.m.get()) >= 59:
            self.minutes.set(int(self.m.get()) - 60)
            self.hours.set(int(self.h.get()) + 1)

    def down_m(self):
        if int(self.m.get()) > 0:
            self.minutes.set(int(self.m.get()) - 1)

    def up_h(self):
        self.hours.set(int(self.h.get()) + 1)

    def down_h(self):
        if int(self.h.get()) > 0:
            self.hours.set(int(self.h.get()) - 1)

    def p_r(self):
        if self.b1['text'] == 'Pause':
            try:
                self.flag = 0
                self.b1['text'] = 'Resume'
                self.b1['image'] = self.img1
            except (Exception, BaseException) as e:
                exstr = traceback.format_exc()
                print(exstr)
        else:
            try:
                self.flag = 1
                self.b1['text'] = 'Pause'
                self.b1['image'] = self.img2
            except (Exception, BaseException) as e:
                exstr = traceback.format_exc()
                print(exstr)

    def Stop(self):
        self.flag = 0

    def file_read(self, basicWin):
        basicWin.destroy()
        #self.ui1(basicWin)
        win_r = Toplevel()
        e_r = StringVar()
        win_r.title('File Explorer')
        win_r.geometry('433x573')
        text = Text(win_r,font=('Asia',10))
        frame=Frame(win_r)
        scroy=Scrollbar(frame)
        self.advanced = True
        
        def f_c():
            file = filedialog.askopenfilename(title='Select a File', filetypes=(('Text files', '*.txt'), ('csv files', '*.csv'), ('all files', '*.*')))
            e_r.set(file)
            text.delete('1.0','end')
            print(file)

            if file[-3:] == 'csv':
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        datas = csv.reader(f)
                        for d in datas:
                            line = '  '.join(d)
                            #print(line)
                            text.insert('end',line+'\n')
                except:
                    with open(file, 'r', encoding='gbk') as f:
                        datas = csv.reader(f)
                        for d in datas:
                            line = '  '.join(d)
                            #print(line)
                            text.insert('end', line+'\n')
            elif file[-3:] == 'txt':
                f = open(file,'r')
                lines = f.readlines()
                fileLength = 0
                count = 0

                for line in lines:
                    fileLength += 1
                
                self.advanced_fileLength = fileLength

                #print("total lines: {}".format(self.advanced_fileLength))
                
                for line in lines :
                    count += 1
                    line = line.strip()

                    self.advanced_flowRateList.append(line)
                    
                    text.insert('end', line+'\n')
                    #print(line)



            elif file != '':
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        datas = f.read()
                        #print(datas)
                        text.insert('0.0', datas)
                except:
                    with open(file, 'r', encoding='gbk') as f:
                        datas = f.read()
                        #print(datas)
                        text.insert('0.0', datas)
            else:
                pass
            
        def quit_(basicWin):
            #basicWin.destroy()
            self.ui1(basicWin)
            win_r.destroy()

        et = Entry(win_r, textvariable=e_r)
        b_c = Button(win_r, text='...', command=f_c)
        b_e = Button(win_r, text='Start',command=lambda: quit_(basicWin))  # ,font=('Times New Roman',16))
        et.place(x=77, y=48, width=279, height=26)
        b_c.place(x=356, y=48, width=35, height=26)
        b_e.place(x=170, y=104, width=100, height=28)
        text.configure(relief = "solid")
        text.place(x = 77,y = 159,width = 279,height = 389)
        frame.place(x = 356,y = 159,width = 22,height = 384)
        scroy.pack(side=RIGHT, fill=Y)
        scroy.config(command=text.yview)
        text.config(yscrollcommand=scroy.set)
        win_r.mainloop()
    
    def ui_prime(self):
        if self.sysPrimed != True :
            primed = Toplevel()
            primed.title('Prime System')
            primed.geometry('551x325')

            def ui_destroy():
                primed.destroy()
            
            def system_primed():
                self.sysPrimed = True
                ui_destroy()
            
            self.b1 = Button(primed, text="Press when pump is primed", font=("Times New Roman", 16), command=system_primed)
            self.b1.pack()

            self.b2 = Button(primed, text="Turn pump on", font=("Times New Roman", 16), command=self.togglePump)
            self.b2.pack()

def loading():
    root = Tk()
    root.title('Blank Screen')
    root.geometry('551x315')
    root.iconbitmap('1.ico')
    gui(root)
    root.mainloop()

if __name__ == '__main__':
    loading()