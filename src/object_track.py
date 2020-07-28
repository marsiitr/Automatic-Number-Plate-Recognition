import cv2
import numpy as np
from random import randint


class Object:
    def __init__(self , name=None):
        self.name=name
        self.tracker=cv2.TrackerKCF_create()
        self.box=None
        self.image = None
        self.text = None
        self.texts = []
        self.frames_lost = 0
        
    def initialize(self , img , box):
        self.tracker.init(img , tuple(map(int, box))) 
        
    def update_text(self,text):
        if len(self.texts)<5:
            p = self.get_probability(text)
            self.texts.append([text,p])
           
        
        maxi = -.01
        mini = 1.01
        i_max = 0
        i_min = 0
        p = self.get_probability(text)
        for i,text in enumerate(self.texts):
            p1 = text[1]
            if p1 > maxi :
                maxi = p1
                i_max = i
            if p1 < mini :
                mini = p1
                i_min = i
                
        if self.texts[i_min][1] != 0:
            self.texts[i_min][0] = text
            self.texts[i_min][1] = p
            self.text = self.texts[i_max][0]
                
    
    def get_probability(self , text):
        misids={'A':['A','4','H'] ,'H' :['H','M','W','A'] ,'W':['W','M','H'], 'N':['N','4','M'] ,'G':['G','6'] ,'C':['C']  , 'B':['B','8','P'] ,'P':['P','R' , 'B'] ,'R':['R','P'], 'O':['O','0'] , 'S':['S','5' , '8'] , 'I':['I','1','7' ,'J' , 'L' , 'T'] , 'L':['L','1','7' , 'J' , 'I' , 'T'] , 'J':['J','1','7' , 'I' , 'L' , 'T'] , 'Z':['Z','2','7'] , 'Q':['Q','0' , '2'] , 'D':['D','0'] , 'M':['M','H','W','N'] , 'E':['E','F' ], 'F':['F','E'] , 'K':['K','X'], 'X':['X','K'] , 'T':['T','J' , 'L' , 'I' , '7' , '1'] , 'U':['U','V' , 'Y' , '0' ,'4'] , 'V':['V','U' , 'Y'  , 'W'] , 'Y':['Y','V' , 'U'] , '4':['4','A','9','U','N'] , '6':['6','G'] , '8':['8','B' ,'5','0','3'] ,'3':['3','8','9'],'9':['9','3' , '4'] , '0':['0','O','Q' , 'D','8','U'] , '5':['5','S','M','8'] , '1':['1','I' , 'J' , 'L' , 'T' , '7'] , '7':['7','I' , 'J' , 'L' , 'T' , '1'] , '2':['2','Z' , 'Q']  }
        a1 = ['AN','AP','AR','AS','BR','CH','CG','DD','DL','GA','GJ','HR','HP','JK','JH','KA','KL','LA','LD','MP','MH','MN','ML','MZ','NL','OD','PY','PB','RJ','SK','TN','TS','TR','UP','UK','WB'] 
        text = ''.join(c for c in text if c.isalnum())
        text = text.upper()
        if len(text)<9 or len(text)>11:
            return 0
        a = text[0:2]
        b = text[2:4]
        c=[]
        d=[]
        p=0
        if len(text) == 9:
            c = text[4]
            d = text[5:]
        if len(text) == 10:
            c = text[4:6]
            d = text[6:]
        if len(text) == 11:
            c = text[4:7]
            d = text[7:]
        
        if a in a1 :
            p+=0.25
        else:
            ch1 = misids[a[0]]
            ch2 = misids[a[1]]
            
            for e in ch1:
                for f in ch2:
                    if p == 0.25:
                        continue
                    if e+f in a1 :
                        a=e+f
                        p+=0.25
                        
                    
        
        if b.isdecimal():
            p+=0.25
        else :
            ch1 = misids[b[0]]
            ch2 = misids[b[1]]
            
            for e in ch1:
                for f in ch2:
                    if p == 0.5:
                        continue
                    if (e+f).isdecimal() :
                        b=e+f
                        p+=0.25
                        break
        
    
        
        if c.isalpha():
            p+=0.25
        else :
            i = ''
            for e in c:
                f=0
                if not e.isalpha():
                    for h in misids[e]:
                        if h.isalpha():
                            i=i+h
                            f=f+1
                            break
                    if f==0:
                        return ''
                else :
                    i=i+e
            c=i
            p+=.25
            
        if d.isdecimal():
            p+=0.25
        else :
            i=''
            for e in d:
                f=0
                if not e.isdecimal():
                    for h in misids[e]:
                        if h.isdecimal():
                            i=i+h
                            f=f+1
                            break
                    if f==0:
                        return ''
                else :
                    i=i+e
            d=i
            p+=0.25
        if len(d) < 4:
            p-=0.2
     
        if len(a+b+c+d) != 10:
            p -= 0.05
        
        return p
        
