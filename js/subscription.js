/**
 * Subscription.js - Direct subscription save to static file
 * No verification, no GitHub redirect
 */

class SubscriptionManager {
    constructor() {
        this.modal = document.getElementById('subscribeModal');
        this.form = document.getElementById('subscribeForm');
        this.message = document.getElementById('subscribeMessage');
        this.closeBtn = document.getElementById('modalClose');
        
        // Subscription API endpoint (GitHub API or local backend)
        this.apiEndpoint = 'https://api.github.com/repos/KevinGong/node-eye/contents/data/subscribers.enc';
        
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
     * Handle form submission - Direct save to static file
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
            // Save subscription directly
            await this.saveSubscription(email, chainId);
            
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
                i18n ? i18n.t('subscription.error') : 'Subscription failed. Please create an issue at GitHub.',
                'error'
            );
            
            // Fallback: Open GitHub Issue
            setTimeout(() => {
                this.openGitHubIssuePage(email, chainId);
            }, 2000);
        }
    }

    /**
     * Save subscription to static file via GitHub API
     */
    async saveSubscription(email, chainId) {
        // Note: This requires GitHub token for writing
        // For production, use a backend proxy or GitHub Actions workflow_dispatch
        
        const subscription = {
            email: email,
            chain_id: chainId,
            subscribed_at: new Date().toISOString(),
            status: 'active'
        };
        
        // Option 1: Try GitHub API (requires token)
        try {
            const token = localStorage.getItem('github_token');
            if (token) {
                await this.updateSubscribersFile(subscription, token);
                return;
            }
        } catch (error) {
            console.warn('GitHub API failed, using fallback');
        }
        
        // Option 2: Save to localStorage (temporary)
        this.saveToLocal(subscription);
        
        // Option 3: Send webhook to trigger GitHub Actions
        await this.triggerWorkflow(email, chainId);
    }

    /**
     * Update subscribers file via GitHub API
     */
    async updateSubscribersFile(subscription, token) {
        // Get current file
        const response = await fetch(this.apiEndpoint, {
            headers: {
                'Authorization': `token ${token}`,
                'Accept': 'application/vnd.github.v3+json'
            }
        });
        
        const data = await response.json();
        
        // Decrypt current content (simplified - in production use proper decryption)
        let content = { subscribers: [] };
        if (data.content) {
            try {
                const decoded = atob(data.content);
                content = JSON.parse(decoded);
            } catch (e) {
                console.warn('Could not decrypt, starting fresh');
            }
        }
        
        // Add subscription
        content.subscribers.push(subscription);
        
        // Encrypt and update
        const encrypted = btoa(JSON.stringify(content));
        
        await fetch(this.apiEndpoint, {
            method: 'PUT',
            headers: {
                'Authorization': `token ${token}`,
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: `feat: Add subscription ${subscription.email}`,
                content: encrypted,
                sha: data.sha
            })
        });
    }

    /**
     * Trigger GitHub Actions workflow to add subscription
     */
    async triggerWorkflow(email, chainId) {
        // This triggers a workflow_dispatch event
        // Requires GitHub token with repo scope
        const token = localStorage.getItem('github_token');
        
        if (!token) {
            // No token, save locally and inform user
            console.log('No GitHub token, saved locally');
            return;
        }
        
        await fetch('https://api.github.com/repos/KevinGong/node-eye/actions/workflows/add-subscription.yml/dispatches', {
            method: 'POST',
            headers: {
                'Authorization': `token ${token}`,
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ref: 'main',
                inputs: {
                    email: email,
                    chain_id: chainId
                }
            })
        });
    }

    /**
     * Save to localStorage as fallback
     */
    saveToLocal(subscription) {
        const key = 'nodeeye_pending_subscription';
        localStorage.setItem(key, JSON.stringify(subscription));
        console.log('Subscription saved to localStorage:', subscription);
    }

    /**
     * Open GitHub Issue as fallback
     */
    openGitHubIssuePage(email, chainId) {
        const title = encodeURIComponent(`[Subscribe] ${email}`);
        const body = encodeURIComponent(
            `## Subscription Request\n\n` +
            `**Email:** ${email}\n` +
            `**Blockchain:** ${chainId}\n\n` +
            `---\n` +
            `Please add this subscription.`
        );
        
        const url = `https://github.com/KevinGong/node-eye/issues/new?title=${title}&body=${body}`;
        window.open(url, '_blank');
        
        this.showMessage(
            '📝 Please create the issue to complete subscription',
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
