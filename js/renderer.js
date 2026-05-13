/**
 * Renderer.js - 页面渲染
 */

class TableRenderer {
    constructor() {
        this.tableBody = document.getElementById('nodeTableBody');
    }

    /**
     * 渲染节点表格
     */
    renderNodes(nodes) {
        if (!nodes || nodes.length === 0) {
            this.renderEmpty();
            return;
        }

        const html = nodes.map((node, index) => this.renderNodeRow(node, index + 1)).join('');
        this.tableBody.innerHTML = html;
        
        // 绑定复制按钮事件
        this.bindCopyButtons();
    }

    /**
     * 渲染单行节点
     */
    renderNodeRow(node, index) {
        const statusClass = node.status === 'online' ? 'online' : 'offline';
        const statusText = node.status === 'online' ? '正常' : '异常';
        const hostPort = `${node.host}:${node.port}`;
        
        return `
            <tr>
                <td class="index-col">${index}</td>
                <td>
                    <div class="host-cell">
                        <span class="host-text">${this.escapeHtml(node.host)}</span>
                        <button class="copy-btn" data-copy="${this.escapeHtml(hostPort)}" title="复制 Host:Port">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                            </svg>
                        </button>
                    </div>
                </td>
                <td>${node.port}</td>
                <td>${node.proto}</td>
                <td class="mono">${this.truncate(node.utxoRoot, 14)}</td>
                <td class="mono">${this.formatNumber(node.height)}</td>
                <td class="mono">${this.formatBlocktime(node.blocktime)}</td>
                <td class="mono">${node.version}</td>
                <td class="mono">${node.protocol}</td>
                <td>${node.connection}</td>
                <td>${node.connectionTime}</td>
                <td>${this.renderStatus(statusClass, statusText)}</td>
                <td>${node.uptime.toFixed(2)}%</td>
                <td>${this.renderUptimeBar(node.hour)}</td>
                <td>${this.renderUptimeBar(node.day)}</td>
                <td>${this.renderUptimeBar(node.month)}</td>
            </tr>
        `;
    }

    /**
     * 渲染状态徽章
     */
    renderStatus(statusClass, statusText) {
        return `
            <span class="status-badge ${statusClass}">
                <span class="status-dot ${statusClass}"></span>
                ${statusText}
            </span>
        `;
    }

    /**
     * 渲染可用率进度条
     */
    renderUptimeBar(value) {
        let level = 'high';
        if (value < 90) level = 'low';
        else if (value < 98) level = 'medium';
        
        return `
            <div class="uptime-bar">
                <span class="uptime-value">${value.toFixed(1)}%</span>
                <div class="uptime-progress">
                    <div class="uptime-fill ${level}" style="width: ${Math.min(value, 100)}%"></div>
                </div>
            </div>
        `;
    }

    /**
     * 渲染空状态
     */
    renderEmpty() {
        this.tableBody.innerHTML = `
            <tr>
                <td colspan="15">
                    <div class="empty-state">
                        <div class="empty-state-icon">📭</div>
                        <p>没有找到匹配的节点</p>
                    </div>
                </td>
            </tr>
        `;
    }

    /**
     * 渲染加载状态
     */
    renderLoading() {
        this.tableBody.innerHTML = `
            <tr>
                <td colspan="15">
                    <div class="loading">
                        <div class="loading-spinner"></div>
                        <span>正在加载节点数据...</span>
                    </div>
                </td>
            </tr>
        `;
    }

    /**
     * 渲染统计信息
     */
    renderStats(nodes, chain) {
        const total = nodes.length;
        const online = nodes.filter(n => n.status === 'online').length;
        const offline = total - online;
        const avgUptime = total > 0 
            ? (nodes.reduce((sum, n) => sum + n.uptime, 0) / total).toFixed(2)
            : 0;

        document.getElementById('currentChain').textContent = chain.name;
        document.getElementById('totalNodes').textContent = total;
        document.getElementById('onlineNodes').textContent = online;
        document.getElementById('offlineNodes').textContent = offline;
        document.getElementById('avgUptime').textContent = avgUptime + '%';
    }

    /**
     * 渲染链选择器
     */
    renderChainSelect(chains, currentChainId, onChange) {
        const select = document.getElementById('chainSelect');
        select.innerHTML = chains.map(chain => `
            <option value="${chain.id}" ${chain.id === currentChainId ? 'selected' : ''}>
                ${chain.icon} ${chain.name} (${chain.symbol})
            </option>
        `).join('');
        
        select.addEventListener('change', (e) => {
            onChange(e.target.value);
        });
    }

    /**
     * 渲染更新时间
     */
    renderUpdateTime(timestamp) {
        document.getElementById('lastUpdate').textContent = 
            window.chainsManager.formatUpdateTime(timestamp);
    }

    /**
     * 工具：转义 HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * 工具：截断文本
     */
    truncate(text, maxLength) {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength - 3) + '...';
    }

    /**
     * 工具：格式化数字（添加千位分隔符）
     */
    formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }

    /**
     * 工具：格式化区块时间
     */
    formatBlocktime(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString('zh-CN', {
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        }).replace(/\//g, '-');
    }

    /**
     * 绑定复制按钮事件
     */
    bindCopyButtons() {
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.stopPropagation();
                const text = btn.dataset.copy;
                try {
                    await navigator.clipboard.writeText(text);
                    // 显示成功提示
                    btn.classList.add('copied');
                    btn.title = '已复制！';
                    setTimeout(() => {
                        btn.classList.remove('copied');
                        btn.title = '复制 Host:Port';
                    }, 2000);
                } catch (err) {
                    // 降级方案
                    const textarea = document.createElement('textarea');
                    textarea.value = text;
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                    btn.classList.add('copied');
                    btn.title = '已复制！';
                    setTimeout(() => {
                        btn.classList.remove('copied');
                        btn.title = '复制 Host:Port';
                    }, 2000);
                }
            });
        });
    }
}

// 导出单例
window.tableRenderer = new TableRenderer();
