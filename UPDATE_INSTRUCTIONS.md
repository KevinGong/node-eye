# Node Eye 数据更新

## 📊 最新数据 (2026-05-13 11:00)

### 统计数据
- **总节点数**: 520
- **在线节点**: 420 (80.8%)
- **离线节点**: 100
- **平均响应时间**: 2540ms

### 软件分布
- ElectrumX: 310
- Fulcrum: 97
- electrs-esplora: 4
- Rostrum: 1

### 推送步骤

在 Windows 上执行：

```cmd
cd 路径\到\node-eye
git pull origin main
git add data/bitcoin.json
git commit -m "Update Bitcoin nodes: 520 nodes (420 online)"
git push origin main
```

或者使用 GitHub Desktop:
1. 打开 GitHub Desktop
2. 选择 node-eye 仓库
3. 看到 `data/bitcoin.json` 的更改
4. 输入提交信息
5. 点击 "Push origin"
