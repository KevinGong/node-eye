/**
 * I18n.js - Internationalization Module
 * Supports multiple languages with dynamic switching
 */

class I18nManager {
    constructor() {
        this.currentLang = 'en';
        this.translations = {};
        this.fallbackLang = 'en';
    }

    /**
     * Load translations for a language
     */
    async loadLanguage(lang) {
        try {
            const response = await fetch(`locales/${lang}.json`);
            if (!response.ok) throw new Error(`Failed to load ${lang}.json`);
            
            this.translations[lang] = await response.json();
            return true;
        } catch (error) {
            console.error(`Failed to load language ${lang}:`, error);
            return false;
        }
    }

    /**
     * Set current language
     */
    async setLanguage(lang) {
        if (!this.translations[lang]) {
            const loaded = await this.loadLanguage(lang);
            if (!loaded) {
                console.warn(`Language ${lang} not available, using fallback`);
                lang = this.fallbackLang;
            }
        }
        
        this.currentLang = lang;
        document.documentElement.lang = lang;
        
        // Update all elements with data-i18n attribute
        this.updatePage();
        
        // Save preference
        localStorage.setItem('nodeeye_lang', lang);
        
        return lang;
    }

    /**
     * Get translation for a key
     */
    t(key, params = {}) {
        const langData = this.translations[this.currentLang] || {};
        const fallbackData = this.translations[this.fallbackLang] || {};
        
        let text = this.getNestedValue(langData, key) || this.getNestedValue(fallbackData, key) || key;
        
        // Replace parameters
        Object.keys(params).forEach(paramKey => {
            text = text.replace(`{${paramKey}}`, params[paramKey]);
        });
        
        return text;
    }

    /**
     * Get nested value from object using dot notation
     */
    getNestedValue(obj, path) {
        return path.split('.').reduce((current, key) => current?.[key], obj);
    }

    /**
     * Update all translatable elements on the page
     */
    updatePage() {
        // Update elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.dataset.i18n;
            const params = el.dataset.i18nParams ? JSON.parse(el.dataset.i18nParams) : {};
            
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = this.t(key, params);
            } else if (el.tagName === 'IMG') {
                el.alt = this.t(key, params);
            } else {
                el.textContent = this.t(key, params);
            }
        });
        
        // Update elements with data-i18n-title attribute
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.dataset.i18nTitle;
            el.title = this.t(key);
        });
        
        // Update table headers
        document.querySelectorAll('th[data-i18n]').forEach(th => {
            th.textContent = this.t(th.dataset.i18n);
        });
        
        // Dispatch event for custom updates
        window.dispatchEvent(new CustomEvent('i18n:updated', { 
            detail: { lang: this.currentLang } 
        }));
    }

    /**
     * Initialize i18n
     */
    async init() {
        // Load default languages
        await this.loadLanguage('en');
        await this.loadLanguage('zh');
        
        // Restore saved language or use default
        const savedLang = localStorage.getItem('nodeeye_lang') || 'en';
        await this.setLanguage(savedLang);
        
        return this;
    }

    /**
     * Get current language
     */
    getCurrentLang() {
        return this.currentLang;
    }

    /**
     * Get all available languages
     */
    getAvailableLanguages() {
        return Object.keys(this.translations);
    }
}

// Export singleton
window.i18n = new I18nManager();
