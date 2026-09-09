var C='nxv1';
self.addEventListener('install',function(e){self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(clients.claim());});
self.addEventListener('fetch',function(e){if(e.request.method!=='GET'||e.request.url.indexOf(self.location.origin)!==0)return;e.respondWith(caches.open(C).then(function(c){return c.match(e.request).then(function(r){return r||fetch(e.request).then(function(n){c.put(e.request,n.clone());return n;});});}));});
