from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile
import utils

class billClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.title("Inventory Management System | Developed by Zynox Tech")
        self.root.resizable(False, False)
        self.root.config(bg=utils.BG_DARK)
        self.cart_list = []
        self.chk_print = 0

        # Apply dark styling to ttk elements
        utils.apply_treeview_theme()

        #------------- title --------------
        logo_path = utils.resolve_path("Inventory-Management-System/images/logo1.png")
        self.icon_title = PhotoImage(file=logo_path)
        
        self.title_label = Label(
            self.root,
            text=" Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=utils.FONT_TITLE,
            bg=utils.BG_CARD,
            fg=utils.FG_LIGHT,
            anchor="w",
            padx=20
        )
        self.title_label.place(x=0, y=0, relwidth=1, height=70)

        #------------ logout button -----------
        self.btn_logout = Button(
            self.root,
            text="Logout",
            font=utils.FONT_BODY_BOLD,
            command=self.logout
        )
        self.btn_logout.place(x=1170, y=15, height=40, width=150)
        utils.style_button(self.btn_logout, bg_color=utils.COLOR_DANGER, hover_color=utils.COLOR_DANGER_HOVER)

        #------------ clock -----------------
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",
            font=utils.FONT_BODY,
            bg=utils.BG_DARK,
            fg=utils.FG_MUTED
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #------------ footer -----------------
        self.lbl_footer = Label(
            self.root,
            text=utils.DEV_TEXT,
            font=utils.FONT_FOOTER,
            bg=utils.BG_DARK,
            fg=utils.FG_MUTED,
            pady=5
        )
        self.lbl_footer.pack(side=BOTTOM, fill=X)

        #-------------- product frame -----------------
        ProductFrame1 = Frame(self.root, bd=0, bg=utils.BG_CARD)
        ProductFrame1.place(x=10, y=110, width=410, height=540)

        pTitle = Label(
            ProductFrame1,
            text="All Products",
            font=utils.FONT_SUBTITLE,
            bg=utils.COLOR_PRIMARY,
            fg="white"
        )
        pTitle.pack(side=TOP, fill=X, pady=(0, 10))
        
        self.var_search = StringVar()

        ProductFrame2 = Frame(ProductFrame1, bd=0, bg=utils.BG_CARD)
        ProductFrame2.place(x=10, y=45, width=390, height=90)

        lbl_search_title = Label(ProductFrame2, text="Search Product | By Name", font=utils.FONT_BODY_BOLD, bg=utils.BG_CARD, fg=utils.COLOR_SUCCESS)
        lbl_search_title.place(x=2, y=5)
        
        lbl_search_name = Label(ProductFrame2, text="Product Name", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        lbl_search_name.place(x=2, y=45)
        
        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=utils.FONT_BODY)
        txt_search.place(x=115, y=45, width=150, height=26)
        utils.style_entry(txt_search)
        
        btn_search = Button(ProductFrame2, text="Search", command=self.search)
        btn_search.place(x=275, y=45, width=105, height=26)
        utils.style_button(btn_search, bg_color=utils.COLOR_PRIMARY, hover_color=utils.COLOR_PRIMARY_HOVER)
        
        btn_show_all = Button(ProductFrame2, text="Show All", command=self.show)
        btn_show_all.place(x=275, y=10, width=105, height=26)
        utils.style_button(btn_show_all, bg_color=utils.COLOR_SUCCESS, hover_color=utils.COLOR_SUCCESS_HOVER)

        ProductFrame3 = Frame(ProductFrame1, bd=0, bg=utils.BG_CARD)
        ProductFrame3.place(x=10, y=140, width=390, height=365)

        scrolly = ttk.Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = ttk.Scrollbar(ProductFrame3, orient=HORIZONTAL)
        
        self.product_Table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        
        self.product_Table.heading("pid", text="P ID")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="Quantity")
        self.product_Table.heading("status", text="Status")
        self.product_Table["show"] = "headings"
        self.product_Table.column("pid", width=40, anchor="center")
        self.product_Table.column("name", width=120)
        self.product_Table.column("price", width=70, anchor="center")
        self.product_Table.column("qty", width=60, anchor="center")
        self.product_Table.column("status", width=70, anchor="center")
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)
        
        lbl_note = Label(ProductFrame1, text="Note: 'Enter 0 Quantity to remove product from Cart'", font=utils.FONT_SMALL, anchor="w", bg=utils.BG_CARD, fg=utils.COLOR_DANGER)
        lbl_note.pack(side=BOTTOM, fill=X, pady=5)

        #-------------- customer frame ---------------
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        CustomerFrame = Frame(self.root, bd=0, bg=utils.BG_CARD)
        CustomerFrame.place(x=430, y=110, width=510, height=75)

        cTitle = Label(CustomerFrame, text="Customer Details", font=utils.FONT_BODY_BOLD, bg=utils.COLOR_PRIMARY, fg="white")
        cTitle.pack(side=TOP, fill=X, pady=(0, 5))

        lbl_name = Label(CustomerFrame, text="Name", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        lbl_name.place(x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.var_cname, font=utils.FONT_BODY)
        txt_name.place(x=70, y=35, width=160, height=26)
        utils.style_entry(txt_name)
        
        lbl_contact = Label(CustomerFrame, text="Contact No.", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        lbl_contact.place(x=250, y=35)
        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=utils.FONT_BODY)
        txt_contact.place(x=350, y=35, width=150, height=26)
        utils.style_entry(txt_contact)

        Cal_Cart_Frame = Frame(self.root, bd=0, bg=utils.BG_CARD)
        Cal_Cart_Frame.place(x=430, y=195, width=510, height=350)

        #--------------- calculator frame ---------------------
        self.var_cal_input = StringVar()

        Cal_Frame = Frame(Cal_Cart_Frame, bd=0, bg=utils.BG_CARD)
        Cal_Frame.place(x=5, y=5, width=255, height=340)

        # Style calculator screen
        self.txt_cal_input = Entry(
            Cal_Frame,
            textvariable=self.var_cal_input,
            font=('arial', 14, 'bold'),
            bg=utils.COLOR_ENTRY_BG,
            fg=utils.COLOR_ENTRY_FG,
            bd=0,
            highlightthickness=1,
            highlightbackground=utils.COLOR_ENTRY_BORDER,
            justify=RIGHT,
            state='readonly'
        )
        self.txt_cal_input.grid(row=0, columnspan=4, ipady=12, padx=2, pady=5, sticky="nsew")

        # Calculator Button Layout
        def make_cal_btn(text, r, c, cmd, bg=utils.BG_DARK, hover=utils.COLOR_ENTRY_BORDER):
            btn = Button(
                Cal_Frame,
                text=text,
                font=('arial', 12, 'bold'),
                command=cmd,
                bd=0,
                relief=FLAT,
                cursor="hand2",
                bg=bg,
                fg="white",
                activebackground=hover,
                activeforeground="white"
            )
            btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
            btn.bind("<Enter>", lambda e: btn.config(bg=hover))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg))
            return btn

        # Number buttons and operators
        make_cal_btn("7", 1, 0, lambda: self.get_input(7))
        make_cal_btn("8", 1, 1, lambda: self.get_input(8))
        make_cal_btn("9", 1, 2, lambda: self.get_input(9))
        make_cal_btn("+", 1, 3, lambda: self.get_input('+'), bg=utils.COLOR_PRIMARY, hover=utils.COLOR_PRIMARY_HOVER)

        make_cal_btn("4", 2, 0, lambda: self.get_input(4))
        make_cal_btn("5", 2, 1, lambda: self.get_input(5))
        make_cal_btn("6", 2, 2, lambda: self.get_input(6))
        make_cal_btn("-", 2, 3, lambda: self.get_input('-'), bg=utils.COLOR_PRIMARY, hover=utils.COLOR_PRIMARY_HOVER)

        make_cal_btn("1", 3, 0, lambda: self.get_input(1))
        make_cal_btn("2", 3, 1, lambda: self.get_input(2))
        make_cal_btn("3", 3, 2, lambda: self.get_input(3))
        make_cal_btn("*", 3, 3, lambda: self.get_input('*'), bg=utils.COLOR_PRIMARY, hover=utils.COLOR_PRIMARY_HOVER)

        make_cal_btn("0", 4, 0, lambda: self.get_input(0))
        make_cal_btn("C", 4, 1, self.clear_cal, bg=utils.COLOR_WARNING, hover=utils.COLOR_WARNING_HOVER)
        make_cal_btn("=", 4, 2, self.perform_cal, bg=utils.COLOR_SUCCESS, hover=utils.COLOR_SUCCESS_HOVER)
        make_cal_btn("/", 4, 3, lambda: self.get_input('/'), bg=utils.COLOR_PRIMARY, hover=utils.COLOR_PRIMARY_HOVER)

        # Row and column resizing configs
        for r in range(5):
            Cal_Frame.rowconfigure(r, weight=1)
        for c in range(4):
            Cal_Frame.columnconfigure(c, weight=1)

        #------------------ cart frame --------------------
        Cart_Frame = Frame(Cal_Cart_Frame, bd=0, bg=utils.BG_CARD)
        Cart_Frame.place(x=265, y=5, width=240, height=340)
        self.cartTitle = Label(Cart_Frame, text="Cart   Total: [0]", font=utils.FONT_BODY_BOLD, bg=utils.COLOR_PRIMARY, fg="white")
        self.cartTitle.pack(side=TOP, fill=X, pady=(0, 5))

        scrolly = ttk.Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx = ttk.Scrollbar(Cart_Frame, orient=HORIZONTAL)
        
        self.CartTable = ttk.Treeview(Cart_Frame, columns=("pid", "name", "price", "qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        self.CartTable.heading("pid", text="P ID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="Qty")
        self.CartTable["show"] = "headings"
        self.CartTable.column("pid", width=40, anchor="center")
        self.CartTable.column("name", width=90)
        self.CartTable.column("price", width=60, anchor="center")
        self.CartTable.column("qty", width=35, anchor="center")
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        #-------------- add cart widgets frame ---------------
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        Add_CartWidgets_Frame = Frame(self.root, bd=0, bg=utils.BG_CARD)
        Add_CartWidgets_Frame.place(x=430, y=555, width=510, height=95)

        lbl_p_name = Label(Add_CartWidgets_Frame, text="Product Name", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        lbl_p_name.place(x=5, y=2)
        txt_p_name = Entry(Add_CartWidgets_Frame, textvariable=self.var_pname, font=utils.FONT_BODY, state='readonly', relief=FLAT, bg=utils.COLOR_ENTRY_BG, fg=utils.FG_MUTED)
        txt_p_name.place(x=5, y=28, width=170, height=26)

        lbl_p_price = Label(Add_CartWidgets_Frame, text="Price Per Qty", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        lbl_p_price.place(x=190, y=2)
        txt_p_price = Entry(Add_CartWidgets_Frame, textvariable=self.var_price, font=utils.FONT_BODY, state='readonly', relief=FLAT, bg=utils.COLOR_ENTRY_BG, fg=utils.FG_MUTED)
        txt_p_price.place(x=190, y=28, width=140, height=26)

        lbl_p_qty = Label(Add_CartWidgets_Frame, text="Quantity", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        lbl_p_qty.place(x=350, y=2)
        txt_p_qty = Entry(Add_CartWidgets_Frame, textvariable=self.var_qty, font=utils.FONT_BODY)
        txt_p_qty.place(x=350, y=28, width=145, height=26)
        utils.style_entry(txt_p_qty)

        self.lbl_inStock = Label(Add_CartWidgets_Frame, text="In Stock", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.COLOR_INFO)
        self.lbl_inStock.place(x=5, y=62)

        btn_clear_cart = Button(Add_CartWidgets_Frame, command=self.clear_cart, text="Clear")
        btn_clear_cart.place(x=190, y=60, width=140, height=30)
        utils.style_button(btn_clear_cart, bg_color=utils.COLOR_WARNING, hover_color=utils.COLOR_WARNING_HOVER)
        
        btn_add_cart = Button(Add_CartWidgets_Frame, command=self.add_update_cart, text="Add | Update")
        btn_add_cart.place(x=350, y=60, width=145, height=30)
        utils.style_button(btn_add_cart, bg_color=utils.COLOR_SUCCESS, hover_color=utils.COLOR_SUCCESS_HOVER)
        
        #------------------- billing area -------------------
        billFrame = Frame(self.root, bd=0, bg=utils.BG_CARD)
        billFrame.place(x=955, y=110, width=385, height=410)

        BTitle = Label(billFrame, text="Customer Bill Area", font=utils.FONT_SUBTITLE, bg=utils.COLOR_PRIMARY, fg="white")
        BTitle.pack(side=TOP, fill=X, pady=(0, 5))
        
        scrolly = ttk.Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)
        utils.style_text(self.txt_bill_area)

        #------------------- billing buttons -----------------------
        billMenuFrame = Frame(self.root, bd=0, bg=utils.BG_CARD)
        billMenuFrame.place(x=955, y=525, width=385, height=125)

        self.lbl_amnt = Label(billMenuFrame, text="Bill Amount\n[0]", font=utils.FONT_BODY_BOLD, bg=utils.COLOR_INFO, fg="white")
        self.lbl_amnt.place(x=5, y=5, width=115, height=50)

        self.lbl_discount = Label(billMenuFrame, text="Discount\n[5%]", font=utils.FONT_BODY_BOLD, bg=utils.COLOR_PRIMARY, fg="white")
        self.lbl_discount.place(x=125, y=5, width=115, height=50)

        self.lbl_net_pay = Label(billMenuFrame, text="Net Pay\n[0]", font=utils.FONT_BODY_BOLD, bg=utils.COLOR_SUCCESS, fg="white")
        self.lbl_net_pay.place(x=245, y=5, width=135, height=50)

        btn_print = Button(billMenuFrame, text="Print", command=self.print_bill)
        btn_print.place(x=5, y=65, width=115, height=45)
        utils.style_button(btn_print, bg_color=utils.COLOR_PRIMARY, hover_color=utils.COLOR_PRIMARY_HOVER)

        btn_clear_all = Button(billMenuFrame, text="Clear All", command=self.clear_all)
        btn_clear_all.place(x=125, y=65, width=115, height=45)
        utils.style_button(btn_clear_all, bg_color=utils.COLOR_DANGER, hover_color=utils.COLOR_DANGER_HOVER)

        btn_generate = Button(billMenuFrame, text="Generate Bill", command=self.generate_bill)
        btn_generate.place(x=245, y=65, width=135, height=45)
        utils.style_button(btn_generate, bg_color=utils.COLOR_SUCCESS, hover_color=utils.COLOR_SUCCESS_HOVER)

        self.show()
        self.update_date_time()

    #---------------------- all functions ------------------------------
    def logout(self):
        op = messagebox.askyesno("Logout", "Do you really want to logout?", parent=self.root)
        if op:
            self.root.destroy()

    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        try:
            self.var_cal_input.set(str(eval(result)))
        except Exception:
            self.var_cal_input.set("Error")

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows = cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('', END, values=row)
            self.var_search.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%" + self.var_search.get() + "%' and status='Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        try:
            f = self.product_Table.focus()
            content = (self.product_Table.item(f))
            row = content['values']
            if not row:
                return
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
            self.var_stock.set(row[3])
            self.var_qty.set('1')
        except Exception:
            pass
    
    def get_data_cart(self, ev):
        try:
            f = self.CartTable.focus()
            content = (self.CartTable.item(f))
            row = content['values']
            if not row:
                return
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_qty.set(row[3])
            self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
            self.var_stock.set(row[4])
        except Exception:
            pass
        
    def add_update_cart(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)
        elif self.var_qty.get() == "":
            messagebox.showerror("Error", "Quantity is required", parent=self.root)
        elif not self.var_qty.get().isdigit():
            messagebox.showerror("Error", "Quantity must be a valid integer", parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror("Error", "Invalid Quantity. Out of Stock", parent=self.root)
        else:
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]
            
            present = "no"
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = "yes"
                    break
                index_ += 1
            
            if present == "yes":
                op = messagebox.askyesno("Confirm", "Product already present.\nDo you want to Update or Remove from the Cart?", parent=self.root)
                if op:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][3] = self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            
            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amnt = self.bill_amnt + (float(row[2]) * int(row[3]))
        self.discount = (self.bill_amnt * 5) / 100
        self.net_pay = self.bill_amnt - self.discount
        self.lbl_amnt.config(text=f"Bill Amnt\n{str(self.bill_amnt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart   Total: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get() == "" or self.var_contact.get() == "":
            messagebox.showerror("Error", "Customer Details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please Add product to the Cart!!!", parent=self.root)
        else:
            #--------- bill top -----------------
            self.bill_top()
            #--------- bill middle --------------
            self.bill_middle()
            #--------- bill bottom --------------
            self.bill_bottom()

            bill_dir = utils.resolve_path('Inventory-Management-System/bill')
            if not os.path.exists(bill_dir):
                try:
                    os.makedirs(bill_dir)
                except Exception:
                    pass
            
            bill_file_path = os.path.join(bill_dir, f"{str(self.invoice)}.txt")
            try:
                with open(bill_file_path, 'w') as fp:
                    fp.write(self.txt_bill_area.get('1.0', END))
                messagebox.showinfo("Saved", "Bill has been generated successfully", parent=self.root)
                self.chk_print = 1
            except Exception as ex:
                messagebox.showerror("Error", f"Could not save bill: {str(ex)}", parent=self.root)

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
\t  Zynox Tech Inventory
\tWebsite: {utils.WEBSITE}
\tEmail: {utils.EMAIL}
{str("="*46)}
 Customer Name: {self.var_cname.get()}
 Ph. no. : {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*46)}
 Product Name\t\t\tQTY\tPrice
{str("="*46)}
'''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("="*46)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*46)}\n
'''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    status = "Inactive"
                else:
                    status = "Active"
                
                price = float(row[2]) * int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END, f"\n {name}\t\t\t{row[3]}\tRs.{price}")
                
                #------------- update qty in product table --------------
                cur.execute("update product set qty=?,status=? where pid=?", (
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text="In Stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.clear_cart()
        self.show()
        self.show_cart()
        self.var_cname.set("")
        self.var_contact.set("")
        self.chk_print = 0
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text="Cart   Total: [0]")
        self.var_search.set("")
        self.lbl_amnt.config(text="Bill Amount\n[0]")
        self.lbl_net_pay.config(text="Net Pay\n[0]")
        
    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(1000, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo("Print", "Please wait while printing", parent=self.root)
            new_file = tempfile.mktemp('.txt')
            try:
                with open(new_file, 'w') as f:
                    f.write(self.txt_bill_area.get('1.0', END))
                os.startfile(new_file, 'print')
            except Exception as ex:
                messagebox.showerror("Error", f"Could not print: {str(ex)}", parent=self.root)
        else:
            messagebox.showinfo("Print", "Please generate bill to print the receipt", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = billClass(root)
    root.mainloop()