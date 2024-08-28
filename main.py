from gui.gui import run_gui
from db.database import init_db
from tkinter import simpledialog, messagebox
import tkinter as tk

# Master password check
def check_master_password(master_password):
    # You can replace this with a more secure system later.
    return master_password == "1526"

def main():
    # Initialize database if not created
    init_db()

    # Master password prompt
    root = tk.Tk()
    root.withdraw()  # Hide the main window while we show the master password dialog

    master_password = simpledialog.askstring("Master Password", "Enter Master Password:", show="*")
    if not check_master_password(master_password):
        messagebox.showerror("Error", "Invalid Master Password!")
        root.quit()
        return

    # Show the main GUI after master password is verified
    run_gui()

if __name__ == "__main__":
    main()
