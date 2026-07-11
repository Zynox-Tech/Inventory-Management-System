from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os
import utils

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System | Developed by Zynox Tech")
        self.root.config(bg=utils.BG_DARK)
        self.root.resizable(True, True)
        self.root.focus_force()

        # Apply dark styling to ttk elements
        utils.apply_treeview_theme()

        self.blll_list = []
        self.var_invoice = StringVar()
        
        #--------------- title ---------------------
        self.lbl_title = Label(
            self.root,
            text="View Customer Bills",
            font=utils.FONT_SUBTITLE,
            bg=utils.COLOR_PRIMARY,
            fg="white"
        )
        self.lbl_title.pack(side=TOP, fill=X, padx=20, pady=20)
        
        self.lbl_invoice = Label(self.root, text="Invoice No.", font=utils.FONT_BODY, bg=utils.BG_DARK, fg=utils.FG_LIGHT)
        self.lbl_invoice.place(x=50, y=95)
        
        self.txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=utils.FONT_BODY)
        self.txt_invoice.place(x=160, y=95, width=180, height=30)
        utils.style_entry(self.txt_invoice)

        self.btn_search = Button(self.root, text="Search", command=self.search)
        self.btn_search.place(x=360, y=95, width=120, height=30)
        utils.style_button(self.btn_search, bg_color=utils.COLOR_PRIMARY, hover_color=utils.COLOR_PRIMARY_HOVER)

        self.btn_clear = Button(self.root, text="Clear", command=self.clear)
        self.btn_clear.place(x=495, y=95, width=120, height=30)
        utils.style_button(self.btn_clear, bg_color=utils.COLOR_WARNING, hover_color=utils.COLOR_WARNING_HOVER)

        #----------------- bill list -------------------
        sales_Frame = Frame(self.root, bd=0, bg=utils.BG_DARK)
        sales_Frame.place(x=50, y=140, width=200, height=330)

        scrolly = ttk.Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sales_List = Listbox(
            sales_Frame,
            font=utils.FONT_BODY,
            bg=utils.BG_CARD,
            fg=utils.FG_LIGHT,
            selectbackground=utils.COLOR_PRIMARY,
            selectforeground="white",
            bd=0,
            highlightthickness=1,
            highlightbackground=utils.COLOR_ENTRY_BORDER,
            highlightcolor=utils.COLOR_PRIMARY,
            yscrollcommand=scrolly.set
        )
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        #--------------- bill area ----------------------
        bill_Frame = Frame(self.root, bd=0, bg=utils.BG_DARK)
        bill_Frame.place(x=280, y=140, width=400, height=330)
        
        self.lbl_title2 = Label(
            bill_Frame,
            text="Customer Bill Area",
            font=utils.FONT_BODY_BOLD,
            bg=utils.COLOR_PRIMARY,
            fg="white"
        )
        self.lbl_title2.pack(side=TOP, fill=X)
        
        scrolly2 = ttk.Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area = Text(bill_Frame, yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)
        utils.style_text(self.bill_area)

        #------------- image -----------------
        img_path = utils.resolve_path("Inventory-Management-System/images/cat2.jpg")
        self.bill_photo = Image.open(img_path)
        self.bill_photo = self.bill_photo.resize((370, 330))
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        self.lbl_image = Label(self.root, image=self.bill_photo, bd=0, bg=utils.BG_DARK)
        self.lbl_image.place(x=700, y=140)
        
        self.show()

#----------------------------------------------------------------------------------------------------
    def show(self):
        del self.blll_list[:]
        self.Sales_List.delete(0, END)
        bill_dir = utils.resolve_path('Inventory-Management-System/bill')
        if not os.path.exists(bill_dir):
            try:
                os.makedirs(bill_dir)
            except Exception:
                pass
        
        if os.path.exists(bill_dir):
            for i in os.listdir(bill_dir):
                if i.split('.')[-1] == 'txt':
                    self.Sales_List.insert(END, i)
                    self.blll_list.append(i.split('.')[0])

    def get_data(self, ev):
        try:
            index_ = self.Sales_List.curselection()
            if not index_:
                return
            file_name = self.Sales_List.get(index_)
            self.bill_area.delete('1.0', END)
            
            bill_path = os.path.join(utils.resolve_path('Inventory-Management-System/bill'), file_name)
            with open(bill_path, 'r') as fp:
                for i in fp:
                    self.bill_area.insert(END, i)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)
        else:
            if self.var_invoice.get() in self.blll_list:
                bill_path = os.path.join(utils.resolve_path('Inventory-Management-System/bill'), f"{self.var_invoice.get()}.txt")
                try:
                    self.bill_area.delete('1.0', END)
                    with open(bill_path, 'r') as fp:
                        for i in fp:
                            self.bill_area.insert(END, i)
                except Exception as ex:
                    messagebox.showerror("Error", f"Error reading file : {str(ex)}", parent=self.root)
            else:
                messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0', END)
        self.var_invoice.set("")

if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()