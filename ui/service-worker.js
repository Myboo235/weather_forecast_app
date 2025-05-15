const cacheName = "v1";

// Call Install Event
self.addEventListener("install", (e) => {
  console.log("Service Worker Installed");

  // e.waitUntil(
  //   caches
  //     .open(cacheName)
  //     .then(cache => {
  //       console.log("Service Worker Caching Files");
  //       cache.addAll(cacheAssets)
  //     })
  //     .then(() => self.skipWaiting())
  // );
})


// Call Activate Event
self.addEventListener("activate", (e) => {
  console.log("Service Worker Activated");

  // Remove old cache
  e.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if(cache !== cacheName){
            console.log("Service Worker Clear Old Cache");
            return caches.delete(cache)
          }
        })
      )
    })
  )
})

self.addEventListener("fetch", e => {
  console.log("Service Worker Fetching");

  e.respondWith(
    fetch(e.request)
      .then(res => {
        // Make a clone of response
        const resClone = res.clone();
        caches
        .open(cacheName)
        .then(cache => {
          console.log("Service Worker Caching Files");
          cache.put(e.request, resClone);
        })

        return res
      })
      .catch(() => caches.match(e.request).then(res => res))
  )
})