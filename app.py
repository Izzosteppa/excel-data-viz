from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'financial_dashboard',
    'user': 'root', 
    'password': '@Siya2507ngqoba',  
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_database():
    """Initialize database and tables"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        
        # Create users table
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """
        
        # Create financial_records table
        financial_records_table = """
        CREATE TABLE IF NOT EXISTS financial_records (
            record_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            year INT NOT NULL,
            month INT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE KEY unique_user_year_month (user_id, year, month)
        )
        """
        
        cursor.execute(users_table)
        cursor.execute(financial_records_table)
        
        # Insert sample user data
        # cursor.execute("SELECT COUNT(*) FROM users")
        # if cursor.fetchone()[0] == 0:
        #     sample_users = [
        #         ("Jane Doe",),
        #         ("Tshepo Ramadukana",),
        #         ("Siyanda Ngqoba",)
        #     ]
        #     cursor.executemany("INSERT INTO users (name) VALUES (%s)", sample_users)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/finances/upload/<int:user_id>/<int:year>', methods=['POST'])
def upload_file(user_id, year):
    """Handle file upload and data processing"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Read Excel file
            df = pd.read_excel(file)
            
            # Validate columns (expecting Month and Amount)
            required_columns = ['Month', 'Amount']
            if not all(col in df.columns for col in required_columns):
                return jsonify({'error': 'Excel file must contain Month and Amount columns'}), 400
            
            # Connect to database
            connection = get_db_connection()
            if not connection:
                return jsonify({'error': 'Database connection failed'}), 500
            
            cursor = connection.cursor()
            
            # Verify user exists
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                return jsonify({'error': 'User not found'}), 404
            
            # Process and insert records
            records_inserted = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    month = int(row['Month'])
                    amount = float(row['Amount'])
                    
                    # Validate month
                    if month < 1 or month > 12:
                        errors.append(f"Row {index + 2}: Invalid month '{row['Month']}'")
                        continue
                    
                    # Validate amount
                    if amount < 0:
                        errors.append(f"Row {index + 2}: Invalid amount '{row['Amount']}'")
                        continue
                    
                    # Insert or update record
                    cursor.execute("""
                        INSERT INTO financial_records (user_id, year, month, amount) 
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE amount = VALUES(amount)
                    """, (user_id, year, month, amount))
                    
                    records_inserted += 1
                    
                except (ValueError, TypeError) as e:
                    errors.append(f"Row {index + 2}: Invalid data format")
                    continue
            
            connection.commit()
            cursor.close()
            connection.close()
            
            if errors:
                return jsonify({
                    'message': f'Uploaded {records_inserted} records with {len(errors)} errors',
                    'records_count': records_inserted,
                    'errors': errors[:5]  # Return first 5 errors
                }), 207  # Partial content
            
            return jsonify({
                'message': f'Successfully uploaded {records_inserted} records',
                'records_count': records_inserted
            })
            
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file format. Please upload .xlsx or .xls files only'}), 400

@app.route('/api/finances/<int:user_id>/<int:year>', methods=['GET'])
def get_financial_data(user_id, year):
    """Retrieve financial data for specified user and year"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Get user name
        cursor.execute("SELECT name FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get financial records
        cursor.execute("""
            SELECT month, amount 
            FROM financial_records 
            WHERE user_id = %s AND year = %s 
            ORDER BY month
        """, (user_id, year))
        
        records = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'user_name': user['name'],
            'year': year,
            'records': records
        })
        
    except Exception as e:
        return jsonify({'error': f'Error retrieving data: {str(e)}'}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name FROM users")
        users = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({'users': users})
        
    except Exception as e:
        return jsonify({'error': f'Error retrieving users: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Starting Financial Dashboard Server...")
    init_database()
    app.run(debug=True, port=5000)