from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import utils

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System | Developed by Zynox Tech")
        self.root.config(bg=utils.BG_DARK)
        self.root.resizable(True, True)
        self.root.focus_force()

        # Apply dark styling to ttk elements
        utils.apply_treeview_theme()

        #------------ variables -------------
        self.var_cat_id = StringVar()
        self.var_name = StringVar()
        
        #--------------- title ---------------------
        self.lbl_title = Label(
            self.root,
            text="Manage Product Category",
            font=utils.FONT_SUBTITLE,
            bg=utils.COLOR_PRIMARY,
            fg="white"
        )
        self.lbl_title.pack(side=TOP, fill=X, padx=20, pady=20)
        
        self.lbl_name = Label(self.root, text="Enter Category Name", font=utils.FONT_BODY_BOLD, bg=utils.BG_DARK, fg=utils.FG_LIGHT)
        self.lbl_name.place(x=50, y=95)
        
        self.txt_name = Entry(self.root, textvariable=self.var_name, font=utils.FONT_BODY)
        self.txt_name.place(x=50, y=140, width=300, height=32)
        utils.style_entry(self.txt_name)

        self.btn_add = Button(self.root, text="ADD", command=self.add)
        self.btn_add.place(x=360, y=140, width=140, height=32)
        utils.style_button(self.btn_add, bg_color=utils.COLOR_SUCCESS, hover_color=utils.COLOR_SUCCESS_HOVER)

        self.btn_delete = Button(self.root, text="Delete", command=self.delete)
        self.btn_delete.place(x=510, y=140, width=140, height=32)
        utils.style_button(self.btn_delete, bg_color=utils.COLOR_DANGER, hover_color=utils.COLOR_DANGER_HOVER)

        #------------ category details -------------
        self.cat_frame = Frame(self.root, bd=0, bg=utils.BG_DARK)
        self.cat_frame.place(x=700, y=95, width=350, height=105)

        self.scrolly = ttk.Scrollbar(self.cat_frame, orient=VERTICAL)
        self.scrollx = ttk.Scrollbar(self.cat_frame, orient=HORIZONTAL)
        
        self.CategoryTable = ttk.Treeview(self.cat_frame, columns=("cid", "name"), yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.scrollx.pack(side=BOTTOM, fill=X)
        self.scrolly.pack(side=RIGHT, fill=Y)
        self.scrollx.config(command=self.CategoryTable.xview)
        self.scrolly.config(command=self.CategoryTable.yview)
        
        self.CategoryTable.heading("cid", text="C ID")
        self.CategoryTable.heading("name", text="Name")
        self.CategoryTable["show"] = "headings"
        self.CategoryTable.column("cid", width=80, anchor="center")
        self.CategoryTable.column("name", width=220)
        
        self.CategoryTable.pack(fill=BOTH, expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        #----------------- images ---------------------
        img1_path = utils.resolve_path("Inventory-Management-System/images/cat.jpg")
        self.im1 = Image.open(img1_path)
        self.im1 = self.im1.resize((480, 240))
        self.im1 = ImageTk.PhotoImage(self.im1)
        self.lbl_im1 = Label(self.root, image=self.im1, bd=0, bg=utils.BG_DARK)
        self.lbl_im1.place(x=50, y=220)

        img2_path = utils.resolve_path("Inventory-Management-System/images/category.jpg")
        self.im2 = Image.open(img2_path)
        self.im2 = self.im2.resize((480, 240))
        self.im2 = ImageTk.PhotoImage(self.im2)
        self.lbl_im2 = Label(self.root, image=self.im2, bd=0, bg=utils.BG_DARK)
        self.lbl_im2.place(x=570, y=220)

#----------------------------------------------------------------------------------
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name must be required", parent=self.root)
            else:
                cur.execute("Select * from category where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Category already present", parent=self.root)
                else:
                    cur.execute("insert into category(name) values(?)", (
                        self.var_name.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
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
            cur.execute("select * from category")
            rows = cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def clear(self):
        self.var_name.set("")
        self.show()

    def get_data(self, ev):
        try:
            f = self.CategoryTable.focus()
            content = (self.CategoryTable.item(f))
            row = content['values']
            if not row:
                return
            self.var_cat_id.set(row[0])
            self.var_name.set(row[1])
        except Exception as ex:
            pass
    
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Category name must be selected", parent=self.root)
            else:
                cur.execute("Select * from category where cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Category Name", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("delete from category where cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        self.clear()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()