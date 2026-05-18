/**
 * App.js - Main Application Logic
 * Updated to support i18n and new data structure
 */

class NodeEyeApp {
    constructor() {
        this.chainsManager = window.chainsManager;
        this.renderer = window.tableRenderer;
        this.subscriptionManager = window.subscriptionManager;
        this.i18n = window.i18n;
        this.currentData = null;
        this.filteredNodes = [];
        
        // Bind DOM elements
        this.searchInput = document.getElementById('searchInput');
        this.statusFilter = document.getElementById('statusFilter');
        this.sortSelect = document.getElementById('sortSelect');
        this.languageSelect = document.getElementById('languageSelect');
        this.subscribeBtn = document.getElementById('subscribeBtn');
        
        // Bind events
        this.bindEvents();
    }

    /**
     * Initialize application
     */
    async init() {
        try {
            // Initialize i18n first
            await this.i18n.init();
            
            // Set language selector value
            if (this.languageSelect) {
                this.languageSelect.value = this.i18n.getCurrentLang();
            }
            
            // Load chain configuration
            await this.chainsManager.loadChains();
            
            // Render chain selector
            this.renderer.renderChainSelect(
                this.chainsManager.getAllChains(),
                this.chainsManager.getCurrentChain().id,
                (chainId) => this.switchChain(chainId)
            );
            
            // Render subscription chain selector
            if (this.subscriptionManager) {
                this.renderer.renderSubscriptionChainSelect(this.chainsManager.getAllChains());
            }
            
            // Load default chain data
            await this.loadCurrentChain();
            
            console.log('Node Eye initialized successfully');
        } catch (error) {
            console.error('Failed to initialize:', error);
            this.renderer.renderEmpty();
        }
    }

    /**
     * Load current chain data
     */
    async loadCurrentChain() {
        this.renderer.renderLoading();
        
        try {
            const chainId = this.chainsManager.getCurrentChain().id;
            const data = await this.chainsManager.loadChainData(chainId);
            
            this.currentData = data;
            this.filteredNodes = [...data.nodes];
            
            // Update UI
            this.renderer.renderUpdateTime(data.lastUpdate);
            this.renderer.renderStats(this.filteredNodes, this.chainsManager.getCurrentChain());
            this.applyFiltersAndSort();
            
        } catch (error) {
            console.error('Failed to load chain data:', error);
            this.renderer.renderEmpty();
        }
    }

    /**
     * Switch chain
     */
    async switchChain(chainId) {
        // Update current chain
        this.chainsManager.currentChain = 
            this.chainsManager.chains.find(c => c.id === chainId);
        
        // Reset filters
        this.searchInput.value = '';
        this.statusFilter.value = 'all';
        this.sortSelect.value = 'per_month-desc';
        
        // Load new chain data
        await this.loadCurrentChain();
    }

    /**
     * Bind events
     */
    bindEvents() {
        // Language switcher
        if (this.languageSelect) {
            this.languageSelect.addEventListener('change', async (e) => {
                await this.i18n.setLanguage(e.target.value);
                // Re-render table with new language
                this.applyFiltersAndSort();
            });
        }
        
        // Subscribe button
        if (this.subscribeBtn && this.subscriptionManager) {
            this.subscribeBtn.addEventListener('click', () => {
                this.subscriptionManager.openModal();
            });
        }
        
        // Search input
        this.searchInput.addEventListener('input', () => {
            this.applyFiltersAndSort();
        });

        // Status filter
        this.statusFilter.addEventListener('change', () => {
            this.applyFiltersAndSort();
        });

        // Sort select
        this.sortSelect.addEventListener('change', () => {
            this.applyFiltersAndSort();
        });

        // Table header click for sorting
        document.querySelectorAll('.node-table th[data-sort]').forEach(th => {
            th.addEventListener('click', () => {
                const field = th.dataset.sort;
                this.handleHeaderSort(field);
            });
        });
        
        // Listen for i18n updates
        window.addEventListener('i18n:updated', () => {
            this.applyFiltersAndSort();
        });
    }

    /**
     * Apply filters and sort
     */
    applyFiltersAndSort() {
        if (!this.currentData) return;

        let nodes = [...this.currentData.nodes];

        // Apply search filter
        const searchTerm = this.searchInput.value.toLowerCase().trim();
        if (searchTerm) {
            nodes = nodes.filter(node => 
                node.host.toLowerCase().includes(searchTerm)
            );
        }

        // Apply status filter
        const statusFilter = this.statusFilter.value;
        if (statusFilter !== 'all') {
            nodes = nodes.filter(node => node.status === statusFilter);
        }

        // Apply sort
        const sortValue = this.sortSelect.value;
        this.sortNodes(nodes, sortValue);

        this.filteredNodes = nodes;
        this.renderer.renderNodes(nodes);
    }

    /**
     * Sort nodes
     */
    sortNodes(nodes, sortValue) {
        const [field, order] = sortValue.split('-');
        const isDesc = order === 'desc';

        nodes.sort((a, b) => {
            let valueA = a[field];
            let valueB = b[field];

            // Special handling for different field types
            if (field === 'host') {
                valueA = valueA.toLowerCase();
                valueB = valueB.toLowerCase();
            } else if (field === 'ssl') {
                valueA = valueA ? 1 : 0;
                valueB = valueB ? 1 : 0;
            } else if (field === 'last_seen') {
                valueA = new Date(valueA || 0);
                valueB = new Date(valueB || 0);
            } else if (['per_hour', 'per_day', 'per_month', 'height', 'port', 'response_time_ms'].includes(field)) {
                valueA = Number(valueA) || 0;
                valueB = Number(valueB) || 0;
            }

            if (valueA < valueB) return isDesc ? 1 : -1;
            if (valueA > valueB) return isDesc ? -1 : 1;
            return 0;
        });
    }

    /**
     * Handle header click sort
     */
    handleHeaderSort(field) {
        const sortMap = {
            'host': 'host-desc',
            'port': 'port-desc',
            'ssl': 'ssl-desc',
            'height': 'height-desc',
            'server_version': 'height-desc',
            'protocol_version': 'height-desc',
            'status': 'height-desc',
            'last_seen': 'last_seen-desc',
            'response_time_ms': 'response_time_ms-desc',
            'per_hour': 'per_hour-desc',
            'per_day': 'per_day-desc',
            'per_month': 'per_month-desc'
        };

        const sortValue = sortMap[field] || 'height-desc';
        this.sortSelect.value = sortValue;
        this.applyFiltersAndSort();
    }

    /**
     * Auto refresh (optional feature)
     */
    startAutoRefresh(intervalMs = 60000) {
        setInterval(async () => {
            console.log('Auto-refreshing...');
            await this.loadCurrentChain();
        }, intervalMs);
    }
}

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new NodeEyeApp();
    window.app.init();
    
    // Optional: enable auto-refresh (every 60 seconds)
    // window.app.startAutoRefresh(60000);
});
