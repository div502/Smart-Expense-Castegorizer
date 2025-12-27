const CACHE_NAME = 'expense-tracker-v1';
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/dashboard/',
  '/add/',
  '/set-budget/',
  '/history/',
  'https://cdn.tailwindcss.com',
  'https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css',
  'https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js',
  'https://cdn.jsdelivr.net/npm/chart.js',
  'https://unpkg.com/aos@2.3.4/dist/aos.css',
  'https://unpkg.com/aos@2.3.4/dist/aos.js'
];

// Install event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      }
    )
  );
});

// Activate event
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Background sync for offline functionality
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

function doBackgroundSync() {
  // Handle offline data sync when connection is restored
  console.log('Background sync triggered');
}