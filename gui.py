from tkinter import *
from tkinter import messagebox
from dbconnect import get_connection
from tkinter import ttk


root = Tk()
root.title("Student Management System")
root.geometry("400x430")
root.resizable(False, False)

# ---------- FUNCTIONS ----------
def add_student():
    roll = entry_roll.get()
    name = entry_name.get()
    cls = entry_class.get()
    marks = entry_marks.get()

    if roll == "" or name == "" or cls == "" or marks == "":
        messagebox.showerror("Error", "All fields are required")
        return

    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        sql = "INSERT INTO students VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (roll, name, cls, marks))
        conn.commit()
        messagebox.showinfo("Success", "Student Added Successfully")

        # Clear fields
        entry_roll.delete(0, END)
        entry_name.delete(0, END)
        entry_class.delete(0, END)
        entry_marks.delete(0, END)

    except:
        messagebox.showerror("Error", "Roll number already exists")

    finally:
        conn.close()

def view_students():
    view_window = Toplevel(root)
    view_window.title("All Students")
    view_window.geometry("500x300")

    tree = ttk.Treeview(view_window, columns=("Roll", "Name", "Class", "Marks"), show="headings")

    tree.heading("Roll", text="Roll No")
    tree.heading("Name", text="Name")
    tree.heading("Class", text="Class")
    tree.heading("Marks", text="Marks")

    tree.column("Roll", width=80)
    tree.column("Name", width=120)
    tree.column("Class", width=100)
    tree.column("Marks", width=80)

    tree.pack(fill=BOTH, expand=True)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", END, values=row)

    conn.close()

def update_student():
    roll = entry_roll.get()
    name = entry_name.get()
    cls = entry_class.get()
    marks = entry_marks.get()

    if roll == "":
        messagebox.showerror("Error", "Enter Roll No to Update")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE students SET name=%s, class=%s, marks=%s WHERE roll_no=%s",
            (name, cls, marks, roll)
        )
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Student not found")
        else:
            messagebox.showinfo("Success", "Student Updated Successfully")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        conn.close()


def delete_student():
    roll = entry_roll.get()

    if roll == "":
        messagebox.showerror("Error", "Enter Roll No to Delete")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM students WHERE roll_no=%s", (roll,))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showerror("Error", "Student not found")
        else:
            messagebox.showinfo("Success", "Student Deleted Successfully")

            # Clear fields
            entry_roll.delete(0, END)
            entry_name.delete(0, END)
            entry_class.delete(0, END)
            entry_marks.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        conn.close()



# ---------- LABELS ----------
Label(root, text="Student Management System", font=("Arial", 16, "bold")).pack(pady=10)

Label(root, text="Roll No").place(x=50, y=70)
Label(root, text="Name").place(x=50, y=110)
Label(root, text="Class").place(x=50, y=150)
Label(root, text="Marks").place(x=50, y=190)

# ---------- ENTRY FIELDS ----------
entry_roll = Entry(root)
entry_name = Entry(root)
entry_class = Entry(root)
entry_marks = Entry(root)

entry_roll.place(x=150, y=70)
entry_name.place(x=150, y=110)
entry_class.place(x=150, y=150)
entry_marks.place(x=150, y=190)

# ---------- BUTTON ----------
Button(root, text="Add Student", width=20, command=add_student).place(x=120, y=250)
Button(root, text="View Students", width=20, command=view_students).place(x=120, y=290)
Button(root, text="Update Student", width=20, command=update_student).place(x=120, y=330)
Button(root, text="Delete Student", width=20, command=delete_student).place(x=120, y=370)

root.mainloop()


