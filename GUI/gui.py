from tkinter import *
import tkinter as tk
import tkinter.messagebox as messagebox
#from ttkbootstrap import Style
import time
import threading
import traceback
from PIL import Image, ImageTk
from tkinter import filedialog
import csv
import serial
import calc

class gui():
    def __init__(self):
        # start serial connection
        
        # '/dev/cu.usbserial-028603D9'
        # '/dev/ttyACM0'
        self.arduino = serial.Serial('/dev/cu.usbserial-01D17AE0', 9600, timeout=1)
        
        time.sleep(2)
        
        self.arduino.write(b"1\r") # connection made

        #r = self.arduino.read().decode()
        #print(r)
        #r = int(r)
        #while r != 1:
        #    r = self.arduino.read().decode()
        #    print(r)
            #    #r = int(r)
        self.root = Tk()
        self.root.title('Blank Screen')
        self.root.geometry('551x315')
        #self.root.iconbitmap('1.ico')
        self.advancedRunDisp = False
        self.hours = IntVar()
        self.minutes = IntVar()
        self.seconds = IntVar()
        self.stress = DoubleVar()
        self.c_hours = IntVar()
        self.c_minutes = IntVar()
        self.c_seconds = IntVar()
        self.flag = 1
        self.f = 1
        self.outOfTime = False
        self.advanced = False
        self.sysPrimed = False
        self.timeUp = False
        self.advaned_timeup = True
        self.advanced_seconds = IntVar()
        self.advanced_minutes = IntVar()
        self.advanced_hours = IntVar()
        self.advanced_iterator = 0
        self.stop_threads = False
        self.advanced_fileLength = IntVar()
        self.advanced_flowRateList = []
        self.advaced_shearStressList = []
        self.advanced_stressTimingList = []
        self.advancedLoopCount = 0
        self.choice = False
        self.p1 = Image.open('1.png')
        self.p2 = Image.open('2.png')
        
        self.p_image1 = self.p1.resize((50, 50))
        self.p_image2 = self.p2.resize((50, 50))
        
        self.img1 = ImageTk.PhotoImage(self.p_image1)
        self.img2 = ImageTk.PhotoImage(self.p_image2)    

        self.ui_prime()
        
        self.root.mainloop()

    def cleanAdvVar(self):
        self.advanced_flowRateList.clear()
        self.advaced_shearStressList.clear()
        self.advanced_stressTimingList.clear()

    def ui_basicORAdv(self) :
        temp = Toplevel()
        temp.title('Choose test type')
        temp.geometry('551x325')

        def ui_destroy():
            temp.destroy()

        def basicTest() :
            self.advanced = False
            self.choice = True
            ui_destroy()
            self.ui1()

        def advTest() :
            self.advanced = True
            self.choice = True
            ui_destroy()
            self.adv_file_read()

        def primeSys() :
            ui_destroy()
            self.sysPrimed = False
            self.ui_prime()

        bt1 = Button(temp, text='Basic Test', command=basicTest).pack()
        bt2 = Button(temp, text='Advanced Test', command=advTest).pack()
        bt3 = Button(temp, text='Prime System', command=primeSys).pack()

    def togglePump(self):
        if self.b2['text'] == "Turn pump off":
            self.arduino.write(b"1\r")
            print("Turn pump on")
            try:
                self.b2['text'] = "Turn pump on"
            except (Exception, BaseException) as e:
                exstr = traceback.format_exc()
                print(exstr)
        else:
            self.arduino.write(b"0\r")
            print("Turn pump off")
            try:
                self.b2['text'] = "Turn pump off"
            except (Exception, BaseException) as e:
                exstr = traceback.format_exc()
                print(exstr)

    def uiAdvancedRun(self):
        if self.advancedRunDisp == False :
            adv = Toplevel()
            adv.title('Running Advanced Screen')
            adv.geometry('551x325')

            def ui_destroy():
                adv.destroy()

            count = 0
            self.advancedRunDisp = True
            # print the values to the screen
            for i in range(0, len(self.advaced_shearStressList)):
                count += 1
                stress = self.advaced_shearStressList[i]
                time = self.advanced_stressTimingList[i]
                dispStr = StringVar()
                
                line = "(" + str(count) + "): " + str(stress) + " mPa, " + str(time[0]) + " hour(s) " + str(time[1]) + " minute(s) " + str(time[2]) + " second(s)"  
                
                dispStr.set(line)

                entry_box = tk.Label(adv, textvariable=str(dispStr), font=('Times New Roman', 22)).pack()
                self.entry_boxes.append(entry_box)
            
            bt1 = Button(adv, text='Done', command=ui_destroy).pack()

        if self.advanced_iterator != len(self.advaced_shearStressList) :
            self.stress.set(float(self.advaced_shearStressList[self.advanced_iterator]))
            flow = calc.calcFlowRate(float(self.advaced_shearStressList[self.advanced_iterator]))
            msg = ("1, " + str(flow)).encode()
            #print(msg)
            self.arduino.write(msg)

            reply = self.arduino.read().decode()
            while reply != "1" :
                reply = self.arduino.read().decode()
            t = self.advanced_stressTimingList[self.advanced_iterator]
            self.advanced_hours = t[0]
            self.advanced_minutes = t[1]
            self.advanced_seconds = t[2]
            self.advtime_confirm()
        else :
            #adv.destroy()
            self.ui_advDone()
            

    def ui1(self):

        basic = Toplevel()
        basic.title('Basic Shear Stress')
        basic.geometry('551x325')
        #proceed = False
        self.hours.set(0)
        self.minutes.set(0)
        self.seconds.set(0)
        self.stress.set(0.0)
        if self.advanced == True:
            # make buttons to proceed
            basic.title('Advanced Shear Stress')  
            
            def proceedButton():
                # delete the check screen
                basic.destroy()
                # call the advanced running screen
                self.advancedRunDisp == False
                self.advanced_iterator = 0
                self.uiAdvancedRun()
                #print("Proceed")
            
            def goBackButton():
                basic.destroy()
                self.advanced = False
                self.ui1()

            self.bt0 = Button(basic, text="Go Back", font=('Times New Roman', 22), command=goBackButton).pack()
            self.bt1 = Button(basic, text="Proceed", font=('Times New Roman', 22), command=proceedButton).pack()
            # divide the flow rate list into stress and time
            for options in self.advanced_flowRateList :
                # split the line at the comma [shear stress] , [time]
                inp = options.split(',')
                # append the shear stress to the shear stress list as a float var
                self.advaced_shearStressList.append(float(inp[0].strip()))
                stress = inp[0].strip() # assign stress to local var
                time = inp[1].strip() # assign the time to a local var
                time = time.split(":") # split the time by the colon
                # append the time to the stress timing list
                self.advanced_stressTimingList.append(time) 
                #print("{}, {}".format(stress, time))

            self.entry_boxes = []
            count = 0
            
            # print stress and time entries to the screen
            for i in range(0, self.advanced_fileLength):
                count += 1
                stress = self.advaced_shearStressList[i]
                time = self.advanced_stressTimingList[i]
                dispStr = StringVar()
                self.stress.set(stress)
                line = "(" + str(count) + "): " + str(stress) + " mPa, " + str(time[0]) + " hour(s) " + str(time[1]) + " minute(s) " + str(time[2]) + " second(s)"  
                dispStr.set(line)

                entry_box = tk.Label(basic, textvariable=str(dispStr), font=('Times New Roman', 22)).pack()
                self.entry_boxes.append(entry_box)

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
            self.bt1 = Button(basic, text='Start', font=("Times New Roman", 16, 'italic'), fg='black', command=lambda: self.time_confirm(basic))
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
            self.flag = 0
            self.arduino.write(b"9\r")
            reply = self.arduino.read().decode()
            while reply != "9" :
                reply = self.arduino.read().decode()
            win.destroy()
            self.ui_basicORAdv()
        
        self.labelStress = Label(win, text='Shear stress (mPa): ', font=('Times New Roman', 18))
        self.labelstressVar = Label(win, textvariable=self.stress, font=("Times New Roman", 18))
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
        
        self.labelStress.place(x=280, y=17, width=150, height=37)
        self.labelstressVar.place(x=440, y=17, width=60, height=37)
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
        self.b1.place(x=450, y=100, width=80, height=90)
        self.b2.place(x=400, y=207, width=139, height=80)
        
        t = threading.Thread(target =lambda: self.set_time(win))
        t.setDaemon(True)
        t.start()

        #self.tControl(t)
        #win.protocol('WM_DELETE_WINDOW', ui_destroy)
        
        #win.mainloop()    

        #pass
    
    def ui_advDone(self):
        win = Toplevel()
        win.title('Finished screen')
        win.geometry('551x325')

        '''
        def nextTest():
            win.destroy()
            self.ui1()
        '''
        def anotherTest():
            win.destroy()
            self.cleanAdvVar()
            self.ui_basicORAdv()
            
        if self.advanced_iterator < self.advanced_fileLength:
            self.advanced_iterator += 1
            win.destroy()
            self.uiAdvancedRun()
        else :
            bt1 = Button(win, text="Another Test", command=anotherTest).pack()
    
    def ui_done(self):
        win = Toplevel()
        win.title('Finished Screen')
        win.geometry('551x325')
        
        def anotherTest():
            win.destroy()
            self.ui1()
        #stress_str = str(self.stress)

        l1 = Label(win,text="Finished test!").pack()
        bt1 = Button(win, text="Do another Test", command=anotherTest).pack()

    def set_time(self, win):
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
                            self.timeUp = True
                            if self.advanced != True :
                                #self.f = 0
                                self.flag = 0
                                #self.ui2()
                                #self.win.destroy()
                                self.stop_threads = True
                                self.ui_done()

                                # write to arduino to close the system
                                self.arduino.write("1, 0".encode())
                                #print("time up")
                                
                                win.destroy()
                                return
                            else :
                                self.flag = 0
                                self.advaned_timeup = True
                                self.stop_threads = True
                                self.ui_advDone()
                                #print("time done advanced")
                                
                                win.destroy()
                                return
                                #self.win.des
                            #pass
                        else:
                            self.hour -= 1
                            self.min = 59
                            self.sec = 59

                time.sleep(1)
                self.c_seconds.set(self.sec)
                self.c_minutes.set(self.min)
                self.c_hours.set(self.hour)
        self.f = 1

    def advtime_confirm(self):
        self.sec = int(self.advanced_seconds)
        self.min = int(self.advanced_minutes)
        self.hour = int(self.advanced_hours)
        self.seconds.set(int(self.sec))
        self.minutes.set(int(self.min))
        self.hours.set(int(self.hour))

        if self.sec != 0 or self.min != 0 or self.hour != 0:
            self.flag = 1
            self.ui2()

    def time_confirm(self, basic):
        #basicWin.update()
        if self.advanced != True:
            if int(self.s.get()) < 0:
                self.seconds.set(0)
                messagebox.showwarning('Warning', 'check the second')
            if int(self.m.get()) < 0:
                self.minutes.set(0)
                messagebox.showwarning('Warning', 'check the minute')
            if int(self.h.get()) < 0:
                self.hours.set(0)
                messagebox.showwarning('Warning', 'check the hour')
            self.sec = int(self.s.get())
            self.min = int(self.m.get())
            self.hour = int(self.h.get())

        if self.sec != 0 or self.min != 0 or self.hour != 0:
            self.flag = 1
            basic.destroy()
            s = float(self.stress.get())
            flow = calc.calcFlowRate(s)
            #print(flow)
            msg = ("1, " + str(flow)).encode()
            #print(msg)
            self.arduino.write(msg)
            reply = self.arduino.read().decode()
            while reply != "1" :
                reply = self.arduino.read().decode()
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
                msg = ("2, " + str(1)).encode()
                self.arduino.write(msg)
                self.b1['text'] = 'Resume'
                self.b1['image'] = self.img1
            except (Exception, BaseException) as e:
                exstr = traceback.format_exc()
                print(exstr)
        else:
            try:
                self.flag = 1
                msg = ("2, " + str(0)).encode()
                self.arduino.write(msg)
                self.b1['text'] = 'Pause'
                self.b1['image'] = self.img2
            except (Exception, BaseException) as e:
                exstr = traceback.format_exc()
                print(exstr)

    def adv_file_read(self):
        print("adv file read")
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
            
        def quit_():
            #basicWin.destroy()
            self.ui1()
            win_r.destroy()

        et = Entry(win_r, textvariable=e_r)
        b_c = Button(win_r, text='...', command=f_c)
        b_e = Button(win_r, text='Start',command=quit_)  # ,font=('Times New Roman',16))
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

    def file_read(self, basicWin):
        basicWin.destroy()
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
            
        def quit_():
            #basicWin.destroy()
            self.ui1()
            win_r.destroy()

        et = Entry(win_r, textvariable=e_r)
        b_c = Button(win_r, text='...', command=f_c)
        b_e = Button(win_r, text='Start',command=quit_)  # ,font=('Times New Roman',16))
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
                self.arduino.write(b"7\r")
                ui_destroy()
                self.ui_basicORAdv()
            
            self.b1 = Button(primed, text="Press when pump is primed", font=("Times New Roman", 16), command=system_primed)
            self.b1.pack()

            self.b2 = Button(primed, text="Turn pump on", font=("Times New Roman", 16), command=self.togglePump)
            self.b2.pack()

if __name__ == '__main__':
    gui()