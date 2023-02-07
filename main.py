from tkinter import *
from PIL import ImageGrab
from Prediction import Model



class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'white'
        self.color_bg = 'black'
        self.old_x = None
        self.old_y = None
        self.penwidth = 30
        self.prediction = -1
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint)#drwaing the line 
        self.c.bind('<ButtonRelease-1>',self.reset)
        self.model = Model()
        self.labelDir = None
        

    def paint(self,e):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND,smooth=True)

        self.old_x = e.x
        self.old_y = e.y

    def reset(self,e):    #reseting or cleaning the canvas 
        self.old_x = None
        self.old_y = None  
        

    def changeW(self,e): #change Width of pen through slider
        self.penwidth = e


    def drawWidgets(self):
        self.saveBtn = Button(self.master, text='Check Prediction', command=self.save)
        self.c = Canvas(self.master,width=280,height=280,bg=self.color_bg,)
        self.c.pack(fill=BOTH, expand=True)
        self.saveBtn.pack(side='top')
        self.clearBtn = Button(self.master, text='Clear', command=self.clear)
        self.clearBtn.pack(side='top')



    #save file as an jpg
    def save(self, e=None):
        x = root.winfo_rootx()+self.c.winfo_x()
        y = root.winfo_rooty()+self.c.winfo_y()
        x1 = x + self.c.winfo_width()
        y1 = y + self.c.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save("image.jpg")
        print('saved image')
        self.prediction = self.model.Predict('image.jpg')    
        print(self.prediction)
        
        if self.labelDir is not None:
            self.labelDir.destroy()

        self.labelDir = Label(self.master, text=str(self.prediction), height=4, font='arial', bd=5)
        self.labelDir.pack(side='bottom')

    def clear(self, e=None):
        self.c.delete(ALL)
    

root = Tk()
main(root)
root.mainloop()