import tkinter as tk
from tkinter import messagebox
from db.database import add_password, get_password, delete_password, backup_database, restore_database
from utils.encryption import encrypt_password, decrypt_password
from utils.password_utils import generate_password, check_password_strength

def run_gui():
    root = tk.Tk()
    root.title("Password Manager")

    # Service input
    tk.Label(root, text="Service:").grid(row=0, column=0)
    service_entry = tk.Entry(root)
    service_entry.grid(row=0, column=1)

    # Username input
    tk.Label(root, text="Username/Email:").grid(row=1, column=0)
    username_entry = tk.Entry(root)
    username_entry.grid(row=1, column=1)

    # URL input
    tk.Label(root, text="URL:").grid(row=2, column=0)
    url_entry = tk.Entry(root)
    url_entry.grid(row=2, column=1)

    # Password input
    tk.Label(root, text="Password:").grid(row=3, column=0)
    password_entry = tk.Entry(root)
    password_entry.grid(row=3, column=1)

    # Notes input
    tk.Label(root, text="Notes:").grid(row=4, column=0)
    notes_entry = tk.Entry(root)
    notes_entry.grid(row=4, column=1)

    # Generate Password Button
    def generate_password_button():
        password_entry.delete(0, tk.END)
        password_entry.insert(0, generate_password())

    generate_btn = tk.Button(root, text="Generate Password", command=generate_password_button)
    generate_btn.grid(row=3, column=2)

    # Add password button
    def add_password_button():
        service = service_entry.get()
        username = username_entry.get()
        url = url_entry.get()
        password = password_entry.get()
        notes = notes_entry.get()

        if not check_password_strength(password):
            messagebox.showerror("Error", "Password does not meet strength requirements.")
            return

        encrypted_password = encrypt_password(password)
        add_password(service, username, url, encrypted_password, notes)
        messagebox.showinfo("Success", f"Password for {service} added.")

    add_btn = tk.Button(root, text="Add Password", command=add_password_button)
    add_btn.grid(row=5, column=0)

    # Retrieve password button
    def retrieve_password_button():
        service = service_entry.get()
        result = get_password(service)

        if result:
            username, url, encrypted_password, notes = result
            password = decrypt_password(encrypted_password)

            username_entry.delete(0, tk.END)
            url_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            notes_entry.delete(0, tk.END)

            username_entry.insert(0, username)
            url_entry.insert(0, url)
            password_entry.insert(0, password)
            notes_entry.insert(0, notes)
        else:
            messagebox.showerror("Error", "Service not found!")

    retrieve_btn = tk.Button(root, text="Retrieve Password", command=retrieve_password_button)
    retrieve_btn.grid(row=5, column=1)

    # Delete password button
    def delete_password_button():
        service = service_entry.get()
        delete_password(service)
        messagebox.showinfo("Success", f"Password for {service} deleted.")

    delete_btn = tk.Button(root, text="Delete Password", command=delete_password_button)
    delete_btn.grid(row=5, column=2)

    # Backup database button
    backup_btn = tk.Button(root, text="Backup Database", command=backup_database)
    backup_btn.grid(row=6, column=0)

    # Restore database button
    restore_btn = tk.Button(root, text="Restore Database", command=restore_database)
    restore_btn.grid(row=6, column=1)

    root.mainloop()
