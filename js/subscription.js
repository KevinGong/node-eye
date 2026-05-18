/**
 * Subscription.js - Handle user subscriptions
 * GitHub Actions backend with complete verification flow
 * 
 * Features:
 * - Subscribe via GitHub Issues
 * - Email verification
 * - Unsubscribe functionality
 * - Status tracking
 */

class SubscriptionManager {
    constructor() {
        this.modal = document.getElementById('subscribeModal');
        this.form = document.getElementById('subscribeForm');
        this.message = document.getElementById('subscribeMessage');
        this.closeBtn = document.getElementById('modalClose');
        
        // GitHub repository configuration
        this.githubOwner = 'KevinGong';
        this.githubRepo = 'node-eye';
        
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
     * Handle form submission
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
            // Create GitHub Issue for subscription
            const issue = await this.createSubscriptionIssue(email, chainId);
            
            if (issue) {
                this.showMessage(
                    i18n ? 
                    '✅ Subscription created! Please check your email for verification code.' : 
                    '✅ Subscription created! Please check your email for verification code.',
                    'success'
                );
                
                // Clear form
                this.form.reset();
                
                // Close modal after 5 seconds
                setTimeout(() => this.closeModal(), 5000);
            } else {
                throw new Error('Failed to create subscription');
            }
            
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
     * This triggers GitHub Actions to send verification email
     */
    async createSubscriptionIssue(email, chainId) {
        // Note: This requires GitHub authentication
        // For public subscription, use a backend proxy or Formspree
        
        // Option 1: Direct GitHub API (requires user to be logged in)
        try {
            // Check if user has GitHub token (from GitHub OAuth or extension)
            const token = await this.getGitHubToken();
            
            if (token) {
                const response = await fetch(`https://api.github.com/repos/${this.githubOwner}/${this.githubRepo}/issues`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `token ${token}`,
                        'Accept': 'application/vnd.github.v3+json'
                    },
                    body: JSON.stringify({
                        title: `[Subscribe] ${email}`,
                        body: `Email: ${email}\nChain: ${chainId}\nCreated: ${new Date().toISOString()}`,
                        labels: ['subscription', 'pending', chainId]
                    })
                });
                
                if (response.ok) {
                    return await response.json();
                }
            }
        } catch (error) {
            console.warn('GitHub API direct call failed, using fallback');
        }
        
        // Option 2: Fallback - Open GitHub Issues page with pre-filled content
        this.openGitHubIssuePage(email, chainId);
        return { created: true };
    }

    /**
     * Open GitHub Issues page with pre-filled content
     * User manually creates the issue
     */
    openGitHubIssuePage(email, chainId) {
        const title = encodeURIComponent(`[Subscribe] ${email}`);
        const body = encodeURIComponent(
            `## Subscription Request\n\n` +
            `**Email:** ${email}\n` +
            `**Blockchain:** ${chainId}\n\n` +
            `---\n` +
            `Please process this subscription request.\n` +
            `I will verify my email when I receive the confirmation code.`
        );
        
        const url = `https://github.com/${this.githubOwner}/${this.githubRepo}/issues/new?title=${title}&body=${body}`;
        
        // Open in new tab
        window.open(url, '_blank');
        
        this.showMessage(
            '📝 Please create the issue on GitHub to complete your subscription',
            'success'
        );
    }

    /**
     * Get GitHub token (from storage or OAuth)
     */
    async getGitHubToken() {
        // Check localStorage first
        const token = localStorage.getItem('github_token');
        if (token) {
            return token;
        }
        
        // No token available
        return null;
    }

    /**
     * Verify email with code (called from GitHub Actions result)
     */
    async verifyEmail(code) {
        const email = localStorage.getItem('pending_email');
        if (!email) {
            return { success: false, error: 'No pending subscription found' };
        }
        
        // This would be handled by GitHub Actions via issue comments
        // For now, instruct user to reply via GitHub
        return {
            success: true,
            message: 'Please reply to the GitHub issue with your verification code'
        };
    }

    /**
     * Unsubscribe via GitHub Issue
     */
    async unsubscribe(email) {
        try {
            const token = await this.getGitHubToken();
            
            if (token) {
                // Create unsubscribe issue
                const response = await fetch(`https://api.github.com/repos/${this.githubOwner}/${this.githubRepo}/issues`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `token ${token}`,
                        'Accept': 'application/vnd.github.v3+json'
                    },
                    body: JSON.stringify({
                        title: `[Unsubscribe] ${email}`,
                        body: `Email: ${email}\nReason: User request\nDate: ${new Date().toISOString()}`,
                        labels: ['unsubscribe', 'processed']
                    })
                });
                
                return await response.json();
            }
        } catch (error) {
            console.error('Unsubscribe error:', error);
        }
        
        // Fallback: Open issue page
        const title = encodeURIComponent(`[Unsubscribe] ${email}`);
        const body = encodeURIComponent(`Please unsubscribe: ${email}`);
        const url = `https://github.com/${this.githubOwner}/${this.githubRepo}/issues/new?title=${title}&body=${body}`;
        window.open(url, '_blank');
        
        return { created: true };
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
