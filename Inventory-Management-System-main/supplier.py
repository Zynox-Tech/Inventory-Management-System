from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import utils

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System | Developed by Zynox Tech")
        self.root.config(bg=utils.BG_DARK)
        self.root.resizable(True, True)
        self.root.focus_force()

        # Apply dark styling to ttk elements
        utils.apply_treeview_theme()

        #------------ all variables --------------
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        
        #---------- Search Frame -------------
        self.lbl_search = Label(self.root, text="Invoice No.", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_search.place(x=700, y=80)

        self.txt_search = Entry(self.root, textvariable=self.var_searchtxt, font=utils.FONT_BODY)
        self.txt_search.place(x=820, y=80, width=140, height=28)
        utils.style_entry(self.txt_search)

        self.btn_search = Button(self.root, command=self.search, text="Search")
        self.btn_search.place(x=980, y=79, width=100, height=28)
        utils.style_button(self.btn_search, bg_color=utils.COLOR_PRIMARY, hover_color=utils.COLOR_PRIMARY_HOVER)

        #-------------- title ---------------
        self.title_lbl = Label(self.root, text="Supplier Details", font=utils.FONT_SUBTITLE, bg=utils.COLOR_PRIMARY, fg="white")
        self.title_lbl.place(x=50, y=10, width=1000, height=40)

        #-------------- content ---------------
        #---------- row 1 ----------------
        self.lbl_supplier_invoice = Label(self.root, text="Invoice No.", font=utils.FONT_BODY, bg=utils.BG_DARK, fg=utils.FG_LIGHT)
        self.lbl_supplier_invoice.place(x=50, y=80)
        
        self.txt_supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=utils.FONT_BODY)
        self.txt_supplier_invoice.place(x=180, y=80, width=180, height=28)
        utils.style_entry(self.txt_supplier_invoice)
        
        #---------- row 2 ----------------
        self.lbl_name = Label(self.root, text="Name", font=utils.FONT_BODY, bg=utils.BG_DARK, fg=utils.FG_LIGHT)
        self.lbl_name.place(x=50, y=120)
        
        self.txt_name = Entry(self.root, textvariable=self.var_name, font=utils.FONT_BODY)
        self.txt_name.place(x=180, y=120, width=180, height=28)
        utils.style_entry(self.txt_name)
        
        #---------- row 3 ----------------
        self.lbl_contact = Label(self.root, text="Contact", font=utils.FONT_BODY, bg=utils.BG_DARK, fg=utils.FG_LIGHT)
        self.lbl_contact.place(x=50, y=160)
        
        self.txt_contact = Entry(self.root, textvariable=self.var_contact, font=utils.FONT_BODY)
        self.txt_contact.place(x=180, y=160, width=180, height=28)
        utils.style_entry(self.txt_contact)
        
        #---------- row 4 ----------------
        self.lbl_desc = Label(self.root, text="Description", font=utils.FONT_BODY, bg=utils.BG_DARK, fg=utils.FG_LIGHT)
        self.lbl_desc.place(x=50, y=200)
        
        self.txt_desc = Text(self.root, font=utils.FONT_BODY)
        self.txt_desc.place(x=180, y=200, width=470, height=120)
        utils.style_text(self.txt_desc)
        
        #-------------- buttons -----------------
        self.btn_add = Button(self.root, text="Save", command=self.add)
        self.btn_add.place(x=180, y=350, width=110, height=35)
        utils.style_button(self.btn_add, bg_color=utils.COLOR_PRIMARY, hover_color=utils.COLOR_PRIMARY_HOVER)

        self.btn_update = Button(self.root, text="Update", command=self.update)
        self.btn_update.place(x=300, y=350, width=110, height=35)
        utils.style_button(self.btn_update, bg_color=utils.COLOR_SUCCESS, hover_color=utils.COLOR_SUCCESS_HOVER)

        self.btn_delete = Button(self.root, text="Delete", command=self.delete)
        self.btn_delete.place(x=420, y=350, width=110, height=35)
        utils.style_button(self.btn_delete, bg_color=utils.COLOR_DANGER, hover_color=utils.COLOR_DANGER_HOVER)

        self.btn_clear = Button(self.root, text="Clear", command=self.clear)
        self.btn_clear.place(x=540, y=350, width=110, height=35)
        utils.style_button(self.btn_clear, bg_color=utils.COLOR_WARNING, hover_color=utils.COLOR_WARNING_HOVER)

        #------------ supplier details -------------
        sup_frame = Frame(self.root, bd=0, bg=utils.BG_DARK)
        sup_frame.place(x=700, y=120, width=380, height=350)

        scrolly = ttk.Scrollbar(sup_frame, orient=VERTICAL)
        scrollx = ttk.Scrollbar(sup_frame, orient=HORIZONTAL)
        
        self.SupplierTable = ttk.Treeview(sup_frame, columns=("invoice", "name", "contact", "desc"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("invoice", text="Invoice")
        self.SupplierTable.heading("name", text="Name")
        self.SupplierTable.heading("contact", text="Contact")
        self.SupplierTable.heading("desc", text="Description")
        
        self.SupplierTable["show"] = "headings"
        self.SupplierTable.column("invoice", width=80, anchor="center")
        self.SupplierTable.column("name", width=100)
        self.SupplierTable.column("contact", width=90, anchor="center")
        self.SupplierTable.column("desc", width=150)
        
        self.SupplierTable.pack(fill=BOTH, expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

#-----------------------------------------------------------------------------------------------------
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Invoice no. is already assigned", parent=self.root)
                else:
                    cur.execute("insert into supplier(invoice,name,contact,desc) values(?,?,?,?)", (
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END).strip(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
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
            cur.execute("select * from supplier")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        try:
            f = self.SupplierTable.focus()
            content = (self.SupplierTable.item(f))
            row = content['values']
            if not row:
                return
            self.var_sup_invoice.set(row[0])
            self.var_name.set(row[1])
            self.var_contact.set(row[2])
            self.txt_desc.delete('1.0', END)
            self.txt_desc.insert(END, row[3])
        except Exception as ex:
            pass

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    cur.execute("update supplier set name=?,contact=?,desc=? where invoice=?", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END).strip(),
                        self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("delete from supplier where invoice=?", (self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Supplier Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Invoice No. should be required", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row != None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()