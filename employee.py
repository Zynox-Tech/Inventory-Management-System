from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import utils

class employeeClass:
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
        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        #---------- Search Frame -------------
        self.SearchFrame = LabelFrame(self.root, text="Search Employee", font=utils.FONT_BODY_BOLD, bd=2, bg=utils.BG_DARK, fg=utils.FG_LIGHT)
        self.SearchFrame.place(x=250, y=10, width=600, height=80)

        #------------ options ----------------
        self.cmb_search = ttk.Combobox(self.SearchFrame, textvariable=self.var_searchby, values=("Select", "Email", "Name", "Contact"), state='readonly', justify=CENTER, font=utils.FONT_BODY)
        self.cmb_search.place(x=10, y=10, width=180, height=30)
        self.cmb_search.current(0)

        self.txt_search = Entry(self.SearchFrame, textvariable=self.var_searchtxt, font=utils.FONT_BODY)
        self.txt_search.place(x=200, y=10, width=200, height=30)
        utils.style_entry(self.txt_search)

        self.btn_search = Button(self.SearchFrame, command=self.search, text="Search")
        self.btn_search.place(x=420, y=10, width=150, height=30)
        utils.style_button(self.btn_search, bg_color=utils.COLOR_PRIMARY, hover_color=utils.COLOR_PRIMARY_HOVER)

        #-------------- title ---------------
        self.title_lbl = Label(self.root, text="Employee Details", font=utils.FONT_SUBTITLE, bg=utils.COLOR_PRIMARY, fg="white")
        self.title_lbl.place(x=50, y=100, width=1000, height=35)

        #-------------- content ---------------
        #---------- row 1 ----------------
        self.lbl_empid = Label(self.root, text="Emp ID", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_empid.place(x=50, y=150)
        self.txt_empid = Entry(self.root, textvariable=self.var_emp_id)
        self.txt_empid.place(x=150, y=150, width=180, height=28)
        utils.style_entry(self.txt_empid)

        self.lbl_gender = Label(self.root, text="Gender", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_gender.place(x=350, y=150)
        self.cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), state='readonly', justify=CENTER, font=utils.FONT_BODY)
        self.cmb_gender.place(x=500, y=150, width=180, height=28)
        self.cmb_gender.current(0)
        
        self.lbl_contact = Label(self.root, text="Contact", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_contact.place(x=750, y=150)
        self.txt_contact = Entry(self.root, textvariable=self.var_contact)
        self.txt_contact.place(x=850, y=150, width=180, height=28)
        utils.style_entry(self.txt_contact)

        #---------- row 2 ----------------
        self.lbl_name = Label(self.root, text="Name", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_name.place(x=50, y=190)
        self.txt_name = Entry(self.root, textvariable=self.var_name)
        self.txt_name.place(x=150, y=190, width=180, height=28)
        utils.style_entry(self.txt_name)

        self.lbl_dob = Label(self.root, text="D.O.B.", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_dob.place(x=350, y=190)
        self.txt_dob = Entry(self.root, textvariable=self.var_dob)
        self.txt_dob.place(x=500, y=190, width=180, height=28)
        utils.style_entry(self.txt_dob)

        self.lbl_doj = Label(self.root, text="D.O.J.", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_doj.place(x=750, y=190)
        self.txt_doj = Entry(self.root, textvariable=self.var_doj)
        self.txt_doj.place(x=850, y=190, width=180, height=28)
        utils.style_entry(self.txt_doj)

        #---------- row 3 ----------------
        self.lbl_email = Label(self.root, text="Email", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_email.place(x=50, y=230)
        self.txt_email = Entry(self.root, textvariable=self.var_email)
        self.txt_email.place(x=150, y=230, width=180, height=28)
        utils.style_entry(self.txt_email)

        self.lbl_pass = Label(self.root, text="Password", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_pass.place(x=350, y=230)
        self.txt_pass = Entry(self.root, textvariable=self.var_pass, show="*")
        self.txt_pass.place(x=500, y=230, width=180, height=28)
        utils.style_entry(self.txt_pass)

        self.lbl_utype = Label(self.root, text="User Type", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_utype.place(x=750, y=230)
        self.cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Employee"), state='readonly', justify=CENTER, font=utils.FONT_BODY)
        self.cmb_utype.place(x=850, y=230, width=180, height=28)
        self.cmb_utype.current(0)
        
        #---------- row 4 ----------------
        self.lbl_address = Label(self.root, text="Address", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_address.place(x=50, y=270)
        self.txt_address = Text(self.root)
        self.txt_address.place(x=150, y=270, width=300, height=60)
        utils.style_text(self.txt_address)

        self.lbl_salary = Label(self.root, text="Salary", bg=utils.BG_DARK, fg=utils.FG_LIGHT, font=utils.FONT_BODY)
        self.lbl_salary.place(x=500, y=270)
        self.txt_salary = Entry(self.root, textvariable=self.var_salary)
        self.txt_salary.place(x=600, y=270, width=180, height=28)
        utils.style_entry(self.txt_salary)
        
        #-------------- buttons -----------------
        self.btn_add = Button(self.root, text="Save", command=self.add)
        self.btn_add.place(x=500, y=315, width=110, height=30)
        utils.style_button(self.btn_add, bg_color=utils.COLOR_PRIMARY, hover_color=utils.COLOR_PRIMARY_HOVER)

        self.btn_update = Button(self.root, text="Update", command=self.update)
        self.btn_update.place(x=620, y=315, width=110, height=30)
        utils.style_button(self.btn_update, bg_color=utils.COLOR_SUCCESS, hover_color=utils.COLOR_SUCCESS_HOVER)

        self.btn_delete = Button(self.root, text="Delete", command=self.delete)
        self.btn_delete.place(x=740, y=315, width=110, height=30)
        utils.style_button(self.btn_delete, bg_color=utils.COLOR_DANGER, hover_color=utils.COLOR_DANGER_HOVER)

        self.btn_clear = Button(self.root, text="Clear", command=self.clear)
        self.btn_clear.place(x=860, y=315, width=110, height=30)
        utils.style_button(self.btn_clear, bg_color=utils.COLOR_WARNING, hover_color=utils.COLOR_WARNING_HOVER)

        #------------ employee details -------------
        emp_frame = Frame(self.root, bd=0, bg=utils.BG_DARK)
        emp_frame.place(x=50, y=360, width=1000, height=130)

        scrolly = ttk.Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = ttk.Scrollbar(emp_frame, orient=HORIZONTAL)
        
        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid", text="EMP ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")
        
        self.EmployeeTable["show"] = "headings"
        self.EmployeeTable.column("eid", width=70, anchor="center")
        self.EmployeeTable.column("name", width=110)
        self.EmployeeTable.column("email", width=140)
        self.EmployeeTable.column("gender", width=70, anchor="center")
        self.EmployeeTable.column("contact", width=100, anchor="center")
        self.EmployeeTable.column("dob", width=90, anchor="center")
        self.EmployeeTable.column("doj", width=90, anchor="center")
        self.EmployeeTable.column("pass", width=90)
        self.EmployeeTable.column("utype", width=90, anchor="center")
        self.EmployeeTable.column("address", width=150)
        self.EmployeeTable.column("salary", width=80, anchor="center")
        
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

#-----------------------------------------------------------------------------------------------------
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This Employee ID is already assigned", parent=self.root)
                else:
                    cur.execute("insert into employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)", (
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END).strip(),
                        self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
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
            cur.execute("select * from employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        try:
            f = self.EmployeeTable.focus()
            content = (self.EmployeeTable.item(f))
            row = content['values']
            if not row:
                return
            self.var_emp_id.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_contact.set(row[4])
            self.var_dob.set(row[5])
            self.var_doj.set(row[6])
            self.var_pass.set(row[7])
            self.var_utype.set(row[8])
            self.txt_address.delete('1.0', END)
            self.txt_address.insert(END, row[9])
            self.var_salary.set(row[10])
        except Exception as ex:
            pass

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    cur.execute("update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END).strip(),
                        self.var_salary.get(),
                        self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("delete from employee where eid=?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0', END)
        self.var_salary.set("")
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
                cur.execute("select * from employee where " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()