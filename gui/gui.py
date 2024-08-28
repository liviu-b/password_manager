import tkinter as tk
from tkinter import messagebox
from db.database import add_password, get_password, delete_password, backup_database, restore_database
from utils.encryption import encrypt_password, decrypt_password
from utils.password_utils import generate_password, check_password_strength

def run_gui():
    root = tk.Tk()
    root.title("Password Manager")

    # Helper function for displaying messages
    def show_message(title, message, error=False):
        if error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)

    # Service input
    tk.Label(root, text="Service:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    service_entry = tk.Entry(root, width=50)
    service_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

    # Username input
    tk.Label(root, text="Username/Email:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    username_entry = tk.Entry(root, width=50)
    username_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

    # URL input
    tk.Label(root, text="URL:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

    # Password input
    tk.Label(root, text="Password:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
    password_entry = tk.Entry(root, show='*', width=50)
    password_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)

    # Toggle Password Visibility
    def toggle_password():
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
            toggle_btn.config(text='Hide Password')
        else:
            password_entry.config(show='*')
            toggle_btn.config(text='Show Password')

    toggle_btn = tk.Button(root, text='Show Password', command=toggle_password)
    toggle_btn.grid(row=4, column=1, padx=5, pady=5, sticky='w')

    # Generate Password Button
    def generate_password_button():
        password_entry.delete(0, tk.END)
        password_entry.insert(0, generate_password())

    generate_btn = tk.Button(root, text="Generate Password", command=generate_password_button)
    generate_btn.grid(row=4, column=2, padx=5, pady=5, sticky='w')

    # Notes input
    tk.Label(root, text="Notes:").grid(row=5, column=0, padx=5, pady=5, sticky='ne')
    notes_entry = tk.Text(root, width=50, height=5)
    notes_entry.grid(row=5, column=1, padx=5, pady=5, columnspan=3)

    # Add password button
    def add_password_button():
        service = service_entry.get()
        username = username_entry.get()
        url = url_entry.get()
        password = password_entry.get()
        notes = notes_entry.get("1.0", tk.END).strip()

        if not service or not username or not url or not password:
            show_message("Error", "All fields except Notes must be filled in.", error=True)
            return

        if not check_password_strength(password):
            show_message("Error", "Password does not meet strength requirements.", error=True)
            return

        encrypted_password = encrypt_password(password)
        add_password(service, username, url, encrypted_password, notes)
        show_message("Success", f"Password for {service} added.")

    add_btn = tk.Button(root, text="Add Password", command=add_password_button, bg='lightgreen')
    add_btn.grid(row=6, column=0, padx=5, pady=5, sticky='ew')

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
            notes_entry.delete("1.0", tk.END)

            username_entry.insert(0, username)
            url_entry.insert(0, url)
            password_entry.insert(0, password)
            notes_entry.insert("1.0", notes)
        else:
            show_message("Error", "Service not found!", error=True)

    retrieve_btn = tk.Button(root, text="Retrieve Password", command=retrieve_password_button, bg='lightgreen')
    retrieve_btn.grid(row=6, column=1, padx=5, pady=5, sticky='ew')

    # Backup database button
    backup_btn = tk.Button(root, text="Backup Database", command=backup_database, bg='lightblue')
    backup_btn.grid(row=7, column=0, padx=5, pady=5, sticky='ew')

    # Restore database button
    restore_btn = tk.Button(root, text="Restore Database", command=restore_database, bg='lightblue')
    restore_btn.grid(row=7, column=1, padx=5, pady=5, sticky='ew')

    # Delete password button
    def delete_password_button():
        service = service_entry.get()
        delete_password(service)
        show_message("Success", f"Password for {service} deleted.")

    delete_btn = tk.Button(root, text="Delete Password", command=delete_password_button, bg='red', fg='white')
    delete_btn.grid(row=7, column=2, padx=5, pady=5, sticky='ew')

    root.mainloop()
