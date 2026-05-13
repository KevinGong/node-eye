/**
 * App.js - 主应用逻辑
 */

class NodeEyeApp {
    constructor() {
        this.chainsManager = window.chainsManager;
        this.renderer = window.tableRenderer;
        this.currentData = null;
        this.filteredNodes = [];
        
        // 绑定 DOM 元素
        this.searchInput = document.getElementById('searchInput');
        this.statusFilter = document.getElementById('statusFilter');
        this.sortSelect = document.getElementById('sortSelect');
        
        // 绑定事件
        this.bindEvents();
    }

    /**
     * 初始化应用
     */
    async init() {
        try {
            // 加载链配置
            await this.chainsManager.loadChains();
            
            // 渲染链选择器
            this.renderer.renderChainSelect(
                this.chainsManager.getAllChains(),
                this.chainsManager.getCurrentChain().id,
                (chainId) => this.switchChain(chainId)
            );
            
            // 加载默认链数据
            await this.loadCurrentChain();
            
            console.log('Node Eye initialized successfully');
        } catch (error) {
            console.error('Failed to initialize:', error);
            this.renderer.renderEmpty();
        }
    }

    /**
     * 加载当前链数据
     */
    async loadCurrentChain() {
        this.renderer.renderLoading();
        
        try {
            const chainId = this.chainsManager.getCurrentChain().id;
            const data = await this.chainsManager.loadChainData(chainId);
            
            this.currentData = data;
            this.filteredNodes = [...data.nodes];
            
            // 更新 UI
            this.renderer.renderUpdateTime(data.lastUpdate);
            this.renderer.renderStats(this.filteredNodes, this.chainsManager.getCurrentChain());
            this.applyFiltersAndSort();
            
        } catch (error) {
            console.error('Failed to load chain data:', error);
            this.renderer.renderEmpty();
        }
    }

    /**
     * 切换链
     */
    async switchChain(chainId) {
        // 更新当前链
        this.chainsManager.currentChain = 
            this.chainsManager.chains.find(c => c.id === chainId);
        
        // 重置筛选条件
        this.searchInput.value = '';
        this.statusFilter.value = 'all';
        this.sortSelect.value = 'height-desc';
        
        // 加载新链数据
        await this.loadCurrentChain();
    }

    /**
     * 绑定事件
     */
    bindEvents() {
        // 搜索输入
        this.searchInput.addEventListener('input', () => {
            this.applyFiltersAndSort();
        });

        // 状态筛选
        this.statusFilter.addEventListener('change', () => {
            this.applyFiltersAndSort();
        });

        // 排序选择
        this.sortSelect.addEventListener('change', () => {
            this.applyFiltersAndSort();
        });

        // 表格头点击排序
        document.querySelectorAll('.node-table th[data-sort]').forEach(th => {
            th.addEventListener('click', () => {
                const field = th.dataset.sort;
                this.handleHeaderSort(field);
            });
        });
    }

    /**
     * 应用筛选和排序
     */
    applyFiltersAndSort() {
        if (!this.currentData) return;

        let nodes = [...this.currentData.nodes];

        // 应用搜索筛选
        const searchTerm = this.searchInput.value.toLowerCase().trim();
        if (searchTerm) {
            nodes = nodes.filter(node => 
                node.host.toLowerCase().includes(searchTerm)
            );
        }

        // 应用状态筛选
        const statusFilter = this.statusFilter.value;
        if (statusFilter !== 'all') {
            nodes = nodes.filter(node => node.status === statusFilter);
        }

        // 应用排序
        const sortValue = this.sortSelect.value;
        this.sortNodes(nodes, sortValue);

        this.filteredNodes = nodes;
        this.renderer.renderNodes(nodes);
    }

    /**
     * 排序节点
     */
    sortNodes(nodes, sortValue) {
        const [field, order] = sortValue.split('-');
        const isDesc = order === 'desc';

        nodes.sort((a, b) => {
            let valueA = a[field];
            let valueB = b[field];

            // 特殊处理
            if (field === 'host') {
                valueA = valueA.toLowerCase();
                valueB = valueB.toLowerCase();
            }

            if (valueA < valueB) return isDesc ? 1 : -1;
            if (valueA > valueB) return isDesc ? -1 : 1;
            return 0;
        });
    }

    /**
     * 处理表头点击排序
     */
    handleHeaderSort(field) {
        const sortMap = {
            'host': 'host-desc',
            'port': 'height-desc',
            'proto': 'height-desc',
            'utxoRoot': 'height-desc',
            'height': 'height-desc',
            'blocktime': 'height-desc',
            'version': 'height-desc',
            'protocol': 'height-desc',
            'connection': 'height-desc',
            'connectionTime': 'height-desc',
            'status': 'height-desc',
            'uptime': 'uptime-desc',
            'hour': 'day-desc',
            'day': 'day-desc',
            'month': 'month-desc'
        };

        const sortValue = sortMap[field] || 'height-desc';
        this.sortSelect.value = sortValue;
        this.applyFiltersAndSort();
    }

    /**
     * 自动刷新（可选功能）
     */
    startAutoRefresh(intervalMs = 60000) {
        setInterval(async () => {
            console.log('Auto-refreshing...');
            await this.loadCurrentChain();
        }, intervalMs);
    }
}

// 启动应用
document.addEventListener('DOMContentLoaded', () => {
    window.app = new NodeEyeApp();
    window.app.init();
    
    // 可选：启用自动刷新（每 60 秒）
    // window.app.startAutoRefresh(60000);
});
