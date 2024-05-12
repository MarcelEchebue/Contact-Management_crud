"""
CRUD avec SQLite3
app.py
"""
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)

# Configuration de la base de données SQLite
DATABASE = 'contacts.db'

# Fonctions utilitaires pour la base de données
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(conn):
    conn.close()

# Routes
@app.route('/')
def index():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts').fetchall()
    close_db_connection(conn)
    return render_template('index.html', contacts=contacts)

# Ajouter un contact
@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        prenom = request.form['prenom']
        nom = request.form['nom']
        telephone = request.form['telephone']
        email = request.form['email']

        conn = get_db_connection()

        # Vérifier si le numéro de téléphone existe déjà
        cursor = conn.execute('SELECT COUNT(*) FROM contacts WHERE telephone = ?', (telephone,))
        telephone_exists = cursor.fetchone()[0] > 0

        # Vérifier si l'e-mail existe déjà
        cursor = conn.execute('SELECT COUNT(*) FROM contacts WHERE email = ?', (email,))
        email_exists = cursor.fetchone()[0] > 0

        if telephone_exists or email_exists:
            # Si le numéro de téléphone ou l'e-mail existe déjà, afficher un message d'erreur
            error_message = "Le numéro de téléphone ou l'e-mail existe déjà dans la base de données."
            return render_template('add_contact.html', error_message=error_message)
        else:
            # Si le numéro de téléphone et l'e-mail n'existent pas encore, effectuer l'INSERT
            conn.execute('INSERT INTO contacts (prenom, nom, telephone, email) VALUES (?, ?, ?, ?)',
                         (prenom, nom, telephone, email))
            conn.commit()
            close_db_connection(conn)
            return redirect(url_for('index'))

    return render_template('add_contact.html')


# Modifier un contact
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        # Récupérer les données du formulaire
        prenom = request.form['prenom']
        nom = request.form['nom']
        telephone = request.form['telephone']
        email = request.form['email']

        # Vérifier si le numéro de téléphone existe déjà
        cursor = conn.execute('SELECT COUNT(*) FROM contacts WHERE telephone = ? AND id != ?', (telephone, id))
        telephone_exists = cursor.fetchone()[0] > 0

        # Vérifier si l'e-mail existe déjà
        cursor = conn.execute('SELECT COUNT(*) FROM contacts WHERE email = ? AND id != ?', (email, id))
        email_exists = cursor.fetchone()[0] > 0

        if telephone_exists or email_exists:
            # Si le numéro de téléphone ou l'e-mail existe déjà, afficher un message d'erreur et rediriger
            flash("Le numéro de téléphone ou l'e-mail existe déjà dans la base de données.")
            return redirect(url_for('index'))
        else:
            # Si le numéro de téléphone et l'e-mail n'existent pas encore, effectuer l'UPDATE
            conn.execute('UPDATE contacts SET prenom = ?, nom = ?, telephone = ?, email = ? WHERE id = ?',
                         (prenom, nom, telephone, email, id))
            conn.commit()
            close_db_connection(conn)
            return redirect(url_for('index'))

    return render_template('edit_contact.html', contact=contact)

# Supprimer un contact
@app.route('/delete/<int:id>')
def delete_contact(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    close_db_connection(conn)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)




"""
crud Management Contact by ECHEBUE
"""
