#!/usr/bin/env python3
"""
Send Node Eye Daily Reports to Subscribers
Called automatically after data update

Usage:
  python send_subscription_emails.py [chain_id]
  
If chain_id not specified, sends for all chains with data
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Import encryption utilities
sys.path.insert(0, str(Path(__file__).parent))
from encrypt_subscribers import load_subscribers, get_subscribers_for_chain

# ============================================================================
# Email Configuration
# ============================================================================

EMAIL_FROM = os.getenv('NODEEYE_EMAIL_FROM', 'your-email@gmail.com')
EMAIL_PASSWORD = os.getenv('NODEEYE_EMAIL_PASSWORD', '')  # Set via environment
SMTP_SERVER = os.getenv('NODEEYE_SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('NODEEYE_SMTP_PORT', '587'))

DATA_DIR = Path(__file__).parent.parent / 'data'

# ============================================================================
# Email Functions
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
        print(f"❌ Failed to send to {to_email}: {e}")
        return False

def send_daily_report(subscriber, chain_data):
    """Send daily report to a single subscriber"""
    email = subscriber['email']
    chain_id = subscriber['chain_id']
    
    # Create email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = email
    msg['Subject'] = f'Node Eye Daily Report - {chain_id.upper()} - {datetime.now().strftime("%Y-%m-%d")}'
    
    # Email body
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
│ Reply to this email with "UNSUBSCRIBE"  │
│ or contact the administrator.           │
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
    
    temp_path.unlink()
    
    return send_email(msg, email)

def send_reports_for_chain(chain_id: str):
    """Send reports for a specific chain"""
    print(f"\n🚀 Sending reports for {chain_id.upper()}...")
    
    # Load chain data
    data_file = DATA_DIR / f'{chain_id}.json'
    if not data_file.exists():
        print(f"⚠️  Data file not found: {data_file}")
        return 0, 1
    
    with open(data_file, 'r', encoding='utf-8') as f:
        chain_data = json.load(f)
    
    # Get subscribers for this chain
    subscribers = get_subscribers_for_chain(chain_id)
    
    if not subscribers:
        print(f"📭 No subscribers for {chain_id}")
        return 0, 0
    
    print(f"📧 Found {len(subscribers)} subscribers")
    
    sent_count = 0
    failed_count = 0
    
    for sub in subscribers:
        success = send_daily_report(sub, chain_data)
        if success:
            sent_count += 1
        else:
            failed_count += 1
    
    return sent_count, failed_count

def send_all_reports():
    """Send reports for all chains"""
    print("\n" + "=" * 60)
    print("👁️  Node Eye Daily Report Sender")
    print("=" * 60)
    print(f"Time: {datetime.now().isoformat()}")
    
    total_sent = 0
    total_failed = 0
    
    # Send for each chain with data
    for chain_file in DATA_DIR.glob('*.json'):
        if chain_file.name == 'subscribers.enc' or chain_file.name == 'chains.json':
            continue
        
        chain_id = chain_file.stem
        sent, failed = send_reports_for_chain(chain_id)
        total_sent += sent
        total_failed += failed
    
    print("\n" + "=" * 60)
    print(f"✅ Complete: {total_sent} sent, {total_failed} failed")
    print("=" * 60)
    
    return total_sent, total_failed

def main():
    """Main entry point"""
    print("\n🚀 Node Eye Subscription Email Sender")
    print(f"   Time: {datetime.now().isoformat()}")
    print(f"   Data Dir: {DATA_DIR}")
    
    # Check if email is configured
    if not EMAIL_PASSWORD:
        print("\n⚠️  WARNING: EMAIL_PASSWORD not set!")
        print("   Set NODEEYE_EMAIL_PASSWORD environment variable to send emails.")
        print("   Running in dry-run mode...\n")
    
    if len(sys.argv) > 1:
        # Send for specific chain
        chain_id = sys.argv[1]
        sent, failed = send_reports_for_chain(chain_id)
    else:
        # Send for all chains
        sent, failed = send_all_reports()
    
    print(f"\n📊 Summary:")
    print(f"   Sent: {sent}")
    print(f"   Failed: {failed}")
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
