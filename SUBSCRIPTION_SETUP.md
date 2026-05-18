# Node Eye 订阅功能完整配置指南

## ✅ 已实现功能清单

| 功能 | 状态 | 说明 |
|------|------|------|
| ✅ 邮箱订阅 | 完成 | 用户可订阅每日报告 |
| ✅ 邮箱验证 | 完成 | 6 位验证码，24 小时有效期 |
| ✅ 取消订阅 | 完成 | 支持邮件回复退订 |
| ✅ 每日定时发送 | 完成 | UTC 9:00 AM 自动发送 |
| ✅ JSON 附件 | 完成 | 包含完整节点数据 |
| ✅ 重试机制 | 完成 | 验证码 3 次尝试限制 |
| ✅ 退订黑名单 | 完成 | 防止重复订阅 |

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│              GitHub Actions 订阅系统                      │
└─────────────────────────────────────────────────────────┘

用户操作              GitHub 处理              邮件发送
   │                      │                      │
   │  1. 网站订阅表单     │                      │
   ├─────────────────────►│                      │
   │                      │  2. 创建 Issue       │
   │                      │  Label: pending      │
   │                      ├─────────────────────►│
   │                      │                      │ 3. 验证邮件
   │                      │                      │ (含 6 位码)
   │                      │                      │
   │  4. 回复验证码       │                      │
   ├─────────────────────►│                      │
   │                      │  5. Issue Comment    │
   │                      │  Label: verified     │
   │                      │                      │
   │                      │  6. 每日 9AM 定时      │
   │                      │  (cron: 0 9 * * *)   │
   │                      ├─────────────────────►│
   │                      │                      │ 7. 日报
   │                      │                      │ (JSON 附件)
   ◄──────────────────────────────────────────────┘
```

---

## 📁 核心文件

### 1. GitHub Actions 工作流

**文件:** `.github/workflows/daily-email.yml`

**触发条件:**
- ⏰ 每天 UTC 9:00 (北京时间 17:00)
- 📝 用户创建 Issue (订阅/退订)
- 💬 用户评论 Issue (验证码)
- 🔧 手动触发 (workflow_dispatch)

### 2. Python 处理脚本

**文件:** `.github/workflows/scripts/subscription_handler.py`

**支持的操作:**
- `send` - 发送每日邮件
- `add` - 添加新订阅
- `verify` - 验证邮箱
- `remove` - 取消订阅
- `list` - 列出所有订阅

### 3. 订阅数据存储

**位置:** GitHub Actions Artifact (`/tmp/subscriptions.json`)

**数据结构:**
```json
{
  "verified": [
    {
      "email": "user@example.com",
      "chain_id": "bitcoin",
      "created_at": "2026-05-18T10:00:00",
      "verified_at": "2026-05-18T10:05:00"
    }
  ],
  "pending": [
    {
      "email": "new@example.com",
      "chain_id": "ethereum",
      "verification_code": "123456",
      "created_at": "2026-05-18T11:00:00",
      "attempts": 0
    }
  ],
  "unsubscribed": [
    {
      "email": "gone@example.com",
      "unsubscribed_at": "2026-05-18T12:00:00",
      "reason": "user_request"
    }
  ]
}
```

---

## 🔧 配置步骤

### 步骤 1: 配置 GitHub Secrets

1. 进入 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下 Secrets:

```bash
# 发件人邮箱
NODEEYE_EMAIL_FROM=your-email@gmail.com

# 邮箱密码 (应用专用密码，不是登录密码!)
NODEEYE_EMAIL_PASSWORD=xxxx xxxx xxxx xxxx

# SMTP 服务器
NODEEYE_SMTP_SERVER=smtp.gmail.com

