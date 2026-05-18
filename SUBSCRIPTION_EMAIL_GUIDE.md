# Node Eye 订阅邮件系统使用指南

## 📋 系统概述

**新方案特点:**
- ✅ 订阅数据存储在加密的静态文件中 (`data/subscribers.enc`)
- ✅ 加密密码：20260518
- ✅ 每次更新数据时自动发送邮件给订阅者
- ✅ 无需 GitHub Actions 定时任务
- ✅ 简单、安全、易维护

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────┐
│              数据更新流程                                │
└─────────────────────────────────────────────────────────┘

1. 运行更新脚本
   ↓
2. 转换最新 Electrum 数据
   ↓
3. 更新 JSON 数据文件
   ↓
4. 提交并推送到 GitHub
   ↓
5. 读取加密的订阅文件
   ↓
6. 发送邮件给所有订阅者
   ↓
7. 完成！
```

---

## 📁 核心文件

| 文件 | 作用 | 说明 |
|------|------|------|
| `data/subscribers.enc` | 订阅数据 | 加密存储，密码 20260518 |
| `scripts/encrypt_subscribers.py` | 加密工具 | 加密/解密/管理订阅 |
| `scripts/send_subscription_emails.py` | 邮件发送 | 发送日报给订阅者 |
| `scripts/update_and_notify.py` | 主流程 | 更新数据 + 发送邮件 |
| `scripts/manage_subscribers.py` | 管理工具 | 交互式管理界面 |

---

## 🔧 配置步骤

### 步骤 1: 配置邮箱环境变量

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export NODEEYE_EMAIL_FROM="your-email@gmail.com"
export NODEEYE_EMAIL_PASSWORD="your-app-password"
export NODEEYE_SMTP_SERVER="smtp.gmail.com"
export NODEEYE_SMTP_PORT="587"

# 生效
source ~/.bashrc
```

### 步骤 2: 测试订阅功能

```bash
cd /home/admin/openclaw/workspace/node-eye

# 添加测试订阅
python scripts/encrypt_subscribers.py add test@example.com bitcoin

# 查看订阅列表
python scripts/encrypt_subscribers.py list
```

### 步骤 3: 测试邮件发送

```bash
# 发送测试邮件
python scripts/send_subscription_emails.py bitcoin
```

---

## 📧 使用方法

### 方法一：完整流程（推荐）

每次更新数据并通知订阅者：

```bash
cd /home/admin/openclaw/workspace/node-eye

# 自动检测最新数据文件
python scripts/update_and_notify.py

# 或指定数据文件
python scripts/update_and_notify.py /path/to/electrum_data.json
```

**执行流程:**
1. ✅ 转换数据
2. ✅ 更新 JSON
3. ✅ 提交到 GitHub
4. ✅ 发送邮件给订阅者

### 方法二：分步执行

```bash
# 1. 仅更新数据
python scripts/convert_data.py /path/to/electrum_data.json

# 2. 手动提交
git add -A
git commit -m "data: Update node data"
git push

# 3. 发送邮件
python scripts/send_subscription_emails.py
```

---

## 🔐 订阅管理

### 添加订阅

```bash
# 命令行方式
python scripts/encrypt_subscribers.py add user@example.com bitcoin

# 交互式方式
python scripts/manage_subscribers.py
# 选择 2. Add new subscriber
```

### 删除订阅

```bash
# 命令行方式
python scripts/encrypt_subscribers.py remove user@example.com

# 交互式方式
python scripts/manage_subscribers.py
# 选择 3. Remove subscriber
```

### 查看订阅列表

```bash
# 简单列表
python scripts/encrypt_subscribers.py list

# 详细信息
python scripts/manage_subscribers.py
# 选择 1. List all subscribers
```

### 备份订阅数据

```bash
# 导出到 JSON
python scripts/manage_subscribers.py
# 选择 4. Export to JSON

# 从 JSON 导入
python scripts/manage_subscribers.py
# 选择 5. Import from JSON
```

---

## 📊 订阅数据结构

### 加密前 (JSON)

```json
{
  "subscribers": [
    {
      "email": "user1@example.com",
      "chain_id": "bitcoin",
      "subscribed_at": "2026-05-18T10:00:00",
      "status": "active"
    },
    {
      "email": "user2@example.com",
      "chain_id": "ethereum",
      "subscribed_at": "2026-05-18T11:00:00",
      "status": "active"
    }
  ]
}
```

### 加密后 (subscribers.enc)

```
Base64 编码的 XOR 加密数据
密码：20260518
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

## 🔍 常见问题

### Q1: 如何查看加密文件内容？

```bash
python scripts/encrypt_subscribers.py decrypt data/subscribers.enc
```

### Q2: 如何修改加密密码？

编辑 `scripts/encrypt_subscribers.py`:
```python
PASSWORD = "20260518"  # 改为新密码
```

然后重新加密所有数据。

### Q3: 邮件发送失败？

检查：
1. 环境变量是否配置
2. 邮箱密码是否正确（使用应用专用密码）
3. 网络连接是否正常

```bash
# 测试配置
echo $NODEEYE_EMAIL_FROM
echo $NODEEYE_EMAIL_PASSWORD
```

### Q4: 如何批量导入订阅？

创建 JSON 文件：
```json
{
  "subscribers": [
    {"email": "user1@example.com", "chain_id": "bitcoin"},
    {"email": "user2@example.com", "chain_id": "bitcoin"}
  ]
}
```

然后导入：
```bash
python scripts/manage_subscribers.py
# 选择 5. Import from JSON
```

---

## 📈 使用统计

### 查看订阅统计

```bash
python scripts/manage_subscribers.py
# 选择 6. View statistics
```

输出示例：
```
============================================================
📊 Subscription Statistics
============================================================
Total Subscribers: 10

By Chain:
  bitcoin: 6
  ethereum: 3
  litecoin: 1

New this week: 2
```

---

## 🔒 安全说明

### 加密方式

- **算法:** XOR 加密
- **密码:** 20260518
- **编码:** Base64

### 安全建议

1. ✅ 不要在代码中硬编码邮箱密码
2. ✅ 使用环境变量存储敏感信息
3. ✅ 定期备份订阅数据
4. ✅ 限制订阅文件访问权限

```bash
# 设置文件权限
chmod 600 data/subscribers.enc
```

---

## 📝 日常维护

### 每日工作流程

```bash
# 1. 获取最新 Electrum 数据
# (系统自动下载或手动放置)

# 2. 运行更新和通知
cd /home/admin/openclaw/workspace/node-eye
python scripts/update_and_notify.py

# 3. 检查运行日志
# 确认数据更新和邮件发送成功
```

### 每周检查

- [ ] 检查订阅用户增长
- [ ] 查看邮件发送成功率
- [ ] 备份订阅数据
- [ ] 清理退订用户

### 每月维护

- [ ] 导出订阅数据备份
- [ ] 检查加密密码安全性
- [ ] 更新 SMTP 配置（如需要）
- [ ] 审查邮件发送日志

---

## 🎯 快速参考

### 添加订阅
```bash
python scripts/encrypt_subscribers.py add user@example.com bitcoin
```

### 删除订阅
```bash
python scripts/encrypt_subscribers.py remove user@example.com
```

### 查看列表
```bash
python scripts/encrypt_subscribers.py list
```

### 更新数据并发送邮件
```bash
python scripts/update_and_notify.py
```

### 仅发送邮件
```bash
python scripts/send_subscription_emails.py
```

### 交互式管理
```bash
python scripts/manage_subscribers.py
```

---

**最后更新:** 2026-05-18  
**版本:** v3.0.0  
**状态:** ✅ 生产就绪
