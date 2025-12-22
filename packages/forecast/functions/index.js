const { VertexAI } = require('@google-cloud/vertexai');

// Initialize Vertex AI
const vertex_ai = new VertexAI({ project: process.env.GCP_PROJECT, location: 'us-central1' });
const model = 'gemini-1.5-flash-001';

// Cloud Run Function Entry Point
exports.generateBrief = async (req, res) => {
    // Enable CORS
    res.set('Access-Control-Allow-Origin', '*');
    if (req.method === 'OPTIONS') {
        res.set('Access-Control-Allow-Methods', 'POST');
        res.set('Access-Control-Allow-Headers', 'Content-Type');
        res.status(204).send('');
        return;
    }

    try {
        const { region, stats } = req.body;

        // Instantiate the model
        const generativeModel = vertex_ai.preview.getGenerativeModel({
            model: model,
            generationConfig: {
                'maxOutputTokens': 256,
                'temperature': 0.7,
            },
        });

        const prompt = `
      Role: Expert Kenyan Policy Analyst.
      Task: Write a concise, urgent 2-sentence brief for the Governor.
      Context: The user is looking at Earth Observation data for ${region}.
      Data: NDVI (Vegetation Health) is ${stats.ndvi}. Flood Risk is ${stats.flood_risk}%.
      
      Output format: A professional status update and a recommended action.
    `;

        const result = await generativeModel.generateContent(prompt);
        const response = await result.response;
        const text = response.candidates[0].content.parts[0].text;

        res.status(200).json({ brief: text });

    } catch (error) {
        console.error(error);
        res.status(500).send('Error generating brief');
    }
};
