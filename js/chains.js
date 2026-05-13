/**
 * Chains.js - 链配置管理
 */

class ChainsManager {
    constructor() {
        this.chains = [];
        this.currentChain = null;
        this.dataPath = 'data/';
    }

    /**
     * 加载链配置
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
     * 加载指定链的节点数据
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
     * 获取当前链
     */
    getCurrentChain() {
        return this.currentChain;
    }

    /**
     * 获取所有链
     */
    getAllChains() {
        return this.chains;
    }

    /**
     * 格式化更新时间
     */
    formatUpdateTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        // 如果是一分钟之内
        if (diff < 60000) {
            return '刚刚更新';
        }
        // 如果是一小时之内
        if (diff < 3600000) {
            const minutes = Math.floor(diff / 60000);
            return `${minutes}分钟前`;
        }
        // 如果是今天
        if (diff < 86400000) {
            const hours = Math.floor(diff / 3600000);
            return `${hours}小时前`;
        }
        
        // 否则显示完整日期
        return date.toLocaleString('zh-CN', {
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// 导出单例
window.chainsManager = new ChainsManager();
