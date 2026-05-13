# Node Eye - 多链区块链志愿者节点监控平台

<div align="center">

👁️ **实时监控 · 多链支持 · 纯静态架构**

一个现代、美观、科技感十足的区块链节点监控平台

[在线演示](#) · [功能特性](#功能特性) · [部署指南](#部署指南) · [数据格式](#数据格式)

</div>

---

## 📖 项目简介

Node Eye 是一个纯静态的区块链志愿者节点监控平台，参考 [Bitcoin Eye](https://1209k.com/bitcoin-eye/ele.php) 的设计风格，采用更现代的深色科技风 UI，类似 Grafana/Prometheus 监控大屏的视觉效果。

项目采用 **纯静态架构**（HTML + CSS + JavaScript），可直接部署到 GitHub Pages，无需后端服务。数据来源于 GitHub 仓库中的 JSON 文件，支持多链切换和实时刷新。

## ✨ 功能特性

### 核心功能
- 🔗 **多链支持** - Bitcoin、Litecoin、Dogecoin、Ethereum，后续可扩展更多链
- 📊 **统计面板** - 节点总数、正常/异常节点数、平均可用率
- 🔍 **搜索筛选** - 按 Host 搜索、按状态筛选（全部/正常/异常）
- 📈 **排序功能** - 支持按 Height、Uptime、Day、Month 升序/降序排序
- 📱 **响应式设计** - 支持桌面端和移动端，表格支持横向滚动

### 监控字段
| 字段 | 说明 |
|------|------|
| Host | 节点地址 |
| Port | 端口号 |
| Proto | 协议类型 |
| UTXO Root | UTXO 根哈希（截断显示） |
| Height | 区块高度 |
| Blocktime | 区块时间 |
| Version | 节点版本 |
| Protocol | 协议版本 |
| Connection | 连接数 |
| ConnectionTime | 连接时长 |
| Status | 状态（正常/异常） |
| Uptime | 总可用率 |
| Hour | 小时可用率（带进度条） |
| Day | 日可用率（带进度条） |
| Month | 月可用率（带进度条） |

### 视觉效果
- 🎨 深色科技风主题（#0a0e1a 背景）
- 💙 科技蓝/紫色渐变点缀
- ✅ 状态颜色：正常绿色、异常红色
- 🌊 动态脉冲动画（在线状态）
- 📊 可用率进度条（高/中/低分级着色）

## 🚀 快速开始

### 本地开发
```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/node-eye.git
cd node-eye

# 使用任意静态服务器启动
# 方式 1: Python
python -m http.server 8080

# 方式 2: Node.js (需要安装 http-server)
npx http-server -p 8080

# 方式 3: VS Code Live Server 插件
# 直接右键 index.html → "Open with Live Server"
```

然后访问 `http://localhost:8080`

### 部署到 GitHub Pages

1. **创建仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Node Eye"
   git remote add origin https://github.com/YOUR_USERNAME/node-eye.git
   git push -u origin main
   ```

2. **启用 GitHub Pages**
   - 进入仓库 Settings → Pages
   - Source 选择 `main` 分支和 `/ (root)` 目录
   - 保存后等待部署完成

3. **访问页面**
   - 你的网站将在 `https://YOUR_USERNAME.github.io/node-eye/` 上线

## 📁 目录结构

```
node-eye/
├── index.html          # 主页面
├── css/
│   └── style.css       # 样式文件（深色科技风）
├── js/
│   ├── app.js          # 主应用逻辑
│   ├── chains.js       # 链配置管理
│   └── renderer.js     # 表格渲染
├── data/
│   ├── chains.json     # 支持的链列表配置
│   ├── bitcoin.json    # Bitcoin 节点数据
│   ├── litecoin.json   # Litecoin 节点数据
│   ├── dogecoin.json   # Dogecoin 节点数据
│   └── ethereum.json   # Ethereum 节点数据
└── README.md           # 项目说明
```

## 📝 数据格式

### chains.json - 链配置
```json
{
  "chains": [
    {
      "id": "bitcoin",
      "name": "Bitcoin",
      "symbol": "BTC",
      "icon": "₿",
      "color": "#f7931a",
      "dataFile": "bitcoin.json"
    }
  ],
  "lastUpdate": "2026-05-12T17:00:00+08:00"
}
```

### xxx.json - 节点数据
```json
{
  "chain": "bitcoin",
  "lastUpdate": "2026-05-12T17:00:00+08:00",
  "nodes": [
    {
      "host": "node1.bitcoin.org",
      "port": 8333,
      "proto": "TCP",
      "utxoRoot": "a1b2c3d4e5f6...",
      "height": 842156,
      "blocktime": "2026-05-12T16:58:32Z",
      "version": "25.0.0",
      "protocol": 70016,
      "connection": 125,
      "connectionTime": "45d 12h 34m",
      "status": "online",
      "uptime": 99.98,
      "hour": 100,
      "day": 99.95,
      "month": 99.87
    }
  ]
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| host | string | ✅ | 节点主机地址 |
| port | number | ✅ | 节点端口 |
| proto | string | ✅ | 协议类型（TCP/UDP 等） |
| utxoRoot | string | ✅ | UTXO 根哈希 |
| height | number | ✅ | 区块高度 |
| blocktime | string | ✅ | 区块时间（ISO 8601） |
| version | string | ✅ | 节点软件版本 |
| protocol | number | ✅ | 协议版本号 |
| connection | number | ✅ | 当前连接数 |
| connectionTime | string | ✅ | 连接时长描述 |
| status | string | ✅ | `online` 或 `offline` |
| uptime | number | ✅ | 总可用率百分比 |
| hour | number | ✅ | 小时可用率百分比 |
| day | number | ✅ | 日可用率百分比 |
| month | number | ✅ | 月可用率百分比 |

## 🔧 扩展开发

### 添加新链
1. 在 `data/chains.json` 中添加新链配置
2. 创建对应的 `data/<chain-id>.json` 节点数据文件
3. 刷新页面即可看到新链选项

### 添加自动刷新
在 `js/app.js` 底部取消注释：
```javascript
window.app.startAutoRefresh(60000); // 60 秒刷新
```

### 自定义样式
编辑 `css/style.css`，修改 CSS 变量：
```css
:root {
    --bg-primary: #0a0e1a;      /* 主背景色 */
    --accent-blue: #3b82f6;     /* 强调蓝色 */
    --accent-purple: #8b5cf6;   /* 强调紫色 */
    --status-online: #10b981;   /* 在线状态色 */
    --status-offline: #ef4444;  /* 离线状态色 */
}
```

## 🚀 后续功能规划

- [ ] Telegram Bot 告警 - 节点异常时发送通知
- [ ] 节点历史趋势 - 可用率变化曲线图
- [ ] 节点地图 - 全球节点地理分布
- [ ] 节点异常分析 - 异常原因统计和告警
- [ ] 自定义告警阈值 - 可配置可用率告警线
- [ ] 数据导出 - CSV/JSON 导出功能
- [ ] API 接口 - 提供 RESTful API 供第三方调用

## 📄 许可证

MIT License

## 🙏 致谢

- 灵感来源：[Bitcoin Eye](https://1209k.com/bitcoin-eye/ele.php)
- UI 风格参考：Grafana、Prometheus 监控大屏

---

<div align="center">

**Node Eye** © 2026 | 纯静态架构 · 开源免费

</div>
