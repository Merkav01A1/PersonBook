import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class AddressBook:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("Address Book")

        # Connect to SQLite database and create a table for contacts
        self.conn = sqlite3.connect("simple_contacts.db")
        self.create_table()

        # Create the graphical user interface (GUI)
        self.create_gui()

    def create_table(self):
        # Create the "contacts" table if it doesn't exist
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                Name TEXT,
                Last_Name TEXT,
                First_Name TEXT,
                Street TEXT,
                ZIP_Code TEXT,
                City TEXT,
                Country TEXT,
                Birthday DATE
            )
        ''')
        self.conn.commit()

    def create_gui(self):
        # Frame with the list of contacts
        self.frame_list = ttk.Frame(self.root)
        self.frame_list.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure row to expand with the window
        self.root.rowconfigure(0, weight=1)

        # List of contacts displayed in a Treeview widget
        self.contacts_list = ttk.Treeview(self.frame_list, columns=(
            "ID", "Name", "Last_Name", "First_Name", "Street", "ZIP_Code", "City", "Country", "Birthday"),
                                          show="headings")

        # Set column widths and headers
        self.contacts_list.column("ID", width=25)
        self.contacts_list.column("Name", width=75)
        self.contacts_list.column("Last_Name", width=125)
        self.contacts_list.column("First_Name", width=100)
        self.contacts_list.column("Street", width=150)
        self.contacts_list.column("ZIP_Code", width=50)
        self.contacts_list.column("City", width=150)
        self.contacts_list.column("Country", width=100)
        self.contacts_list.column("Birthday", width=75)

        self.contacts_list.heading("ID", text="ID")
        self.contacts_list.heading("Name", text="Name")
        self.contacts_list.heading("Last_Name", text="Last Name")
        self.contacts_list.heading("First_Name", text="First Name")
        self.contacts_list.heading("Street", text="Street")
        self.contacts_list.heading("ZIP_Code", text="ZIP Code")
        self.contacts_list.heading("City", text="City")
        self.contacts_list.heading("Country", text="Country")
        self.contacts_list.heading("Birthday", text="Birthday")
        self.contacts_list.pack(side=tk.LEFT)

        self.contacts_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Make it expand in both directions

        # Scrollbar for the list of contacts
        scrollbar = ttk.Scrollbar(self.frame_list, orient=tk.VERTICAL, command=self.contacts_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contacts_list.configure(yscrollcommand=scrollbar.set)

        # Buttons for adding, editing, and deleting contacts
        self.frame_buttons = ttk.Frame(self.root)
        self.frame_buttons.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(self.frame_buttons, text="Add Contact", command=self.add_contact).grid(row=0, column=0, pady=5)
        ttk.Button(self.frame_buttons, text="Edit Contact", command=self.edit_contact).grid(row=1, column=0, pady=5)
        ttk.Button(self.frame_buttons, text="Delete Contact", command=self.delete_contact).grid(row=2, column=0, pady=5)

        # Load existing contacts data
        self.display_contacts()

    def display_contacts(self):
        # Display contacts in the Treeview widget
        self.contacts_list.delete(*self.contacts_list.get_children())
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM contacts')
        contacts = cursor.fetchall()

        for contact in contacts:
            self.contacts_list.insert("", "end", values=contact)

    def add_contact(self):
        # Open a new window for adding a contact
        AddEditContact(self.root, self.conn, self.display_contacts)

    def edit_contact(self):
        # Edit the selected contact
        selected_item = self.contacts_list.selection()
        if selected_item:
            contact_id = self.contacts_list.item(selected_item, "values")[0]
            AddEditContact(self.root, self.conn, self.display_contacts, contact_id)
        else:
            messagebox.showwarning("Warning", "Select a contact to edit.")

    def delete_contact(self):
        # Delete the selected contact
        selected_item = self.contacts_list.selection()
        if selected_item:
            contact_id = self.contacts_list.item(selected_item, "values")[0]
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM contacts WHERE ID=?', (contact_id,))
            contact = cursor.fetchone()

            if contact:
                confirmation = messagebox.askyesno("Confirmation",
                                                    f"Are you sure you want to delete the contact: {contact[1]}?")
                if confirmation:
                    cursor.execute('DELETE FROM contacts WHERE ID=?', (contact_id,))
                    self.conn.commit()
                    self.display_contacts()
                    messagebox.showinfo("Success", f"Contact {contact[1]} has been deleted successfully!")
        else:
            messagebox.showwarning("Warning", "Select a contact to delete.")

class AddEditContact:
    def __init__(self, root, conn, callback, contact_id=None):
        # Initialize the window for adding/editing contacts
        self.root = root
        self.conn = conn
        self.callback = callback
        self.contact_id = contact_id

        self.create_gui()

    def create_gui(self):
        # Create GUI components for entering contact information
        self.top = tk.Toplevel(self.root)
        if self.contact_id is not None:
            self.top.title("Edit Contact")
        else:
            self.top.title("Add Contact")

        tk.Label(self.top, text="Name*:", anchor="e").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.top, text="Last Name:", anchor="e").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.top, text="First Name:", anchor="e").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.top, text="Street:", anchor="e").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.top, text="ZIP Code:", anchor="e").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.top, text="City:", anchor="e").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.top, text="Country:", anchor="e").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.top, text="Birthday:", anchor="e").grid(row=7, column=0, padx=5, pady=5, sticky="e")

        self.name_entry = tk.Entry(self.top)
        self.last_name_entry = tk.Entry(self.top)
        self.first_name_entry = tk.Entry(self.top)
        self.street_entry = tk.Entry(self.top)
        self.zip_code_entry = tk.Entry(self.top)
        self.city_entry = tk.Entry(self.top)
        self.country_entry = tk.Entry(self.top)
        self.birthday_entry = tk.Entry(self.top)

        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.first_name_entry.grid(row=2, column=1, padx=5, pady=5)
        self.street_entry.grid(row=3, column=1, padx=5, pady=5)
        self.zip_code_entry.grid(row=4, column=1, padx=5, pady=5)
        self.city_entry.grid(row=5, column=1, padx=5, pady=5)
        self.country_entry.grid(row=6, column=1, padx=5, pady=5)
        self.birthday_entry.grid(row=7, column=1, padx=5, pady=5)

        # Fill in fields for editing if contact_id is provided
        if self.contact_id is not None:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM contacts WHERE ID=?', (self.contact_id,))
            contact = cursor.fetchone()
            if contact:
                self.name_entry.insert(0, contact[1])
                self.last_name_entry.insert(0, contact[2])
                self.first_name_entry.insert(0, contact[3])
                self.street_entry.insert(0, contact[4])
                self.zip_code_entry.insert(0, contact[5])
                self.city_entry.insert(0, contact[6])
                self.country_entry.insert(0, contact[7])
                self.birthday_entry.insert(0, contact[8])

        tk.Button(self.top, text="Save", command=self.save_contact).grid(row=8, column=0, columnspan=2, pady=10)

    def save_contact(self):
        # Save the contact information
        name = self.name_entry.get()
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        street = self.street_entry.get()
        zip_code = self.zip_code_entry.get()
        city = self.city_entry.get()
        country = self.country_entry.get()
        birthday = self.birthday_entry.get()

        if name:
            cursor = self.conn.cursor()
            if self.contact_id is not None:
                cursor.execute('''
                    UPDATE contacts
                    SET Name=?, Last_Name=?, First_Name=?, Street=?, ZIP_Code=?, City=?, Country=?, Birthday=?
                    WHERE ID=?
                ''', (name, last_name, first_name, street, zip_code, city, country, birthday, self.contact_id))
            else:
                cursor.execute('''
                    INSERT INTO contacts (Name, Last_Name, First_Name, Street, ZIP_Code, City, Country, Birthday)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, last_name, first_name, street, zip_code, city, country, birthday))

            self.conn.commit()
            self.callback()
            self.top.destroy()
            messagebox.showinfo("Success", f"Contact {name} has been saved successfully.")
        else:
            messagebox.showwarning("Warning", "Name is required!")

def add_multiple_contacts(address_book):
    # Function to add multiple contacts
    conn = sqlite3.connect("simple_contacts.db")
    contacts_data = [
        # Add your contact data here
    ]

    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO contacts (Name, Last_Name, First_Name, Street, ZIP_Code, City, Country, Birthday)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', contacts_data)

    conn.commit()
    conn.close()

    # Refresh the contacts view directly from the AddressBook object
    address_book.display_contacts()


if __name__ == "__main__":
    # Main block
    root = tk.Tk()
    application = AddressBook(root)

    # Add multiple contacts when the program is launched
    add_multiple_contacts(application)

    root.mainloop()
