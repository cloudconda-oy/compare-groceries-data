from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import psycopg2

app = Flask(__name__)
CORS(app)

@app.route('/query',methods=['POST'])
def handle_query():
    query = request.json.get('query')
    
    # PostgreSQL database connection details
    host = 'localhost'
    database = 'groceries_app'
    user = 'postgres'
    password = 'postgres12'

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    cursor = conn.cursor()
    query = f"SELECT * FROM master WHERE title LIKE '%{query}%'"
    cursor.execute(query)

    column_names = [desc[0] for desc in cursor.description]
    result = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Return the query result as a response
    return {'columns': column_names, 'results': result}


if __name__ == '__main__':
    app.run()