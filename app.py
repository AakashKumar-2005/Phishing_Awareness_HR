from flask import Flask, request, jsonify
from flask_mysql_connector import MySQL
from datetime import datetime

# Flask app initialization
app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'KPYJKPYJ1&a'
app.config['MYSQL_DATABASE'] = 'phishing_simulation'

# Initialize MySQL
mysql = MySQL(app)

# Helper function to execute database queries
def execute_query(query, values=None):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(query, values or ())
    conn.commit()
    return cursor

# Route to track email opens (via tracking pixel)
@app.route('/track-email', methods=['GET'])
def track_email():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Update the database when the email is viewed
    query = '''
        UPDATE interactions 
        SET status = 'viewed', email_viewed_at = %s 
        WHERE email = %s AND status = 'unopened'
    '''
    execute_query(query, (datetime.now(), email))
    return '', 204  # Transparent response for tracking pixel

# Route to track link clicks
@app.route('/track-click', methods=['POST'])
def track_click():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Update the database when the link is clicked
    query = '''
        UPDATE interactions 
        SET status = 'clicked', link_clicked_at = %s 
        WHERE email = %s
    '''
    execute_query(query, (datetime.now(), email))
    return jsonify({'message': 'Click tracked successfully!'}), 200

# Route to add email addresses to the database
@app.route('/add-email', methods=['POST'])
def add_email():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    try:
        # Insert a new email into the database
        query = 'INSERT INTO interactions (email) VALUES (%s)'
        execute_query(query, (email,))
        return jsonify({'message': 'Email added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get report summary
@app.route('/report', methods=['GET'])
def get_report():
    query = '''
        SELECT email, status, email_viewed_at, link_clicked_at 
        FROM interactions
    '''
    cursor = execute_query(query)
    results = cursor.fetchall()
    cursor.close()

    # Return report as JSON
    report = [
        {
            'email': row[0],
            'status': row[1],
            'email_viewed_at': row[2],
            'link_clicked_at': row[3]
        }
        for row in results
    ]
    return jsonify(report), 200

# Main route to test server
@app.route('/')
def index():
    return "Phishing Simulation Backend is running!"

if __name__ == '__main__':
    app.run(debug=True)
