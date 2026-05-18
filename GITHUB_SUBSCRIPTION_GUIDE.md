# Node Eye - GitHub 静态页面订阅功能实现指南

## ⚠️ GitHub Pages 限制说明

GitHub Pages 是**纯静态托管服务**，无法运行：
- ❌ Python/Node.js 后端代码
- ❌ 数据库 (SQLite/MySQL)
- ❌ 定时任务 (Cron)
- ❌ SMTP 邮件发送

**因此，原生的 Flask 后端方案在 GitHub Pages 上无法工作！**

---

## ✅ 解决方案：GitHub Actions + Issues

我们使用 GitHub 原生功能实现完整订阅系统：

| 功能 | 传统方案 | GitHub 方案 |
|------|---------|------------|
| 数据库 | SQLite | GitHub Issues + Labels |
| 后端 API | Flask | GitHub Actions |
| 定时任务 | Cron | GitHub Actions Schedule |
| 邮件发送 | SMTP | GitHub Actions + SMTP |
| 用户验证 | 数据库字段 | Issue Labels |

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────┐
│              GitHub 生态订阅系统                          │
└─────────────────────────────────────────────────────────┘

用户操作                GitHub 处理                 邮件发送
   │                      │                          │
   │  1. 填写订阅表单      │                          │
   ├─────────────────────►│                          │
   │                      │  2. 创建 Issue           │
   │                      │  [订阅] user@email.com   │
   │                      │  Label: bitcoin, pending │
   │                      ├─────────────────────────►│
   │                      │                          │ 3. 发送验证邮件
   │                      │                          │ 含验证码
   │  4. 回复验证码       │                          │
   ├─────────────────────►│                          │
   │                      │  5. 更新 Issue Label     │
   │                      │  pending → verified      │
   │                      │                          │
   │                      │  6. 每天 9AM 定时触发     │
   │                      │  (cron: 0 9 * * *)       │
   │                      ├─────────────────────────►│
   │                      │                          │ 7. 发送日报
   │                      │                          │ 带 JSON 附件
   ◄──────────────────────────────────────────────────┘
   收到邮件
```

---

## 📁 核心文件

### 1. GitHub Actions 工作流

**文件:** `.github/workflows/daily-email.yml`

```yaml
name: Daily Email Reports

on:
  # 每天 9:00 AM UTC 运行
  schedule:
    - cron: '0 9 * * *'
  
  # 手动触发
  workflow_dispatch:
    inputs:
      action:
        description: 'Action type'
        type: choice
        options: [send, add, verify, remove]
  
  # Issue 事件（订阅请求）
  issues:
    types: [opened, labeled, closed]
```

### 2. Python 处理脚本

**文件:** `.github/workflows/scripts/subscription_handler.py`

功能：
- ✅ 添加订阅（待验证）
- ✅ 验证邮箱（验证码）
- ✅ 删除订阅（退订）
- ✅ 发送每日邮件
- ✅ 发送验证邮件

### 3. 订阅数据存储

**方式:** GitHub Issues + Labels

```
Issue Title: [订阅] user@example.com
Issue Body:
  Email: user@example.com
  Chain: bitcoin
  Created: 2026-05-18
  Status: pending

Labels:
  - subscription
  - pending
  - bitcoin
```

验证后：
```
Labels:
  - subscription
  - verified  ← 改为 verified
  - bitcoin
