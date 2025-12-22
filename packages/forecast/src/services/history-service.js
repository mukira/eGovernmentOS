import { GEEAuthService } from './gee-auth.js';

// Firestore REST API Endpoint
const PROJECT_ID = '50302662170'; // Extracted from user's API Key details image
const BASE_URL = `https://firestore.googleapis.com/v1/projects/${PROJECT_ID}/databases/(default)/documents/briefs`;

export class HistoryService {
    constructor() {
        this.authService = new GEEAuthService();
    }

    async saveBrief(region, content, stats) {
        const token = await this.authService.getAuthToken(false);
        if (!token) {
            console.log("Dev Mode: No Auth Token available. Skipping history save.");
            return;
        }

        const doc = {
            fields: {
                region: { stringValue: region },
                content: { stringValue: content },
                timestamp: { timestampValue: new Date().toISOString() },
                ndvi: { doubleValue: stats.ndvi },
                flood_risk: { integerValue: stats.flood_risk }
            }
        };

        try {
            const response = await fetch(BASE_URL, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(doc)
            });

            if (response.ok) {
                console.log("Brief saved to Firestore!");
            } else {
                console.error("Firestore Save Error:", await response.text());
            }
        } catch (error) {
            console.error("Firestore Network Error:", error);
        }
    }

    async getHistory() {
        const token = await this.authService.getAuthToken(false);
        if (!token) return [];

        try {
            const response = await fetch(BASE_URL, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                return data.documents ? data.documents.map(this._formatDoc) : [];
            }
        } catch (error) {
            console.error("Error fetching history:", error);
        }
        return [];
    }

    _formatDoc(doc) {
        const fields = doc.fields;
        return {
            id: doc.name.split('/').pop(),
            region: fields.region.stringValue,
            content: fields.content.stringValue,
            date: new Date(fields.timestamp.timestampValue).toLocaleString()
        };
    }
}
