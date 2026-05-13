# Node Eye - 多链区块链志愿者节点监控平台

## 项目概述
开发一个纯静态的区块链节点监控平台，参考 https://1209k.com/bitcoin-eye/ele.php 风格，但采用更现代、科技感的设计。

## 技术栈
- HTML5 + CSS3 + Vanilla JavaScript
- 部署：GitHub Pages
- 数据源：GitHub 仓库中的 JSON 文件

## 目录结构
```
node-eye/
├── index.html          # 主页面
├── css/
│   └── style.css       # 样式文件
├── js/
│   ├── app.js          # 主应用逻辑
│   ├── chains.js       # 链配置
│   └── renderer.js     # 页面渲染
├── data/
│   ├── chains.json     # 支持的链列表
│   ├── bitcoin.json    # Bitcoin 节点数据
│   ├── litecoin.json   # Litecoin 节点数据
│   ├── dogecoin.json   # Dogecoin 节点数据
│   └── ethereum.json   # Ethereum 节点数据
└── README.md           # 项目说明
```

## 执行步骤

- [ ] 步骤 1: 创建项目目录结构
- [ ] 步骤 2: 编写 chains.json（链配置）
- [ ] 步骤 3: 编写示例节点数据（bitcoin.json 等）
- [ ] 步骤 4: 编写 index.html（页面结构）
- [ ] 步骤 5: 编写 style.css（深色科技风样式）
- [ ] 步骤 6: 编写 app.js（主应用逻辑）
- [ ] 步骤 7: 编写 chains.js（链配置管理）
- [ ] 步骤 8: 编写 renderer.js（表格渲染）
- [ ] 步骤 9: 测试页面功能
- [ ] 步骤 10: 编写 README.md

## 功能特性

### 核心功能
1. **多链切换** - 顶部下拉选择支持的链
2. **统计面板** - 节点总数、正常/异常数、平均可用率
3. **节点表格** - 完整字段展示，状态颜色区分
4. **搜索筛选** - 按 Host 搜索，按状态筛选
5. **排序功能** - 按 Height/Uptime/Day/Month 排序

### 表格字段
| 字段 | 说明 |
|------|------|
| Host | 节点地址 |
| Port | 端口 |
| Proto | 协议 |
| UTXO Root | UTXO 根 |
| Height | 区块高度 |
| Blocktime | 区块时间 |
| Version | 版本 |
| Protocol | 协议版本 |
| Connection | 连接数 |
| ConnectionTime | 连接时间 |
| Status | 状态（正常/异常） |
| Uptime | 在线时长 |
| Hour | 小时可用率 |
| Day | 日可用率 |
| Month | 月可用率 |

## 视觉风格
- 深色背景（#0a0e1a, #111827）
- 科技蓝/紫色点缀（#3b82f6, #8b5cf6）
- 状态色：正常绿色（#10b981），异常红色（#ef4444）
- 类似 Grafana/Prometheus 监控大屏风格
- 移动端响应式，表格横向滚动

## 当前进度
- [x] 步骤 1: 创建项目目录结构 ✅
- [x] 步骤 2: 编写 chains.json（链配置） ✅
- [x] 步骤 3: 编写示例节点数据 ✅
- [x] 步骤 4: 编写 index.html（页面结构） ✅
- [x] 步骤 5: 编写 style.css（深色科技风样式） ✅
- [x] 步骤 6: 编写 app.js（主应用逻辑） ✅
- [x] 步骤 7: 编写 chains.js（链配置管理） ✅
- [x] 步骤 8: 编写 renderer.js（表格渲染） ✅
- [x] 步骤 9: 测试页面功能（本地验证） ✅
- [x] 步骤 10: 编写 README.md ✅

## ✅ 项目完成

所有文件已创建完成，项目结构如下：
- index.html - 主页面
- css/style.css - 深色科技风样式
- js/app.js - 主应用逻辑
- js/chains.js - 链配置管理
- js/renderer.js - 表格渲染
- data/chains.json - 链配置
- data/*.json - 各链节点数据
- README.md - 项目文档

已打包发送 `node-eye.zip` 给用户。