```

---

## 🔧 配置步骤

### 1. 设置 GitHub Secrets

在 GitHub 仓库 Settings → Secrets and variables → Actions 中添加：

```bash
NODEEYE_EMAIL_FROM=your-email@gmail.com
NODEEYE_EMAIL_PASSWORD=your-app-password
NODEEYE_SMTP_SERVER=smtp.gmail.com
NODEEYE_SMTP_PORT=587
```

### 2. Gmail 配置（如使用 Gmail）

1. 启用两步验证
2. 生成应用专用密码：https://myaccount.google.com/apppasswords
3. 将 16 位密码填入 `NODEEYE_EMAIL_PASSWORD`

### 3. 启用 GitHub Actions

1. 进入仓库 Actions 标签
2. 确认工作流已启用
3. 手动触发一次测试

---

## 📧 用户使用流程

### 方式一：网站表单订阅（推荐）

1. 点击网站 "📧 订阅" 按钮
2. 填写邮箱和选择区块链
3. 提交后自动创建 GitHub Issue
4. 收到验证邮件
5. 回复验证码
6. 订阅生效，开始接收日报

### 方式二：直接创建 Issue

1. 访问 GitHub 仓库 Issues
2. 点击 "New Issue"
3. 标题：`[订阅] your@email.com`
4. 内容：
   ```
   Email: your@email.com
   Chain: bitcoin
   ```
5. 提交后等待验证邮件

### 方式三：邮件退订

收到日报时，回复邮件：
```
Subject: UNSUBSCRIBE
```

系统会自动删除订阅。

---

## 🎯 前端集成

### 更新 subscription.js

由于是静态页面，订阅数据直接提交到 GitHub：

```javascript
async handleSubmit(e) {
    e.preventDefault();
    
    const email = document.getElementById('subscribeEmail').value;
    const chainId = document.getElementById('subscribeChain').value;
    
    // 方案 1: 使用 GitHub API 创建 Issue
    await this.createGitHubIssue(email, chainId);
    
    // 方案 2: 使用 Formspree 等表单服务
    // await this.submitToFormspree(email, chainId);
    
    // 方案 3: 使用 EmailJS 直接发送邮件
    // await this.sendViaEmailJS(email, chainId);
}

async createGitHubIssue(email, chainId) {
    // 注意：这需要用户有 GitHub 账号
    // 对于公开订阅，建议使用方式 2 或 3
    const response = await fetch('https://api.github.com/repos/KevinGong/node-eye/issues', {
        method: 'POST',
        headers: {
            'Authorization': `token ${GITHUB_TOKEN}`,
            'Accept': 'application/vnd.github.v3+json'
        },
        body: JSON.stringify({
            title: `[订阅] ${email}`,
            body: `Email: ${email}\nChain: ${chainId}\nCreated: ${new Date().toISOString()}`,
            labels: ['subscription', 'pending', chainId]
        })
    });
    
    return await response.json();
}
```

---

## 🚀 推荐方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **GitHub Issues** | 完全免费，无需外部服务 | 需要 GitHub API 集成 | 技术用户 |
| **Formspree** | 简单，无需代码 | 免费版有限制 | 小型项目 |
| **EmailJS** | 前端直接发邮件 | 需要配置模板 | 快速原型 |
| **Vercel Functions** | 完整后端能力 | 需要迁移部署 | 生产环境 |

### 最佳实践：混合方案

```
1. 网站表单 → Formspree/EmailJS → 发送订阅请求
2. Formspree Webhook → GitHub Actions → 处理订阅
3. GitHub Actions → 发送验证邮件
4. 用户回复 → GitHub Actions → 验证并激活
5. 每日定时 → GitHub Actions → 发送日报
```

---

## 📝 完整实现清单

- [x] GitHub Actions 工作流配置
- [x] Python 订阅处理脚本
- [x] 邮箱验证功能
- [x] 退订功能
- [x] 每日定时邮件
- [x] JSON 附件发送
- [ ] 前端表单集成（需选择方案）
- [ ] GitHub Secrets 配置
- [ ] 测试验证流程

---

## 🔒 安全注意事项

1. **GitHub Token 保护**
   - 不要在前端代码中硬编码 Token
   - 使用 GitHub Actions 的 secrets 机制

2. **邮箱验证**
   - 必须验证邮箱所有权
   - 防止恶意订阅

3. **退订便利**
   - 每封邮件包含退订说明
   - 支持回复退订

4. **速率限制**
   - GitHub Actions 有使用限制
   - 免费版：2000 分钟/月

---

## 📊 GitHub Actions 限制

| 套餐 | 并发任务 | 每月分钟数 | 存储 |
|------|---------|-----------|------|
| Free | 20 | 2,000 | 500 MB |
| Pro | 30 | 3,000 | 10 GB |
| Team | 40 | 4,000 | 20 GB |

**估算：**
- 每日邮件发送：~5 分钟/天 = 150 分钟/月
- 订阅处理：~1 分钟/订阅
- **完全在免费额度内！**

---

## 🎯 下一步

1. **选择订阅提交方式**
   - GitHub API（需要 Token）
   - Formspree（推荐，简单）
   - EmailJS（前端直发）

2. **配置 GitHub Secrets**

3. **测试完整流程**
   - 订阅 → 验证 → 接收日报 → 退订

4. **监控和优化**
   - 查看 Actions 日志
   - 优化邮件模板

---

**总结：** 使用 GitHub Actions 可以在纯静态页面上实现完整的订阅功能，无需后端服务器！
