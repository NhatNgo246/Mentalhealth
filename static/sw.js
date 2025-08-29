
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
