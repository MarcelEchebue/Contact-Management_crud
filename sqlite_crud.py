"""
CRUD avec SQLite3
sqlite_crud.py
"""
import sqlite3


def create_table():
    # Connect to sqlite database
    conn = sqlite3.connect("contacts.db")
    # cursor object
    cursor = conn.cursor()
    # drop query
    cursor.execute("DROP TABLE IF EXISTS contacts")
    # create query
    query = """CREATE TABLE IF NOT EXISTS contacts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prenom TEXT NOT NULL,
            nom TEXT NOT NULL,
            telephone TEXT NOT NULL,
            email TEXT NOT NULL)"""
    cursor.execute(query)
    # commit and close
    conn.commit()
    conn.close()


def add_contact(prenom, nom, telephone, email):
    conn = sqlite3.connect("contacts.db")
    req = "INSERT INTO contacts(prenom, nom, telephone, email) VALUES (?, ?, ?, ?)"
    cur = conn.cursor()
    cur.execute(req, (prenom, nom, telephone, email))
    conn.commit()
    conn.close()


def update_contact(prenom, nom, telephone, email, id):
    """Mise à jour """
    conn = sqlite3.connect("contacts.db")
    req = "UPDATE contacts SET prenom = ?, nom = ?, telephone = ?, email = ? WHERE id = ?"
    cur = conn.cursor()
    cur.execute(req, (prenom, nom, telephone, email, id))
    conn.commit()
    conn.close()


def delete_contact(id):
    """Suppression"""
    conn = sqlite3.connect("contacts.db")
    req = "DELETE FROM contacts WHERE id = ?"
    cur = conn.cursor()
    cur.execute(req, (id,))
    conn.commit()
    conn.close()


def get_all_contacts():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.execute("SELECT * from contacts")
    print(cursor.fetchall())
    conn.close()


def save_contact():
    prenom = input("Enter le prenom: ")
    nom = input("Enter nom: ")
    telephone = input("Enter telephone number: ")
    email = input("Enter email address: ")
    add_contact(prenom, nom, telephone, email)
    print("Contact saved successfully!")


if __name__ == "__main__":
    create_table()
