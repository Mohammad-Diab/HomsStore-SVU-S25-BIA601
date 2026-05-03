class BehaviorTracker {
    constructor() {
        this.userId = 1; // Default for demo
        this.sessionStart = Date.now();
        this.pageCategory = this.detectCategory();
        this.productId = this.detectProductId();
        this.API_URL = 'http://localhost:5000/api/track';
        
        this.init();
    }

    detectCategory() {
        // Simple logic to extract category from page context or URL
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('category') || 'General';
    }

    detectProductId() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('id');
    }

    async trackEvent(eventType, additionalData = {}) {
        const duration = Math.floor((Date.now() - this.sessionStart) / 1000);
        
        const payload = {
            user_id: this.userId,
            event_type: eventType,
            product_id: additionalData.productId || this.productId,
            category: additionalData.category || this.pageCategory,
            duration: duration,
            search_query: additionalData.searchQuery || null
        };

        try {
            await fetch(this.API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } catch (e) {
            console.error('Tracking failed', e);
        }
    }

    init() {
        // Track page view
        if (this.productId) {
            this.trackEvent('view');
        } else {
            this.trackEvent('browse');
        }

        // Track clicks on products
        document.addEventListener('click', (e) => {
            const productLink = e.target.closest('a[href*="product-details.html"]');
            if (productLink) {
                const url = new URL(productLink.href, window.location.origin);
                const pId = url.searchParams.get('id');
                if (pId) {
                    this.trackEvent('click', { productId: pId });
                }
            }
        });

        // Track search
        const searchInput = document.querySelector('input[placeholder*="Search"]');
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && searchInput.value.trim()) {
                    this.trackEvent('search', { searchQuery: searchInput.value.trim() });
                }
            });
        }

        // Track exit/unload for duration
        window.addEventListener('beforeunload', () => {
            this.trackEvent('exit');
        });
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    window.behaviorTracker = new BehaviorTracker();
});
