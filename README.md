# Node Eye - Multi-Chain Blockchain Node Monitoring Platform

<div align="center">

👁️ **Real-time Monitoring · Multi-Chain Support · Subscription Feature**

A modern, beautiful, tech-styled blockchain node monitoring platform

[Online Demo](#) · [Features](#features) · [Deployment](#deployment) · [API](#api)

</div>

---

## 📖 Introduction

Node Eye is a modern blockchain node monitoring platform with a dark tech-style UI, inspired by [Bitcoin Eye](https://1209k.com/bitcoin-eye/ele.php) and designed like Grafana/Prometheus monitoring dashboards.

**Frontend**: Pure static architecture (HTML + CSS + JavaScript), deployable to GitHub Pages  
**Backend**: Optional Flask API for subscription management and daily email reports

## ✨ Features

### Core Features
- 🔗 **Multi-Chain Support** - Bitcoin, Litecoin, Dogecoin, Ethereum, and more
- 📊 **Statistics Dashboard** - Total nodes, online/offline counts, average uptime
- 🔍 **Search & Filter** - Search by host, filter by status (all/online/offline)
- 📈 **Sorting** - Sort by height, hourly/daily/monthly uptime (ascending/descending)
- 📋 **One-Click Copy** - Copy node address (host:port) instantly
- 📱 **Responsive Design** - Desktop and mobile support, horizontal scroll for tables

### 🆕 New Features (v2.0)
- 🌐 **Multi-Language Support** - English and Chinese (easily extensible)
- 📧 **Subscription System** - Subscribe to daily JSON reports for your preferred blockchain
- 📊 **Enhanced Table Columns** - SSL status, response time, connection time, and more

### Monitored Fields
| Field | Description |
|-------|-------------|
| Host | Node address |
| Port | Port number |
| SSL | SSL/TLS enabled (✓/✗) |
| Height | Block height |
| Version | Server version |
| Protocol | Protocol version |
| Status | Connection status (open/offline) |
| Connection Time | Last seen timestamp |
| Response Time | Response time in ms |
| Hourly Uptime | Hourly uptime percentage |
| Daily Uptime | Daily uptime percentage |
| Monthly Uptime | Monthly uptime percentage |

### Visual Effects
- 🎨 Dark tech theme (#0a0e1a background)
- 💙 Tech blue/purple gradient accents
- ✅ Status colors: Green (online), Red (offline)
- 🌊 Pulse animation for online status
- 📊 Uptime progress bars with color grading

## 🚀 Quick Start

### Local Development
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/node-eye.git
cd node-eye

# Start with any static server
# Option 1: Python
python -m http.server 8080

# Option 2: Node.js (requires http-server)
npx http-server -p 8080

# Option 3: VS Code Live Server
# Right-click index.html → "Open with Live Server"
```

Then visit `http://localhost:8080`

### Backend API (Optional)

The backend provides subscription management and daily email sending:

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Set environment variables
export NODEEYE_EMAIL_FROM="your-email@gmail.com"
export NODEEYE_EMAIL_PASSWORD="your-app-password"
export NODEEYE_SMTP_SERVER="smtp.gmail.com"
export NODEEYE_SMTP_PORT="587"

# Start the API server
python app.py

# Server runs on http://localhost:5000
```

### API Endpoints

#### Subscribe to Daily Reports
```bash
POST /api/subscribe
Content-Type: application/json

{
  "email": "user@example.com",
  "chainId": "bitcoin"
}
```

Response:
```json
{
  "success": true,
  "message": "Subscription successful",
  "email": "user@example.com",
  "chainId": "bitcoin"
}
```

#### Get All Subscriptions (Admin)
```bash
GET /api/subscriptions
```

#### Send Daily Emails (Cron Job)
```bash
POST /api/send-daily-emails
```

### Daily Email Cron Job

Set up a cron job to send daily emails automatically:

```bash
# Edit crontab
crontab -e

# Add this line to send emails at 9:00 AM UTC daily
0 9 * * * /usr/bin/python3 /path/to/node-eye/backend/send_daily_emails.py >> /var/log/nodeeye_emails.log 2>&1
```

See `backend/cron-example.sh` for detailed configuration.

### Deploy to GitHub Pages

1. **Create Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Node Eye"
   git remote add origin https://github.com/YOUR_USERNAME/node-eye.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to Settings → Pages
   - Select `main` branch and `/ (root)` directory
   - Save and wait for deployment

3. **Access Your Site**
   - Your site will be live at `https://YOUR_USERNAME.github.io/node-eye/`

## 📁 Directory Structure

```
node-eye/
├── index.html                 # Main HTML file
├── css/
│   └── style.css             # Stylesheet
├── js/
│   ├── i18n.js               # Internationalization module
│   ├── chains.js             # Chain configuration manager
│   ├── renderer.js           # Table renderer
│   ├── app.js                # Main application logic
│   └── subscription.js       # Subscription handler
├── locales/
│   ├── en.json               # English translations
│   └── zh.json               # Chinese translations
├── data/
│   ├── chains.json           # Chain configuration
│   ├── bitcoin.json          # Bitcoin node data
│   ├── ethereum.json         # Ethereum node data
│   └── ...                   # Other chains
├── backend/                   # Optional backend API
│   ├── app.py                # Flask API server
│   ├── send_daily_emails.py  # Daily email sender
│   ├── requirements.txt      # Python dependencies
│   └── cron-example.sh       # Cron job example
├── convert_data.py           # Data conversion script
└── README.md                 # This file
```

## 🌐 Multi-Language Support

Node Eye supports multiple languages with easy switching:

- **Default**: English
- **Available**: English (🇺🇸), Chinese (🇨🇳)
- **Add More**: Create `locales/<lang>.json` following the existing format

Language preference is saved in localStorage and persists across sessions.

## 📧 Subscription Feature

Users can subscribe to receive daily JSON reports for their preferred blockchain:

1. Click the "📧 Subscribe" button
2. Enter email address
3. Select blockchain
4. Click "Subscribe"

Subscriptions are stored in:
- **Backend**: SQLite database (when API is available)
- **Frontend**: localStorage (fallback mode)

Daily emails include:
- Summary statistics (total, online, offline nodes)
- Last update timestamp
- Attached JSON file with detailed node data

## 🔧 Configuration

### Environment Variables (Backend)

| Variable | Description | Default |
|----------|-------------|---------|
| `NODEEYE_EMAIL_FROM` | Sender email address | `noreply@nodeeye.io` |
| `NODEEYE_EMAIL_PASSWORD` | SMTP password | (empty) |
| `NODEEYE_SMTP_SERVER` | SMTP server | `smtp.gmail.com` |
| `NODEEYE_SMTP_PORT` | SMTP port | `587` |
| `NODEEYE_PORT` | API server port | `5000` |

### Data Format

Node data JSON structure:

```json
{
  "chain": "bitcoin",
  "lastUpdate": "2026-05-18T11:00:00+08:00",
  "nodes": [
    {
      "host": "node.example.com",
      "port": 50002,
      "ssl": true,
      "height": 949206,
      "server_version": "Fulcrum 2.1.0",
      "protocol_version": "1.4",
      "status": "open",
      "last_seen": "2026-05-18 10:30:00",
      "response_time_ms": 2478,
      "per_hour": 1.0000,
      "per_day": 1.0000,
      "per_month": 0.9988
    }
  ]
}
```

## 🛠️ Development

### Update Node Data

Run the conversion script to update node data from Electrum discovery:

```bash
python3 convert_data.py
```

Or use the update script:

```bash
python3 update_data.py
```

### Add New Chain

1. Add chain to `data/chains.json`:
   ```json
   {
     "id": "newchain",
     "name": "New Chain",
     "symbol": "NEW",
     "icon": "🆕",
     "color": "#123456",
     "dataFile": "newchain.json"
   }
   ```

2. Create `data/newchain.json` with node data

3. The chain will appear in the selector automatically

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

- GitHub Issues: Report bugs or request features
- Email: support@nodeeye.io (for subscription issues)

---

<div align="center">

**Node Eye** © 2026 | Built with ❤️ for the blockchain community

</div>
