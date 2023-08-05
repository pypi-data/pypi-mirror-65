# file = money.py
# version 1.1.2


 



from tkinter import *
from tkinter import ttk
import sys, sqlite3
import os

root = Tk()


vatrate = 20

root.title("MONEY")
root.option_add('*tearoff', FALSE)

    
    
def usegeditcust():
   print     ("using gedit")
   os.chdir  ("/home/terry/Desktop/moneyinpy")
   os.system ("gedit genlist.txt")

   
    

conn2 = sqlite3.connect('moneysql')
conn2.isolation_level = None
c = conn2.cursor()


def setup():
    print ("setting up")

    c.execute('''
        CREATE TABLE IF NOT EXISTS accounts(seq INTEGER UNIQUE, entrydate DATE, ref TEXT, clas TEXT, descript TEXT, debit FLOAT, credit FLOAT, balance FLOAT)''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS balances(seq INTEGER UNIQUE, balance FLOAT)''')



def setbalance():
    print ("Setting balance")
    def doit():
             print("doit")
             balanceedt=      balancebox.get()
             print("balances balance =",  balanceedt)


             
             c.execute("INSERT INTO balances  (seq, balance) VALUES(?,?)", (1, balanceedt))


   
    addrecframe =    ttk.Frame(root)
    balance =        ttk.Label(addrecframe,   text=  "Start Balance")
    
    balancebox=         ttk.Entry  (addrecframe)
    
    additbutton = ttk.Button (addrecframe, text = "OK",   command=doit)
    donebutton  = ttk.Button (addrecframe, text = "Done", command = addrecframe.destroy)
    
    
    addrecframe.grid    (column=0, row=5)
    balance.grid        (column=0, row=1)
    
    balancebox.grid    (column=1, row=1)
    
    
    
    
        
    additbutton.grid (column=5, row=6)
    donebutton.grid  (column =4, row=6)

 
   
def genlist(ktype):


    invfile=open ("/home/terry/Desktop/moneyinpy/genlist.txt", 'w')

    if ktype == 1:
        print ("list 1")
        
        c.execute ("select * from accounts ORDER BY seq")
        inv=""
        inv = "                        STATEMENT   \n"
        inv = inv + "_____________________________________________________________________________________________________________________________________\n"
        inv = inv + "Sequence Num     Date       Ref   Class                Description        Debit                Credit            Balance   \n"
        inv = inv + "_____________________________________________________________________________________________________________________________________\n"

 
    for row in c:
            inv = inv + '%(number)-15s' %    {"number": row[0]}  
            inv = inv + '%(number)-12s' %    {"number": row[1]}
            inv = inv + '%(number)-8s'  %    {"number": row[2]}
            inv = inv + '%(number)-22s' %    {"number": row[3]}
            inv = inv + '%(number)-15s' %    {"number": row[4]}
            inv = inv + '%(number)-22s' %    {"number": row[5]}
            inv = inv + '%(number)-10s' %    {"number": row[6]}
            inv = inv + '%(number)-14s' %    {"number": row[7]}

            inv = inv+"\n"
            


    txt=Text(root, width=200)
    txt.insert(END, inv)
  
    invfile.write (inv)
    print ("listing statement again")
    inv = ""
    invfile.close


    content2 = ttk.Frame(root)
    button2 = Button(content2, text = "Use gedit ??", command = usegeditcust)
    content2.grid(column=0, row=0)
    button2.grid(column=0, row=10)
    print ("in the box")
    txt.grid (column=0, row=7)


 

     

def addentry():
    print("Adding entry")
