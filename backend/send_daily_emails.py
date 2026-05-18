#!/usr/bin/env python3
"""
Daily Email Sender Script
Send JSON reports to all subscribers
Run this daily via cron job
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app import send_daily_emails, init_db

def main():
    """Main entry point"""
    print("🚀 Starting daily email sender...")
    
    # Initialize database
    init_db()
    
    # Check environment variables
    if not os.getenv('NODEEYE_EMAIL_FROM'):
        print("⚠️  Warning: NODEEYE_EMAIL_FROM not set, emails will be logged only")
    
    # Send emails
    result = send_daily_emails()
    
    print(f"✅ Daily email sender completed")
    return result

if __name__ == '__main__':
    main()
