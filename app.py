from tkinter import *
from tkinter import filedialog, messagebox, ttk
from sic import Sic
from sicxe import SicXE
from tkinter import *
import tkinter as tk


class Application:
    #gui design
    def __init__(self, master) -> None:
        self.menu = None
        self.master = master
        self.master = master
        master.configure(bg='#000000')
        tk.Label(master,
                 text="", bg='#000000').pack()
        tk.Label(master,
                 text="", bg='#000000').pack()
        tk.Label(master,
                 text="", bg='#000000').pack()
        tk.Label(master,
                 text="Project Systems Phase 2",
                 fg="#d8bfd8",
                 font=("Times", 60), bg='#000000').pack()
        tk.Label(master,
                 text="Choose Absolute Loader or Linker Loader",
                 fg="#d8bfd8",
                 bg="#000000",
                 font="Helvetica 24 bold italic", padx=20, pady=20).pack()
        self.radio = StringVar()
        R1 = Radiobutton(master, text="Absolute Loader", fg="#d8bfd8",bg='#000000', variable=self.radio, value="sic", command=self.handleSelect, font=("Times", 30))
        R1.pack(anchor=CENTER)
        R2 = Radiobutton(master, text="Linker Loader", fg="#d8bfd8",bg='#000000', variable=self.radio ,value="sicxe", command=self.handleSelect,font=("Times", 30))
        R2.pack(anchor=CENTER)
        tk.Label(master,
                 text="", bg='#000000').pack()
        tk.Label(master,
                 text="", bg='#000000').pack()
        tk.Label(master,
                 text="", bg='#000000').pack()


    def handleSelect(self):
        #radio button to select(sic or sicxe)
        selection = self.radio.get()
        print(selection)
        if selection == "sic":
            sic = Sic()
        if selection == "sicxe":
            sic_xe = SicXE()