# accounts(entrydate, ref, class, descript, banorcash, debit, credit,  balance)''')

    def doit():
             print("doit")
             seqedt=          seqbox.get()
             entrydateedt=    entrydatebox. get()
             refedt=          refbox.get()
             clasedt=         clasbox.get()
             descriptedt=     descriptbox.get()
             debitedt=        debitbox.get()
             creditedt=       creditbox.get()

             balseq = seqbox.get()
             intbalseq=int(balseq)-1
             
             currbal=0
             print ("balseq=", balseq, intbalseq)
             c.execute ("select * from balances where seq="+ str(intbalseq))
             for row in c:
                  print ("wots i got")
                  print( '%(number)-15s' %    {"number": row[0]})
                  print('%(number)-12s'  %    {"number": row[1]})
                  currbal=('%(number)-12s'  %    {"number": row[1]})
                  print ("curr bal", currbal)
                  print("creditedt =", creditedt)
                  print("debitedt=", debitedt)
                  newcurrbal = float(currbal) - float(debitedt) + float(creditedt)
                  print ("new currbal=", newcurrbal)
                  print("seqedt=", seqedt)

                  c.execute ("INSERT INTO balances (seq, balance) VALUES (?,?)",  (seqedt, str(newcurrbal)))
             
                  c.execute("INSERT INTO accounts  (seq, entrydate, ref, clas, descript, debit, credit, balance) VALUES(?,?,?,?,?,?,?,?)", (seqedt, entrydateedt, refedt, clasedt, descriptedt, debitedt, creditedt, newcurrbal))
            

    addrecframe =    ttk.Frame(root)
    seq=             ttk.Label(addrecframe,   text=  "Sequence Number")
    entrydate=       ttk.Label(addrecframe,   text=  "Entry Date")
    ref=             ttk.Label(addrecframe,   text=  "Reference")
    clas=            ttk.Label(addrecframe,   text=  "Class")
    descript=        ttk.Label(addrecframe,   text=  "Description")
    debit=           ttk.Label(addrecframe,   text=  "Debit amount")
    credit=          ttk.Label(addrecframe,   text=  "Credit Amount")
                               

    seqbox=             ttk.Entry  (addrecframe)
    entrydatebox =      ttk.Entry  (addrecframe)
    refbox =            ttk.Entry  (addrecframe)
    clasbox =           ttk.Entry  (addrecframe)
    descriptbox  =      ttk.Entry  (addrecframe)
    debitbox=           ttk.Entry  (addrecframe)
    creditbox=          ttk.Entry  (addrecframe)

    
    additbutton = ttk.Button (addrecframe, text = "OK",   command=doit)
    donebutton  = ttk.Button (addrecframe, text = "Done", command = addrecframe.destroy)
    
    
    addrecframe.grid    (column=0, row=5)
    seq.grid            (column=0, row=0)
    entrydate.grid      (column=0, row=1)
    ref.grid            (column=0, row=2)
    clas.grid           (column=0, row=3)
    descript.grid       (column=0, row=4)
    debit.grid          (column=0, row=6)
    credit.grid         (column=0, row=7)

    
    
        
    seqbox.grid        (column=1, row=0)        
    entrydatebox.grid  (column=1, row=1)
    refbox.grid        (column=1, row=2)
    clasbox.grid       (column=1, row=3)
    descriptbox.grid   (column=1, row=4)
    debitbox.grid      (column=1, row=6)
    creditbox.grid     (column=1, row=7)
    
    
    
        
    additbutton.grid (column=5, row=6)
    donebutton.grid  (column =4, row=6)



def statement():
    print("Statement")
    genlist(1)
    

def bankstate():
    print("Bank Statement")
    genlist(2)

def cashstate():
    print("Cash Statement")
    genlist(3)

    
    
    
    

# lets try a menu bar

win            = Toplevel(root, width=300)
win.geometry('300x50-250+180')
menubar            = Menu(win)
win['menu']        = menubar
menu_dataentry     = Menu(menubar)
menu_details       = Menu(menubar)
menu_summary       = Menu(menubar)
menu_setup         = Menu(menubar)

menubar.add_cascade(menu=menu_dataentry,  label='Data Entry')
menubar.add_cascade(menu=menu_details,    label='Details')
menubar.add_cascade(menu=menu_setup,      label='Setup')

menu_dataentry.add_command(label='Add Entry',            command=addentry)
menu_details.add_command  (label='Statement',            command=statement)
menu_setup.add_command    (label='Set Database Name',    command=setup)
menu_setup.add_command    (label='Set Start Balance',    command=setbalance)




root.mainloop()

