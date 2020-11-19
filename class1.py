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

class Nonpriority_system:
    
    def __init__(self):
        self.d = 200
        self.p_min = 0
        self.rec_min = 0
        self.time = 0
        self.time_step = 0.5 #after how many sec will the graph update
        self.u = 2 #mean rate of exponential distribution
        self.lam1 = 5 #mean rate of poisson process
        self.num_user = 0
        self.num_bs = 0
        self.channel_per_bs = 5
        
    def initialise(self):
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
            bs.channel = self.channel_per_bs
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
        
        status = self.check_handoff()
        return status
    
    def check_handoff(self):
        temp = []
        for i in self.user_info:
            if(i.pow_cur< self.p_min and i.call ==1):
                self.num_handoff += 1
                user_id = str(i.user_id)
                bs_id = str(i.bs_id)
                power = str(i.pow_cur)
                
                temp.append('handoff required:\n'+'user_id: '+user_id+'\n'+\
                            'bs_id: '+bs_id+'\n'+'power: '+power+'\n\n')
                temp1 = self.handoff_algo(i)
                
                if(temp1 != 0):
                    i = temp1
                    user_id = str(i.user_id)
                    bs_id = str(i.bs_id)
                    power = str(i.pow_cur)

                    temp.append('handoff success:\n'+'user_id: '+user_id+'\n'+\
                                'bs_id: '+bs_id+'\n'+'power: '+power+'\n\n')
                else:
                    user_id = str(i.user_id)
                    bs_id = str(i.bs_id)
                    power = str(i.pow_cur)

                    temp.append('handoff FAILED:\n'+'user_id: '+user_id+'\n'+\
                                'bs_id: '+bs_id+'\n'+'power: '+power+'\n\n')
     
        return temp
    
    def handoff_algo(self,ms):
        # self.rec_min = -70
        temp = sorted(ms.pow, key=lambda x: x[1], reverse = True)
        
        for i in temp:
            if (i[1]> self.rec_min and ms.bs_id != i[0]):
                if(self.check_channel(i[0]) == 1):
                    self.add_call(ms.user_id,i[0])
                    self.delete_call(ms.user_id,ms.bs_id)
                    ms.bs_id = i[0]
                    ms.pow_cur = i[1]
                    self.num_handoff_success += 1
                    return ms
        return 0
        
    def check_channel(self,bs_id):
        bs = self.search_bs_info(bs_id)
        if(len(bs.call_id) < bs.channel):
            return 1
        
        return 0
                               
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
                    if(j[1] > self.p_min):
                        i.bs_id = j[0]
                        i.pow_cur = j[1]
                
    def search_bs_info(self, bs_id):
        #returns the bs object of the bs_id given
        for i in self.bs_info:
            if(i.bs_id == bs_id):
                return i
                
    def call_update(self):
    
        
        for i in self.user_info:
            if(i.call == 1 and i.call_duration>0):
                i.call_duration -= self.time_step
                
                if(i.call_duration<=0):
                    i.call = 0
                    self.delete_call(i.user_id,i.bs_id)
                    i.last_call = self.time
                    i.next_call = self.time + np.random.poisson(lam=self.lam1, size=None)
                         
            elif(i.call == 0):
                if(i.next_call == self.time):
                    self.call_total += 1
                    if(self.check_channel(i.bs_id) ==1):
                        i.call = 1 
                        self.add_call(i.user_id,i.bs_id)
                        i.call_duration = np.random.exponential(scale=self.u , size=None)
                        
                    else:
                        i.next_call = self.time + np.random.poisson(lam=self.lam1, size=None)
                        self.call_drop += 1
                        
        if(self.call_total != 0):                
            self.call_drop_prob = self.call_drop*100/self.call_total
        
    def add_call(self,user_id,bs_id):
        for i in self.bs_info:
            if(i.bs_id == bs_id):
                i.call_id.append(user_id)
                
    def delete_call(self,user_id,bs_id):
        for i in self.bs_info:
            if(i.bs_id == bs_id):
                i.call_id.remove(user_id)
            
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
            self.channel = 0