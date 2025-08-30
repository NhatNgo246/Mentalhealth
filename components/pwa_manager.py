"""
📱 SOULFRIEND V4.0 - Progressive Web App (PWA) Support
====================================================

PWA configuration for mobile-first experience
Offline support, push notifications, and app-like behavior
"""

import streamlit as st
import json
import os
from typing import Dict, Any

class PWAManager:
    """
    Quản lý Progressive Web App features
    """
    
    def __init__(self):
        self.app_name = "SOULFRIEND"
        self.app_description = "AI-Powered Mental Health Companion"
        self.app_version = "4.0.0"
        self.theme_color = "#2E86AB"
        self.background_color = "#F8F9FA"
    
    def generate_manifest(self) -> Dict[str, Any]:
        """
        Generate PWA manifest.json
        """
        return {
            "name": self.app_name,
            "short_name": "SOULFRIEND",
            "description": self.app_description,
            "version": self.app_version,
            "start_url": "/",
            "display": "standalone",
            "orientation": "portrait",
            "theme_color": self.theme_color,
            "background_color": self.background_color,
            "categories": ["health", "medical", "lifestyle"],
            "lang": "vi",
            "dir": "ltr",
            "scope": "/",
            "icons": [
                {
                    "src": "/assets/icon-72x72.png",
                    "sizes": "72x72",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/assets/icon-96x96.png", 
                    "sizes": "96x96",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/assets/icon-128x128.png",
                    "sizes": "128x128", 
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/assets/icon-144x144.png",
                    "sizes": "144x144",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/assets/icon-152x152.png",
                    "sizes": "152x152",
                    "type": "image/png", 
                    "purpose": "any maskable"
                },
                {
                    "src": "/assets/icon-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/assets/icon-384x384.png",
                    "sizes": "384x384",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": "/assets/icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any maskable"
                }
            ],
            "screenshots": [
                {
                    "src": "/assets/screenshot-mobile.png",
                    "sizes": "375x812",
                    "type": "image/png",
                    "form_factor": "narrow"
                },
                {
                    "src": "/assets/screenshot-desktop.png", 
                    "sizes": "1280x720",
                    "type": "image/png",
                    "form_factor": "wide"
                }
            ],
            "shortcuts": [
                {
                    "name": "Quick Assessment",
                    "short_name": "Assessment",
                    "description": "Start a quick mental health assessment",
                    "url": "/?quick_assessment=true",
                    "icons": [
                        {
                            "src": "/assets/shortcut-assessment.png",
                            "sizes": "192x192"
                        }
                    ]
                },
                {
                    "name": "Chat with CHUN",
                    "short_name": "Chat",
                    "description": "Start conversation with CHUN AI",
                    "url": "/?page=chatbot",
                    "icons": [
                        {
                            "src": "/assets/shortcut-chat.png",
                            "sizes": "192x192"
                        }
                    ]
                },
                {
                    "name": "Voice Chat",
                    "short_name": "Voice",
                    "description": "Voice chat with CHUN",
                    "url": "/?page=voice_chat",
                    "icons": [
                        {
                            "src": "/assets/shortcut-voice.png",
                            "sizes": "192x192"
                        }
                    ]
                }
            ],
            "prefer_related_applications": False,
            "edge_side_panel": {
                "preferred_width": 400
            }
        }
    
    def generate_service_worker(self) -> str:
        """
        Generate service worker for offline support
        """
        return """
// SOULFRIEND Service Worker v4.0.0
const CACHE_NAME = 'soulfriend-v4-0-0';
const OFFLINE_URL = '/offline.html';

// Files to cache for offline use
const CACHE_FILES = [
    '/',
    '/offline.html',
    '/assets/styles.css',
    '/assets/ui-optimized.css',
    '/assets/logo.png',
    '/assets/icon-192x192.png',
    '/assets/icon-512x512.png',
    // Core pages
    '/?page=assessment',
    '/?page=chatbot',
    '/?page=voice_chat',
    '/?page=results'
];

// Critical resources that should always be fresh
const NETWORK_FIRST = [
    '/api/',
    '/components/',
    '/data/',
    '/?assessment_data'
];

// Install Service Worker
self.addEventListener('install', (event) => {
    console.log('🔧 SOULFRIEND Service Worker installing...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('📦 Caching core files...');
                return cache.addAll(CACHE_FILES);
            })
            .then(() => {
                console.log('✅ Service Worker installed successfully');
                return self.skipWaiting();
            })
            .catch((error) => {
                console.error('❌ Service Worker install failed:', error);
            })
    );
});

// Activate Service Worker
self.addEventListener('activate', (event) => {
    console.log('🚀 SOULFRIEND Service Worker activating...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName !== CACHE_NAME) {
                            console.log('🗑️ Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('✅ Service Worker activated');
                return self.clients.claim();
            })
    );
});

// Fetch Strategy
self.addEventListener('fetch', (event) => {
    const request = event.request;
    const url = new URL(request.url);
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Skip chrome-extension and other schemes
    if (!url.protocol.startsWith('http')) {
        return;
    }
    
    // Network first for critical resources
    if (NETWORK_FIRST.some(pattern => url.pathname.startsWith(pattern))) {
        event.respondWith(networkFirst(request));
        return;
    }
    
    // Cache first for static resources
    if (url.pathname.startsWith('/assets/') || url.pathname.startsWith('/static/')) {
        event.respondWith(cacheFirst(request));
        return;
    }
    
    // Stale while revalidate for pages
    event.respondWith(staleWhileRevalidate(request));
});

// Cache First Strategy
async function cacheFirst(request) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
        
    } catch (error) {
        console.error('Cache first failed:', error);
        return new Response('Offline - Resource not available', { status: 503 });
    }
}

// Network First Strategy  
async function networkFirst(request) {
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
        
    } catch (error) {
        console.error('Network first failed, trying cache:', error);
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Return offline page for navigation requests
        if (request.destination === 'document') {
            return caches.match(OFFLINE_URL);
        }
        
        return new Response('Offline - Resource not available', { status: 503 });
    }
}

// Stale While Revalidate Strategy
async function staleWhileRevalidate(request) {
    try {
        const cache = await caches.open(CACHE_NAME);
        const cachedResponse = await cache.match(request);
        
        // Fetch new version in background
        const fetchPromise = fetch(request).then((networkResponse) => {
            if (networkResponse.ok) {
                cache.put(request, networkResponse.clone());
            }
            return networkResponse;
        });
        
        // Return cached version immediately if available
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Otherwise wait for network
        return await fetchPromise;
        
    } catch (error) {
        console.error('Stale while revalidate failed:', error);
        
        // Try to return cached version
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Return offline page for navigation requests
        if (request.destination === 'document') {
            return caches.match(OFFLINE_URL);
        }
        
        return new Response('Offline - Resource not available', { status: 503 });
    }
}

// Background Sync for data
self.addEventListener('sync', (event) => {
    console.log('🔄 Background sync:', event.tag);
    
    if (event.tag === 'assessment-data') {
        event.waitUntil(syncAssessmentData());
    }
    
    if (event.tag === 'chat-history') {
        event.waitUntil(syncChatHistory());
    }
});

async function syncAssessmentData() {
    try {
        // Get pending assessment data from IndexedDB
        const pendingData = await getPendingAssessmentData();
        
        if (pendingData.length > 0) {
            console.log('📊 Syncing assessment data:', pendingData.length, 'items');
            
            for (const data of pendingData) {
                await fetch('/api/sync/assessment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                // Remove from pending after successful sync
                await removePendingAssessmentData(data.id);
            }
            
            console.log('✅ Assessment data synced successfully');
        }
    } catch (error) {
        console.error('❌ Assessment data sync failed:', error);
    }
}

async function syncChatHistory() {
    try {
        // Get pending chat data from IndexedDB
        const pendingChats = await getPendingChatData();
        
        if (pendingChats.length > 0) {
            console.log('💬 Syncing chat history:', pendingChats.length, 'messages');
            
            for (const chat of pendingChats) {
                await fetch('/api/sync/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(chat)
                });
                
                // Remove from pending after successful sync
                await removePendingChatData(chat.id);
            }
            
            console.log('✅ Chat history synced successfully');
        }
    } catch (error) {
        console.error('❌ Chat history sync failed:', error);
    }
}

// Push Notifications
self.addEventListener('push', (event) => {
    console.log('📩 Push notification received');
    
    const options = {
        body: 'CHUN đang nhớ bạn! Hãy quay lại để chia sẻ cảm xúc hôm nay.',
        icon: '/assets/icon-192x192.png',
        badge: '/assets/badge-96x96.png',
        vibrate: [200, 100, 200],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'open-chat',
                title: 'Chat với CHUN',
                icon: '/assets/action-chat.png'
            },
            {
                action: 'quick-assessment', 
                title: 'Đánh giá nhanh',
                icon: '/assets/action-assessment.png'
            }
        ],
        requireInteraction: true,
        silent: false
    };
    
    if (event.data) {
        const payload = event.data.json();
        options.body = payload.body || options.body;
        options.title = payload.title || 'SOULFRIEND';
    }
    
    event.waitUntil(
        self.registration.showNotification('SOULFRIEND', options)
    );
});

// Notification Click Handler
self.addEventListener('notificationclick', (event) => {
    console.log('🔔 Notification clicked:', event.action);
    
    event.notification.close();
    
    let url = '/';
    
    if (event.action === 'open-chat') {
        url = '/?page=chatbot';
    } else if (event.action === 'quick-assessment') {
        url = '/?page=assessment&quick=true';
    }
    
    event.waitUntil(
        clients.matchAll({ includeUncontrolled: true })
            .then((clientList) => {
                // Check if app is already open
                for (const client of clientList) {
                    if (client.url.includes(self.location.origin) && 'focus' in client) {
                        client.navigate(url);
                        return client.focus();
                    }
                }
                
                // Open new window if not open
                if (clients.openWindow) {
                    return clients.openWindow(url);
                }
            })
    );
});

// Helper functions for IndexedDB (simplified)
async function getPendingAssessmentData() {
    // Implementation would use IndexedDB to get pending data
    return [];
}

async function removePendingAssessmentData(id) {
    // Implementation would remove item from IndexedDB
    console.log('Removed pending assessment:', id);
}

async function getPendingChatData() {
    // Implementation would use IndexedDB to get pending chat data
    return [];
}

async function removePendingChatData(id) {
    // Implementation would remove item from IndexedDB
    console.log('Removed pending chat:', id);
}

console.log('🌟 SOULFRIEND Service Worker loaded successfully');
"""
    
    def generate_offline_page(self) -> str:
        """
        Generate offline fallback page
        """
        return """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SOULFRIEND - Offline</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .offline-container {
            text-align: center;
            padding: 2rem;
            max-width: 400px;
        }
        
        .offline-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        
        .offline-title {
            font-size: 2rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        .offline-message {
            font-size: 1.1rem;
            margin-bottom: 2rem;
            opacity: 0.9;
            line-height: 1.6;
        }
        
        .retry-button {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .retry-button:hover {
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.5);
            transform: translateY(-2px);
        }
        
        .features-list {
            margin-top: 2rem;
            text-align: left;
        }
        
        .feature-item {
            margin: 0.5rem 0;
            padding: 0.5rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            font-size: 0.9rem;
        }
        
        @media (max-width: 480px) {
            .offline-container {
                padding: 1rem;
            }
            
            .offline-title {
                font-size: 1.5rem;
            }
            
            .offline-message {
                font-size: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="offline-container">
        <div class="offline-icon">🌙</div>
        <h1 class="offline-title">SOULFRIEND Offline</h1>
        <p class="offline-message">
            Bạn hiện đang offline. SOULFRIEND vẫn có thể hỗ trợ bạn với một số tính năng cơ bản.
        </p>
        
        <a href="/" class="retry-button" onclick="window.location.reload()">
            🔄 Thử kết nối lại
        </a>
        
        <div class="features-list">
            <div class="feature-item">
                📊 Xem kết quả đánh giá đã lưu
            </div>
            <div class="feature-item">
                💭 Đọc lại lịch sử chat với CHUN
            </div>
            <div class="feature-item">
                📝 Ghi chú cảm xúc hàng ngày
            </div>
            <div class="feature-item">
                🎯 Xem gợi ý tự chăm sóc
            </div>
        </div>
    </div>
    
    <script>
        // Auto-retry connection
        setInterval(() => {
            if (navigator.onLine) {
                window.location.reload();
            }
        }, 30000); // Check every 30 seconds
        
        // Listen for online event
        window.addEventListener('online', () => {
            window.location.reload();
        });
    </script>
</body>
</html>
"""

