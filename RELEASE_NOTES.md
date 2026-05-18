# Node Eye v2.0 - Release Notes

**Release Date:** 2026-05-18  
**Version:** 2.0.0  
**Status:** ✅ Released to GitHub

---

## 🎉 Major Features

### 1. 🌐 Multi-Language Support

Node Eye now supports multiple languages with seamless switching:

- **Default Language:** English
- **Supported Languages:** 
  - 🇺🇸 English
  - 🇨🇳 中文 (Chinese)
- **Easy Extension:** Add new languages by creating `locales/<lang>.json`

**How to Use:**
- Language switcher located in the header (top-right)
- Preference saved in localStorage
- All UI text, table headers, and messages are translated

**Files:**
- `js/i18n.js` - Internationalization module
- `locales/en.json` - English translations
- `locales/zh.json` - Chinese translations

---

### 2. 📧 Subscription System

Users can now subscribe to receive daily JSON reports for their preferred blockchain:

**Frontend:**
- Subscribe button in header (📧 Subscribe)
- Beautiful modal with email + blockchain selection
- Success/error messages with i18n support
- localStorage fallback when backend unavailable

**Backend API (Flask):**
- `POST /api/subscribe` - Register subscription
- `GET /api/subscriptions` - List all subscriptions (admin)
- `POST /api/send-daily-emails` - Send daily reports
- SQLite database for persistent storage

**Email Features:**
- Daily automated emails at configurable time
- JSON file attachment with full node data
- Summary statistics in email body
- SMTP support (Gmail, SendGrid, etc.)

**Setup:**
```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Configure environment
export NODEEYE_EMAIL_FROM="your-email@gmail.com"
export NODEEYE_EMAIL_PASSWORD="your-app-password"

# Start API server
python app.py

# Set up daily cron job (9 AM UTC)
crontab -e
# Add: 0 9 * * * /usr/bin/python3 /path/to/backend/send_daily_emails.py
```

**Files:**
- `backend/app.py` - Flask API server
- `backend/send_daily_emails.py` - Daily email script
- `backend/cron-example.sh` - Cron configuration example
- `js/subscription.js` - Frontend subscription handler

---

### 3. 📊 Enhanced Table Columns

Updated table structure to match new JSON field specification:

| Column | Description | JSON Field |
|--------|-------------|------------|
| # | Row number | - |
| Host | Node address | `host` |
| Port | Port number | `port` |
| SSL | SSL/TLS status | `ssl` |
| Height | Block height | `height` |
| Version | Server version | `server_version` |
| Protocol | Protocol version | `protocol_version` |
| Status | Connection status | `status` |
| Connection Time | Last seen timestamp | `last_seen` |
| Response Time | Response time (ms) | `response_time_ms` |
| Hourly | Hourly uptime | `per_hour` |
| Daily | Daily uptime | `per_day` |
| Monthly | Monthly uptime | `per_month` |

**Visual Improvements:**
- SSL badge with ✓/✗ icon
- Response time displayed in ms
- Uptime bars with color grading (high/medium/low)
-Sortable by all new columns

**Files:**
- `convert_data.py` - Updated data conversion
- `update_data.py` - Updated data updater
- `js/renderer.js` - Enhanced table renderer
- `data/bitcoin.json` - Sample data with new structure

---

## 🔧 Technical Changes

### Code Quality
- ✅ All code comments converted to English
- ✅ Improved code organization and modularity
- ✅ Better error handling and fallbacks
- ✅ Comprehensive documentation

### Architecture
- Frontend remains pure static (GitHub Pages compatible)
- Backend is optional (degrades gracefully without it)
- Subscription storage: Backend DB → localStorage fallback
- Multi-language: JSON-based translation system

### Dependencies
**Frontend:** None (vanilla JavaScript)  
**Backend:**
- Flask 3.0.0
- Flask-CORS 4.0.0

---

## 📝 Migration Guide

### For Existing Deployments

1. **Update Code:**
   ```bash
   git pull origin main
   ```

2. **Update Data Files:**
   - Existing JSON files will still work
   - Run `convert_data.py` to update to new format
   - Or manually update field names

3. **Optional: Enable Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

4. **Optional: Set Up Daily Emails**
   - Configure environment variables
   - Add cron job (see `cron-example.sh`)

### Field Name Changes

If you have custom integrations, note these field name changes:

| Old Field | New Field |
|-----------|-----------|
| `proto` | `ssl` (boolean) |
| `version` | `server_version` |
| `protocol` | `protocol_version` |
| `connection` | `status` |
| `connectionTime` | `last_seen` |
| `uptime` | `per_hour` |
| `hour` | (removed) |
| `day` | `per_day` |
| `month` | `per_month` |

---

## 🎯 Usage Examples

### Subscribe via API

```bash
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "chainId": "bitcoin"}'
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

### Get All Subscriptions

```bash
curl http://localhost:5000/api/subscriptions
```

### Trigger Daily Emails

```bash
curl -X POST http://localhost:5000/api/send-daily-emails
```

---

## 🐛 Known Issues

- None at this time
- Report issues on GitHub: https://github.com/KevinGong/node-eye/issues

---

## 🚀 Future Roadmap

- [ ] Telegram Bot alerts for node downtime
- [ ] Node history trends and charts
- [ ] Geographic node map
- [ ] Node anomaly detection
- [ ] More languages (Japanese, Korean, Spanish, etc.)
- [ ] User dashboard for subscription management
- [ ] Email template customization

---

## 📊 Statistics

- **Lines of Code:** ~2,500+ (frontend + backend)
- **Files Changed:** 18
- **New Files:** 8
- **Languages Supported:** 2 (easily extensible)
- **API Endpoints:** 4

---

## 🙏 Credits

- Original concept: Bitcoin Eye (https://1209k.com/bitcoin-eye/)
- UI Design: Dark tech theme inspired by Grafana/Prometheus
- Developed by: Node Eye Team

---

## 📄 License

MIT License - See LICENSE file for details

---

**Upgrade Now:**
```bash
cd /path/to/node-eye
git pull origin main
```

**Questions?** Check the updated README.md or open an issue on GitHub.
