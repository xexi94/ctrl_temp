import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk                # python 3
from tkinter import filedialog
from tkinter import ttk

import serial
import os

#Basics
'''
ser = serial.Serial('/dev/ttyACM0', 9600) # device, BAUD
while True:
    data = ser.readline()
    if data:
        print(data)
'''
LARGE_FONT = ("Verdana",12)
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)    
        
        self.title("ProgramName")
        self.variable = "Hellomellow" 
        self.resizable(0,0)

        if os.name == 'nt':
            None
            #self.iconbitmap("Images/thermometer.ico") 
        elif os.name == 'posix':
            None
        self.geometry("850x550") 

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (MainPage,):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("MainPage")


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    
class MainPage(tk.Frame):
    
       
    def __init__(self, parent, controller):
        
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        self.dev_select()
        
        
        self.option = tk.StringVar(self)
        self.option.set(optionList[0])
        w=ttk.OptionMenu(self,self.option,*optionList)
        
        
        button1 = ttk.Button(self, text="Start",command=self.start)
        button2 = ttk.Button(self, text="STOP",command=self.stop)
        
        w.place(x=638,y=275,width=110,heigh=30)
        button1.place(x=638,y=367,width=110,heigh=30)
        button2.place(x=638,y=458,width=110,heigh=30)
        
        
        
        global running
        running = False
        
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
            try:
                data = ser.readline()
                if data:
                    print (int(data[:-1]))
                    f.write(str(int(data[:-1]))+"\n")
            except (NameError,FileNotFoundError):
                print("NameError")
        else:
            print("NaN")
        
        self.after(500, self.scanning)   
    
    def start(self):
        global running
        global ser
        global f
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
        running = False
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
                popup.destroy()
        def no():
            if os.name == 'nt':
                None
            elif os.name == 'posix':
                dir_path = os.path.dirname(os.path.realpath(__file__))
                os.system("rm "+dir_path+"/tempfiles/temp01.txt")
                popup.destroy()

        popup = tk.Tk()
        popup.resizable(0,0)
        popup.geometry("200x100")
        if os.name == 'nt':
            None
        elif os.name == 'posix':
            None
        popup.wm_title("")
        message=ttk.Label(popup,text="description")
        Ys = tk.Button(popup,text="Yes",command=yes)
        Bl = tk.Button(popup,text="No",command=no)
        message.grid()
        Ys.grid()
        Bl.grid()
        popup.mainloop()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()