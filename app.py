from flask import Flask, render_template, request, redirect, url_for
import sqlite3

db = sqlite3.connect('database.db', check_same_thread=False)

db.execute("""CREATE TABLE IF NOT EXISTS todo_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    completed TEXT
    )""")
db.commit()

app = Flask(__name__, static_folder="static")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task_description = request.form['task_description']

        db.execute(f"""INSERT INTO todo_items 
        (item_name, completed) VALUES 
        ("{task_description}", "No")""")
        db.commit()
    
    data = db.execute('SELECT * FROM todo_items').fetchall()
    
    return render_template("home.html", data=data)


@app.route('/delete/<int:id>')
def delete(id):
    db.execute(f'DELETE FROM todo_items WHERE id={id}')
    db.commit()
    return redirect(url_for('home'))


@app.route('/complete/<int:id>')
def complete(id):
    data = db.execute(f'SELECT * FROM todo_items WHERE id={id}').fetchone()
    if data[2] == 'Yes':
        status = 'No'
    else:
        status = 'Yes'

    db.execute(f'UPDATE todo_items SET completed="{status}" WHERE id={id}')
    db.commit()
    return redirect(url_for('home'))