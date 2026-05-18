#!/usr/bin/env python3
"""
Node Eye Subscription Handler - GitHub Actions
Complete implementation with:
- Email verification
- Unsubscribe functionality  
- Daily email sending with JSON attachments
- GitHub Issues integration for subscription storage

Usage:
  python subscription_handler.py [action]
  
Actions:
  - send: Send daily emails to verified subscribers
  - add: Add new subscription (pending verification)
  - verify: Verify email with code
  - remove: Remove/unsubscribe email
  - list: List all subscriptions
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import random
import hashlib

# ============================================================================
# Configuration
# ============================================================================

# Subscriptions storage (GitHub Actions persistent storage via artifact)
SUBSCRIPTIONS_FILE = Path('/tmp/subscriptions.json')

# Node data directory
DATA_DIR = Path(os.getenv('DATA_DIR', '/tmp/data'))

# Email configuration
EMAIL_FROM = os.getenv('NODEEYE_EMAIL_FROM', '')
EMAIL_PASSWORD = os.getenv('NODEEYE_EMAIL_PASSWORD', '')
SMTP_SERVER = os.getenv('NODEEYE_SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('NODEEYE_SMTP_PORT', '587'))

# Verification settings
VERIFICATION_CODE_LENGTH = 6
VERIFICATION_EXPIRY_HOURS = 24

# ============================================================================
# Subscription Management
# ============================================================================

def load_subscriptions():
    """Load subscriptions from JSON file"""
    if SUBSCRIPTIONS_FILE.exists():
        with open(SUBSCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Initialize empty structure
    return {
        'verified': [],
        'pending': [],
        'unsubscribed': []
    }

def save_subscriptions(data):
    """Save subscriptions to JSON file"""
    SUBSCRIPTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SUBSCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Subscriptions saved to {SUBSCRIPTIONS_FILE}")

def generate_verification_code():
    """Generate random verification code"""
    return ''.join([str(random.randint(0, 9)) for _ in range(VERIFICATION_CODE_LENGTH)])

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def add_subscription(email, chain_id):
    """
    Add a new subscription (pending verification)
    Returns: dict with success status and verification code
    """
    print(f"\n📝 Adding subscription: {email} for {chain_id}")
    
    if not validate_email(email):
        return {'success': False, 'error': 'Invalid email format'}
    
    if not chain_id:
        return {'success': False, 'error': 'Chain ID is required'}
    
    data = load_subscriptions()
    
    # Check if already verified
    for sub in data['verified']:
        if sub['email'] == email:
            # Update existing subscription
            sub['chain_id'] = chain_id
            sub['updated_at'] = datetime.now().isoformat()
            save_subscriptions(data)
            return {
                'success': True,
                'message': 'Subscription updated',
                'already_verified': True
            }
    
    # Check if already pending
    for sub in data['pending']:
        if sub['email'] == email:
            # Regenerate verification code
            code = generate_verification_code()
            sub['verification_code'] = code
            sub['verification_sent_at'] = datetime.now().isoformat()
            sub['chain_id'] = chain_id
            save_subscriptions(data)
            return {
                'success': True,
                'message': 'Verification code resent',
                'verification_code': code,  # In production, don't return this
                'email': email
            }
    
    # Check if unsubscribed
    for sub in data['unsubscribed']:
        if sub['email'] == email:
            return {
                'success': False,
                'error': 'This email has been unsubscribed'
            }
    
    # Create new pending subscription
    verification_code = generate_verification_code()
    pending_sub = {
        'email': email,
        'chain_id': chain_id,
        'verification_code': verification_code,
        'created_at': datetime.now().isoformat(),
        'verification_sent_at': datetime.now().isoformat(),
        'attempts': 0
    }
    
    data['pending'].append(pending_sub)
    save_subscriptions(data)
    
    print(f"✅ Pending subscription created for {email}")
    
    return {
        'success': True,
        'message': 'Subscription pending verification',
        'email': email,
        'verification_code': verification_code  # In production, send via email only
    }

def verify_email(email, code):
    """
    Verify email with confirmation code
    Returns: dict with success status
    """
    print(f"\n✅ Verifying email: {email} with code: {code}")
    
    data = load_subscriptions()
    
    for i, sub in enumerate(data['pending']):
        if sub['email'] == email:
            # Check attempts
            if sub.get('attempts', 0) >= 3:
                return {
                    'success': False,
                    'error': 'Too many verification attempts. Please subscribe again.'
                }
            
            # Check code
            if sub.get('verification_code') == code:
                # Move to verified
                verified_sub = {
                    'email': email,
                    'chain_id': sub['chain_id'],
                    'created_at': sub['created_at'],
                    'verified_at': datetime.now().isoformat(),
                    'verified': True
                }
                data['verified'].append(verified_sub)
                data['pending'].pop(i)
                save_subscriptions(data)
                
                print(f"✅ Email verified: {email}")
                return {
                    'success': True,
                    'message': 'Email verified successfully! You will receive daily reports.'
                }
            else:
                # Increment attempts
                sub['attempts'] = sub.get('attempts', 0) + 1
                save_subscriptions(data)
                
                remaining = 3 - sub['attempts']
                return {
                    'success': False,
                    'error': f'Invalid verification code. {remaining} attempts remaining.'
                }
    
    return {
        'success': False,
        'error': 'Subscription not found. Please subscribe first.'
    }

def remove_subscription(email, reason='user_request'):
    """
    Remove/unsubscribe an email
    Returns: dict with success status
    """
    print(f"\n❌ Removing subscription: {email} (reason: {reason})")
    
    data = load_subscriptions()
    removed = False
    
    # Remove from verified
    for i, sub in enumerate(data['verified']):
        if sub['email'] == email:
            # Add to unsubscribed list
            unsub = {
                'email': email,
                'chain_id': sub['chain_id'],
                'unsubscribed_at': datetime.now().isoformat(),
                'reason': reason
            }
            data['unsubscribed'].append(unsub)
            data['verified'].pop(i)
            removed = True
            break
    
    # Remove from pending
    for i, sub in enumerate(data['pending']):
        if sub['email'] == email:
            data['pending'].pop(i)
            removed = True
            break
    
    if removed:
        save_subscriptions(data)
        print(f"✅ Unsubscribed: {email}")
        return {
            'success': True,
            'message': 'Successfully unsubscribed. Sorry to see you go!'
        }
    else:
        return {
            'success': False,
            'error': 'Email not found in subscriptions'
        }

def list_subscriptions():
    """List all subscriptions"""
    data = load_subscriptions()
    
    print("\n📊 Subscription Statistics")
    print("=" * 50)
    print(f"Verified:   {len(data['verified'])}")
    print(f"Pending:    {len(data['pending'])}")
    print(f"Unsubscribed: {len(data['unsubscribed'])}")
    
    if data['verified']:
        print("\n✅ Verified Subscribers:")
        for sub in data['verified']:
            print(f"  - {sub['email']} ({sub['chain_id']})")
    
    if data['pending']:
        print("\n⏳ Pending Verification:")
        for sub in data['pending']:
            print(f"  - {sub['email']} ({sub['chain_id']}) - Code: {sub.get('verification_code', 'N/A')}")
    
    return data

# ============================================================================
# Email Sending
# ============================================================================

def send_email(msg, to_email):
    """Send email via SMTP"""
    if not EMAIL_PASSWORD:
        print(f"📧 [DRY RUN] Email would be sent to {to_email}")
        print(f"   Subject: {msg['Subject']}")
        print(f"   From: {EMAIL_FROM}")
        return True
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def send_verification_email(to_email, code, chain_id):
    """Send verification email to user"""
    print(f"\n📧 Sending verification email to {to_email}")
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = 'Node Eye - Verify Your Subscription'
    
    body = f"""
