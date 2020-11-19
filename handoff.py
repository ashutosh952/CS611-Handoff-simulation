import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import random
from math import log
from class1 import *
from class2 import *
from class3 import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import time
import matplotlib.animation as animation

    
def quit(window):
    window.destroy()

LARGE_FONT= ("Verdana", 12)

class Application(Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.pages = []
        
        for F in (Handoff_threshold, Start_page, Non_priority,Priority,Handoff_queue):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(Start_page)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class Start_page(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = Button(self, text="Handoff_threshold",
                            command=lambda: controller.show_frame(Handoff_threshold))
        button.pack()
        
class Handoff_threshold(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="Priority choose", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = Button(self, text="Non-priority scheme",
                            command=lambda: controller.show_frame(Non_priority))
        button1.pack()
        button2 = Button(self, text="Priority scheme",
                            command=lambda: controller.show_frame(Priority))
        button2.pack()
        button2 = Button(self, text="Handoff queue scheme",
                            command=lambda: controller.show_frame(Handoff_queue))
        button2.pack()

class Non_priority(Frame):

    def __init__(self, parent, controller):
        
        Frame.__init__(self,parent)
        
        self.sys = Nonpriority_system()
        
        back = Button(self, text="Back to start page",\
                         command=lambda: controller.show_frame(Start_page))
        plot_button = Button(master = self, command = lambda: self.start() , text = "Plot graph") 
        initialise_button = Button(self, command = self.sys.initialise,text = "Initialise system")
        quit_button = Button(master = self,command= lambda: quit(app),text = "Quit!")
        start_button = Button(master = self,command= lambda: self.play(), text = "PLay")
        pause_button = Button(master = self,command= lambda: self.pause(), text = "Pause")
        self.status = Text(self, height=20, width=30, font=LARGE_FONT)
        self.p_min_label = Label(self, text="Minimum power", font=LARGE_FONT)
        self.u_label = Label(self, text="mu", font=LARGE_FONT)
        self.num_bs_label = Label(self,text ='NUM BS', font = LARGE_FONT)
        self.num_user_label = Label(self,text ='NUM MS', font = LARGE_FONT)
        self.num_user = Entry(self,font=LARGE_FONT)
        self.num_bs = Entry(self, font=LARGE_FONT)
        self.num_channel_label = Label(self,text ='NUM Channel per BS', font = LARGE_FONT)
        self.num_channel = Entry(self,font=LARGE_FONT)
   

        self.p_min = Entry(self,font=LARGE_FONT)
        self.submit_button = Button(self, text = 'submit',command = lambda: self.submit())
        self.u = Entry(self,font=LARGE_FONT)
        self.clear_button = Button(self, text = 'clear status',command = lambda: self.clear_status())
        
        self.call_detail = Text(self, height=10, width=20, font=LARGE_FONT)
        self.rec_min_label = Label(self,text ='Minimun recieved power', font = LARGE_FONT)
        self.rec_min = Entry(self,font=LARGE_FONT)
        
        
        plot_button.grid(row = 1, column = 0)
        initialise_button.grid(row = 1, column = 1)
        quit_button.grid(row = 2, column = 0)
        start_button.grid(row = 2, column = 1)
        pause_button.grid(row = 3, column = 1)
        self.status.grid(row = 20, column = 1)
        self.p_min_label.grid(row = 4, column = 0 )
        self.p_min.grid(row = 4, column = 1)
        self.u_label.grid(row = 5, column = 0 )
        self.u.grid(row = 5, column = 1)
        self.num_bs_label.grid(row = 6, column = 0 )
        self.num_bs.grid(row = 6, column = 1)
        self.num_user_label.grid(row = 7, column = 0 )
        self.num_user.grid(row = 7, column = 1)
        self.num_channel_label.grid(row = 8, column = 0)
        self.num_channel.grid(row = 8, column = 1)
        self.rec_min_label.grid(row = 9,column = 0)
        self.rec_min.grid(row = 9,column = 1)
        back.grid(row = 15, column = 1)

        
        self.submit_button.grid(row = 5, column = 2  )
        self.clear_button.grid(row = 5, column = 3)
        self.call_detail.grid(row = 1 , column = 2)
        
    def clear_status(self):
        self.status.delete('1.0', END)
        self.call_detail.delete('1.0', END)
        
    def submit(self):
        self.sys.p_min = float(self.p_min.get())
        self.sys.u = float(self.u.get())
        self.sys.num_bs = int(self.num_bs.get())
        self.sys.num_user = int(self.num_user.get())
        self.sys.channel_per_bs = int(self.num_channel.get())
        self.sys.rec_min = float(self.rec_min.get())

    def print_status(self,text):
        self.status.insert(END, text)
        
    def play(self):
        self.ani1.event_source.start()
        
    def pause(self):
        self.ani1.event_source.stop()
        
    def start(self):
        self.fig1 = Figure(figsize = (6, 6), dpi = 100)
        self.ax1 = self.fig1.add_subplot(1,1,1)
        self.ax1.axis([-1,self.sys.d+1,-1,self.sys.d+1])
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master = self)   
        self.canvas1.draw() 
        self.canvas1.get_tk_widget().grid(row = 20,column = 0)
        self.ani1 = animation.FuncAnimation(self.fig1, self.animate1, frames=100,interval=200)
        
        self.fig2 = Figure(figsize = (5, 5), dpi = 100)
        self.ax2 = self.fig2.add_subplot(1,1,1)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master = self)   
        self.canvas2.draw() 
        self.canvas2.get_tk_widget().grid(row = 20,column = 2)
        
    
    def print_call_detail(self):
        self.call_detail.delete('1.0', END)
        self.call_detail.insert(END, 'call drop%: ' + str(self.sys.call_drop_prob) + '\n')
        self.call_detail.insert(END, 'num_handoff: ' + str(self.sys.num_handoff)+ '\n')
        self.call_detail.insert(END, 'successful handoff: ' +str(self.sys.num_handoff_success) + '\n')
        
    def plot_channel_status(self):
        x = []
        y = []
        for i in self.sys.bs_info:
            x.append(i.bs_id)
            y.append(len(i.call_id))
            
        self.ax2.clear()
        self.ax2.bar(x,y, color = 'green')
        self.canvas2.draw()
        
    def plot_system(self):
        x_bs = []
        y_bs = []
        for i in range(self.sys.num_bs):
            x_bs.append(self.sys.bs_info[i].x)
            y_bs.append(self.sys.bs_info[i].y)


        x_user = []
        y_user = []
        for i in range(self.sys.num_user):
            x_user.append(self.sys.user_info[i].x)
            y_user.append(self.sys.user_info[i].y)

        self.ax1.clear()
        self.ax1.scatter(x_bs,y_bs,marker = '^', s = 200, color = 'red')
        self.ax1.scatter(x_user, y_user, marker='+', s = 100, color = 'green')
        self.ax1.axis([-1,self.sys.d+1,-1,self.sys.d+1])
        
        
        for i in self.sys.user_info:
            bs = self.sys.search_bs_info(i.bs_id)
            if(i.call == 1):
                self.ax1.plot([i.x,bs.x], [i.y, bs.y])
        
        self.canvas1.draw()
    
    def animate1(self,i):

        self.plot_system()
        self.plot_channel_status()
        #take next step in the animation
        temp = self.sys.take_step()
        self.print_call_detail()
        if(len(temp)!=0):
            for i in temp:
                self.print_status(i)
        

class Priority(Frame):

    def __init__(self, parent, controller):
        
        Frame.__init__(self,parent)
        
        self.sys = Priority_system()
        
        back = Button(self, text="Back to start page",\
                         command=lambda: controller.show_frame(Start_page))
        plot_button = Button(master = self, command = lambda: self.start() , text = "Plot graph") 
        initialise_button = Button(self, command = self.sys.initialise,text = "Initialise system")
        quit_button = Button(master = self,command= lambda: quit(app),text = "Quit!")
        start_button = Button(master = self,command= lambda: self.play(), text = "PLay")
        pause_button = Button(master = self,command= lambda: self.pause(), text = "Pause")
        self.status = Text(self, height=20, width=30, font=LARGE_FONT)
        self.p_min_label = Label(self, text="Minimum power", font=LARGE_FONT)
        self.u_label = Label(self, text="mu", font=LARGE_FONT)
        self.num_bs_label = Label(self,text ='NUM BS', font = LARGE_FONT)
        self.num_user_label = Label(self,text ='NUM MS', font = LARGE_FONT)
        self.num_user = Entry(self,font=LARGE_FONT)
        self.num_bs = Entry(self, font=LARGE_FONT)
        self.num_channel_label = Label(self,text ='NUM Channel per BS', font = LARGE_FONT)
        self.num_channel = Entry(self,font=LARGE_FONT)

        self.num_channel_handoff_label = Label(self,text ='NUM Channel handoff', font = LARGE_FONT)
        self.num_channel_handoff = Entry(self,font=LARGE_FONT)
        self.rec_min_label = Label(self,text ='Minimun recieved power', font = LARGE_FONT)
        self.rec_min = Entry(self,font=LARGE_FONT)

        self.p_min = Entry(self,font=LARGE_FONT)
        self.submit_button = Button(self, text = 'submit',command = lambda: self.submit())
        self.u = Entry(self,font=LARGE_FONT)
        self.clear_button = Button(self, text = 'clear status',command = lambda: self.clear_status())
        
        self.call_detail = Text(self, height=10, width=20, font=LARGE_FONT)
        
        plot_button.grid(row = 1, column = 0)
        initialise_button.grid(row = 1, column = 1)
        quit_button.grid(row = 2, column = 0)
        start_button.grid(row = 2, column = 1)
        pause_button.grid(row = 3, column = 1)
        self.status.grid(row = 20, column = 1)
        self.p_min_label.grid(row = 4, column = 0 )
        self.p_min.grid(row = 4, column = 1)
        self.u_label.grid(row = 5, column = 0 )
        self.u.grid(row = 5, column = 1)
        self.num_bs_label.grid(row = 6, column = 0 )
        self.num_bs.grid(row = 6, column = 1)
        self.num_user_label.grid(row = 7, column = 0 )
        self.num_user.grid(row = 7, column = 1)
        self.num_channel_label.grid(row = 8, column = 0)
        self.num_channel.grid(row = 8, column = 1)
        self.num_channel_handoff_label.grid(row = 9, column = 0)
        self.num_channel_handoff.grid(row = 9, column = 1)
        self.rec_min_label.grid(row = 10,column = 0)
        self.rec_min.grid(row = 10,column = 1)
        back.grid(row = 15, column = 1)
        
        self.submit_button.grid(row = 5, column = 2  )
        self.clear_button.grid(row = 5, column = 3)
        self.call_detail.grid(row = 1 , column = 2)
        
    def clear_status(self):
        self.status.delete('1.0', END)
        self.call_detail.delete('1.0', END)
        
    def submit(self):
        self.sys.p_min = float(self.p_min.get())
        self.sys.u = float(self.u.get())
        self.sys.num_bs = int(self.num_bs.get())
        self.sys.num_user = int(self.num_user.get())
        self.sys.channel = int(self.num_channel.get())
        self.sys.channel_handoff = int(self.num_channel_handoff.get())
        self.sys.rec_min = float(self.rec_min.get())
        # print(self.sys.channel)
    
    def print_status(self,text):
        self.status.insert(END, text)
        
    def play(self):
        self.ani1.event_source.start()
        
    def pause(self):
        self.ani1.event_source.stop()
        
    def start(self):
        self.fig1 = Figure(figsize = (6, 6), dpi = 100)
        self.ax1 = self.fig1.add_subplot(1,1,1)
        self.ax1.axis([-1,self.sys.d+1,-1,self.sys.d+1])
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master = self)   
        self.canvas1.draw() 
        self.canvas1.get_tk_widget().grid(row = 20,column = 0)
        self.ani1 = animation.FuncAnimation(self.fig1, self.animate1, frames=100,interval=200)
        
        self.fig2 = Figure(figsize = (5, 5), dpi = 100)
        self.ax2 = self.fig2.add_subplot(1,1,1)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master = self)   
        self.canvas2.draw() 
        self.canvas2.get_tk_widget().grid(row = 20,column = 2)
    
    def print_call_detail(self):
        self.call_detail.delete('1.0', END)
        self.call_detail.insert(END, 'call drop%: ' + str(self.sys.call_drop_prob) + '\n')
        self.call_detail.insert(END, 'num_handoff: ' + str(self.sys.num_handoff)+ '\n')
        self.call_detail.insert(END, 'successful handoff: ' +str(self.sys.num_handoff_success) + '\n')
        
    def plot_channel_status(self):
        
        x = []
        y_call = []
        y_handoff = []
        
        for i in self.sys.bs_info:
            x.append(i.bs_id)
            y_call.append(i.channel_call)
            y_handoff.append(i.channel_handoff)
        
        self.ax2.clear()
        self.ax2.bar([i-0.14 for i in x],y_call, color = 'green',width=0.25)
        self.ax2.bar([i+0.14 for i in x],y_handoff, color = 'red',width=0.25)
        self.canvas2.draw()
        
    def plot_system(self):
        
        x_bs = []
        y_bs = []
        for i in range(self.sys.num_bs):
            x_bs.append(self.sys.bs_info[i].x)
            y_bs.append(self.sys.bs_info[i].y)


        x_user = []
        y_user = []
        for i in range(self.sys.num_user):
            x_user.append(self.sys.user_info[i].x)
            y_user.append(self.sys.user_info[i].y)

        self.ax1.clear()
        self.ax1.scatter(x_bs,y_bs,marker = '^', s = 200, color = 'red')
        self.ax1.scatter(x_user, y_user, marker='+', s = 100, color = 'green')
        self.ax1.axis([-1,self.sys.d+1,-1,self.sys.d+1])
        
        
        for i in self.sys.user_info:
            bs = self.sys.search_bs_info(i.bs_id)
            if(i.call == 1):
                self.ax1.plot([i.x,bs.x], [i.y, bs.y])
        
        self.canvas1.draw()
    
    def animate1(self,i):

        self.plot_system()
        self.plot_channel_status()
        #take next step in the animation
        temp = self.sys.take_step()
        self.print_call_detail()
        if(len(temp)!=0):
            for i in temp:
                self.print_status(i)

