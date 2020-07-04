from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Mysql Connection
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

#settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    conn = mysql.connect
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        conn.commit()
        flash('Contacto agregado exitosamente!!!')
        return redirect(url_for('Index'))


@app.route('/edit_contact/<string:id>')
def edit_contact(id):
    conn = mysql.connect
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('edit_contact.html', contact = data[0])

@app.route('/update_contact/<string:id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute('UPDATE contacts SET fullname = %s, email = %s, phone = %s WHERE id = %s', (fullname, email, phone, id))
        conn.commit()
        flash('Contacto Actualizado Exitosamente!!!')
        return redirect(url_for('Index'))

@app.route('/delete_contact/<string:id>')
def edit_delete(id):
    conn = mysql.connect
    cur = conn.cursor()
    cur.execute('DELETE FROM contacts WHERE id={0}'.format(id))
    conn.commit()
    flash('Contacto removido exitosamente!!!')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
