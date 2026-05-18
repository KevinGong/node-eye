#!/usr/bin/env python3
"""
Node Eye Backend API
Handles subscription management and daily email sending
"""

import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend API calls

# Configuration
DB_PATH = Path(__file__).parent / 'subscriptions.db'
DATA_DIR = Path(__file__).parent.parent / 'data'
EMAIL_FROM = os.getenv('NODEEYE_EMAIL_FROM', 'noreply@nodeeye.io')
EMAIL_PASSWORD = os.getenv('NODEEYE_EMAIL_PASSWORD', '')
SMTP_SERVER = os.getenv('NODEEYE_SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('NODEEYE_SMTP_PORT', '587'))

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            chain_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            active BOOLEAN DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """
    Register a new subscription
    Expects: { "email": "user@example.com", "chainId": "bitcoin" }
    """
    data = request.json
    
    if not data or 'email' not in data or 'chainId' not in data:
        return jsonify({'error': 'Email and chainId are required'}), 400
    
    email = data['email']
    chain_id = data['chainId']
    
    # Basic email validation
    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Invalid email format'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if subscription exists
        cursor.execute('SELECT id FROM subscriptions WHERE email = ?', (email,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing subscription
            cursor.execute('''
                UPDATE subscriptions 
                SET chain_id = ?, updated_at = ?, active = 1 
                WHERE email = ?
            ''', (chain_id, datetime.now(), email))
            print(f"📧 Updated subscription for {email} -> {chain_id}")
        else:
            # Create new subscription
            cursor.execute('''
                INSERT INTO subscriptions (email, chain_id, created_at, updated_at, active)
                VALUES (?, ?, ?, ?, 1)
            ''', (email, chain_id, datetime.now(), datetime.now()))
            print(f"📧 New subscription: {email} -> {chain_id}")
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Subscription successful',
            'email': email,
            'chainId': chain_id
        }), 200
        
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        print(f"❌ Subscription error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscriptions', methods=['GET'])
def get_subscriptions():
    """
    Get all active subscriptions (admin endpoint)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, chain_id, created_at, updated_at, active
            FROM subscriptions
            WHERE active = 1
            ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        subscriptions = []
        for row in rows:
            subscriptions.append({
                'id': row['id'],
                'email': row['email'],
                'chainId': row['chain_id'],
                'createdAt': row['created_at'],
                'updatedAt': row['updated_at'],
                'active': bool(row['active'])
            })
        
        return jsonify({
            'success': True,
            'count': len(subscriptions),
            'subscriptions': subscriptions
        }), 200
        
    except Exception as e:
        print(f"❌ Error fetching subscriptions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-daily-emails', methods=['POST'])
def send_daily_emails():
    """
    Send daily JSON reports to all subscribers
    Triggered by cron job daily
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT email, chain_id FROM subscriptions WHERE active = 1')
        subscribers = cursor.fetchall()
        conn.close()
        
        if not subscribers:
            return jsonify({'success': True, 'message': 'No subscribers', 'sent': 0}), 200
        
        sent_count = 0
        failed_count = 0
        
        for email, chain_id in subscribers:
            try:
                # Load JSON data for the chain
                data_file = DATA_DIR / f'{chain_id}.json'
                if not data_file.exists():
                    print(f"⚠️  Data file not found: {data_file}")
                    failed_count += 1
                    continue
                
                with open(data_file, 'r', encoding='utf-8') as f:
                    chain_data = json.load(f)
                
                # Send email
                send_email_with_attachment(
                    to_email=email,
                    chain_id=chain_id,
                    chain_data=chain_data
                )
                
                sent_count += 1
                print(f"✅ Email sent to {email} for {chain_id}")
                
            except Exception as e:
                print(f"❌ Failed to send to {email}: {e}")
                failed_count += 1
        
        return jsonify({
            'success': True,
            'message': f'Sent {sent_count} emails, {failed_count} failed',
            'sent': sent_count,
            'failed': failed_count
        }), 200
        
    except Exception as e:
        print(f"❌ Error sending emails: {e}")
        return jsonify({'error': str(e)}), 500

def send_email_with_attachment(to_email, chain_id, chain_data):
    """
    Send email with JSON file attachment
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = f'Node Eye Daily Report - {chain_id.upper()} - {datetime.now().strftime("%Y-%m-%d")}'
    
    # Email body
    body = f"""
    Hello,
    
    Here is your daily Node Eye report for {chain_id.upper()}.
    
    Summary:
    - Total Nodes: {chain_data.get('summary', {}).get('total', len(chain_data.get('nodes', [])))}
    - Online Nodes: {chain_data.get('summary', {}).get('online', 0)}
    - Offline Nodes: {chain_data.get('summary', {}).get('offline', 0)}
    - Last Update: {chain_data.get('lastUpdate', 'N/A')}
    
    The attached JSON file contains detailed node information.
    
    Best regards,
    Node Eye Team
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach JSON file
    filename = f'{chain_id}_nodes_{datetime.now().strftime("%Y%m%d")}.json'
    
    # Create a temporary file for attachment
    temp_path = Path('/tmp') / filename
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(chain_data, f, indent=2, ensure_ascii=False)
    
    with open(temp_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="{filename}"'
        )
        msg.attach(part)
    
    # Clean up temp file
    temp_path.unlink()
    
    # Send via SMTP
    if EMAIL_PASSWORD:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
    else:
        # Log email content if no SMTP configured (for testing)
        print(f"📧 Email would be sent to {to_email}")
        print(f"   Subject: {msg['Subject']}")
        print(f"   Body: {body[:200]}...")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected' if DB_PATH.exists() else 'not_initialized'
    }), 200

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Start Flask server
    port = int(os.getenv('NODEEYE_PORT', 5000))
    print(f"🚀 Starting Node Eye Backend API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