class Handoff_queue(Frame):

    def __init__(self, parent, controller):
        
        Frame.__init__(self,parent)
        
        self.sys = Handoff_queue_system()
        
        back = Button(self, text="Back to start page",\
                         command=lambda: controller.show_frame(Start_page))
        plot_button = Button(master = self, command = lambda: self.start() , text = "Plot graph") 
        initialise_button = Button(self, command = self.sys.initialise,text = "Initialise system")
        quit_button = Button(master = self,command= lambda: quit(app),text = "Quit!")
        start_button = Button(master = self,command= lambda: self.play(), text = "PLay")
        pause_button = Button(master = self,command= lambda: self.pause(), text = "Pause")
        self.status = Text(self, height=20, width=30, font=LARGE_FONT)
        self.p_min_label = Label(self, text="Minimum power", font=LARGE_FONT)
        self.u_label = Label(self, text="mu", font=LARGE_FONT)
        self.num_bs_label = Label(self,text ='NUM BS', font = LARGE_FONT)
        self.num_user_label = Label(self,text ='NUM MS', font = LARGE_FONT)
        self.num_user = Entry(self,font=LARGE_FONT)
        self.num_bs = Entry(self, font=LARGE_FONT)
        self.num_channel_label = Label(self,text ='NUM Channel per BS', font = LARGE_FONT)
        self.num_channel = Entry(self,font=LARGE_FONT)
        self.len_queue_label = Label(self,text ='Max queue len', font = LARGE_FONT)
        self.len_queue = Entry(self,font=LARGE_FONT)

        self.num_channel_handoff_label = Label(self,text ='NUM Channel handoff', font = LARGE_FONT)
        self.num_channel_handoff = Entry(self,font=LARGE_FONT)
        self.rec_min_label = Label(self,text ='Minimun recieved power', font = LARGE_FONT)
        self.rec_min = Entry(self,font=LARGE_FONT)

        self.p_min = Entry(self,font=LARGE_FONT)
        self.submit_button = Button(self, text = 'submit',command = lambda: self.submit())
        self.u = Entry(self,font=LARGE_FONT)
        self.clear_button = Button(self, text = 'clear status',command = lambda: self.clear_status())
        
        self.call_detail = Text(self, height=10, width=20, font=LARGE_FONT)
        
        plot_button.grid(row = 1, column = 0)
        initialise_button.grid(row = 1, column = 1)
        quit_button.grid(row = 2, column = 0)
        start_button.grid(row = 2, column = 1)
        pause_button.grid(row = 3, column = 1)
        self.status.grid(row = 20, column = 1)
        self.p_min_label.grid(row = 4, column = 0 )
        self.p_min.grid(row = 4, column = 1)
        self.u_label.grid(row = 5, column = 0 )
        self.u.grid(row = 5, column = 1)
        self.num_bs_label.grid(row = 6, column = 0 )
        self.num_bs.grid(row = 6, column = 1)
        self.num_user_label.grid(row = 7, column = 0 )
        self.num_user.grid(row = 7, column = 1)
        self.num_channel_label.grid(row = 8, column = 0)
        self.num_channel.grid(row = 8, column = 1)
        self.num_channel_handoff_label.grid(row = 9, column = 0)
        self.num_channel_handoff.grid(row = 9, column = 1)
        self.rec_min_label.grid(row = 10,column = 0)
        self.rec_min.grid(row = 10,column = 1)
        self.len_queue_label.grid(row = 11,column = 0)
        self.len_queue.grid(row = 11,column = 1)
        back.grid(row = 15, column = 1)
        
        self.submit_button.grid(row = 5, column = 2  )
        self.clear_button.grid(row = 5, column = 3)
        self.call_detail.grid(row = 1 , column = 2)
        
    def clear_status(self):
        self.status.delete('1.0', END)
        self.call_detail.delete('1.0', END)
        
    def submit(self):
        self.sys.p_min = float(self.p_min.get())
        self.sys.u = float(self.u.get())
        self.sys.num_bs = int(self.num_bs.get())
        self.sys.num_user = int(self.num_user.get())
        self.sys.channel = int(self.num_channel.get())
        self.sys.channel_handoff = int(self.num_channel_handoff.get())
        self.sys.rec_min = float(self.rec_min.get())
        self.sys.max_queue_len = int(self.len_queue.get())
        # print(self.sys.channel)
    
    def print_status(self,text):
        self.status.insert(END, text)
        
    def play(self):
        self.ani1.event_source.start()
        
    def pause(self):
        self.ani1.event_source.stop()
        
    def start(self):
        self.fig1 = Figure(figsize = (6, 6), dpi = 100)
        self.ax1 = self.fig1.add_subplot(1,1,1)
        self.ax1.axis([-1,self.sys.d+1,-1,self.sys.d+1])
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master = self)   
        self.canvas1.draw() 
        self.canvas1.get_tk_widget().grid(row = 20,column = 0)
        self.ani1 = animation.FuncAnimation(self.fig1, self.animate1, frames=100,interval=200)
        
        self.fig2 = Figure(figsize = (5, 5), dpi = 100)
        self.ax2 = self.fig2.add_subplot(1,1,1)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master = self)
        self.canvas2.draw() 
        self.canvas2.get_tk_widget().grid(row = 20,column = 2)

        self.fig3 = Figure(figsize = (5, 5), dpi = 100)
        self.ax3 = self.fig3.add_subplot(1,1,1)
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master = self)
        self.canvas3.draw() 
        self.canvas3.get_tk_widget().grid(row = 20,column = 3)

        # self.fig3 = Figure(figsize = (5, 5), dpi = 100)
        # self.ax3 = self.fig3.add_subplot(1,1,1)
        # self.canvas3 = FigureCanvasTkAgg(self.fig3, master = self)
        # self.canvas3.draw() 
        # self.canvas3.get_tk_widget().grid(row = 20,column = 3)
    
    def print_call_detail(self):
        self.call_detail.delete('1.0', END)
        self.call_detail.insert(END, 'call drop%: ' + str(self.sys.call_drop_prob) + '\n')
        self.call_detail.insert(END, 'num_handoff: ' + str(self.sys.num_handoff)+ '\n')
        self.call_detail.insert(END, 'successful handoff: ' +str(self.sys.num_handoff_success) + '\n')
        
    def plot_channel_status(self):
        
        x = []
        y_call = []
        y_handoff = []
        
        for i in self.sys.bs_info:
            x.append(i.bs_id)
            y_call.append(i.channel_call)
            y_handoff.append(i.channel_handoff)
        
        self.ax2.clear()
        self.ax2.bar([i-0.14 for i in x],y_call, color = 'green',width=0.25)
        self.ax2.bar([i+0.14 for i in x],y_handoff, color = 'red',width=0.25)
        self.canvas2.draw()
    
    def plot_queue_status(self):
        
        x = []
        y = []
        
        for i in self.sys.bs_info:
            x.append(i.bs_id)
            y.append(len(i.handoff_queue))
        
        self.ax3.clear()
        self.ax3.bar(x,y,color = 'grey')
        self.canvas3.draw()
        
    def plot_system(self):
        
        x_bs = []
        y_bs = []
        for i in range(self.sys.num_bs):
            x_bs.append(self.sys.bs_info[i].x)
            y_bs.append(self.sys.bs_info[i].y)


        x_user = []
        y_user = []
        for i in range(self.sys.num_user):
            x_user.append(self.sys.user_info[i].x)
            y_user.append(self.sys.user_info[i].y)

        self.ax1.clear()
        self.ax1.scatter(x_bs,y_bs,marker = '^', s = 200, color = 'red')
        self.ax1.scatter(x_user, y_user, marker='+', s = 100, color = 'green')
        self.ax1.axis([-1,self.sys.d+1,-1,self.sys.d+1])
        
        
        for i in self.sys.user_info:
            j = self.sys.search_bs_info(i.bs_id)
            bs = self.sys.bs_info[j]
            if(i.call == 1):
                self.ax1.plot([i.x,bs.x], [i.y, bs.y])
        
        self.canvas1.draw()
    
    def animate1(self,i):
        
        self.plot_system()
        self.plot_channel_status()
        self.plot_queue_status()
        self.sys.take_step()
        self.print_call_detail()
        if(len(self.sys.status)!=0):
            for i in self.sys.status:
                self.print_status(i)


app = Application()
app.geometry('1000x1000')
app.mainloop()  