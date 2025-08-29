"""
📱 Progressive Web App (PWA) Configuration
Mobile optimization và offline capabilities cho SOULFRIEND V2.0
"""

import json
import os
from typing import Dict

class PWAGenerator:
    """
    Generate PWA configuration files và mobile optimizations
    """
    
    def __init__(self, app_name: str = "SOULFRIEND", app_url: str = "http://localhost:8501"):
        self.app_name = app_name
        self.app_url = app_url
        self.manifest_path = "/workspaces/Mentalhealth/static/manifest.json"
        self.sw_path = "/workspaces/Mentalhealth/static/sw.js"
        
        # Ensure static directory exists
        os.makedirs(os.path.dirname(self.manifest_path), exist_ok=True)
    
    def generate_manifest(self) -> Dict:
        """Generate PWA manifest.json"""
        manifest = {
            "name": "SOULFRIEND - Mental Health Support",
            "short_name": "SOULFRIEND",
            "description": "AI-powered mental health assessment and support platform",
            "version": "2.0.0",
            "start_url": "/",
            "display": "standalone",
            "orientation": "portrait-primary",
            "theme_color": "#667eea",
            "background_color": "#ffffff",
            "scope": "/",
            "lang": "vi-VN",
            "dir": "ltr",
            "categories": ["health", "medical", "wellness"],
            "icons": [
                {
                    "src": "/static/icon-72.png",
                    "sizes": "72x72",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icon-96.png", 
                    "sizes": "96x96",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icon-128.png",
                    "sizes": "128x128", 
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icon-144.png",
                    "sizes": "144x144",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icon-152.png",
                    "sizes": "152x152",
                    "type": "image/png", 
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icon-192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icon-384.png",
                    "sizes": "384x384",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/static/icon-512.png",
                    "sizes": "512x512", 
                    "type": "image/png",
                    "purpose": "any maskable"
                }
            ],
            "screenshots": [
                {
                    "src": "/static/screenshot-desktop.png",
                    "sizes": "1280x720",
                    "type": "image/png",
                    "platform": "wide"
                },
                {
                    "src": "/static/screenshot-mobile.png", 
                    "sizes": "390x844",
                    "type": "image/png",
                    "platform": "narrow"
                }
            ],
            "features": [
                "cross-platform",
                "offline-support", 
                "push-notifications",
                "installable"
            ],
            "related_applications": [],
            "prefer_related_applications": False,
            "shortcuts": [
                {
                    "name": "Quick Assessment",
                    "short_name": "Assessment", 
                    "description": "Start a quick mental health assessment",
                    "url": "/assessment",
                    "icons": [{"src": "/static/icon-96.png", "sizes": "96x96"}]
                },
                {
                    "name": "View Results",
                    "short_name": "Results",
                    "description": "View your assessment results", 
                    "url": "/results",
                    "icons": [{"src": "/static/icon-96.png", "sizes": "96x96"}]
                }
            ]
        }
        
        # Save manifest
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        return manifest
    
    def generate_service_worker(self) -> str:
        """Generate service worker for offline functionality"""
        sw_content = '''
// SOULFRIEND Service Worker v2.0
// Offline functionality và caching

const CACHE_NAME = 'soulfriend-v2.0';
const API_CACHE_NAME = 'soulfriend-api-v2.0';

// Resources to cache for offline use
const STATIC_RESOURCES = [
    '/',
    '/static/manifest.json',
    '/static/icon-192.png',
    '/static/icon-512.png',
    // Add other static resources
];

// API endpoints to cache
const API_ENDPOINTS = [
    '/api/questionnaires',
    '/api/assessments',
    // Add other API endpoints
];

// Install event - cache resources
self.addEventListener('install', event => {
    console.log('SOULFRIEND SW: Installing...');
    
    event.waitUntil(
        Promise.all([
            // Cache static resources
            caches.open(CACHE_NAME).then(cache => {
                return cache.addAll(STATIC_RESOURCES);
            }),
            // Initialize API cache
            caches.open(API_CACHE_NAME)
        ]).then(() => {
            console.log('SOULFRIEND SW: Installed successfully');
            return self.skipWaiting();
        })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('SOULFRIEND SW: Activating...');
    
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME && cacheName !== API_CACHE_NAME) {
                        console.log('SOULFRIEND SW: Deleting old cache', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log('SOULFRIEND SW: Activated');
            return self.clients.claim();
        })
    );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', event => {
    const request = event.request;
    const url = new URL(request.url);
    
    // Handle API requests
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(handleApiRequest(request));
        return;
    }
    
    // Handle static resources
    if (request.method === 'GET') {
        event.respondWith(handleStaticRequest(request));
    }
});

// Handle API requests with cache-first strategy for assessments
async function handleApiRequest(request) {
    const cache = await caches.open(API_CACHE_NAME);
    
    try {
        // Try network first
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            // Cache successful responses
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.log('SOULFRIEND SW: Network failed, trying cache', error);
        
        // Fall back to cache
        const cachedResponse = await cache.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Return offline message for API calls
        return new Response(
            JSON.stringify({
                error: 'Offline',
                message: 'Bạn đang offline. Một số tính năng có thể không khả dụng.'
            }),
            {
                status: 503,
                statusText: 'Service Unavailable',
                headers: { 'Content-Type': 'application/json' }
            }
        );
    }
}

// Handle static requests with cache-first strategy
async function handleStaticRequest(request) {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
        return cachedResponse;
    }
    
    try {
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.log('SOULFRIEND SW: Failed to fetch', request.url, error);
        
        // Return offline page for navigation requests
        if (request.mode === 'navigate') {
            return caches.match('/offline.html') || new Response(
                '<h1>Offline</h1><p>Bạn đang offline. Vui lòng kiểm tra kết nối mạng.</p>',
                { headers: { 'Content-Type': 'text/html' } }
            );
        }
        
        throw error;
    }
}

// Background sync for assessment submissions
self.addEventListener('sync', event => {
    console.log('SOULFRIEND SW: Background sync', event.tag);
    
    if (event.tag === 'assessment-submission') {
        event.waitUntil(syncAssessmentSubmissions());
    }
});

// Sync pending assessment submissions when online
async function syncAssessmentSubmissions() {
    try {
        // Get pending submissions from IndexedDB or localStorage
        const pendingSubmissions = await getPendingSubmissions();
        
        for (const submission of pendingSubmissions) {
            try {
                const response = await fetch('/api/assessments', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(submission.data)
                });
                
                if (response.ok) {
                    await removePendingSubmission(submission.id);
                    console.log('SOULFRIEND SW: Synced assessment', submission.id);
                }
            } catch (error) {
                console.log('SOULFRIEND SW: Failed to sync assessment', submission.id, error);
            }
        }
    } catch (error) {
        console.log('SOULFRIEND SW: Background sync failed', error);
    }
}

// Placeholder functions for offline data management
async function getPendingSubmissions() {
    // Implementation would use IndexedDB to store offline submissions
    return [];
}

async function removePendingSubmission(id) {
    // Implementation would remove synced submission from IndexedDB
    console.log('Removing synced submission', id);
}

// Push notification handling
self.addEventListener('push', event => {
    console.log('SOULFRIEND SW: Push notification received');
    
    if (!event.data) {
        return;
    }
    
    const data = event.data.json();
    const options = {
        body: data.body || 'SOULFRIEND notification',
        icon: '/static/icon-192.png',
        badge: '/static/icon-96.png',
        tag: data.tag || 'soulfriend-notification',
        requireInteraction: data.requireInteraction || false,
        actions: data.actions || [],
        data: data.data || {}
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title || 'SOULFRIEND', options)
    );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
    console.log('SOULFRIEND SW: Notification clicked', event.notification.tag);
    
    event.notification.close();
    
    const urlToOpen = event.notification.data?.url || '/';
    
    event.waitUntil(
        self.clients.matchAll({ type: 'window' }).then(clients => {
            // Check if app is already open
            for (const client of clients) {
                if (client.url === urlToOpen && 'focus' in client) {
                    return client.focus();
                }
            }
            
            // Open new window
            if (self.clients.openWindow) {
                return self.clients.openWindow(urlToOpen);
            }
        })
    );
});

console.log('SOULFRIEND Service Worker v2.0 loaded');
'''
        
        # Save service worker
        with open(self.sw_path, 'w', encoding='utf-8') as f:
            f.write(sw_content)
        
        return sw_content
    
    def generate_mobile_css(self) -> str:
        """Generate mobile-optimized CSS"""
        mobile_css = '''
/* SOULFRIEND Mobile Optimization CSS */

/* Base mobile styles */
@media screen and (max-width: 768px) {
    .main .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* Mobile header */
    .mobile-header {
        position: sticky;
        top: 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        z-index: 1000;
        border-radius: 0 0 10px 10px;
        margin-bottom: 1rem;
    }
    
    .mobile-header h1 {
        font-size: 1.5rem;
        margin: 0;
        text-align: center;
    }
    
    /* Mobile navigation */
    .mobile-nav {
        display: flex;
        justify-content: space-around;
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .mobile-nav-item {
        flex: 1;
        text-align: center;
        padding: 0.5rem;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    
    .mobile-nav-item:hover {
        background-color: #e9ecef;
    }
    
    .mobile-nav-item.active {
        background-color: #667eea;
        color: white;
    }
    
    /* Mobile questionnaire styles */
    .mobile-question-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: none;
    }
    
    .mobile-question-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        line-height: 1.4;
    }
    
    /* Mobile radio buttons */
    .mobile-radio-group {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .mobile-radio-item {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .mobile-radio-item:hover {
        border-color: #667eea;
        background-color: #f8f9ff;
    }
    
    .mobile-radio-item.selected {
        border-color: #667eea;
        background-color: #667eea;
        color: white;
    }
    
    /* Mobile buttons */
    .mobile-button {
        width: 100%;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
        margin: 0.5rem 0;
    }
    
    .mobile-button-primary {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .mobile-button-secondary {
        background: #f8f9fa;
        color: #6c757d;
        border: 2px solid #e9ecef;
    }
    
    .mobile-button:active {
        transform: translateY(1px);
    }
    
    /* Mobile results */
    .mobile-result-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .mobile-score-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-size: 2rem;
        font-weight: bold;
        color: white;
    }
    
    .score-low { background: linear-gradient(135deg, #2ecc71, #27ae60); }
    .score-mild { background: linear-gradient(135deg, #f39c12, #e67e22); }
    .score-moderate { background: linear-gradient(135deg, #e74c3c, #c0392b); }
    .score-severe { background: linear-gradient(135deg, #8e44ad, #71368a); }
    
    /* Mobile accessibility */
    .mobile-accessibility {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1001;
    }
    
    .accessibility-button {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #667eea;
        color: white;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        font-size: 1.2rem;
    }
    
    /* Touch-friendly spacing */
    .touchable {
        min-height: 44px;
        min-width: 44px;
    }
    
    /* Mobile typography */
    body {
        font-size: 16px;
        line-height: 1.5;
    }
    
    h1 { font-size: 1.8rem; }
    h2 { font-size: 1.5rem; }
    h3 { font-size: 1.3rem; }
    
    /* Mobile forms */
    .mobile-form-group {
        margin-bottom: 1.5rem;
    }
    
    .mobile-input {
        width: 100%;
        padding: 1rem;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        font-size: 1rem;
        transition: border-color 0.3s;
    }
    
    .mobile-input:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Mobile progress indicator */
    .mobile-progress {
        background: #e9ecef;
        height: 8px;
        border-radius: 4px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .mobile-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
    }
    
    /* Mobile modal */
    .mobile-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 2000;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
    }
    
    .mobile-modal-content {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        max-width: 90vw;
        max-height: 80vh;
        overflow-y: auto;
    }
}

/* PWA install prompt */
.pwa-install-prompt {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #667eea;
    color: white;
    padding: 1rem;
    transform: translateY(100%);
    transition: transform 0.3s;
    z-index: 1000;
}

.pwa-install-prompt.show {
    transform: translateY(0);
}

.pwa-install-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 600px;
    margin: 0 auto;
}

.pwa-install-text {
    flex: 1;
    margin-right: 1rem;
}

.pwa-install-buttons {
    display: flex;
    gap: 0.5rem;
}

.pwa-install-button {
    padding: 0.5rem 1rem;
    border: 2px solid white;
    background: transparent;
    color: white;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 600;
}

.pwa-install-button.primary {
    background: white;
    color: #667eea;
}

/* Offline indicator */
.offline-indicator {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: #e74c3c;
    color: white;
    text-align: center;
    padding: 0.5rem;
    transform: translateY(-100%);
    transition: transform 0.3s;
    z-index: 1001;
}

.offline-indicator.show {
    transform: translateY(0);
}
'''
        
        css_path = "/workspaces/Mentalhealth/static/mobile.css"
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(mobile_css)
        
        return mobile_css
    
    def generate_pwa_integration_code(self) -> str:
        """Generate JavaScript code for PWA integration"""
        pwa_js = '''
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
'''
        
        js_path = "/workspaces/Mentalhealth/static/pwa.js"
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(pwa_js)
        
        return pwa_js

def generate_pwa_files():
    """Generate all PWA files"""
    pwa_generator = PWAGenerator()
    
    print("🔧 Generating PWA files...")
    
    # Generate manifest
    manifest = pwa_generator.generate_manifest()
    print("✅ Generated manifest.json")
    
    # Generate service worker
    sw_content = pwa_generator.generate_service_worker()
    print("✅ Generated service worker")
    
    # Generate mobile CSS
    mobile_css = pwa_generator.generate_mobile_css()
    print("✅ Generated mobile CSS")
    
    # Generate PWA integration JS
    pwa_js = pwa_generator.generate_pwa_integration_code()
    print("✅ Generated PWA integration JavaScript")
    
    return {
        "manifest": manifest,
        "service_worker": sw_content,
        "mobile_css": mobile_css,
        "pwa_js": pwa_js
    }

if __name__ == "__main__":
    # Generate PWA files
    pwa_files = generate_pwa_files()
    
    print("\n📱 PWA Generation Complete!")
    print("=" * 40)
    print("✅ manifest.json")
    print("✅ sw.js (Service Worker)")
    print("✅ mobile.css") 
    print("✅ pwa.js")
    print("\n🚀 SOULFRIEND is now PWA-ready!")
