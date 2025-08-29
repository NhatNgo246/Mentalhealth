
// SOULFRIEND PWA Integration
class SOULFRIENDPWAManager {
    constructor() {
        this.deferredPrompt = null;
        this.isOnline = navigator.onLine;
        this.init();
    }
    
    async init() {
        // Register service worker
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/static/sw.js');
                console.log('SOULFRIEND SW registered:', registration);
                
                // Handle updates
                registration.addEventListener('updatefound', () => {
                    this.handleSWUpdate(registration);
                });
            } catch (error) {
                console.error('SOULFRIEND SW registration failed:', error);
            }
        }
        
        // Setup PWA install prompt
        this.setupInstallPrompt();
        
        // Setup offline/online detection
        this.setupOfflineDetection();
        
        // Setup mobile optimizations
        this.setupMobileOptimizations();
    }
    
    setupInstallPrompt() {
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallPrompt();
        });
        
        window.addEventListener('appinstalled', () => {
            console.log('SOULFRIEND PWA installed');
            this.hideInstallPrompt();
            this.deferredPrompt = null;
        });
    }
    
    showInstallPrompt() {
        const promptHTML = `
            <div class="pwa-install-prompt" id="pwa-install-prompt">
                <div class="pwa-install-content">
                    <div class="pwa-install-text">
                        <strong>Cài đặt SOULFRIEND</strong><br>
                        Truy cập nhanh và sử dụng offline
                    </div>
                    <div class="pwa-install-buttons">
                        <button class="pwa-install-button" onclick="pwaBanner.dismiss()">
                            Bỏ qua
                        </button>
                        <button class="pwa-install-button primary" onclick="pwaBanner.install()">
                            Cài đặt
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', promptHTML);
        
        setTimeout(() => {
            document.getElementById('pwa-install-prompt').classList.add('show');
        }, 2000);
    }
    
    hideInstallPrompt() {
        const prompt = document.getElementById('pwa-install-prompt');
        if (prompt) {
            prompt.remove();
        }
    }
    
    async installPWA() {
        if (this.deferredPrompt) {
            this.deferredPrompt.prompt();
            const choiceResult = await this.deferredPrompt.userChoice;
            
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted PWA install');
            }
            
            this.deferredPrompt = null;
            this.hideInstallPrompt();
        }
    }
    
    dismissInstallPrompt() {
        this.hideInstallPrompt();
        localStorage.setItem('pwa-install-dismissed', Date.now());
    }
    
    setupOfflineDetection() {
        // Create offline indicator
        const offlineHTML = `
            <div class="offline-indicator" id="offline-indicator">
                📴 Bạn đang offline. Một số tính năng có thể không khả dụng.
            </div>
        `;
        
        document.body.insertAdjacentHTML('afterbegin', offlineHTML);
        
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.hideOfflineIndicator();
            this.syncOfflineData();
        });
        
        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showOfflineIndicator();
        });
        
        // Initial state
        if (!this.isOnline) {
            this.showOfflineIndicator();
        }
    }
    
    showOfflineIndicator() {
        document.getElementById('offline-indicator').classList.add('show');
    }
    
    hideOfflineIndicator() {
        document.getElementById('offline-indicator').classList.remove('show');
    }
    
    async syncOfflineData() {
        if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
            const registration = await navigator.serviceWorker.ready;
            await registration.sync.register('assessment-submission');
        }
    }
    
    setupMobileOptimizations() {
        // Add mobile viewport meta tag if not present
        if (!document.querySelector('meta[name="viewport"]')) {
            const viewport = document.createElement('meta');
            viewport.name = 'viewport';
            viewport.content = 'width=device-width, initial-scale=1.0, user-scalable=no';
            document.head.appendChild(viewport);
        }
        
        // Add mobile CSS
        const mobileCSS = document.createElement('link');
        mobileCSS.rel = 'stylesheet';
        mobileCSS.href = '/static/mobile.css';
        document.head.appendChild(mobileCSS);
        
        // Setup touch gestures
        this.setupTouchGestures();
        
        // Setup mobile navigation
        this.setupMobileNavigation();
    }
    
    setupTouchGestures() {
        let startY = 0;
        let startX = 0;
        
        document.addEventListener('touchstart', (e) => {
            startY = e.touches[0].clientY;
            startX = e.touches[0].clientX;
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            const endY = e.changedTouches[0].clientY;
            const endX = e.changedTouches[0].clientX;
            const diffY = startY - endY;
            const diffX = startX - endX;
            
            // Implement pull-to-refresh
            if (diffY < -100 && Math.abs(diffX) < 50 && window.scrollY === 0) {
                this.handlePullToRefresh();
            }
        }, { passive: true });
    }
    
    setupMobileNavigation() {
        // Add mobile navigation if not present
        if (!document.querySelector('.mobile-nav')) {
            const navHTML = `
                <div class="mobile-nav">
                    <div class="mobile-nav-item" data-page="assessment">
                        📝 Đánh giá
                    </div>
                    <div class="mobile-nav-item" data-page="results">
                        📊 Kết quả
                    </div>
                    <div class="mobile-nav-item" data-page="resources">
                        📚 Tài nguyên
                    </div>
                </div>
            `;
            
            document.body.insertAdjacentHTML('afterbegin', navHTML);
            
            // Setup navigation handlers
            document.querySelectorAll('.mobile-nav-item').forEach(item => {
                item.addEventListener('click', (e) => {
                    const page = e.target.dataset.page;
                    this.navigateToPage(page);
                });
            });
        }
    }
    
    navigateToPage(page) {
        // Remove active class from all items
        document.querySelectorAll('.mobile-nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Add active class to clicked item
        document.querySelector(`[data-page="${page}"]`).classList.add('active');
        
        // Navigate to page (implementation depends on routing system)
        console.log('Navigating to:', page);
    }
    
    handlePullToRefresh() {
        console.log('Pull to refresh triggered');
        window.location.reload();
    }
    
    handleSWUpdate(registration) {
        const newWorker = registration.installing;
        
        newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                // Show update available notification
                this.showUpdateNotification();
            }
        });
    }
    
    showUpdateNotification() {
        const notification = document.createElement('div');
        notification.className = 'update-notification';
        notification.innerHTML = `
            <div class="update-content">
                <span>Có bản cập nhật mới!</span>
                <button onclick="window.location.reload()">Cập nhật</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
    }
}

// PWA Manager instance
const pwaManager = new SOULFRIENDPWAManager();

// Global PWA banner controls
window.pwaBanner = {
    install: () => pwaManager.installPWA(),
    dismiss: () => pwaManager.dismissInstallPrompt()
};

// Export for use in other modules
window.SOULFRIENDPWAManager = SOULFRIENDPWAManager;

console.log('SOULFRIEND PWA Manager initialized');
