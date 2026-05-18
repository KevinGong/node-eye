# ⚙️ 订阅功能配置检查清单

## 📋 配置步骤 (按顺序完成)

### 1️⃣ 配置 Gmail (如使用 Gmail)

- [ ] 启用 Google 两步验证
  - 访问：https://myaccount.google.com/security
  - 启用 "2-Step Verification"

- [ ] 生成应用专用密码
  - 访问：https://myaccount.google.com/apppasswords
  - 选择 "Mail" → 选择设备
  - **复制 16 位密码** (只显示一次!)

---

### 2️⃣ 配置 GitHub Secrets

- [ ] 进入仓库 Settings → Secrets and variables → Actions

- [ ] 添加 `NODEEYE_EMAIL_FROM`
  ```
  Value: your-email@gmail.com
  ```

- [ ] 添加 `NODEEYE_EMAIL_PASSWORD`
  ```
  Value: xxxx xxxx xxxx xxxx (应用专用密码)
  ```

- [ ] 添加 `NODEEYE_SMTP_SERVER`
  ```
  Value: smtp.gmail.com
  ```

- [ ] 添加 `NODEEYE_SMTP_PORT`
  ```
  Value: 587
  ```

---

### 3️⃣ 启用 GitHub Actions

- [ ] 进入仓库 **Actions** 标签

- [ ] 确认看到 "Daily Email Reports" 工作流

- [ ] 点击工作流 → **Run workflow**

- [ ] 选择 action: `list`

- [ ] 点击绿色按钮运行

- [ ] 检查运行结果应为:
  ```
  📊 Subscription Statistics
  ====================
  Verified:   0
  Pending:    0
  Unsubscribed: 0
  ```

---

### 4️⃣ 测试订阅流程

#### 测试 1: 创建订阅

- [ ] 点击网站 "📧 Subscribe" 按钮

- [ ] 填写测试邮箱

- [ ] 选择区块链 (bitcoin)

- [ ] 点击 "Subscribe"

- [ ] 确认创建了 GitHub Issue
  - 标题：`[Subscribe] your@email.com`
  - Labels: subscription, pending, bitcoin

#### 测试 2: 验证邮箱

- [ ] 检查测试邮箱是否收到验证邮件

- [ ] 邮件应包含 6 位验证码

- [ ] 在 GitHub Issue 中评论验证码

- [ ] 确认 Issue Labels 变为: verified, bitcoin

#### 测试 3: 发送日报

- [ ] 进入 Actions → Daily Email Reports

- [ ] 点击 **Run workflow**

- [ ] 选择 action: `send`

- [ ] 点击运行

- [ ] 检查测试邮箱是否收到日报

- [ ] 确认邮件包含:
  - ✅ 主题：Node Eye Daily Report - BITCOIN - YYYY-MM-DD
  - ✅ 摘要统计 (Total, Online, Offline)
  - ✅ JSON 附件

---

### 5️⃣ 测试退订流程

- [ ] 回复日报邮件

- [ ] 主题包含：UNSUBSCRIBE

- [ ] 等待 GitHub Actions 运行

- [ ] 确认订阅被移除

- [ ] 再次运行 `send` action

- [ ] 确认退订邮箱不再收到邮件

---

### 6️⃣ 配置定时任务

- [ ] 确认工作流包含 schedule 触发器
  ```yaml
  schedule:
    - cron: '0 9 * * *'
  ```

- [ ] 时间换算:
  - UTC 9:00 = 北京时间 17:00
  - UTC 9:00 = 美东时间 5:00 AM

- [ ] 如需调整时间，编辑 `.github/workflows/daily-email.yml`

---

## 🔍 验证清单

### GitHub Actions 状态

- [ ] 工作流已启用
- [ ] 最近运行成功
- [ ] 无错误日志
- [ ] Artifact 正常上传

### 邮件功能

- [ ] 验证邮件能发送
- [ ] 日报邮件能发送
- [ ] 附件包含 JSON
- [ ] 退订能处理

### 数据安全

- [ ] Secrets 未泄露
- [ ] 前端无敏感信息
- [ ] 订阅数据正常存储
- [ ] Artifact  retention 30 天

---

## 📊 监控指标

### 每周检查

- [ ] Actions 运行时长 (< 10 分钟)
- [ ] 邮件发送成功率 (> 95%)
- [ ] GitHub 用量 (< 2000 分钟/月)

### 每月检查

- [ ] 订阅用户增长
- [ ] 退订率 (< 5%)
- [ ] 邮件打开率
- [ ] 用户反馈

---

## 🐛 故障排查

### 问题：邮件发送失败

**检查:**
1. Secrets 配置是否正确
2. 邮箱密码是否过期
3. Gmail 是否阻止登录

**解决:**
```bash
# 查看 Actions 日志
Actions → Daily Email Reports → Latest Run → View logs

# 查找错误信息
❌ Failed to send email: ...
```

### 问题：验证邮件收不到

**检查:**
1. 邮箱地址是否正确
2. 垃圾邮件文件夹
3. SMTP 配置

**解决:**
1. 重新订阅
2. 检查 Actions 日志
3. 手动触发验证

### 问题：定时任务未执行

**检查:**
1. 工作流是否启用
2. cron 表达式是否正确
3. GitHub 服务状态

**解决:**
1. 手动触发一次
2. 检查仓库设置
3. 查看 GitHub Status

---

## 📞 获取帮助

### 文档

- 完整指南：SUBSCRIPTION_SETUP.md
- 架构说明：GITHUB_SUBSCRIPTION_GUIDE.md
- README.md

### GitHub

- Issues: https://github.com/KevinGong/node-eye/issues
- Actions: https://github.com/KevinGong/node-eye/actions

### 检查清单完成时间

- [ ] 步骤 1: Gmail 配置 (5 分钟)
- [ ] 步骤 2: GitHub Secrets (5 分钟)
- [ ] 步骤 3: 启用 Actions (5 分钟)
- [ ] 步骤 4: 测试流程 (15 分钟)
- [ ] 步骤 5: 测试退订 (5 分钟)
- [ ] 步骤 6: 定时配置 (5 分钟)

**预计总时间:** 40 分钟

---

## ✅ 完成标志

全部完成后，你应该能够:

1. ✅ 用户通过网站订阅
2. ✅ 自动发送验证邮件
3. ✅ 用户验证后激活订阅
4. ✅ 每天自动发送日报
5. ✅ 用户可随时退订
6. ✅ 所有数据存储在 GitHub

**恭喜！订阅系统配置完成！🎉**

---

**最后更新:** 2026-05-18  
**版本:** v2.1.0
