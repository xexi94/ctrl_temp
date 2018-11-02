import tkinter as tk                # python 3
from tkinter import filedialog
import serial
import os

'''
ser = serial.Serial('/dev/ttyACM0', 9600) # device, BAUD
while True:
    data = ser.readline()
    if data:
        print(data)
'''
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        global running
        running = False
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
        label = tk.Label(self, text="This is the main page")#, font=controller.title_font
        label.pack(side="top", fill="x", pady=10)

        #DEVICE SELECTION
        optionList=["     "]
        if os.name == 'nt':
        	None
            
        elif os.name == 'posix':
        	lines = os.popen("dmesg | grep tty").readlines()
        	for i in lines:
        		aux = i[i.find('tty')::]
        		device = aux[0:(aux.find(" "))-1]
        		if (bool(os.popen("test -e /dev/"+device+" && echo True || echo False").readlines()) == True):
        			optionList.append(device)
        		else:
        			optionList.append("     ")
        	optionList = sorted(list(set(optionList)))
        
        self.option = tk.StringVar(self)
        self.option.set(optionList[0])
        w=tk.OptionMenu(self,self.option,*optionList)
        w.pack(side=tk.LEFT)
        
        #DATA ACQUISITION
        def scanning():
            if running:
                try:
                    data = ser.readline()
                    if data:
                        print (str(data))
                        f.write(str(float(data))+"\n")
                except (NameError,FileNotFoundError):
                    print("NameError")
            else:
                print("NaN")
            self.after(500, scanning)   
                    
            
        def start():
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


        def stop():
            global running
            running = False
            try:
                f.close()
            except (NameError,FileNotFoundError):
                print("NameError")
            popupmsg()
        


        def popupmsg():

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
            message=tk.Label(popup,text="description")
            Ys = tk.Button(popup,text="Yes",command=yes)
            Bl = tk.Button(popup,text="No",command=no)
            message.pack()
            Ys.pack(side=tk.BOTTOM,pady=4)
            Bl.pack(side=tk.BOTTOM,pady=4)
            popup.mainloop()
        
        #BUTTONS
        button1 = tk.Button(self, text="Start",command=start)
        button2 = tk.Button(self, text="STOP",command=stop)
        button1.pack(side=tk.LEFT)
        button2.pack(side=tk.LEFT)

        self.after(500, scanning)
        #button1 = tk.Button(self, text="Go to Page One",
         #                   command=lambda: controller.show_frame("PageOne"))
        #button2 = tk.Button(self, text="Go to Page Two",
        #                    command=lambda: controller.show_frame("PageTwo"))


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()