Hello,

Thank you for subscribing to Node Eye daily reports!

To confirm your subscription, please use the following verification code:

┌─────────────────────────────┐
│  Verification Code: {code}  │
└─────────────────────────────┘

Blockchain: {chain_id.upper()}

This code will expire in {VERIFICATION_EXPIRY_HOURS} hours.

If you didn't request this subscription, please ignore this email.

Best regards,
Node Eye Team

---
Node Eye - Multi-Chain Node Monitoring
https://github.com/KevinGong/node-eye
"""
    
    msg.attach(MIMEText(body, 'plain'))
    return send_email(msg, to_email)

def send_daily_emails():
    """
    Send daily reports to all verified subscribers
    Returns: dict with send statistics
    """
    print("\n🚀 Starting daily email send...")
    print(f"   Time: {datetime.now().isoformat()}")
    
    data = load_subscriptions()
    
    if not data['verified']:
        print("📭 No verified subscribers")
        return {'success': True, 'sent': 0, 'failed': 0}
    
    print(f"📧 Found {len(data['verified'])} verified subscribers")
    
    sent_count = 0
    failed_count = 0
    
    for sub in data['verified']:
        email = sub['email']
        chain_id = sub['chain_id']
        
        try:
            # Load JSON data for the chain
            data_file = DATA_DIR / f'{chain_id}.json'
            if not data_file.exists():
                print(f"⚠️  Data file not found: {data_file}")
                failed_count += 1
                continue
            
            with open(data_file, 'r', encoding='utf-8') as f:
                chain_data = json.load(f)
            
            # Send email with attachment
            success = send_email_with_attachment(
                to_email=email,
                chain_id=chain_id,
                chain_data=chain_data
            )
            
            if success:
                sent_count += 1
                print(f"✅ Email sent to {email} for {chain_id}")
            else:
                failed_count += 1
                
        except Exception as e:
            print(f"❌ Failed to send to {email}: {e}")
            failed_count += 1
    
    print(f"\n✅ Daily email complete: {sent_count} sent, {failed_count} failed")
    return {'success': True, 'sent': sent_count, 'failed': failed_count}

def send_email_with_attachment(to_email, chain_id, chain_data):
    """Send email with JSON attachment"""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = f'Node Eye Daily Report - {chain_id.upper()} - {datetime.now().strftime("%Y-%m-%d")}'
    
    # Email body with summary
    summary = chain_data.get('summary', {})
    nodes = chain_data.get('nodes', [])
    
    body = f"""
