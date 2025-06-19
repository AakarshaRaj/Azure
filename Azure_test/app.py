from flask import Flask, render_template, request
import pymssql

app = Flask(__name__)

# Replace these with your actual Azure SQL Database values
AZURE_SQL_SERVER = 'devnewapp.database.windows.net'
AZURE_SQL_USERNAME = 'CICD@devnewapp'
AZURE_SQL_PASSWORD = 'Azure@12345'
AZURE_SQL_DATABASE = 'cicd_testDB'

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    message = request.form['message']

    if not name or not message:
        return "Name and message are required.", 400

    try:
        # Connect to Azure SQL using pymssql
        conn = pymssql.connect(
            server=AZURE_SQL_SERVER,
            user=AZURE_SQL_USERNAME,
            password=AZURE_SQL_PASSWORD,
            database=AZURE_SQL_DATABASE
        )
        cursor = conn.cursor()

        # Ensure the table exists
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'messages')
            CREATE TABLE messages (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(100),
                message NVARCHAR(1000)
            )
        ''')

        # Insert data
        cursor.execute("INSERT INTO messages (name, message) VALUES (%s, %s)", (name, message))
        conn.commit()

        cursor.close()
        conn.close()
        return "Message submitted successfully!"

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8000)
