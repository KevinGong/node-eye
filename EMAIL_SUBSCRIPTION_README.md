# Node Eye 邮件订阅系统

## 📋 系统说明

**订阅流程:**
1. 用户点击网站 "📧 Subscribe" 按钮
2. 输入邮箱 + 选择区块链
3. 提交后保存到订阅文件
4. 每次数据更新自动发送邮件

**数据流程:**
```
用户订阅 → 保存到 data/subscribers.enc (加密)
   ↓
你更新数据 → 运行 update_and_notify.py
   ↓
自动读取订阅文件 → 发送邮件给所有订阅者
   ↓
完成！
```

---

## 🔧 配置步骤

### 步骤 1: 配置邮箱环境变量

```bash
# 添加到 ~/.bashrc
export NODEEYE_EMAIL_FROM="your-email@gmail.com"
export NODEEYE_EMAIL_PASSWORD="your-app-password"
export NODEEYE_SMTP_SERVER="smtp.gmail.com"
export NODEEYE_SMTP_PORT="587"

# 生效
source ~/.bashrc
```

### 步骤 2: 获取 Gmail 应用专用密码

1. 访问：https://myaccount.google.com/apppasswords
2. 选择 "Mail" → 你的设备
3. 复制 16 位密码
4. 填入 `NODEEYE_EMAIL_PASSWORD`

---

## 📧 使用方法

### 添加订阅者

**方式一：命令行添加**
```bash
cd /home/admin/openclaw/workspace/node-eye
python3 scripts/encrypt_subscribers.py add user@example.com bitcoin
```

**方式二：网站订阅**
1. 用户点击 "📧 Subscribe"
2. 填写邮箱和区块链
3. 提交后自动保存

### 查看订阅列表

```bash
python3 scripts/encrypt_subscribers.py list
```

### 更新数据并发送邮件

```bash
# 一键完成：更新数据 + 提交 GitHub + 发送邮件
python3 scripts/update_and_notify.py
```

**自动完成:**
1. ✅ 检测最新 Electrum 数据
2. ✅ 转换为 Node Eye 格式
3. ✅ 更新 JSON 文件
4. ✅ 提交到 GitHub
5. ✅ 读取订阅文件
6. ✅ 发送邮件给所有订阅者

---

## 📊 订阅数据存储

**文件:** `data/subscribers.enc`

**加密:**
- 密码：20260518
- 方式：XOR + Base64

**结构:**
```json
{
  "subscribers": [
    {
      "email": "user@example.com",
      "chain_id": "bitcoin",
      "subscribed_at": "2026-05-18T16:00:00",
      "status": "active"
    }
  ]
}
```

---

## 📧 邮件内容

**主题:** Node Eye Daily Report - BITCOIN - 2026-05-18

**正文:**
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

## 🔍 常用命令

### 添加订阅
```bash
python3 scripts/encrypt_subscribers.py add user@example.com bitcoin
```

### 查看列表
```bash
python3 scripts/encrypt_subscribers.py list
```

### 更新数据并发送邮件
```bash
python3 scripts/update_and_notify.py
```

### 仅发送邮件
```bash
python3 scripts/send_subscription_emails.py
```

---

## ⚠️ 注意事项

1. **每次更新数据时必须运行** `update_and_notify.py`
   - 会自动发送邮件给所有订阅者
   - 无需额外操作

2. **邮箱配置必须正确**
   - 使用 Gmail 应用专用密码
   - 不要使用登录密码

3. **订阅文件加密存储**
   - 密码：20260518
   - 可安全提交到 GitHub

---

## 📞 故障排查

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
# 添加测试订阅
python3 scripts/encrypt_subscribers.py add test@example.com bitcoin

# 验证
python3 scripts/encrypt_subscribers.py list
```

---

**最后更新:** 2026-05-19  
**版本:** v3.2.0  
**状态:** ✅ 生产就绪
