# Node Eye Implementation Plan

## Task: Multi-language Support + Subscription Feature + Table Format Update

**Created:** 2026-05-18 11:40

---

## Requirements

### 1. Multi-language Support
- Default: English
- Support: Chinese (and other common languages)
- Language switcher in UI

### 2. Code Comments
- All comments must be in English

### 3. Subscription Feature
- Backend API to store user email + blockchain preference
- Daily email job to send JSON file for subscribed blockchain
- Simple registration form on website

### 4. Table Format Update
New columns based on provided spec:

| English | Chinese | JSON Field |
|---------|---------|------------|
| # | # | - |
| Host | 节点地址 | host |
| Port | 端口 | port |
| SSL | ssl | ssl |
| Height | 区块高度 | height |
| Version | 版本 | server_version |
| Protocol | 版本号 | protocol_version |
| Connection | 在线状态 | status |
| ConnectionTime | 连接时间 | last_seen |
| Response Time | 连接延时 | response_time_ms |
| Uptime Hour | 小时可用率 | per_hour |
| Uptime Day | 日可用率 | per_day |
| Uptime Month | 月可用率 | per_month |

---

## Implementation Steps

### Phase 1: Update Data Structure
- [ ] Update `convert_data.py` to match new JSON field names
- [ ] Update `update_data.py` to use new field names
- [ ] Update sample data files to reflect new structure

### Phase 2: Multi-language Support
- [ ] Create `js/i18n.js` - internationalization module
- [ ] Create `locales/en.json` - English translations
- [ ] Create `locales/zh.json` - Chinese translations
- [ ] Update `index.html` to add language switcher
- [ ] Update all JS files to use i18n for text content
- [ ] Update table headers to use i18n

### Phase 3: Table Format Update
- [ ] Update table headers in `index.html`
- [ ] Update `renderer.js` to render new columns
- [ ] Add SSL column (boolean icon)
- [ ] Add Connection/Status column
- [ ] Add ConnectionTime column
- [ ] Add Response Time column
- [ ] Update sort mappings in `app.js`

### Phase 4: Subscription Feature (Backend)
- [ ] Create `backend/app.py` - Simple Flask/FastAPI server
- [ ] Create subscription API endpoints:
  - `POST /api/subscribe` - Register email + blockchain
  - `GET /api/subscriptions` - List subscriptions (admin)
- [ ] Create SQLite database for subscriptions
- [ ] Create daily email sender script
- [ ] Set up cron job for daily emails

### Phase 5: Subscription Feature (Frontend)
- [ ] Add subscription modal/form to `index.html`
- [ ] Add subscription button in control bar
- [ ] Create `js/subscription.js` - handle subscription logic
- [ ] Add success/error messages (i18n supported)

### Phase 6: Code Cleanup
- [ ] Review all JS files, ensure comments are in English
- [ ] Review all Python files, ensure comments are in English
- [ ] Test all functionality
- [ ] Update README.md with new features

### Phase 7: Deploy to GitHub
- [ ] Commit all changes
- [ ] Push to GitHub using existing token

---

## Current Progress

**Status:** ✅ All phases completed! Ready to commit and push to GitHub

### Completed:
- ✅ Phase 1: Data structure updated (convert_data.py, update_data.py)
- ✅ Phase 2: Multi-language support implemented (i18n.js, en.json, zh.json)
- ✅ Phase 3: Table format updated (all new columns added)
- ✅ Phase 4: Backend API created (Flask app with subscription endpoints)
- ✅ Phase 5: Subscription frontend implemented (modal, form, JS)
- ✅ Phase 6: Code cleanup (all comments in English)
- ✅ Phase 7: Ready to deploy (git add, commit, push)

---

## Notes

- GitHub token is already configured in git remote URL
- Backend can be simple Flask app or serverless function
- Email sending can use SMTP or third-party service (SendGrid, etc.)
- For now, focus on frontend + data structure first, then backend
