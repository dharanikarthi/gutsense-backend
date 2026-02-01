/**
 * Simplified Food Analysis API - Works without external dependencies
 * Provides mock analysis while we debug the Gemini integration
 */

export default async function handler(req, res) {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Handle preflight
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { image } = req.body;

        if (!image) {
            return res.status(400).json({ error: 'Image required' });
        }

        // Mock analysis - replace with Gemini when working
        const mockAnalysis = {
            name: "Indian Food Detected",
            category: "indian",
            confidence: 85,
            spiceLevel: 3,
            gutImpact: "medium",
            fermented: false,
            reaction: "caution",
            explanation: "This appears to be an Indian dish. The spices and preparation method suggest moderate gut impact. Consider your spice tolerance.",
            alternatives: ["Plain rice", "Steamed vegetables", "Yogurt"],
            tips: ["Eat slowly", "Drink water", "Monitor your response"],
            nutritionalInfo: {
                calories: "200-400 per serving",
                fiber: "medium",
                probiotics: false,
                inflammatory: false
            },
            recognitionMethod: "mock_analysis",
            timestamp: new Date().toISOString(),
            note: "This is a mock response while Gemini integration is being configured"
        };

        return res.status(200).json(mockAnalysis);

    } catch (error) {
        return res.status(500).json({
            error: 'Analysis failed',
            message: error.message,
            timestamp: new Date().toISOString()
        });
    }
}