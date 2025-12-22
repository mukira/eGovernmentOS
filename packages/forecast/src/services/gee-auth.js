export class GEEAuthService {
    constructor() {
        this.token = null;
    }

    async getAuthToken(interactive = false) {
        return new Promise((resolve, reject) => {
            chrome.identity.getAuthToken({ interactive: interactive }, (token) => {
                if (chrome.runtime.lastError) {
                    // Start interactive flow if non-interactive fails and interactive was requested
                    if (interactive && !this.token) {
                        console.log("Interactive auth required.");
                    }
                    console.warn("Auth Error:", chrome.runtime.lastError);
                    resolve(null);
                } else {
                    this.token = token;
                    resolve(token);
                }
            });
        });
    }

    async removeCachedToken(token) {
        return new Promise((resolve) => {
            chrome.identity.removeCachedAuthToken({ token: token }, () => {
                this.token = null;
                resolve();
            });
        });
    }

    isAuthenticated() {
        return !!this.token;
    }
}
