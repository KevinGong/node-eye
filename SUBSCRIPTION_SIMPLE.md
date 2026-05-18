# Node Eye 简易订阅系统

## 📋 系统特点

**简化后的订阅流程:**
- ✅ 无需邮箱验证
- ✅ 无需退订功能
- ✅ 点击订阅 → 输入邮箱 → 直接保存
- ✅ 每次数据更新自动发送邮件

---

## 🏗️ 订阅流程

```
用户操作:
1. 点击 "📧 Subscribe" 按钮
   ↓
2. 输入邮箱 + 选择区块链
   ↓
3. 点击 "Subscribe"
   ↓
4. 创建 GitHub Issue (自动保存)
   ↓
5. 订阅完成！

系统操作:
1. 管理员运行 update_and_notify.py
   ↓
2. 读取订阅列表
   ↓
3. 发送邮件给所有订阅者
   ↓
4. 完成！
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

### 添加订阅（管理员）

```bash
cd /home/admin/openclaw/workspace/node-eye

# 添加订阅
python3 scripts/encrypt_subscribers.py add user@example.com bitcoin

# 查看列表
python3 scripts/encrypt_subscribers.py list
```

### 更新数据并发送邮件

```bash
# 一键完成
python3 scripts/update_and_notify.py
```

**自动完成:**
1. ✅ 转换最新数据
2. ✅ 更新 JSON 文件
3. ✅ 提交到 GitHub
4. ✅ 发送邮件给所有订阅者

---

## 📊 订阅数据结构

**文件:** `data/subscribers.enc` (加密存储)

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

**加密:**
- 密码：20260518
- 方式：XOR + Base64

---

## 🎯 用户订阅流程

### 方式一：网站订阅

1. 点击网站 "📧 Subscribe" 按钮
2. 填写邮箱和区块链
3. 点击 "Subscribe"
4. 自动打开 GitHub Issue 页面
5. 提交 Issue 完成订阅

### 方式二：管理员直接添加

```bash
python3 scripts/encrypt_subscribers.py add user@example.com bitcoin
```

---

## 📧 邮件内容示例

**主题:** Node Eye Daily Report - BITCOIN - 2026-05-18

**正文:**
```
Hello,

Here is your daily Node Eye report for BITCOIN.

┌─────────────────────────────────────────┐
│              Summary                    │
├─────────────────────────────────────────┤
│ Total Nodes:        486
│ Online Nodes:       390
│ Offline Nodes:      96
│ Avg Response Time:  2355ms
└─────────────────────────────────────────┘

Last Update: 2026-05-18T12:22:15

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

1. **无退订功能**
   - 如需退订，联系管理员手动删除
   - 或忽略邮件

2. **无邮箱验证**
   - 订阅直接生效
   - 立即可以收到邮件

3. **加密存储**
   - 订阅数据加密保存
   - 密码：20260518
   - 可安全提交到 GitHub

---

## 📞 故障排查

### 邮件发送失败

```bash
# 检查环境变量
echo $NODEEYE_EMAIL_FROM
echo $NODEEYE_EMAIL_PASSWORD
```

### 订阅列表为空

```bash
# 添加订阅
python3 scripts/encrypt_subscribers.py add user@example.com bitcoin
```

---

**最后更新:** 2026-05-18  
**版本:** v3.1.0 (简化版)  
**状态:** ✅ 生产就绪
