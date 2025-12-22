/**
 * dev-mocks.js
 * Mocks Chrome Extension APIs for Local Development
 */

if (!window.chrome) {
    window.chrome = {};
}

// 1. Mock chrome.runtime
if (!window.chrome.runtime) {
    window.chrome.runtime = {
        lastError: null,
        sendMessage: (message, callback) => {
            console.log('[Mock chrome.runtime.sendMessage]', message);
            if (callback) callback({ status: 'success', mocked: true });
        },
        onMessage: {
            addListener: (callback) => {
                console.log('[Mock chrome.runtime.onMessage] Listener added');
                // Could simulate incoming messages here if needed
            }
        },
        getURL: (path) => {
            return path; // Simple relative path for dev
        }
    };
}

// 2. Mock chrome.identity
if (!window.chrome.identity) {
    window.chrome.identity = {
        getAuthToken: ({ interactive }, callback) => {
            console.log(`[Mock chrome.identity.getAuthToken] Interactive: ${interactive}`);
            // Return null to trigger the "Simulated Fallback" in gee-service.js
            // Or return a dummy string if we wanted to test the "Authenticated" path (but fetch would fail)
            // For UI testing, the simulated path is often better.
            callback(null);
        },
        removeCachedAuthToken: ({ token }, callback) => {
            console.log('[Mock chrome.identity.removeCachedAuthToken]', token);
            if (callback) callback();
        }
    };
}

// 3. Mock chrome.storage.local
if (!window.chrome.storage) {
    window.chrome.storage = {};
}

if (!window.chrome.storage.local) {
    window.chrome.storage.local = {
        get: (keys, callback) => {
            console.log('[Mock chrome.storage.local.get]', keys);
            const result = {};
            const keyArray = Array.isArray(keys) ? keys : [keys];
            keyArray.forEach(k => {
                const val = localStorage.getItem(k);
                if (val) {
                    try {
                        result[k] = JSON.parse(val);
                    } catch (e) {
                        result[k] = val;
                    }
                }
            });
            if (callback) callback(result);
        },
        set: (items, callback) => {
            console.log('[Mock chrome.storage.local.set]', items);
            Object.keys(items).forEach(k => {
                localStorage.setItem(k, JSON.stringify(items[k]));
            });
            if (callback) callback();
        }
    };
}

console.log('✅ Chrome API Mocks Loaded');
