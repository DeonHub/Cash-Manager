const STATIC_CACHE_NAME = 'cash_manager_static__v1';
const DYNAMIC_CACHE_NAME = 'cash_manager_dynamic__v1';
const ASSETS = []; // DYNAMICALLY GENERATED IN PYTHON VIEW
const UNCACHEABLE_URLS = []; // DYNAMICALLY GENERATED IN PYTHON VIEW

//cache size limit function
const LIMIT_CACHE_SIZE = (name, size) => {
    caches.open(name).then(cache => {
        cache.keys().then(keys => {
            if (keys.length > size) {
                cache.delete(keys[0]).then(LIMIT_CACHE_SIZE(name, size));
            }
        });
    });
}
self.addEventListener('install', event => {
    // console.log('sw installed');
    const filesUpdate = cache => {
        const stack = [];
        // console.log('caching shell assets', cache);
        // console.log({ "ASSETS": ASSETS });
        ASSETS.forEach(file => stack.push(
            cache.add(file).catch(_ => console.error(`can't load ${file} to cache`))
        ));
        return Promise.all(stack);
    };

    event.waitUntil(caches.open(STATIC_CACHE_NAME).then(filesUpdate));
    self.skipWaiting();
});

//activate service worker.
self.addEventListener('activate', event => {
    // console.log('sw activated'); 
    event.waitUntil(
        caches.keys().then(keys => {
            console.log({ keys });
            return Promise.all(keys
                    .filter(key => key !== STATIC_CACHE_NAME && key !== DYNAMIC_CACHE_NAME)
                    .map(key => caches.delete(key))
                )
        })
    )
});

//fetch event
self.addEventListener('fetch', event => {
    let allowCache = true;
    for (const uUrl of UNCACHEABLE_URLS) {
        if (event.request.url.indexOf(uUrl) === 0) {
            allowCache = false;
        }
    }
    if (!allowCache) return;
    if (!(event.request.url.indexOf('http://') === 0)) return;
    if ((event.request.url.indexOf("api.") < 0) && (event.request.url.indexOf("db-api-v2.") < 0) && (event.request.url.indexOf("/api/") < 0)) {
        if (event.request.url.indexOf("/login") > -1) {
            null;
        } else {
            event.respondWith(
                caches.match(event.request).then(cacheResponse => {
                    return cacheResponse || fetch(event.request).then(fetchResponse => {
                        return caches.open(DYNAMIC_CACHE_NAME).then(cache => {
                            cache.put(event.request.url, fetchResponse.clone());
                            LIMIT_CACHE_SIZE(DYNAMIC_CACHE_NAME, 30)
                            return fetchResponse;
                        });
                    });
                }).catch(() => {
                    if (event.request.url.indexOf('.png') > -1) {
                        // return caches.match(ASSETS[2]);
                    } else if (event.request.url.indexOf('.jpg') > -1) {
                        // return caches.match(ASSETS[2]);
                    } else {
                        // when all fails revert to default html
                        return caches.match(ASSETS[2]);
                    }
                })
            );
        }
    }
});