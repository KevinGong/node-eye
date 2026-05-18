/**
 * Subscription.js - Handle user subscriptions
 * Manages email + blockchain preference storage
 */

class SubscriptionManager {
    constructor() {
        this.modal = document.getElementById('subscribeModal');
        this.form = document.getElementById('subscribeForm');
        this.message = document.getElementById('subscribeMessage');
        this.closeBtn = document.getElementById('modalClose');
        this.apiEndpoint = '/api/subscribe'; // Backend API endpoint
        
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
        
        // For now, store in localStorage (backend integration later)
        const subscription = {
            email: email,
            chainId: chainId,
            subscribedAt: new Date().toISOString()
        };
        
        try {
            // Try to send to backend API
            await this.sendToBackend(subscription);
            this.showMessage(
                i18n ? i18n.t('subscription.success') : 'Successfully subscribed! You\'ll receive daily updates.',
                'success'
            );
            
            // Save to localStorage as backup
            this.saveToLocal(subscription);
            
            // Close modal after 2 seconds
            setTimeout(() => this.closeModal(), 2000);
            
        } catch (error) {
            console.error('Subscription error:', error);
            // Fallback to localStorage only
            this.saveToLocal(subscription);
            this.showMessage(
                i18n ? i18n.t('subscription.success') : 'Successfully subscribed! (Local storage only)',
                'success'
            );
            setTimeout(() => this.closeModal(), 2000);
        }
    }

    /**
     * Send subscription to backend API
     */
    async sendToBackend(subscription) {
        const response = await fetch(this.apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(subscription)
        });
        
        if (!response.ok) {
            throw new Error('Backend API not available');
        }
        
        return await response.json();
    }

    /**
     * Save subscription to localStorage
     */
    saveToLocal(subscription) {
        const key = 'nodeeye_subscription';
        localStorage.setItem(key, JSON.stringify(subscription));
        console.log('Subscription saved to localStorage:', subscription);
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

    /**
     * Get current subscription from localStorage
     */
    getLocalSubscription() {
        const key = 'nodeeye_subscription';
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    }
}

// Export singleton
window.subscriptionManager = new SubscriptionManager();
