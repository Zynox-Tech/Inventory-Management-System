from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import sqlite3
import os
import utils

from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.title("Inventory Management System | Developed by Zynox Tech")
        self.root.resizable(True, True)
        self.root.config(bg=utils.BG_DARK)

        # Setup custom styles for Treeview/Combobox
        utils.apply_treeview_theme()

        #------------- title --------------
        # Resolve logo image path
        logo_path = utils.resolve_path("Inventory-Management-System/images/logo1.png")
        self.icon_title = PhotoImage(file=logo_path)
        
        # Header title banner
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

        #---------------- left menu ---------------
        menu_img_path = utils.resolve_path("Inventory-Management-System/images/menu_im.png")
        self.MenuLogo = Image.open(menu_img_path)
        self.MenuLogo = self.MenuLogo.resize((196, 170))
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)
        
        LeftMenu = Frame(self.root, bd=0, bg=utils.BG_CARD)
        LeftMenu.place(x=0, y=102, width=200, height=565)

        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo, bg=utils.BG_CARD)
        lbl_menuLogo.pack(side=TOP, fill=X)

        lbl_menu = Label(
            LeftMenu,
            text="MENU",
            font=utils.FONT_SUBTITLE,
            bg=utils.COLOR_PRIMARY,
            fg="white"
        )
        lbl_menu.pack(side=TOP, fill=X, pady=(10, 5))

        side_icon_path = utils.resolve_path("Inventory-Management-System/images/side.png")
        self.icon_side = PhotoImage(file=side_icon_path)
        
        # Menu Button Config
        self.btn_employee = Button(LeftMenu, text=" Employee", command=self.employee, image=self.icon_side, compound=LEFT, padx=15, anchor="w")
        self.btn_employee.pack(side=TOP, fill=X, pady=2)
        utils.style_button(self.btn_employee, bg_color=utils.BG_CARD, hover_color=utils.COLOR_PRIMARY)
        
        self.btn_supplier = Button(LeftMenu, text=" Supplier", command=self.supplier, image=self.icon_side, compound=LEFT, padx=15, anchor="w")
        self.btn_supplier.pack(side=TOP, fill=X, pady=2)
        utils.style_button(self.btn_supplier, bg_color=utils.BG_CARD, hover_color=utils.COLOR_PRIMARY)
        
        self.btn_category = Button(LeftMenu, text=" Category", command=self.category, image=self.icon_side, compound=LEFT, padx=15, anchor="w")
        self.btn_category.pack(side=TOP, fill=X, pady=2)
        utils.style_button(self.btn_category, bg_color=utils.BG_CARD, hover_color=utils.COLOR_PRIMARY)
        
        self.btn_product = Button(LeftMenu, text=" Products", command=self.product, image=self.icon_side, compound=LEFT, padx=15, anchor="w")
        self.btn_product.pack(side=TOP, fill=X, pady=2)
        utils.style_button(self.btn_product, bg_color=utils.BG_CARD, hover_color=utils.COLOR_PRIMARY)
        
        self.btn_sales = Button(LeftMenu, text=" Sales", command=self.sales, image=self.icon_side, compound=LEFT, padx=15, anchor="w")
        self.btn_sales.pack(side=TOP, fill=X, pady=2)
        utils.style_button(self.btn_sales, bg_color=utils.BG_CARD, hover_color=utils.COLOR_PRIMARY)
        
        self.btn_exit = Button(LeftMenu, text=" Exit", command=self.root.destroy, image=self.icon_side, compound=LEFT, padx=15, anchor="w")
        self.btn_exit.pack(side=TOP, fill=X, pady=2)
        utils.style_button(self.btn_exit, bg_color=utils.BG_CARD, hover_color=utils.COLOR_DANGER)

        #----------- content ----------------
        self.lbl_employee = Label(
            self.root,
            text="Total Employee\n[ 0 ]",
            bd=0,
            bg=utils.COLOR_INFO,
            fg="white",
            font=utils.FONT_SUBTITLE
        )
        self.lbl_employee.place(x=290, y=150, height=150, width=310)

        self.lbl_supplier = Label(
            self.root,
            text="Total Supplier\n[ 0 ]",
            bd=0,
            bg=utils.COLOR_WARNING,
            fg="white",
            font=utils.FONT_SUBTITLE
        )
        self.lbl_supplier.place(x=640, y=150, height=150, width=310)

        self.lbl_category = Label(
            self.root,
            text="Total Category\n[ 0 ]",
            bd=0,
            bg=utils.COLOR_PRIMARY,
            fg="white",
            font=utils.FONT_SUBTITLE
        )
        self.lbl_category.place(x=990, y=150, height=150, width=310)

        self.lbl_product = Label(
            self.root,
            text="Total Product\n[ 0 ]",
            bd=0,
            bg="#8B5CF6", # purple
            fg="white",
            font=utils.FONT_SUBTITLE
        )
        self.lbl_product.place(x=460, y=340, height=150, width=310)

        self.lbl_sales = Label(
            self.root,
            text="Total Sales\n[ 0 ]",
            bd=0,
            bg=utils.COLOR_SUCCESS,
            fg="white",
            font=utils.FONT_SUBTITLE
        )
        self.lbl_sales.place(x=810, y=340, height=150, width=310)

        #------------ footer -----------------
        lbl_footer = Label(
            self.root,
            text=utils.DEV_TEXT,
            font=utils.FONT_FOOTER,
            bg=utils.BG_DARK,
            fg=utils.FG_MUTED,
            pady=10
        )
        lbl_footer.pack(side=BOTTOM, fill=X)

        self.update_content()

    #-------------- functions ----------------
    def logout(self):
        op = messagebox.askyesno("Logout", "Do you really want to logout?", parent=self.root)
        if op:
            self.root.destroy()

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[ {str(len(product))} ]")

            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[ {str(len(category))} ]")

            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n[ {str(len(employee))} ]")

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n[ {str(len(supplier))} ]")
            
            bill_dir = utils.resolve_path("Inventory-Management-System/bill")
            bill = 0
            if os.path.exists(bill_dir):
                bill = len([f for f in os.listdir(bill_dir) if f.endswith('.txt')])
            self.lbl_sales.config(text=f"Total Sales\n[ {str(bill)} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(1000, self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()