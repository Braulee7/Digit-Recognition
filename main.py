from tkinter import *
from PIL import ImageGrab, Image, ImageDraw
from Prediction import Model
import os



class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'white'
        self.color_bg = 'black'
        self.old_x = None
        self.old_y = None
        self.penwidth = 25
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint)#drwaing the line 
        self.c.bind('<ButtonRelease-1>',self.reset)
        self.model = Model()
        self.labelDir = None
        self.image1 = Image.new('RGB', (280, 280), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image1)
        

    def paint(self,e):
        #draw on tkinter canvas and PIL canvas to get image
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND,smooth=True)
            self.draw.line([(self.old_x, self.old_y), (e.x, e.y)], fill='white', width=self.penwidth)

        self.old_x = e.x
        self.old_y = e.y

    def reset(self,e):    #reseting or cleaning the canvas 
        self.old_x = None
        self.old_y = None  
        

    #draw all widgets to tkinter root
    def drawWidgets(self):
        self.saveBtn = Button(self.master, text='Check Prediction', command=self.save)
        self.c = Canvas(self.master,width=280,height=280,bg=self.color_bg,)
        self.c.pack(expand=False)
        self.saveBtn.pack(side='top')
        self.clearBtn = Button(self.master, text='Clear', command=self.clear)
        self.clearBtn.pack(side='top')



    #save file as an jpg and get prediction
    def save(self, e=None):
        self.image1.save('image.jpg')
        self.draw.rectangle([0, 0, 500, 500], outline='black', fill='black')

        #get prediction and present to user
        self.prediction = self.model.Predict('image.jpg')    
        
        if self.labelDir is not None:
            self.labelDir.destroy()

        self.labelDir = Label(self.master, text=str(self.prediction), height=4, font='arial', bd=5)
        self.labelDir.pack(side='bottom')

    def clear(self, e=None):
        self.c.delete(ALL)
    

root = Tk()
main(root)
root.mainloop()