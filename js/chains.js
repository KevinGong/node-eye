/**
 * Chains.js - Chain Configuration Management
 * Manages blockchain chain settings and data loading
 */

class ChainsManager {
    constructor() {
        this.chains = [];
        this.currentChain = null;
        this.dataPath = 'data/';
        this.lastUpdate = null;
    }

    /**
     * Load chain configuration from chains.json
     */
    async loadChains() {
        try {
            const response = await fetch(this.dataPath + 'chains.json');
            if (!response.ok) throw new Error('Failed to load chains.json');
            
            const data = await response.json();
            this.chains = data.chains;
            this.lastUpdate = data.lastUpdate;
            
            if (this.chains.length > 0) {
                this.currentChain = this.chains[0];
            }
            
            return this.chains;
        } catch (error) {
            console.error('Error loading chains:', error);
            throw error;
        }
    }

    /**
     * Load node data for specified chain
     */
    async loadChainData(chainId) {
        try {
            const chain = this.chains.find(c => c.id === chainId);
            if (!chain) throw new Error(`Chain ${chainId} not found`);
            
            const response = await fetch(this.dataPath + chain.dataFile);
            if (!response.ok) throw new Error(`Failed to load ${chain.dataFile}`);
            
            const data = await response.json();
            this.currentChain = chain;
            
            return data;
        } catch (error) {
            console.error('Error loading chain data:', error);
            throw error;
        }
    }

    /**
     * Get current chain
     */
    getCurrentChain() {
        return this.currentChain;
    }

    /**
     * Get all chains
     */
    getAllChains() {
        return this.chains;
    }

    /**
     * Format update time for display
     */
    formatUpdateTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        // Less than 1 minute ago
        if (diff < 60000) {
            return 'Just now';
        }
        // Less than 1 hour ago
        if (diff < 3600000) {
            const minutes = Math.floor(diff / 60000);
            return `${minutes} minutes ago`;
        }
        // Today
        if (diff < 86400000) {
            const hours = Math.floor(diff / 3600000);
            return `${hours} hours ago`;
        }
        
        // Show full date
        return date.toLocaleString('en-US', {
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// Export singleton
window.chainsManager = new ChainsManager();
