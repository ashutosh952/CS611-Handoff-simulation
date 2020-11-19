import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import random
from math import log
from class1 import *

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import time
import matplotlib.animation as animation

class Priority_system:

    def __init__(self):
        self.d = 200
        self.p_min = -56
        self.rec_min = -52
        self.time = 0
        self.time_step = 0.5 #after how many sec will the graph update
        self.u = 10 #mean rate of exponential distribution
        self.lam1 = 5 #mean rate of poisson process
        self.num_user = 1000
        self.num_bs = 5
        self.channel = 20
        self.channel_handoff = 5
        
    def initialise(self):
        self.p_call_cut = -70
        self.call_total = 0
        self.call_drop = 0
        self.call_drop_prob = 0
        self.num_handoff_success = 0
        self.num_handoff = 0
        self.time = 0
        bs_id = 0
        user_id = 0
        
        self.bs_info = []
        self.user_info = []
        
        for i in range(self.num_bs):
            bs = self.BS()
            bs.x = random.randint(0,self.d)
            bs.y = random.randint(0,self.d)
            bs.bs_id = bs_id
            # bs.channel = self.channel_per_bs
            # bs.channel_handoff = self.channel_handoff
            bs_id +=1
            self.bs_info.append(bs)
            
        for i in range(self.num_user):
            ms = self.MS()
            ms.x = random.randint(0,self.d)
            ms.y = random.randint(0,self.d)
            ms.user_id = user_id 
            ms.next_call = np.random.poisson(lam=self.lam1, size=None)
            user_id+=1
            self.user_info.append(ms)
            
        self.measure_power()
        
        for i in self.user_info:        
            temp = sorted(i.pow, key=lambda x: x[1], reverse = True)    
            
            i.bs_id = temp[0][0]
            i.pow_cur = temp[0][1]
            
        self.call_update()
        
        
    def take_step(self):
        
        for i in self.user_info:
            #the user has to be within box
            if(i.x>self.d or i.y>self.d or i.x<0 or i.y<0):
                if(i.call == 1):
                    self.delete_call(i.user_id,i.bs_id)
                self.user_info.remove(i)
                self.num_user -=1
                
            else:
                i.x += random.choices([0,5,-5], weights = [0.4,0.3,0.3],k=1)[0]
                i.y += random.choices([0,5,-5], weights = [0.4,0.3,0.3],k=1)[0]
        
        self.measure_power()
        
        self.time += self.time_step
        self.call_update()
        
        self.check_handoff()
        
    
    def check_handoff(self):
        self.status = []
        for i in self.user_info:
            if(i.pow_cur< self.p_min and i.call ==1):
                self.num_handoff += 1
                user_id = str(i.user_id)
                bs_id = str(i.bs_id)
                power = str(i.pow_cur)
                
                self.status.append('handoff required:\n'+'user_id: '+user_id+'\n'+\
                            'bs_id: '+bs_id+'\n'+'power: '+power+'\n\n')
                temp1 = self.handoff_algo(i)
                
                if(temp1 != 0):
                    i = temp1
                    user_id = str(i.user_id)
                    bs_id = str(i.bs_id)
                    power = str(i.pow_cur)

                    self.status.append('handoff success:\n'+'user_id: '+user_id+'\n'+\
                                'bs_id: '+bs_id+'\n'+'power: '+power+'\n\n')
                else:
                    user_id = str(i.user_id)
                    bs_id = str(i.bs_id)
                    power = str(i.pow_cur)

                    self.status.append('handoff FAILED:\n'+'user_id: '+user_id+'\n'+\
                                'bs_id: '+bs_id+'\n'+'power: '+power+'\n\n')
     
    
    def handoff_algo(self,ms):
        
        temp = sorted(ms.pow, key=lambda x: x[1], reverse = True)
        
        for i in temp:
            if (i[1]> self.rec_min and ms.bs_id != i[0]):
                val = self.check_channel(i[0],0)
                if(val in [0,1]):
                    self.add_call(ms.user_id,i[0],val)
                    self.delete_call(ms.user_id,ms.bs_id)
                    ms.bs_id = i[0]
                    ms.pow_cur = i[1]
                    self.num_handoff_success += 1
                    return ms

        return 0

    def add_call(self,user_id,bs_id,type):
        #type 0: dedicated handoff channel
        #type 1: normal call channel
        i = self.search_bs_info(bs_id)
        bs = self.bs_info[i]
        if(type == 1):
            bs.call_id.append(user_id)
            bs.channel_call+=1
        if(type == 0):
            bs.handoff_id.append(user_id)
            bs.channel_handoff += 1

        self.bs_info[i] = bs
                
    def delete_call(self,user_id,bs_id):
        i = self.search_bs_info(bs_id)
        bs = self.bs_info[i]
        if(user_id in bs.call_id):
            bs.call_id.remove(user_id)
            bs.channel_call -=1
        else:
            bs.handoff_id.remove(user_id)
            bs.channel_handoff-=1

        self.bs_info[i] = bs
        
    def check_channel(self,bs_id,type):
        #type 1 is orginating call
        #type 0 is handoff call
        i = self.search_bs_info(bs_id)
        bs = self.bs_info[i]
        if(type == 1):
            if(bs.channel_call  < (self.channel- self.channel_handoff)):
                return 0 #add call to originating call channel
            else:
                return 1 #no space to add call, drop the call
        if(type == 0):
            if(bs.channel_handoff < self.channel_handoff):
                return 0 #add handoff to dedicated handoff channel

            elif((bs.channel_call+bs.channel_handoff) <self.channel):
                return 1 #add handoff to normal call channel

            else:
                return 2 #no space for the handoff call/can't accept
                               
    def measure_power(self):
        path_loss = 3
        k1 = 0
        k2 = 10*path_loss
    
        x = np.random.normal(loc = 0, scale = 2)
        #update the power recieved by BSs
        for i in self.user_info:
            i.pow = []
            for j in self.bs_info:
                
                d = self.dist(i.x,i.y,j.x,j.y)
                if(d!=0):
                    power = k1 - k2*log(d,10) + x
                    
                else:
                    power = k1 + x
                if(j.bs_id == i.bs_id):
                    i.pow_cur = power
                i.pow.append([j.bs_id,power])
                
        #change the BS the Ms is following if power<p_min
        for i in self.user_info:
            if(i.call == 0 and i.pow_cur < self.p_min):
                temp = sorted(i.pow, key=lambda x: x[1], reverse = True)    
                for j in temp:
                    if(j[1] > self.p_call_cut):
                        i.bs_id = j[0]
                        i.pow_cur = j[1]
                
                
    def search_bs_info(self, bs_id):
        #returns the bs object index of the bs_id given
        for i in range(len(self.bs_info)):
            if(self.bs_info[i].bs_id == bs_id):
                return i
                
    def call_update(self):
        
        for i in self.user_info:
            if(i.call == 1 and i.call_duration>0):
                i.call_duration -= self.time_step

                if(i.pow_cur<self.p_call_cut):
                    i.call = 0
                    i.call_duration = 0
                    self.delete_call(i.user_id,i.bs_id)
                    self.call_drop+=1
                    i.last_call = self.time
                    i.next_call = self.time + np.random.poisson(lam=self.lam1, size=None)
                
                elif(i.call_duration<=0):
                    i.call = 0
                    self.delete_call(i.user_id,i.bs_id)
                    i.last_call = self.time
                    i.next_call = self.time + np.random.poisson(lam=self.lam1, size=None)
                         
            elif(i.call == 0):
                if(i.next_call == self.time):
                    self.call_total += 1
                    if(self.check_channel(i.bs_id,1) ==0):
                        i.call = 1 
                        self.add_call(i.user_id,i.bs_id,1)
                        i.call_duration = np.random.exponential(scale=self.u , size=None)
                        
                    else:
                        i.next_call = self.time + np.random.poisson(lam=self.lam1, size=None)
                        self.call_drop += 1
                        
        if(self.call_total != 0):                
            self.call_drop_prob = self.call_drop*100/self.call_total
            
    def dist(self,x1,y1,x2,y2):
        return np.sqrt((x1-x2)**2 + (y1-y2)**2)

    
    class MS:
        def __init__(self):
            self.call = 0
            self.x = 0
            self.y = 0
            self.bs_id = 0
            self.user_id = 0
            self.pow = []
            self.pow_cur = 0
            self.bs = 0
            self.call_duration = 0
            self.last_call = 0
            self.next_call = 0

    class BS:
        def __init__(self):
            self.x = 0
            self.y = 0
            self.bs_id = 0
            self.call_id = []
            self.handoff_id = []
            self.channel_call = 0
            self.channel_handoff = 0