
import tkinter
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import numpy as np
import pandas as pd
from pandastable import Table
import tkinter as tk

#convert int to hex
def to_hex(value, numOfBits):
    return hex((value + (1 << numOfBits)) % (1 << numOfBits))


class SicXE:
    #gui for sicxe
    def __init__(self) -> None:
        self.control_sections = None
        self.labelsDf = None
        self.estab = {}
        self.defs = []
        self.defs_addresses = []
        self.filepath = ""
        self.startingAddress = "000000"
        self.startingAddressEntry = None
        self.arr = []
        self.addresses = []
        self.lengths = []
        self.tRecs = ""
        self.df = None
        self.start = None
        self.name = None
        self.found_address = None
        self.label = None
        self.op = None
        self.val = None
        self.firstChar = ""
        self.color = {}
        self.indexx = []
        menu = Tk()
        menu.geometry("1000x700")
        menu.title("Linker Loader")
        menu.configure(bg='#000000')
        tk.Label(menu,
                 text="", bg='#000000').pack()
        tk.Label(menu,
                 text="", bg='#000000').pack()
        tk.Label(menu,
                 text="", bg='#000000').pack()
        tk.Label(menu,
                 text="SHOW LINKER LOADER(SICXE PROGRAM)",
                 fg="#d8bfd8",
                 font=("Times", 40), bg='#000000').pack()

        tk.Label(menu,
                 text="INSERT starting address",
                 fg="#d8bfd8",
                 bg='#000000',
                 font="Helvetica 24 bold italic", padx=20, pady=20).pack(fill=BOTH)
        Label(menu, text="", bg='#000000').pack(fill=BOTH)
        self.startingAddressEntry = Entry(menu)
        self.startingAddressEntry.pack()
        Label(menu, text="", bg='#000000').pack(fill=BOTH)
        Button(menu, text="Modify address", borderwidth=5, command=self.setStartingAddress, pady=10, padx=10,
               font="Times 20",fg="#d8bfd8").pack()
        Label(menu, text="", bg='#000000').pack(fill=BOTH)
        tk.Label(menu,
             text="Import SICXE FILL (HDRTME)",
             fg="#d8bfd8",
             bg='#000000',
             font="Helvetica 24 bold italic", padx=20, pady=20).pack(fill=BOTH)
        Label(menu, text="", bg='#000000').pack(fill=BOTH)
        button = Button(menu, text="Impot txt file",borderwidth=5, command=self.openfile,pady=10,padx=10,font="Times 20",fg="#d8bfd8").pack()
        Button(menu, text = "Show ESTAB",  borderwidth=5,command=self.getESTAB,pady=10,padx=15,font="Times 20",fg="#d8bfd8").pack()
        tk.Label(menu,
                 text="", bg='#000000').pack()
        tk.Label(menu,
                 text="", bg='#000000').pack()
        tk.Label(menu,
                 text="", bg='#000000').pack()

        menu.mainloop()
    #open the HTDRME
    def openfile(self):
        file = filedialog.askopenfile(mode="r", filetypes=[("Text Files", "*.txt")])
        self.filepath = file.name
        self.genESTAB()
        self.setAddresses()
        self.genMemory()
        self.loadData()
        self.modifyData()
        self.genTable()

    #get starting address (from user)
    def setStartingAddress(self):
        print("starting address is:")
        self.startingAddress = self.startingAddressEntry.get()
        print(self.startingAddress)

    def genESTAB(self):
        hdrtme = open(self.filepath, "r")
        #to store control sections
        self.cs = []
        control_add = []
        csleng = []
        for i in hdrtme:
            if i[0] == 'H':
                #PROGA/B/C
                name_of_prog = i[1:6]
                #new starting address=starting add+modified address
                address = hex(int(i[7:13], 16) + int(self.startingAddress, 16)).replace("0x", "").zfill(6).upper()
                #length of prog
                length = i[13:].strip()
                #name control sec in arr
                self.cs.append(name_of_prog)
                #address control sec addressess in arr
                control_add.append(address)
                #leng control sec length in arr
                csleng.append(length)
            #extrenal defintion
            if i[0] == 'D':
                i = i.strip()
                #name of extdef (6 bits)
                self.defs = [i[x:x+ 6] for x in range(1, len(i), 12)]
                #add of extdef var
                self.defs_addresses = [i[x:x + 6] for x in range(7, len(i), 12)]

                #lbls(label) dictionary
                lbls = {}

                #name and  addresses
                for definition, definition_address in zip(self.defs, self.defs_addresses):
                    #name:address(dictionary)
                    lbls[definition.replace("X", "")] = definition_address
                self.estab[name_of_prog] = {"Address": address, "Length": length, "Labels": lbls}

        for i in range(1, len(control_add)):
            #new address=address+leng of prog
            control_add[i] = hex(int(control_add[i - 1], 16) + int(csleng[i - 1], 16)).replace("0x", "").zfill(6)

        for addr, (k, val) in zip(control_add, self.estab.items()):
            #get al address
            val['Address'] = addr
            for dk, dval in val['Labels'].items():
                #lbls+add
                val['Labels'][dk] = hex(int(val['Labels'][dk], 16) + int(val['Address'], 16)).replace("0x", "").zfill(6).upper()
        #estab
        self.labelsDf = pd.DataFrame.from_dict(self.estab, orient='index')
        self.labelsDf.to_csv("estab.csv", encoding=None, index=False, sep=' ')

        # convert (estab)csv to txt file

        with open('estab.csv', 'r') as f_in, open('Ext_Sym_Table.txt', 'w') as f_out:
            #Read the cvs file and store in variable
            content = f_in.read()
            # el content to txt file
            f_out.write(content)


    def getESTAB(self): #gui ESTAB
        root_estab = Tk()
        root_estab.geometry("600x300")
        root_estab.title("ESTAB")
        frame = Frame(root_estab)
        frame.pack(fill="both", expand=True)
        table = Table(frame, dataframe=self.labelsDf)
        table.show()
        table.showindex = True
        root_estab.mainloop()

    def setAddresses(self):
        hteREC = open(self.filepath, "r")

        for i in hteREC:
            if i[0] == 'H':
                name = i[1:6]
                start = self.estab[name.replace("X", "")]['Address']
            if i[0] == 'T':
                # start add in t record
                x = int(i[1:7], 16) + int(start, 16)
                print("add trec:")
                print(hex(x))
                self.addresses.append(hex(x).replace("0x", "").zfill(6).upper())
                self.lengths.append(i[7:9])
                self.tRecs += i[9:].strip()
        self.arr = [self.tRecs[i:i + 2] for i in range(0, len(self.tRecs), 2)]
        self.arr = np.array(self.arr)

    def genMemory(self):
        first_add = min(self.addresses)[:5] + "0"
        last_add = max(self.addresses)[:5] + "0"
        memory_add = np.arange(int(first_add, 16), int(last_add, 16) + 32, 16)

        def add_to_hex(x): return hex(x)

        def hex_add(x): return x.replace("0x", "").zfill(6).upper()

        #address to hex
        mem_hex_add = np.array([add_to_hex(x) for x in memory_add])
        #delete (ox)
        mem_hex_add = np.array([hex_add(x) for x in mem_hex_add])

        self.df = pd.DataFrame(np.zeros((len(memory_add), 16)), index=mem_hex_add, columns=np.arange(0, 16))
        self.df = self.df.astype(str)
        self.indexx = pd.Index(mem_hex_add)


    def loadData(self):
        j = 0
        for address, leng in zip(self.addresses, self.lengths):
            end_add = (int(address, 16) + int(leng, 16)) - 1
            current = int(address[0:5] + "0", 16)
            column = int(address[5], 16)
            add = int(address.upper(), 16)
            while add < end_add:
                if column == 16:
                    column = 0
                    current = current + 16
                row = hex(current).replace("0x", "").zfill(6).upper()
                add = int(row[:len(row) - 1] + hex(column).replace("0x", "").upper(), 16)
                self.df.at[row, column] = self.arr[j].upper()
                j += 1
                column += 1

    def modifyData(self):

        hteREC = open(self.filepath, "r")

        for i in hteREC:
            self.firstChar = ""
            if i[0] == 'H':
                self.name = i[1:6]
                print("Control:   ",self.name)
                #ADDRESS OF PROGA/B/C
                self.start = self.estab[self.name.replace("X", "")]['Address']

            if i[0] == 'M':
                print("M record:  ",i)
                n = hex(int(i[1:7], 16) + int(self.start, 16)).replace("0x", "").zfill(6).upper()


                #M00001905+LISTA
                # el line to pieces
                #row +add of proga/b/c
                row = n[0:5] + "0".upper()
                print('row: ')
                print(row)
                column = int(n[5:6], 16)
                #2 bits
                leng = i[7:9]
                #(+/-)
                self.op = i[9:10]
                #lista
                self.label = i[10:].strip()

                #To color the updated cells after modification:
                #each column has a indexed number in the rows
                if column < 14: #if the column is less that 14, get the number ndex in the row
                    if self.indexx.get_loc(row) in self.color:
                        self.color[self.indexx.get_loc(row)].extend([column, column + 1, column + 2]) #highlight all the columns (6 bits)
                    else:
                        self.color[self.indexx.get_loc(row)] = [column, column + 1, column + 2] #add it in the in array
                    self.val = str(self.df.loc[row, column]) + str(self.df.loc[row, column + 1]) + str(self.df.loc[row, column + 2])
                #if the column is 14
                elif column == 14:
                    if self.indexx.get_loc(row) in self.color:
                        self.color[self.indexx.get_loc(row)].extend([column, column + 1]) #select column 14 and 15
                    else:
                        self.color[self.indexx.get_loc(row)] = [column, column + 1]
                    #column gedeed
                    self.color[
                        self.indexx.get_loc(hex(int(row, 16) + 16).replace("0x", "").zfill(6).upper())] = [0]
                    self.val = str(self.df.loc[row, column]) + str(self.df.loc[row, column + 1]) + str(
                        self.self.df.loc[hex(int(row, 16) + 16).replace("0x", "").zfill(6).upper(), 0])
                elif column == 15:
                    if self.indexx.get_loc(row) in self.color:
                        self.color[self.indexx.get_loc(row)].extend([column])
                    else:
                        self.color[self.indexx.get_loc(row)] = [column]

                    #2 column gedeed
                    self.color[
                        self.indexx.get_loc(hex(int(row, 16) + 16).replace("0x", "").zfill(6).upper())] = [0, 1]
                    self.val = str(self.df.loc[row, column]) + str(
                        self.df.loc[hex(int(row, 16) + 16).replace("0x", "").zfill(6).upper(), 0]) + str(
                        self.df.loc[hex(int(row, 16) + 16).replace("0x", "").zfill(6).upper(), 1])

                if leng == '05':
                    self.firstChar = self.val[0]
                    self.val = self.val[1:]
                for k, v in self.estab.items(): # estab items: PROGA : LISTA,ENDA W their addresses
                    #lista==lista
                    if k == self.label:
                        self.found_address = self.estab[k]['Address']
                        print("Program val=  ", self.found_address) #start add
                        break
                    for dk, dv in v['Labels'].items(): #dk: ENDA, dv: address
                        if dk == self.label:
                            self.found_address = dv
                            print("Label=  ",self.found_address)#el cell el bn8ayar feeha
                            break
                #if we found modification using el +
                if self.op == "+":
                    #update the value with the extref from M record
                    self.val = self.firstChar + hex(int(self.val, 16) + int(self.found_address, 16)).replace("0x", "").zfill(6).upper()[-int(leng):]
                # if we found modification using el -
                if self.op == "-":
                    # update the value with the extref from M record
                    y = int(self.val, 16) - int(self.found_address, 16)
                    #call the to_hex function to change the value to hex
                    self.val = self.firstChar + to_hex(y, 32).replace("0x", "").zfill(6).upper()[-int(leng):]
                if column < 14:
                    #highlighting the 3 columns to be changed
                    self.df.at[row, column] = self.val[0:2]
                    self.df.at[row, column + 1] = self.val[2:4]
                    self.df.at[row, column + 2] = self.val[4:6]
                if column == 14:
                    #highlight 14,15,first column in the new row
                    self.df.at[row, column] = self.val[0:2] #14
                    self.df.at[row, column + 1] = self.val[2:4] #15
                    self.df.at[hex(int(row, 16).replace("0x", "").zfill(6).upper() + 16), 0] = self.val[4:6] #first column in the new row
                if column == 15:
                    #select 15,first column in the new row, the second column in the new row
                    self.df.at[row, column] = self.val[0:2] #15
                    self.df.at[hex(int(row, 16) + 16).replace("0x", "").zfill(6).upper(), 0] = self.val[2:4] #first column in the new row
                    self.df.at[hex(int(row, 16) + 16).replace("0x", "").zfill(6).upper(), 1] = self.val[4:6] #second column in the new row

                print("The modi val is:   ", self.val)
        #print updated table
        print(self.df)


    def genTable(self):
        sicxe_root = Tk()
        sicxe_root.geometry("600x500")
        sicxe_root.title("Linker Loader")
        frame = Frame(sicxe_root)
        frame.pack(expand=True)
        column_hex = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        self.df.columns = column_hex
        table = Table(frame, dataframe=self.df, width=500, maxcellwidth=30)
        table.show()
        table.showindex = True

        #coloring the updated values according to k: dictionary key, and v: key values
        for k, val in self.color.items():
            print(k,val)
            table.setRowColors(rows=[k], cols=val, clr='#d8bfd8')
        sicxe_root.mainloop()