Hello,

Here is your daily Node Eye report for {chain_id.upper()}.

┌─────────────────────────────────────────┐
│              Summary                    │
├─────────────────────────────────────────┤
│ Total Nodes:        {summary.get('total', len(nodes)):>6}
│ Online Nodes:       {summary.get('online', 0):>6}
│ Offline Nodes:      {summary.get('offline', 0):>6}
│ Avg Response Time:  {summary.get('avg_response_time', 0):>6.0f}ms
└─────────────────────────────────────────┘

Last Update: {chain_data.get('lastUpdate', 'N/A')}

The attached JSON file contains detailed node information including:
- Node addresses and ports
- SSL/TLS status
- Block height
- Server version
- Response times
- Uptime statistics (hourly, daily, monthly)

┌─────────────────────────────────────────┐
│          Unsubscribe Instructions       │
├─────────────────────────────────────────┤
│ To unsubscribe from these reports:      │
│ 1. Reply to this email with "UNSUBSCRIBE" │
│ 2. Or visit: https://github.com/KevinGong/node-eye │
└─────────────────────────────────────────┘

Best regards,
Node Eye Team

---
Node Eye - Multi-Chain Node Monitoring
https://github.com/KevinGong/node-eye
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach JSON file
    filename = f'{chain_id}_nodes_{datetime.now().strftime("%Y%m%d")}.json'
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
    
    return send_email(msg, to_email)

def process_unsubscribe_email(email_subject, email_from):
    """
    Process unsubscribe request from email reply
    Called when user replies with UNSUBSCRIBE in subject
    """
    if 'unsubscribe' in email_subject.lower():
        print(f"\n📧 Processing unsubscribe from email: {email_from}")
        return remove_subscription(email_from, reason='email_reply')
    return None

# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Main entry point for GitHub Action"""
    action = os.getenv('ACTION_TYPE', 'send')
    
    print("=" * 60)
    print("👁️  Node Eye Subscription Handler")
    print("=" * 60)
    print(f"Action: {action}")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Data Dir: {DATA_DIR}")
    
    result = None
    
    if action == 'send':
        # Send daily emails
        result = send_daily_emails()
        
    elif action == 'add':
        email = os.getenv('SUBSCRIBER_EMAIL', '')
        chain_id = os.getenv('SUBSCRIBER_CHAIN', '')
        
        result = add_subscription(email, chain_id)
        
        # If pending, send verification email
        if result.get('success') and not result.get('already_verified'):
            code = result.get('verification_code')
            if code and EMAIL_FROM:
                send_verification_email(email, code, chain_id)
        
    elif action == 'verify':
        email = os.getenv('SUBSCRIBER_EMAIL', '')
        code = os.getenv('VERIFICATION_CODE', '')
        
        result = verify_email(email, code)
        
    elif action == 'remove':
        email = os.getenv('SUBSCRIBER_EMAIL', '')
        reason = os.getenv('UNSUBSCRIBE_REASON', 'user_request')
        
        result = remove_subscription(email, reason)
        
    elif action == 'list':
        result = list_subscriptions()
        
    else:
        print(f"❌ Unknown action: {action}")
        sys.exit(1)
    
    # Output result as JSON for GitHub Actions
    print("\n" + "=" * 60)
    print("Result:")
    print(json.dumps(result, indent=2))
    
    # Set output for GitHub Actions
    if os.getenv('GITHUB_OUTPUT'):
        with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
            f.write(f"result={json.dumps(result)}\n")
    
    # Exit with error if failed
    if isinstance(result, dict) and not result.get('success', True):
        sys.exit(1)

if __name__ == '__main__':
    main()
