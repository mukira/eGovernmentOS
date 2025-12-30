// POLYFILL FOR BROWSEROS API
(function () {
    if (typeof chrome === 'undefined') return;

    // Ensure chrome.browserOS exists
    if (!chrome.browserOS) {
        chrome.browserOS = {};
    }

    console.log("[Polyfill] Initializing eGovernmentOS Polyfill...");

    // Mock getVersionNumber
    chrome.browserOS.getVersionNumber = function (callback) {
        console.log("[Polyfill] getVersionNumber called");
        if (callback) callback("0.0.0.35");
    };

    // Mock getBrowserosVersionNumber
    chrome.browserOS.getBrowserosVersionNumber = function (callback) {
        console.log("[Polyfill] getBrowserosVersionNumber called");
        if (callback) callback("0.0.0.35");
    };

    // Specific mock for getPref
    const originalGetPref = chrome.browserOS.getPref;
    chrome.browserOS.getPref = function (prefName, callback) {
        console.log("[Polyfill] getPref called for:", prefName);

        if (prefName === "browseros.server.agent_port") {
            if (callback) callback({ value: 9200 }); // Specialist Port (DEFAULT)
            return;
        }
        if (prefName === "browseros.server.mcp_port") {
            if (callback) callback({ value: 9100 }); // MCP Port (DEFAULT)
            return;
        }
        if (prefName === "browseros.server.extension_port") {
            if (callback) callback({ value: 9300 }); // Controller Port (DEFAULT)
            return;
        }
        if (prefName === "browseros.server.allow_remote_in_mcp") {
            if (callback) callback({ value: true });
            return;
        }

        // Fallback to original if available, otherwise return null
        if (originalGetPref) {
            originalGetPref(prefName, callback);
        } else {
            if (callback) callback(null);
        }
    };

    // Robust Mock Creator
    function forceOverwrite(methodName, mockFn) {
        try {
            // Try simple assignment first
            chrome.browserOS[methodName] = mockFn;

            // Verify if it stuck
            if (chrome.browserOS[methodName] !== mockFn) {
                console.warn(`[Polyfill] Simple assignment failed for ${methodName}, trying defineProperty`);
                Object.defineProperty(chrome.browserOS, methodName, {
                    value: mockFn,
                    writable: true,
                    configurable: true,
                    enumerable: true
                });
            }
            console.log(`[Polyfill] Successfully mocked ${methodName}`);
        } catch (e) {
            console.error(`[Polyfill] Failed to overwrite ${methodName}:`, e);
        }
    }

    // Mock methods with proper return values
    const mockReturnValues = {
        getInteractiveSnapshot: { elements: [] },
        getPageLoadStatus: {
            isResourcesLoading: false,
            isDOMContentLoaded: true,
            isPageComplete: true
        },
        getAccessibilityTree: { nodes: [] },
        captureScreenshot: "data:image/png;base64,",
        getSnapshot: { text: "", links: [] },
        executeJavaScript: undefined,
        getAllPrefs: []
    };

    const mockMethods = [
        'getInteractiveSnapshot', 'click', 'inputText', 'clear', 'scrollToNode',
        'sendKeys', 'getPageLoadStatus', 'getAccessibilityTree', 'captureScreenshot',
        'getSnapshot', 'logMetric', 'executeJavaScript', 'clickCoordinates',
        'typeAtCoordinates', 'setPref', 'getAllPrefs'
    ];

    mockMethods.forEach(method => {
        forceOverwrite(method, function (...args) {
            console.log(`[Polyfill] chrome.browserOS.${method} called`, args);
            // Execute callback if last arg is function
            const lastArg = args[args.length - 1];
            if (typeof lastArg === 'function') {
                const returnValue = mockReturnValues[method] !== undefined
                    ? mockReturnValues[method]
                    : undefined;
                lastArg(returnValue);
            }
        });
    });

    // Mock chrome.topSites.get if missing (for New Tab Page)
    if (!chrome.topSites) {
        chrome.topSites = {};
    }
    if (!chrome.topSites.get) {
        chrome.topSites.get = function (callback) {
            console.log("[Polyfill] chrome.topSites.get called");
            if (callback) {
                callback([]);
                return;
            }
            return Promise.resolve([]);
        };
    }

    // Mock sidePanel.browserosToggle
    if (chrome.sidePanel && !chrome.sidePanel.browserosToggle) {
        chrome.sidePanel.browserosToggle = async function (args) {
            console.log("[Polyfill] chrome.sidePanel.browserosToggle called", args);
            try {
                if (args && args.tabId) {
                    await chrome.sidePanel.open({ tabId: args.tabId });
                } else {
                    const window = await chrome.windows.getLastFocused();
                    await chrome.sidePanel.open({ windowId: window.id });
                }
            } catch (e) {
                console.error("[Polyfill] Failed to toggle side panel", e);
            }
        };
    }

    // Mock sidePanel.browserosIsOpen
    if (chrome.sidePanel && !chrome.sidePanel.browserosIsOpen) {
        chrome.sidePanel.browserosIsOpen = async function () { return false; };
    }

})();
