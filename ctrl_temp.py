import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk                # python 3
from tkinter import filedialog
from tkinter import ttk

import serial
import os
#hola

LARGE_FONT = ("Verdana",12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)
CHRONO_FONT = ("Times",42)
style.use("ggplot")

gr = Figure(figsize=(5,5), dpi=100)
a = gr.add_subplot(111)
time = 0



def animate(i):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = dir_path+"/tempfiles"
    pullData = open(path+"/temp01.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(float(x))
            yList.append(int(y))

    a.clear()
    a.set_ylim([0,100])
    a.set_xlabel("time (s)")
    a.set_ylabel("temperature (C)")
    a.plot(xList, yList)
    

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)    
        
        tk.Tk.title(self, "ctrl_temp beta 1")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (MainPage,):
            
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    
class MainPage(tk.Frame):
    
       
    def __init__(self, parent, controller):
        
        
        tk.Frame.__init__(self, parent)
        
        
        self.dev_select()
        
        
        self.option = tk.StringVar(self)
        self.option.set(optionList[0])
        w=ttk.OptionMenu(self,self.option,*optionList)
        
        
        button1 = ttk.Button(self, text="Start",command=self.start)
        button2 = ttk.Button(self, text="STOP",command=self.stop)
        label1 = ttk.Label(self,text="Device slection",font=LARGE_FONT)
        label2 = tk.Label(self,bg="orange")
        label3 = tk.Label(self,bg="Blue")
        label1.place(x=540,y=280)
        label2.place(x=505,y=10,width=340,heigh=200)
        #label3.place(x=505,y=270,width=170,heigh=300)
        w.place(x=700,y=275,width=110,heigh=30)
        button1.place(x=700,y=367,width=110,heigh=30)
        button2.place(x=700,y=458,width=110,heigh=30)
        
        canvas = FigureCanvasTkAgg(gr, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.LEFT,expand=False)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP,anchor=tk.W,expand=False)
        
        
        global running
        
        running = False
        
        if os.name == 'nt':
            None
        elif os.name == 'posix':
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = dir_path+"/tempfiles"        
            t = open(path+"/temp01.txt","w")
        self.chrono_temp(0, 0)
        self.scanning()
    
    def dev_select(self):
        global optionList
        optionList=["     "]
                
        if os.name == 'nt':
            None
                        
        elif os.name == 'posix': 
            lines = os.popen("dmesg | grep tty").readlines()
            for i in lines:
                aux = i[i.find('tty')::]
                device = aux[0:(aux.find(" "))-1]
                statment = str((os.popen("test -e /dev/"+device+" && echo True || echo False").readlines()))
                if (statment[2:-4] == "True"):
                        
                    optionList.append(device)
                else:
                    optionList.append("     ")
                    
            optionList = sorted(list(set(optionList))) 
    def scanning(self):
         
        if running:
            global time 
            try:
                
                data = ser.readline()
                if data:
                    #print (str(time)+","+str(int(data[:-1])))
                    f.write(str(time)+","+str(int(data[:-1]))+"\n")
                    f.flush()
            except (NameError,FileNotFoundError):
                
                print("NameError")
            self.chrono_temp(time,int(data[:-1]) )
            time = time +0.5
            
        else:
            pass
            #print("NaN")
        
        self.after(500, self.scanning)
         
    
    def start(self):
        global running
        global ser
        global f
        global path
        running = True
        if os.name == 'nt':
            None
        elif os.name == 'posix':
                
            dev=str(self.option.get())
            dir_path = os.path.dirname(os.path.realpath(__file__))
            ser = serial.Serial(str('/dev/'+dev), 9600)                    
            path = dir_path+"/tempfiles"
                    
            f = open(path+"/temp01.txt","w")
         
    def stop(self):
        global running
        global ser
        global f
        global time
        running = False
        time = 0
        
        try:
            f.close()
        except (NameError,FileNotFoundError):
            print("NameError")
        ser.close()
        
        self.popupmsg()

    def popupmsg(self):

        def yes():
            if os.name == 'nt':
                None
            elif os.name == 'posix':
                dir_path = os.path.dirname(os.path.realpath(__file__))
                l = open(dir_path+"/tempfiles/temp01.txt",'r')
                a=l.readlines()
                q = filedialog.asksaveasfile(initialdir="./",title="Selec Folder",filetypes = (("text files","*.txt"),("all files","*.*")))
                for i in range(len(a)):
                    q.write(str(a[i]))
                q.close()
                    
                os.system("rm "+dir_path+"/tempfiles/temp01.txt")
                
                path = dir_path+"/tempfiles"        
                t = open(path+"/temp01.txt","w")
                popup.destroy()
        def no():
            if os.name == 'nt':
                None
            elif os.name == 'posix':
                dir_path = os.path.dirname(os.path.realpath(__file__))
                os.system("rm "+dir_path+"/tempfiles/temp01.txt")
                
                path = dir_path+"/tempfiles"        
                t = open(path+"/temp01.txt","w")
                popup.destroy()

        popup = tk.Tk()
        popup.title("Save file")
        popup.resizable(0,0)
        popup.geometry("300x150")
        if os.name == 'nt':
            None
        elif os.name == 'posix':
            None
        popup.wm_title("")
        message=ttk.Label(popup,text="Do you want to save this file?",font=NORM_FONT)
        Ys = ttk.Button(popup,text="Yes",command=yes)
        Bl = ttk.Button(popup,text="No",command=no)
        message.pack(side=tk.TOP,anchor=tk.CENTER,pady=10)
        Ys.place(x=95,y=50,width=110,heigh=30)
        Bl.place(x=95,y=100,width=110,heigh=30)
        popup.mainloop()
    
    def chrono_temp(self,secon,tempera):
        
        global chronometer
        global temperature
        chronometer = tk.Label(self,text="time: "+str(secon)+" s",font=CHRONO_FONT,bg="orange")
        temperature = tk.Label(self,text="temp: "+str(tempera)+" C",font=CHRONO_FONT,bg="orange")
        
        chronometer.place(x=510,y=30)
        temperature.place(x=510,y=120)
        
        
app = SampleApp()
app.resizable(width=0, height=0)
app.geometry("850x550")
ani = animation.FuncAnimation(gr, animate, interval=500) 
app.mainloop()