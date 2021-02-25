import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
    print("Table created successfully")
    conn.close()


init_sqlite_db()

app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/enter-new/')
def enter_new_student():
    return render_template('Student.html')


@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        try:
            name = request.form['name']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, addr, city, pin) VALUES (?, ?, ?, ?)", (name, addr, city, pin))
                con.commit()
                msg = "Record successfully added."

        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + e

        finally:
            con.close()
            return render_template('result.html', msg=msg)


@app.route('/show-records/', methods=['GET'])
def show_records():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM students")
            records = cur.fetchall()

    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database.")
    finally:
        con.close()
        return jsonify(records)



if __name__ == "__main__":
    app.run(debug=True)
