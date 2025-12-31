import { GoogleGenerativeAI } from '@google/generative-ai';
// Note: @google/genai usually exports GoogleGenerativeAI from @google/generative-ai if it's a wrapper, 
// or allows direct use. But let's check imports.
// Wait, package.json has "@google/genai": "1.30.0". 
// The "google-generative-ai" is the package name for the older one.
// The new one is "@google/genai" (?) No, let's try the standard import which seems to be what Vercel SDK uses.
// Actually, let's use a simple fetch to the REST API to avoid SDK import issues in this standalone script.

const apiKey = process.env.GEMINI_API_KEY;
if (!apiKey) {
    console.error("No API key provided");
    process.exit(1);
}

const url = `https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`;

async function listModels() {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            const text = await response.text();
            throw new Error(`HTTP ${response.status}: ${text}`);
        }
        const data = await response.json();
        console.log("Available Models:");
        (data.models || []).forEach((m: any) => {
            if (m.name.includes('flash') || m.name.includes('gemini')) {
                console.log(`- ${m.name.replace('models/', '')} (${m.displayName})`);
            }
        });
    } catch (error) {
        console.error("Error listing models:", error);
    }
}

listModels();
