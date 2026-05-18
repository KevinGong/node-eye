/**
 * Subscription.js - Simple subscription without verification
 * Direct save upon submission
 */

class SubscriptionManager {
    constructor() {
        this.modal = document.getElementById('subscribeModal');
        this.form = document.getElementById('subscribeForm');
        this.message = document.getElementById('subscribeMessage');
        this.closeBtn = document.getElementById('modalClose');
        
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.closeModal());
        }
        
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        }
        
        // Close modal when clicking outside
        if (this.modal) {
            this.modal.addEventListener('click', (e) => {
                if (e.target === this.modal) {
                    this.closeModal();
                }
            });
        }
    }

    /**
     * Open subscription modal
     */
    openModal() {
        if (this.modal) {
            this.modal.style.display = 'block';
            this.message.textContent = '';
            this.message.className = 'form-message';
        }
    }

    /**
     * Close subscription modal
     */
    closeModal() {
        if (this.modal) {
            this.modal.style.display = 'none';
        }
    }

    /**
     * Handle form submission - Direct save, no verification
     */
    async handleSubmit(e) {
        e.preventDefault();
        
        const email = document.getElementById('subscribeEmail').value;
        const chainId = document.getElementById('subscribeChain').value;
        const i18n = window.i18n;
        
        if (!email || !chainId) {
            this.showMessage(i18n ? i18n.t('subscription.error') : 'Please fill in all fields', 'error');
            return;
        }
        
        // Show loading state
        this.showMessage('Processing...', '');
        
        try {
            // Create GitHub Issue for subscription (direct save)
            await this.createSubscriptionIssue(email, chainId);
            
            this.showMessage(
                i18n ? 
                '✅ Subscription successful! You will receive daily reports.' : 
                '✅ Subscription successful! You will receive daily reports.',
                'success'
            );
            
            // Clear form
            this.form.reset();
            
            // Close modal after 3 seconds
            setTimeout(() => this.closeModal(), 3000);
            
        } catch (error) {
            console.error('Subscription error:', error);
            this.showMessage(
                i18n ? i18n.t('subscription.error') : 'Subscription failed. Please try again.',
                'error'
            );
        }
    }

    /**
     * Create GitHub Issue for subscription
     */
    async createSubscriptionIssue(email, chainId) {
        // Open GitHub Issues page with pre-filled content
        this.openGitHubIssuePage(email, chainId);
    }

    /**
     * Open GitHub Issues page with pre-filled content
     */
    openGitHubIssuePage(email, chainId) {
        const title = encodeURIComponent(`[Subscribe] ${email}`);
        const body = encodeURIComponent(
            `## Subscription Request\n\n` +
            `**Email:** ${email}\n` +
            `**Blockchain:** ${chainId}\n\n` +
            `---\n` +
            `Please add this subscription directly. No verification needed.`
        );
        
        const url = `https://github.com/KevinGong/node-eye/issues/new?title=${title}&body=${body}`;
        
        // Open in new tab
        window.open(url, '_blank');
        
        this.showMessage(
            '📝 Please create the issue on GitHub to complete your subscription',
            'success'
        );
    }

    /**
     * Show message in modal
     */
    showMessage(text, type) {
        if (this.message) {
            this.message.textContent = text;
            this.message.className = `form-message ${type}`;
        }
    }
}

// Export singleton
window.subscriptionManager = new SubscriptionManager();
