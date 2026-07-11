from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import utils

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System | Developed by Zynox Tech")
        self.root.config(bg=utils.BG_DARK)
        self.root.resizable(True, True)
        self.root.focus_force()

        # Apply dark styling to ttk elements
        utils.apply_treeview_theme()

        #----------- variables -------------
        self.var_cat = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.var_pid = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        # Fetch Category and Supplier options
        self.fetch_cat_sup()

        # Main product details frame
        product_Frame = Frame(self.root, bd=0, bg=utils.BG_CARD)
        product_Frame.place(x=20, y=10, width=440, height=480)

        #------------ title --------------
        title = Label(product_Frame, text="Manage Product Details", font=utils.FONT_SUBTITLE, bg=utils.COLOR_PRIMARY, fg="white")
        title.pack(side=TOP, fill=X, pady=(0, 15))

        self.lbl_category = Label(product_Frame, text="Category", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        self.lbl_category.place(x=30, y=60)
        self.lbl_supplier = Label(product_Frame, text="Supplier", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        self.lbl_supplier.place(x=30, y=110)
        self.lbl_product_name = Label(product_Frame, text="Name", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        self.lbl_product_name.place(x=30, y=160)
        self.lbl_price = Label(product_Frame, text="Price", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        self.lbl_price.place(x=30, y=210)
        self.lbl_qty = Label(product_Frame, text="Quantity", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        self.lbl_qty.place(x=30, y=260)
        self.lbl_status = Label(product_Frame, text="Status", font=utils.FONT_BODY, bg=utils.BG_CARD, fg=utils.FG_LIGHT)
        self.lbl_status.place(x=30, y=310)

        self.cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat, values=self.cat_list, state='readonly', justify=CENTER, font=utils.FONT_BODY)
        self.cmb_cat.place(x=160, y=60, width=220, height=28)
        if self.cat_list:
            self.cmb_cat.current(0)

        self.cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup, values=self.sup_list, state='readonly', justify=CENTER, font=utils.FONT_BODY)
        self.cmb_sup.place(x=160, y=110, width=220, height=28)
        if self.sup_list:
            self.cmb_sup.current(0)

        self.txt_name = Entry(product_Frame, textvariable=self.var_name, font=utils.FONT_BODY)
        self.txt_name.place(x=160, y=160, width=220, height=28)
        utils.style_entry(self.txt_name)

        self.txt_price = Entry(product_Frame, textvariable=self.var_price, font=utils.FONT_BODY)
        self.txt_price.place(x=160, y=210, width=220, height=28)
        utils.style_entry(self.txt_price)

        self.txt_qty = Entry(product_Frame, textvariable=self.var_qty, font=utils.FONT_BODY)
        self.txt_qty.place(x=160, y=260, width=220, height=28)
        utils.style_entry(self.txt_qty)

        self.cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active", "Inactive"), state='readonly', justify=CENTER, font=utils.FONT_BODY)
        self.cmb_status.place(x=160, y=310, width=220, height=28)
        self.cmb_status.current(0)

        #-------------- buttons -----------------
        self.btn_add = Button(product_Frame, text="Save", command=self.add)
        self.btn_add.place(x=10, y=400, width=95, height=35)
        utils.style_button(self.btn_add, bg_color=utils.COLOR_PRIMARY, hover_color=utils.COLOR_PRIMARY_HOVER)

        self.btn_update = Button(product_Frame, text="Update", command=self.update)
        self.btn_update.place(x=115, y=400, width=95, height=35)
        utils.style_button(self.btn_update, bg_color=utils.COLOR_SUCCESS, hover_color=utils.COLOR_SUCCESS_HOVER)

        self.btn_delete = Button(product_Frame, text="Delete", command=self.delete)
        self.btn_delete.place(x=220, y=400, width=95, height=35)
        utils.style_button(self.btn_delete, bg_color=utils.COLOR_DANGER, hover_color=utils.COLOR_DANGER_HOVER)

        self.btn_clear = Button(product_Frame, text="Clear", command=self.clear)
        self.btn_clear.place(x=325, y=400, width=95, height=35)
        utils.style_button(self.btn_clear, bg_color=utils.COLOR_WARNING, hover_color=utils.COLOR_WARNING_HOVER)

        #---------- Search Frame -------------
        self.SearchFrame = LabelFrame(self.root, text="Search Product", font=utils.FONT_BODY_BOLD, bd=2, bg=utils.BG_DARK, fg=utils.FG_LIGHT)
        self.SearchFrame.place(x=480, y=10, width=600, height=80)

        #------------ options ----------------
        self.cmb_search = ttk.Combobox(self.SearchFrame, textvariable=self.var_searchby, values=("Select", "Category", "Supplier", "Name"), state='readonly', justify=CENTER, font=utils.FONT_BODY)
        self.cmb_search.place(x=10, y=10, width=180, height=30)
        self.cmb_search.current(0)

        self.txt_search = Entry(self.SearchFrame, textvariable=self.var_searchtxt, font=utils.FONT_BODY)
        self.txt_search.place(x=200, y=10, width=200, height=30)
        utils.style_entry(self.txt_search)

        self.btn_search = Button(self.SearchFrame, text="Search", command=self.search)
        self.btn_search.place(x=420, y=10, width=150, height=30)
        utils.style_button(self.btn_search, bg_color=utils.COLOR_PRIMARY, hover_color=utils.COLOR_PRIMARY_HOVER)

        #------------ product details -------------
        product_frame = Frame(self.root, bd=0, bg=utils.BG_DARK)
        product_frame.place(x=480, y=100, width=600, height=390)

        scrolly = ttk.Scrollbar(product_frame, orient=VERTICAL)
        scrollx = ttk.Scrollbar(product_frame, orient=HORIZONTAL)
        
        self.ProductTable = ttk.Treeview(product_frame, columns=("pid", "Category", "Supplier", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid", text="P ID")
        self.ProductTable.heading("Category", text="Category")
        self.ProductTable.heading("Supplier", text="Supplier")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("qty", text="Quantity")
        self.ProductTable.heading("status", text="Status")
        
        self.ProductTable["show"] = "headings"
        self.ProductTable.column("pid", width=50, anchor="center")
        self.ProductTable.column("Category", width=100)
        self.ProductTable.column("Supplier", width=100)
        self.ProductTable.column("name", width=120)
        self.ProductTable.column("price", width=70, anchor="center")
        self.ProductTable.column("qty", width=70, anchor="center")
        self.ProductTable.column("status", width=70, anchor="center")
        
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        
        self.show()

#-----------------------------------------------------------------------------------------------------
    def fetch_cat_sup(self):
        self.cat_list.append("Select")
        self.sup_list.append("Select")
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select name from category")
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            
            cur.execute("select name from supplier")
            sup = cur.fetchall()
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or self.var_sup.get() == "Select" or self.var_sup.get() == "Empty" or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("Select * from product where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Product already present", parent=self.root)
                else:
                    cur.execute("insert into product(Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        try:
            f = self.ProductTable.focus()
            content = (self.ProductTable.item(f))
            row = content['values']
            if not row:
                return
            self.var_pid.set(row[0])
            self.var_cat.set(row[1])
            self.var_sup.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.var_status.set(row[6])
        except Exception as ex:
            pass

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select product from list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    cur.execute("update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select Product from the list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("delete from product where pid=?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute("select * from product where " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()