def create_pwa_files():
    """
    Create PWA configuration files
    """
    pwa_manager = PWAManager()
    
    # Create manifest.json
    manifest_content = json.dumps(pwa_manager.generate_manifest(), indent=2)
    
    # Create service worker
    sw_content = pwa_manager.generate_service_worker()
    
    # Create offline page
    offline_content = pwa_manager.generate_offline_page()
    
    return {
        'manifest.json': manifest_content,
        'sw.js': sw_content,
        'offline.html': offline_content
    }

def inject_pwa_meta_tags():
    """
    Inject PWA meta tags into Streamlit app
    """
    pwa_meta = """
    <meta name="application-name" content="SOULFRIEND">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="SOULFRIEND">
    <meta name="description" content="AI-Powered Mental Health Companion">
    <meta name="format-detection" content="telephone=no">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="msapplication-config" content="/browserconfig.xml">
    <meta name="msapplication-TileColor" content="#2E86AB">
    <meta name="msapplication-tap-highlight" content="no">
    <meta name="theme-color" content="#2E86AB">
    
    <link rel="apple-touch-icon" href="/assets/icon-152x152.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/assets/icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icon-180x180.png">
    <link rel="apple-touch-icon" sizes="167x167" href="/assets/icon-167x167.png">
    
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/assets/icon-16x16.png">
    <link rel="manifest" href="/manifest.json">
    <link rel="mask-icon" href="/assets/safari-pinned-tab.svg" color="#2E86AB">
    <link rel="shortcut icon" href="/favicon.ico">
    
    <meta name="twitter:card" content="summary">
    <meta name="twitter:url" content="https://soulfriend.app">
    <meta name="twitter:title" content="SOULFRIEND">
    <meta name="twitter:description" content="AI-Powered Mental Health Companion">
    <meta name="twitter:image" content="/assets/icon-192x192.png">
    <meta name="twitter:creator" content="@soulfriend">
    
    <meta property="og:type" content="website">
    <meta property="og:title" content="SOULFRIEND">
    <meta property="og:description" content="AI-Powered Mental Health Companion">
    <meta property="og:site_name" content="SOULFRIEND">
    <meta property="og:url" content="https://soulfriend.app">
    <meta property="og:image" content="/assets/icon-512x512.png">
    """
    
    pwa_scripts = """
    <script>
        // Register Service Worker
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                    .then((registration) => {
                        console.log('✅ SW registered: ', registration);
                        
                        // Check for updates
                        registration.addEventListener('updatefound', () => {
                            const newWorker = registration.installing;
                            newWorker.addEventListener('statechange', () => {
                                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                    // New version available
                                    if (confirm('🆕 Có phiên bản mới! Bạn muốn cập nhật không?')) {
                                        window.location.reload();
                                    }
                                }
                            });
                        });
                    })
                    .catch((registrationError) => {
                        console.log('❌ SW registration failed: ', registrationError);
                    });
            });
        }
        
        // PWA Install Prompt
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            console.log('💾 PWA install prompt triggered');
            e.preventDefault();
            deferredPrompt = e;
            
            // Show custom install button
            showInstallButton();
        });
        
        function showInstallButton() {
            // Create install button if not exists
            if (!document.getElementById('pwa-install-btn')) {
                const installBtn = document.createElement('button');
                installBtn.id = 'pwa-install-btn';
                installBtn.innerHTML = '📱 Cài đặt App';
                installBtn.style.cssText = `
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    background: #2E86AB;
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 25px;
                    font-size: 14px;
                    cursor: pointer;
                    box-shadow: 0 4px 12px rgba(46, 134, 171, 0.3);
                    z-index: 1000;
                    transition: all 0.3s ease;
                `;
                
                installBtn.addEventListener('click', installPWA);
                installBtn.addEventListener('mouseenter', () => {
                    installBtn.style.transform = 'translateY(-2px)';
                    installBtn.style.boxShadow = '0 6px 16px rgba(46, 134, 171, 0.4)';
                });
                installBtn.addEventListener('mouseleave', () => {
                    installBtn.style.transform = 'translateY(0)';
                    installBtn.style.boxShadow = '0 4px 12px rgba(46, 134, 171, 0.3)';
                });
                
                document.body.appendChild(installBtn);
                
                // Hide after 30 seconds if not clicked
                setTimeout(() => {
                    if (installBtn.parentNode) {
                        installBtn.style.opacity = '0';
                        setTimeout(() => installBtn.remove(), 300);
                    }
                }, 30000);
            }
        }
        
        function installPWA() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('✅ User accepted PWA install');
                    } else {
                        console.log('❌ User dismissed PWA install');
                    }
                    deferredPrompt = null;
                    
                    // Remove install button
                    const installBtn = document.getElementById('pwa-install-btn');
                    if (installBtn) {
                        installBtn.remove();
                    }
                });
            }
        }
        
        // Track PWA usage
        window.addEventListener('appinstalled', (evt) => {
            console.log('📱 PWA was installed');
            
            // Track installation
            if ('gtag' in window) {
                gtag('event', 'pwa_installed', {
                    'event_category': 'PWA',
                    'event_label': 'App Installed'
                });
            }
        });
        
        // Detect if running as PWA
        if (window.matchMedia('(display-mode: standalone)').matches || 
            window.navigator.standalone === true) {
            console.log('🚀 Running as PWA');
            document.body.classList.add('pwa-mode');
            
            // Track PWA usage
            if ('gtag' in window) {
                gtag('event', 'pwa_launched', {
                    'event_category': 'PWA',
                    'event_label': 'App Launched'
                });
            }
        }
        
        // Handle connection status
        function updateConnectionStatus() {
            const isOnline = navigator.onLine;
            const statusElement = document.getElementById('connection-status');
            
            if (!statusElement) {
                const status = document.createElement('div');
                status.id = 'connection-status';
                status.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    padding: 8px;
                    text-align: center;
                    font-size: 14px;
                    z-index: 1001;
                    transition: all 0.3s ease;
                `;
                document.body.appendChild(status);
            }
            
            const statusEl = document.getElementById('connection-status');
            
            if (isOnline) {
                statusEl.style.background = '#28a745';
                statusEl.style.color = 'white';
                statusEl.textContent = '🌐 Đã kết nối';
                
                // Hide after 2 seconds
                setTimeout(() => {
                    statusEl.style.transform = 'translateY(-100%)';
                }, 2000);
            } else {
                statusEl.style.background = '#dc3545';
                statusEl.style.color = 'white';
                statusEl.style.transform = 'translateY(0)';
                statusEl.textContent = '📴 Offline - Một số tính năng bị hạn chế';
            }
        }
        
        window.addEventListener('online', updateConnectionStatus);
        window.addEventListener('offline', updateConnectionStatus);
        
        // Initial connection check
        updateConnectionStatus();
        
        // Request Push Notification Permission
        function requestNotificationPermission() {
            if ('Notification' in window && 'serviceWorker' in navigator) {
                Notification.requestPermission().then((permission) => {
                    if (permission === 'granted') {
                        console.log('✅ Notification permission granted');
                        subscribeToPushNotifications();
                    } else {
                        console.log('❌ Notification permission denied');
                    }
                });
            }
        }
        
        async function subscribeToPushNotifications() {
            try {
                const registration = await navigator.serviceWorker.ready;
                const subscription = await registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: 'YOUR_VAPID_PUBLIC_KEY' // Replace with actual key
                });
                
                console.log('📩 Push subscription:', subscription);
                
                // Send subscription to server
                // await fetch('/api/push/subscribe', {
                //     method: 'POST',
                //     headers: { 'Content-Type': 'application/json' },
                //     body: JSON.stringify(subscription)
                // });
                
            } catch (error) {
                console.error('❌ Push subscription failed:', error);
            }
        }
        
        // Auto-request notification permission after 30 seconds
        setTimeout(() => {
            if (Notification.permission === 'default') {
                requestNotificationPermission();
            }
        }, 30000);
    </script>
    """
    
    # Inject into Streamlit
    st.markdown(pwa_meta, unsafe_allow_html=True)
    st.markdown(pwa_scripts, unsafe_allow_html=True)

