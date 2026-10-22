import io
import requests
import webbrowser
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk,Image

class NewsApp:
    def __init__(self):
        #fetch data
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=11449d7389d14923aa67bb784f38fa11').json()
        #print(data)                                   #.json sirf obj dega or .json() data fetch krega
        #initial GUI load   
        self.load_gui()                         
        
        #load the 1st news item
        self.load_news_item(0)
    def load_gui(self):                                #GUI
        self.root = Tk()
        self.root.title('News App')
        self.root.geometry('350x600')
        self.root.resizable(0,0)
        self.root.config(background='black')
    def clear(self):                                   #clear out the screen
        for i in self.root.pack_slaves():
            i.destroy()
    def load_news_item(self,index):
        #clear the screen for new news item
        self.clear()

        #image
        try:                                           #Image is loaded
            img_url = self.data['articles'][index]['urlToImage']            #fetching img from dictionary
            raw_data = urlopen(img_url).read()                              #fetching img from url
            im = Image.open(io.BytesIO(raw_data)).resize((350,250))         #image store huyi as a raw_data
            photo = ImageTk.PhotoImage(im)                                  #image tkinter conversion
        except:                                        #If Image is not loaded
            img_url = 'https://images.wondershare.com/repairit/article/fixing-the-image-not-available-error-01.png'
            raw_data = urlopen(img_url).read()                              #fetching img from url
            im = Image.open(io.BytesIO(raw_data)).resize((350,250))         #image store huyi as a raw_data
            photo = ImageTk.PhotoImage(im)                                  #image tkinter conversion

        label = Label(self.root,image=photo)                                #images me kya dal rha h
        label.pack()                                                        #pure pack ko dal do

        heading = Label(self.root,text=self.data['articles'][index]['title'],bg='black',fg='white',
                        wraplength=350,justify='center')                    #heading fetch ho rhi h data me se
        heading.pack(pady=(10,20))                                          #Padding
        heading.config(font=('verdana',15))                                 #font

        details = Label(self.root,text=self.data['articles'][index]['description'],bg='black',fg='white',
                                wraplength=350,justify='center')            #details fetch ho rhi h
        details.pack(pady=(2,15))                                           #Padding
        details.config(font=('verdana',12))                                 #font

        #frame.pack(expand=True, fill=BOTH)  Ye frame ko window ke andar layout manager ke through place karega:
        frame = Frame(self.root,bg='black')#expand=True -> Frame jitni bhi extra space available hogi usme expand ho jaayega.
        frame.pack(expand=True,fill=BOTH)  #fill=BOTH -> Frame horizontally aur vertically dono directions me stretch ho jaayega 

        if index != 0:                                              #1st index pr 'Prev' invisible rhega
            prev = Button(frame,text='Prev',width=16,height=3,command=lambda :self.load_news_item(index-1))
            prev.pack(side=LEFT)                                    #Used to go on previous news

        read = Button(frame,text='Read More',width=16,height=3,command=lambda :self.open_link(self.data['articles'][index]['url']))
        read.pack(side=LEFT)                                        #Used to open up browser link

        if index != len(self.data['articles'])-1:                   #last index pr 'Next' invisible rhega
            next = Button(frame,text='Next',width=16,height=3,command=lambda :self.load_news_item(index+1))
            next.pack(side=LEFT)                                    #Used to open up next news

        self.root.mainloop()

    def open_link(self,url):                                        #Used to open link in browser
        webbrowser.open(url)
obj = NewsApp()