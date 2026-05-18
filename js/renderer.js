/**
 * Renderer.js - Page Rendering
 * Updated to support new table columns and i18n
 */

class TableRenderer {
    constructor() {
        this.tableBody = document.getElementById('nodeTableBody');
        this.i18n = window.i18n;
    }

    /**
     * Render node table
     */
    renderNodes(nodes) {
        if (!nodes || nodes.length === 0) {
            this.renderEmpty();
            return;
        }

        const html = nodes.map((node, index) => this.renderNodeRow(node, index + 1)).join('');
        this.tableBody.innerHTML = html;
        
        // Bind copy button events
        this.bindCopyButtons();
    }

    /**
     * Render single node row
     */
    renderNodeRow(node, index) {
        const statusClass = node.status === 'open' ? 'online' : 'offline';
        const statusText = this.i18n ? this.i18n.t(`status.${node.status}`) : (node.status === 'open' ? 'Open' : 'Offline');
        const hostPort = `${node.host}:${node.port}`;
        
        return `
            <tr>
                <td class="index-col">${index}</td>
                <td>
                    <div class="host-cell">
                        <span class="host-text">${this.escapeHtml(node.host)}</span>
                        <button class="copy-btn" data-copy="${this.escapeHtml(hostPort)}" title="${this.i18n ? this.i18n.t('copyAddress') : 'Copy node address'}">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                            </svg>
                        </button>
                    </div>
                </td>
                <td>${node.port}</td>
                <td class="ssl-cell">${this.renderSslIcon(node.ssl)}</td>
                <td class="mono">${this.formatNumber(node.height)}</td>
                <td class="mono">${this.escapeHtml(node.server_version || '')}</td>
                <td class="mono">${node.protocol_version || ''}</td>
                <td>${this.renderStatus(statusClass, statusText)}</td>
                <td class="mono">${node.last_seen || ''}</td>
                <td class="mono">${node.response_time_ms ? node.response_time_ms + ' ms' : '-'}</td>
                <td>${this.renderUptimeCell(node.per_hour)}</td>
                <td>${this.renderUptimeCell(node.per_day)}</td>
                <td>${this.renderUptimeCell(node.per_month)}</td>
            </tr>
        `;
    }

    /**
     * Render SSL icon
     */
    renderSslIcon(ssl) {
        if (ssl) {
            return '<span class="ssl-badge ssl-yes">✓ SSL</span>';
        } else {
            return '<span class="ssl-badge ssl-no">✗ TCP</span>';
        }
    }

    /**
     * Render uptime cell with bar
     */
    renderUptimeCell(value) {
        if (value === undefined || value === null) {
            return '-';
        }
        
        const percentage = (value * 100).toFixed(2);
        let level = 'high';
        if (value < 0.90) level = 'low';
        else if (value < 0.98) level = 'medium';
        
        return `
            <div class="uptime-bar">
                <span class="uptime-value">${percentage}%</span>
                <div class="uptime-progress">
                    <div class="uptime-fill ${level}" style="width: ${Math.min(value * 100, 100)}%"></div>
                </div>
            </div>
        `;
    }

    /**
     * Render status badge
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
     * Render empty state
     */
    renderEmpty() {
        const emptyText = this.i18n ? this.i18n.t('empty') : 'No matching nodes found';
        this.tableBody.innerHTML = `
            <tr>
                <td colspan="13">
                    <div class="empty-state">
                        <div class="empty-state-icon">📭</div>
                        <p>${emptyText}</p>
                    </div>
                </td>
            </tr>
        `;
    }

    /**
     * Render loading state
     */
    renderLoading() {
        const loadingText = this.i18n ? this.i18n.t('loading') : 'Loading node data...';
        this.tableBody.innerHTML = `
            <tr>
                <td colspan="13">
                    <div class="loading">
                        <div class="loading-spinner"></div>
                        <span>${loadingText}</span>
                    </div>
                </td>
            </tr>
        `;
    }

    /**
     * Render statistics
     */
    renderStats(nodes, chain) {
        const total = nodes.length;
        const online = nodes.filter(n => n.status === 'open').length;
        const offline = total - online;
        const avgUptime = total > 0 
            ? (nodes.reduce((sum, n) => sum + (n.per_month || 0), 0) / total * 100).toFixed(2)
            : 0;

        document.getElementById('currentChain').textContent = `${chain.icon} ${chain.name}`;
        document.getElementById('totalNodes').textContent = total;
        document.getElementById('onlineNodes').textContent = online;
        document.getElementById('offlineNodes').textContent = offline;
        document.getElementById('avgUptime').textContent = avgUptime + '%';
    }

    /**
     * Render chain selector
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
     * Render update time
     */
    renderUpdateTime(timestamp) {
        document.getElementById('lastUpdate').textContent = 
            window.chainsManager.formatUpdateTime(timestamp);
    }

    /**
     * Render subscription chain selector
     */
    renderSubscriptionChainSelect(chains) {
        const select = document.getElementById('subscribeChain');
        if (!select) return;
        
        select.innerHTML = chains.map(chain => `
            <option value="${chain.id}">
                ${chain.icon} ${chain.name} (${chain.symbol})
            </option>
        `).join('');
    }

    /**
     * Utility: Escape HTML
     */
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Utility: Format number with thousands separator
     */
    formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }

    /**
     * Bind copy button events
     */
    bindCopyButtons() {
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.stopPropagation();
                const text = btn.dataset.copy;
                const copySuccess = this.i18n ? this.i18n.t('copySuccess') : 'Copied!';
                
                try {
                    await navigator.clipboard.writeText(text);
                    btn.classList.add('copied');
                    btn.title = copySuccess;
                    setTimeout(() => {
                        btn.classList.remove('copied');
                        btn.title = this.i18n ? this.i18n.t('copyAddress') : 'Copy node address';
                    }, 2000);
                } catch (err) {
                    const textarea = document.createElement('textarea');
                    textarea.value = text;
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                    btn.classList.add('copied');
                    btn.title = copySuccess;
                    setTimeout(() => {
                        btn.classList.remove('copied');
                        btn.title = this.i18n ? this.i18n.t('copyAddress') : 'Copy node address';
                    }, 2000);
                }
            });
        });
    }
}

// Export singleton
window.tableRenderer = new TableRenderer();
