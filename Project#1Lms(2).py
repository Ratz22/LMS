import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Database Setup
def init_db():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                 id INTEGER PRIMARY KEY,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL,
                 year INTEGER,
                 available INTEGER DEFAULT 1)''')
    conn.commit()
    conn.close()

# Book Functions
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()
    if title and author and year.isdigit():
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
                  (title, author, int(year)))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book added successfully!")
        refresh_books()
    else:
        messagebox.showerror("Error", "Please fill all fields correctly!")

def refresh_books():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    for row in c.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def delete_book():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a book to delete!")
        return
    book_id = tree.item(selected_item)['values'][0]
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book deleted!")
    refresh_books()

# GUI Setup
root = tk.Tk()
root.title("Futuristic Library Management System")
root.geometry("800x600")
root.configure(bg="#1e1e2e")

# Styling
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#2e2e3e", foreground="white", rowheight=25, fieldbackground="#2e2e3e")
style.map("Treeview", background=[("selected", "#00ffaa")])

# Frame for Inputs
frame = tk.Frame(root, bg="#2e2e3e", padx=20, pady=20)
frame.pack(pady=20, fill="x")

# Labels & Entries
tk.Label(frame, text="Title", fg="white", bg="#2e2e3e").grid(row=0, column=0, padx=10)
title_entry = tk.Entry(frame, width=30)
title_entry.grid(row=0, column=1, padx=10)

tk.Label(frame, text="Author", fg="white", bg="#2e2e3e").grid(row=0, column=2, padx=10)
author_entry = tk.Entry(frame, width=30)
author_entry.grid(row=0, column=3, padx=10)

tk.Label(frame, text="Year", fg="white", bg="#2e2e3e").grid(row=0, column=4, padx=10)
year_entry = tk.Entry(frame, width=10)
year_entry.grid(row=0, column=5, padx=10)

# Buttons
add_button = tk.Button(frame, text="Add Book", command=add_book, bg="#00ffaa", fg="#222", padx=10, pady=5)
add_button.grid(row=1, column=2, pady=10)

delete_button = tk.Button(frame, text="Delete Book", command=delete_book, bg="#ff5555", fg="#222", padx=10, pady=5)
delete_button.grid(row=1, column=3, pady=10)

# Book List
columns = ("ID", "Title", "Author", "Year", "Available")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)
tree.pack(expand=True, fill="both", padx=20, pady=20)

refresh_books()

root.mainloop()

# Initialize Database
init_db()