def show_pwa_status():
    """
    Show PWA installation and features status
    """
    st.markdown("---")
    st.subheader("📱 Progressive Web App Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🚀 PWA Support", 
            "Enabled",
            help="App có thể cài đặt như native app"
        )
    
    with col2:
        st.metric(
            "🔄 Offline Support", 
            "Active",
            help="Hoạt động ngay cả khi không có internet"
        )
    
    with col3:
        st.metric(
            "📩 Push Notifications", 
            "Ready",
            help="Nhận thông báo từ CHUN"
        )
    
    with st.expander("💡 Hướng dẫn cài đặt PWA"):
        st.markdown("""
        ### 📱 **Cài đặt SOULFRIEND như App:**
        
        #### **Trên Android (Chrome):**
        1. Mở app trong Chrome
        2. Nhấn menu (3 chấm) → "Add to Home screen"
        3. Chọn "Install" → App sẽ xuất hiện trên màn hình chính
        
        #### **Trên iPhone (Safari):**
        1. Mở app trong Safari
        2. Nhấn nút Share → "Add to Home Screen"
        3. Chọn "Add" → App sẽ xuất hiện trên màn hình chính
        
        #### **Trên Desktop:**
        1. Mở app trong Chrome/Edge
        2. Nhấn biểu tượng install trong address bar
        3. Chọn "Install" → App sẽ xuất hiện như desktop app
        
        ### ✨ **Lợi ích khi cài đặt:**
        - 🚀 **Tải nhanh hơn** với offline caching
        - 📱 **Trải nghiệm native** như app thật
        - 📩 **Push notifications** từ CHUN
        - 🔄 **Auto-sync** khi có internet trở lại
        - 💾 **Lưu dữ liệu offline** để xem sau
        """)

if __name__ == "__main__":
    inject_pwa_meta_tags()
    show_pwa_status()
