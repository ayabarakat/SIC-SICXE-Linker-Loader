from tkinter import *
from tkinter import filedialog, messagebox, ttk
import numpy as np
import pandas as pd
from pandastable import Table
import tkinter as tk
import matplotlib.pyplot as plt


class Sic:
    #gui design
    def __init__(self) -> None:
        self.arr = []
        self.addresses = []
        self.lengths = []
        self.tRecs = ""
        self.df = None
        self.colored= {}
        self.filepath = ""
        menu = Tk()
        menu.geometry("900x500")
        menu.title("Absolute Loader")
        menu.configure(bg='#000000')
        tk.Label(menu,
                 text="", bg='#000000').pack()
        tk.Label(menu,
                 text="", bg='#000000').pack()
        tk.Label(menu,
                 text="", bg='#000000').pack()
        tk.Label(menu,
                 text="SHOW ABSOULTE LOADER(SIC PROGRAM)",
                 fg="#d8bfd8",
                 font=("Times", 30), bg='#000000').pack()
        tk.Label(menu,
                 text="Import SIC FILE(HTE)",
                 fg="#d8bfd8",
                 bg='#000000',
                 font="Helvetica 24 bold italic", padx=25, pady=25).pack(fill=BOTH)
        tk.Label(menu,
                 text="", bg='#000000').pack()
        button = Button(menu, text="import txt file", borderwidth=5, font="Times 20",fg="#d8bfd8", command=self.openfile,pady=10,padx=20)
        button.pack()
        tk.Label(menu,
                 text="", bg='#000000').pack()
        tk.Label(menu,
                 text="", bg='#000000').pack()
        tk.Label(menu,
                 text="", bg='#000000').pack()

        menu.mainloop()

    def openfile(self):
        #hena ana b2raa al file
        file = filedialog.askopenfile(mode="r", filetypes=[("Text Files", "*.txt")])
        self.filepath = file.name
        #if file is imported
        if file:
            #hte record
            self.hteReadFile()
            # generating memory address
            self.generateMemoryAdresses()
            # call  for loading data
            self.loadData()
            #  generating table
            self.generateSICTable()


    def hteReadFile(self):
        hte = open(self.filepath, "r")
        #i==>line
        for i in hte:
            if i[0] == 'T':
                print(i)
                #start address(6 bits)
                self.addresses.append(i[1:7])
                #length of the T record(2 bit)
                self.lengths.append(i[7:9])
                #object code l7d elnext line
                self.tRecs += i[9:].strip()
        #bn2sm objcodes in t record to(2bits)
        array = [self.tRecs[i:i + 2] for i in range(0, len(self.tRecs), 2)]
        self.arr = np.array(array)

    #memory address
    def generateMemoryAdresses(self):

        first_add = min(self.addresses)[:5] + "0"
        last_add = max(self.addresses)[:5] + "0"

        #mbeen awl add w a5r add
        memory_add = np.arange(int(first_add, 16), int(last_add, 16) + 32, 16)
        #change the add to hex
        memory_hex_add = np.array([hex(x) for x in memory_add]) #contains the object code
        print("address:")
        print(memory_add)
        #remove "0x" from the hex address(zyada in add)
        memory_hex_add= np.array([x.replace("0x", "").zfill(6).upper() for x in memory_hex_add]) #b7t add in coulmns
        print("mem hex add")
        print(memory_hex_add)
        memory = np.zeros((len(memory_hex_add), 16), dtype=int)

        #create table in gui w b7t rows and columns
        self.df = pd.DataFrame(np.zeros((len(memory_add), 16)), index=memory_hex_add , columns=np.arange(0, 16))
        self.df = self.df.astype(str).replace('0.0',np.nan) #change 0.0 values with nan(not number) (empty cells)
        self.df = self.df.dropna(how='all') #delete all columns that are all Nan (empty cells)



    def loadData(self):
        j = 0
        #connect the address and length variables to the self ones
        for add_, leng in zip(self.addresses, self.lengths):
            #end address
            end_add = (int(add_, 16) + int(leng, 16)) - 1
            #current address
            current = int(add_[0:5] + "0", 16)
            #column that we are standing
            column = int(add_[5], 16)
            print("columnns:")
            print(column)
            #uppercase and convert add to (hex)
            add = int(add_.upper(), 16)

            #checking if the address is still in bound
            while add < end_add:
                #Go to new row lma row yend
                if column == 16:
                    column = 0
                    current = current + 16
                #get new row add in (hex)
                row = hex(current).replace("0x", "").zfill(6)
                #add (in decimal)
                add = int(row[:len(row) - 1] + hex(column).replace("0x", "").upper(), 16)
                print("add:")
                print(add)

                #insert bits in arr table
                self.df.at[row, column] = self.arr[j].upper()
                j += 1
                column += 1
        print("data :")
        print(self.df)


    #Generate table
    def generateSICTable(self): #gui

        root_sic = Tk()
        root_sic.geometry("600x500")
        root_sic.title("Absolute Loader")
        frame = Frame(root_sic)
        frame.pack(fill="both", expand=True)
        col_in_Hex = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        self.df.columns=col_in_Hex
        table = Table(frame ,dataframe=self.df, width=500, maxcellwidth=30)

        table.show()
        table.showindex = True
        root_sic.mainloop()
