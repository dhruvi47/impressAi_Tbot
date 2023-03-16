from flask import Flask, render_template
import psycopg2

conn = psycopg2.connect(database="mydatabase", user="myusername", password="mypassword", host="localhost", port="5432")
cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    # Retrieve the user call data from the database
    cur.execute('SELECT user_id, stupid_calls, fat_calls, dumb_calls FROM user_calls')
    rows = cur.fetchall()

    # Render the template with the user call data
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
