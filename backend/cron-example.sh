#!/bin/bash
# Node Eye Daily Email Cron Job
# Add this to your crontab: crontab -e
# Example: Send daily emails at 9:00 AM UTC every day

# Set environment variables
export NODEEYE_EMAIL_FROM="your-email@gmail.com"
export NODEEYE_EMAIL_PASSWORD="your-app-password"
export NODEEYE_SMTP_SERVER="smtp.gmail.com"
export NODEEYE_SMTP_PORT="587"
export NODEEYE_PORT="5000"

# Change to script directory
cd /home/admin/openclaw/workspace/node-eye/backend

# Run daily email sender at 9:00 AM UTC
0 9 * * * /usr/bin/python3 /home/admin/openclaw/workspace/node-eye/backend/send_daily_emails.py >> /var/log/nodeeye_emails.log 2>&1
