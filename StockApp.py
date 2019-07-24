
import tkinter as tk
import requests
import time
import threading
import datetime
import sqlite3 

root= tk.Tk()


#Creating the Window Size
canvas1= tk.Canvas(root, height=700, width= 600)
canvas1.pack()

#Database connection
conn=sqlite3.connect('database.db')
curs=conn.cursor()




def information():

    def onFrameConfigure(canvas):
        canvas.config(scrollregion=canvas.bbox("all"))

    #Main Canvas/Frame for Information 
    canvas= tk.Canvas(root, bg='#B7E589', scrollregion=(0,0,200,800))
    infoframe1=tk.Frame(canvas,bg= '#B7E589')
    
    #Entry Frame
    frame1= tk.Frame(root,bg='#B7E589')
    
    #Scrollbar
    scrollbar=tk.Scrollbar(root,orient= tk.VERTICAL, command= canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    #Placements
    scrollbar.place(relx=0.948,rely= 0.2,relheight=0.7, relwidth= 0.03)
    canvas.place( relx= 0.05, rely= 0.20, relwidth=0.9, relheight=0.7)
    frame1.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.1)
    infoframe1.place(relx=0, rely= 0, relwidth=1, relheight=1)

    #Creating window because frames that are placed, packed, or gridded cannot be scrolled
    canvas.create_window((4,4),window=infoframe1,anchor="nw",height= 10000, width= 530)
    
    infoframe1.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    #Information Panel
    panel=tk.Label(infoframe1, bd=5, bg='white',text='The current stock data', anchor= 'nw', justify= 'left')
    panel.place(relheight=0.997, relwidth= 0.95, relx= 0.025, rely= 0.001)


    #Buttons linked with commands
    def button():
        entry1= tk.Entry(frame1,font= 40)
        entry1.place(relx=0.05, rely=0.1, relwidth= 0.6, relheight=0.8)
        button1= tk.Button(frame1, text= "Search", command=lambda:search(entry1.get()))
        button1.place(relx= 0.75, rely=0.1, relwidth= 0.2, relheight= 0.8)

        button2= tk.Button(root, text= "Symbol Search", command= lambda:getdata(entry1.get()))
        button2.place(relx= 0.75, rely= 0.92, relwidth= 0.2, relheight= 0.05)

        button3= tk.Button(root, text= "Database Search", command= lambda:alldata(entry1.get()))
        button3.place(relx= 0.54, rely= 0.92, relwidth= 0.2, relheight= 0.05)

        clearbutton=tk.Button(root,text= "Clear Search", command= lambda: clear())
        clearbutton.place(relx=0.05, rely= 0.92, relwidth=0.2, relheight= 0.05)

    #API for getting data. Returns dictionary, third value is a list of more dictionaries
    def search(entry):
        key= 'VLh9dIpvpBu80ctCpoGE3CwBLOknydaWm7AZi4rFkxxFRkY18gBZEKiIBrcJ'
        url= 'https://api.worldtradingdata.com/api/v1/stock?symbol=AAPL,MSFT,HSBA.L&api_token=VLh9dIpvpBu80ctCpoGE3CwBLOknydaWm7AZi4rFkxxFRkY18gBZEKiIBrcJ'
        params= {'APPID': key, 'q': entry}
        response= requests.get(url,params=params)
        values=response.json()
        for i in values['data']:
            if i['symbol']== entry:
                info= (i['name'] +'\n Price: ' + i['price'] +'\n Price Open: '
                                        +i['price_open'] + '\n Day High: '+ i['day_high']
                                           + '\n Day Low: ' + i['day_low'] + '\n Day Change: ' + str((float(i['day_high']) - float(i['day_low']))))
                panel.config(text='Name: ' + info)
                now=datetime.datetime.now()
    #Creating parameters for entering information into the database based on search
                params1= (now, i['symbol'], info)
                curs.execute("INSERT INTO stocks VALUES(?, ?, ?)", params1)


    #Accesses database to retrieve information for specific stock 
    def getdata(entry):
        params2=entry
        curs.execute("SELECT * from stocks WHERE name=?", (params2,))
        newlist=curs.fetchall()
        joinedstring=''
        for i in newlist:
            for x in i:
                joinedstring+=x + '\n'
            joinedstring+= ' ______________________________________ ' + '\n'
        panel.config(text=(joinedstring))

    #Accesses database to retrieve all stock information
    def alldata(entry):
        params2=entry
        curs.execute("SELECT * from stocks")
        newlist=curs.fetchall()
        joinedstring=''
        for i in newlist:
            for x in i:
                joinedstring+=x + '\n'
            joinedstring+= ' ______________________________________ ' + '\n'
        panel.config(text=(joinedstring))

    #Clears database
    def clear():
        panel.config(text='Cleared')


    #Exception handling for database if not already created
    def sqlite3():
        try:
            curs.execute("""CREATE TABLE stocks(time text, name text, information text)""")
        except:
            print('Database already exists')
    

       
   
    button()
    sqlite3()




information()
conn.commit()

root.mainloop()