# SMTP 端口
NODEEYE_SMTP_PORT=587
```

### 步骤 2: Gmail 配置 (如使用 Gmail)

1. **启用两步验证**
   - 访问：https://myaccount.google.com/security
   - 启用 "2-Step Verification"

2. **生成应用专用密码**
   - 访问：https://myaccount.google.com/apppasswords
   - 选择 "Mail" 和你的设备
   - 复制生成的 16 位密码
   - 填入 `NODEEYE_EMAIL_PASSWORD`

3. **允许不太安全的应用** (可选)
   - 如果使用普通密码，需要启用
   - 但推荐使用应用专用密码

### 步骤 3: 启用 GitHub Actions

1. 进入仓库 **Actions** 标签
2. 找到 "Daily Email Reports" 工作流
3. 确认状态为启用
4. 点击工作流 → **Run workflow** 测试一次

### 步骤 4: 测试完整流程

#### 测试订阅
1. 点击网站 "📧 Subscribe" 按钮
2. 填写邮箱和区块链
3. 提交后应创建 GitHub Issue

#### 测试验证
1. 查看 GitHub Issue
2. 评论验证码 (如：123456)
3. Issue 应标记为 verified

#### 测试邮件发送
1. 进入 Actions → Daily Email Reports
2. 点击 **Run workflow**
3. 选择 action: `send`
4. 点击运行
5. 检查邮箱是否收到日报

---

## 📧 用户使用流程

### 方式一：网站订阅 (推荐)

1. **点击订阅按钮**
   - 网站右上角 "📧 Subscribe"

2. **填写信息**
   - Email: your@email.com
   - Blockchain: Bitcoin/Ethereum/etc.

3. **创建 GitHub Issue**
   - 自动跳转或手动创建
   - 标题：`[Subscribe] your@email.com`
   - 内容包含邮箱和区块链

4. **接收验证邮件**
   - 系统自动发送 6 位验证码
   - 24 小时内有效

5. **验证邮箱**
   - 在 Issue 中评论验证码
   - 或回复验证邮件

6. **开始接收日报**
   - 每天 UTC 9:00 (北京 17:00)
   - 带 JSON 附件

### 方式二：直接创建 Issue

1. 访问：https://github.com/KevinGong/node-eye/issues/new
2. 标题：`[Subscribe] your@email.com`
3. 内容：
   ```
   Email: your@email.com
   Chain: bitcoin
   ```
4. 提交后等待验证邮件

### 方式三：邮件退订

收到日报时：
1. 回复邮件
2. 主题包含 "UNSUBSCRIBE"
3. 系统自动处理退订

---

## 🔍 管理订阅

### 查看所有订阅

1. 进入 Actions → Daily Email Reports
2. 点击 **Run workflow**
3. 选择 action: `list`
4. 查看运行日志

### 手动添加订阅

```bash
# GitHub Actions 手动触发
action: add
email: user@example.com
chain_id: bitcoin
```

### 手动验证邮箱

```bash
# GitHub Actions 手动触发
action: verify
email: user@example.com
verification_code: 123456
```

### 手动退订

```bash
# GitHub Actions 手动触发
action: remove
email: user@example.com
reason: spam_complaint
```

---

## 📊 监控和维护

### 查看运行日志

1. 进入 **Actions** 标签
2. 选择 "Daily Email Reports"
3. 点击具体运行记录
4. 查看详细日志

### 订阅数据统计

每次运行会输出：
```
📊 Subscription Statistics
============================================================
Verified:   10
Pending:    2
Unsubscribed: 1

✅ Verified Subscribers:
  - user1@example.com (bitcoin)
  - user2@example.com (ethereum)

⏳ Pending Verification:
  - user3@example.com (litecoin) - Code: 123456
```

### 邮件发送统计

```
🚀 Starting daily email send...
   Time: 2026-05-18T09:00:00
📧 Found 10 verified subscribers
✅ Email sent to user1@example.com for bitcoin
✅ Email sent to user2@example.com for ethereum
...
✅ Daily email complete: 10 sent, 0 failed
```

---

## ⚠️ 常见问题

### Q1: 邮件发送失败

**原因:**
- SMTP 配置错误
- 邮箱密码错误
- Gmail 安全限制

**解决:**
1. 检查 Secrets 配置
2. 使用应用专用密码
3. 查看 Actions 日志详情

### Q2: 验证码收不到

**原因:**
- 邮箱地址错误
- 邮件进入垃圾箱
- SMTP 未配置

**解决:**
1. 检查邮箱拼写
2. 查看垃圾邮件文件夹
3. 手动在 Actions 中触发验证

### Q3: 订阅数据丢失

**原因:**
- GitHub Artifact 过期 (30 天)
- 工作流被删除

**解决:**
1. 定期导出订阅数据
2. 使用外部数据库备份

### Q4: GitHub Actions 限制

**免费套餐:**
- 2000 分钟/月
- 20 个并发任务

**估算用量:**
- 每日邮件：~5 分钟/天 = 150 分钟/月
- 订阅处理：~1 分钟/次
- **完全在免费额度内**

---

## 🔒 安全最佳实践

### 1. 保护 GitHub Secrets

- ✅ 不要在前端代码中暴露
- ✅ 定期轮换密码
- ✅ 使用应用专用密码

### 2. 邮箱验证

- ✅ 必须验证邮箱所有权
- ✅ 验证码 24 小时过期
- ✅ 3 次尝试限制

### 3. 退订便利

- ✅ 每封邮件包含退订说明
- ✅ 支持回复退订
- ✅ 立即处理退订请求

### 4. 数据保护

- ✅ 不存储敏感信息
- ✅ 仅存储邮箱和区块链偏好
- ✅ 退订后加入黑名单

---

## 📈 性能优化

### 减少 Actions 运行时间

1. **批量处理**
   - 每日邮件一次发送所有订阅者
   - 避免逐个触发

2. **缓存数据**
   - 订阅数据缓存在 Artifact
   - 节点数据缓存在 /tmp/data

3. **优化脚本**
   - 减少不必要的依赖
   - 使用 Python 标准库

### 监控 GitHub 用量

```bash
# 查看每月用量
Settings → Billing → Actions

# 设置用量提醒
Settings → Actions → General → Workflow permissions
```

---

## 🎯 下一步增强

### 短期 (可选)

- [ ] 订阅确认邮件模板优化
- [ ] 日报邮件模板美化
- [ ] 退订原因统计
- [ ] 订阅来源追踪

### 长期 (可选)

- [ ] 用户偏好设置 (发送时间、频率)
- [ ] 多区块链订阅
- [ ] 邮件打开率统计
- [ ] A/B 测试邮件模板

---

## 📞 技术支持

### GitHub Issues
- 订阅问题：https://github.com/KevinGong/node-eye/issues
- 功能建议：新建 Issue

### 文档
- 完整指南：SUBSCRIPTION_SETUP.md
- GitHub 配置：GITHUB_SUBSCRIPTION_GUIDE.md

---

**最后更新:** 2026-05-18  
**版本:** v2.1.0  
**状态:** ✅ 生产就绪
