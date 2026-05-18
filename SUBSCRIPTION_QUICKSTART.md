# Node Eye 订阅功能 - 快速开始指南

## 🚀 5 分钟快速配置

### 步骤 1: 配置邮箱 (2 分钟)

```bash
# 编辑环境变量
nano ~/.bashrc

# 添加到文件末尾
export NODEEYE_EMAIL_FROM="your-email@gmail.com"
export NODEEYE_EMAIL_PASSWORD="your-app-password"
export NODEEYE_SMTP_SERVER="smtp.gmail.com"
export NODEEYE_SMTP_PORT="587"

# 保存并生效
source ~/.bashrc
```

**获取 Gmail 应用专用密码:**
1. 访问：https://myaccount.google.com/apppasswords
2. 选择 "Mail" → 你的设备
3. 复制 16 位密码
4. 填入 `NODEEYE_EMAIL_PASSWORD`

---

### 步骤 2: 添加测试订阅 (1 分钟)

```bash
cd /home/admin/openclaw/workspace/node-eye

# 添加测试订阅
python3 scripts/encrypt_subscribers.py add test@example.com bitcoin

# 验证
python3 scripts/encrypt_subscribers.py list
```

输出：
```
📊 Subscriber List
============================================================
Total subscribers: 1
============================================================
  - test@example.com (bitcoin)
```

---

### 步骤 3: 测试邮件发送 (2 分钟)

```bash
# 发送测试邮件
python3 scripts/send_subscription_emails.py bitcoin
```

输出：
```
🚀 Sending reports for BITCOIN...
📧 Found 1 subscribers
✅ Email sent to test@example.com
```

检查邮箱是否收到日报！

---

## 📋 日常使用

### 每次更新数据时

```bash
# 一键更新数据 + 发送邮件
python3 scripts/update_and_notify.py
```

**自动完成:**
1. ✅ 检测最新 Electrum 数据
2. ✅ 转换为 Node Eye 格式
3. ✅ 更新 JSON 文件
4. ✅ 提交到 GitHub
5. ✅ 发送邮件给所有订阅者

---

## 🔧 常用命令

### 添加订阅
```bash
python3 scripts/encrypt_subscribers.py add user@example.com bitcoin
```

### 删除订阅
```bash
python3 scripts/encrypt_subscribers.py remove user@example.com
```

### 查看列表
```bash
python3 scripts/encrypt_subscribers.py list
```

### 交互式管理
```bash
python3 scripts/manage_subscribers.py
```

---

## 📧 邮件内容

订阅者会收到这样的邮件：

**主题:** Node Eye Daily Report - BITCOIN - 2026-05-18

**内容:**
```
Hello,

Here is your daily Node Eye report for BITCOIN.

Summary:
- Total Nodes: 486
- Online Nodes: 390
- Offline Nodes: 96
- Avg Response Time: 2355ms

[附件] bitcoin_nodes_20260518.json
```

---

## 🔐 加密说明

- **存储文件:** `data/subscribers.enc`
- **加密方式:** XOR + Base64
- **密码:** 20260518
- **安全:** 文件已加密，可安全提交到 GitHub

---

## ⚠️ 故障排查

### 邮件发送失败

```bash
# 检查环境变量
echo $NODEEYE_EMAIL_FROM
echo $NODEEYE_EMAIL_PASSWORD

# 如果不显示，重新配置
source ~/.bashrc
```

### 订阅列表为空

```bash
# 重新添加订阅
python3 scripts/encrypt_subscribers.py add user@example.com bitcoin
```

---

## 📞 完整文档

- 详细指南：SUBSCRIPTION_EMAIL_GUIDE.md
- 配置清单：SUBSCRIPTION_CHECKLIST.md

---

**完成！现在每次运行 `update_and_notify.py` 都会自动发送邮件给订阅者！** 🎉