class Tracker :
    def __init__(self):
        self.objects = []
        self.counter=1
        
    def new_boxes(self , img , boxes):
        l=len(self.objects)
        for n,box in enumerate(boxes):
            self.objects.append(Object(self.counter))
            self.objects[l+n].initialize(img , box)
            self.counter += 1
    
    def check_if_new(self , img , boxes , objects):
        new = []
        for box in boxes:
            a=True
            maxi = 0
            for o in objects:
                (x1,y1,w1,h1) = tuple(map(int, box))
                (x2,y2,w2,h2) = tuple(map(int, o.box))
                d = self.iou((x1 , y1 , x1+w1 , y1+h1) , (x2 , y2 , x2+w2 , y2+h2))                
                if d>maxi :
                    maxi = d                    
            if maxi < 0.1 :
                new.append(box)
        
        self.new_boxes(img , new)
        
    def update_objects(self , img , boxes):
        to_del= []
        objects=[]
        for (n,object) in enumerate(self.objects):
            s , object.box = object.tracker.update(img)
            if s:
                self.del_gone(object)
                if object.frames_lost <10:
                    objects.append(object)
                # if not self.del_gone(object.box) :
                #     objects.append(object)
                    # to_del.append(n)
                    # continue
                # objects.append(object)
        
        # for n in to_del:
        #     self.objects.pop[n]
        i=0
        while True:
            if self.objects[i].frames_lost >10:
                self.objects.pop(i)
                i -= 1
            i += 1
            if i == len(self.objects):
                break
            
        self.check_if_new(img , boxes , objects)
        
        self.label_object(img , objects)
        
    def label_object(self , img , objects):
        for o in objects:
            (x,y,w,h) = tuple(map(int, o.box))
            pts1 = (x,y)
            pts2 = (x+w,y+h)
            cv2.rectangle(img , pts1 , pts2 , (255,125,25),3)
            cv2.putText(img , str(o.name) , (int(x+w/2) , int(y+h/2)) ,cv2.FONT_HERSHEY_SIMPLEX , 1 , (25,125,255) , 3)
    
    # def del_gone(self , box):
    #     if 0 in tuple(map(int, box)):
    #         return True
    #     return False
    def del_gone(self , object):
        if 0 in tuple(map(int, object.box)):
            object.frames_lost += 1
        else :
            object.frames_lost = 0
        

    def iou(self , box1, box2):
        
        (box1_x1, box1_y1, box1_x2, box1_y2) = box1
        (box2_x1, box2_y1, box2_x2, box2_y2) = box2
        
        xi1 = max(box1_x1,box2_x1)
        yi1 = max(box1_y1,box2_y1)
        xi2 = min(box1_x2,box2_x2)
        yi2 = min(box1_y2,box2_y2)
        inter_width = xi2-xi1
        inter_height = yi2-yi1
        inter_area = max(inter_height, 0)*max(inter_width, 0)
        
        box1_area = (box1_y2 - box1_y1)*(box1_x2 - box1_x1) 
        box2_area = (box2_y2 - box2_y1)*(box2_x2 - box2_x1)
        union_area = box1_area + box2_area - inter_area
        
        iou = inter_area / union_area
        
        return iou

