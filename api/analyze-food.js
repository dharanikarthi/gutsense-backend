/**
 * Vercel Serverless Function for Food Analysis using Google Gemini
 * Securely processes food images and returns gut health analysis
 */

import { GoogleGenerativeAI } from '@google/generative-ai';

// Initialize Gemini AI with API key from environment
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

export default async function handler(req, res) {
    // Set CORS headers for frontend access
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Handle preflight OPTIONS request
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    // Only allow POST requests
    if (req.method !== 'POST') {
        return res.status(405).json({ 
            error: 'Method not allowed',
            message: 'Only POST requests are supported'
        });
    }

    try {
        // Validate API key exists
        if (!process.env.GEMINI_API_KEY) {
            console.error('❌ GEMINI_API_KEY not found in environment variables');
            return res.status(500).json({
                error: 'Configuration error',
                message: 'API key not configured'
            });
        }

        // Extract image data from request
        const { image, food_name } = req.body;

        if (!image) {
            return res.status(400).json({
                error: 'Bad request',
                message: 'Image data is required'
            });
        }

        console.log('🔍 Processing food analysis request...');

        // Get Gemini model
        const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });

        // Prepare the image for Gemini
        let imageData;
        if (image.startsWith('data:image/')) {
            // Remove data URL prefix
            const base64Data = image.split(',')[1];
            const mimeType = image.split(';')[0].split(':')[1];
            
            imageData = {
                inlineData: {
                    data: base64Data,
                    mimeType: mimeType
                }
            };
        } else {
            // Assume it's already base64
            imageData = {
                inlineData: {
                    data: image,
                    mimeType: "image/jpeg"
                }
            };
        }

        // Create detailed prompt for food analysis
        const prompt = `
You are a specialized AI nutritionist and gut health expert. Analyze this food image and provide a comprehensive gut health assessment.

TASK: Identify the food and provide detailed gut health analysis.

RESPONSE FORMAT (JSON only):
{
    "name": "Food Name",
    "category": "food_category",
    "confidence": 85,
    "spiceLevel": 3,
    "gutImpact": "low|medium|high|very_high",
    "fermented": true/false,
    "reaction": "excellent|suitable|caution|avoid",
    "explanation": "Detailed explanation of gut health impact",
    "alternatives": ["Alternative 1", "Alternative 2", "Alternative 3"],
    "tips": ["Tip 1", "Tip 2", "Tip 3"],
    "nutritionalInfo": {
        "calories": "estimated per serving",
        "fiber": "high|medium|low",
        "probiotics": true/false,
        "inflammatory": true/false
    },
    "recognitionMethod": "gemini_ai",
    "timestamp": "${new Date().toISOString()}"
}

ANALYSIS GUIDELINES:
1. FOOD IDENTIFICATION: Identify the specific food item(s) in the image
2. GUT HEALTH FOCUS: Prioritize digestive health impact
3. SPICE LEVEL: Rate 0-5 (0=no spice, 5=very spicy)
4. GUT IMPACT: Consider fiber, spices, oils, processing level
5. REACTION LEVELS:
   - excellent: Great for gut health (fermented foods, high fiber)
   - suitable: Generally okay with minor considerations
   - caution: May cause issues for sensitive individuals
   - avoid: Likely to cause digestive problems

6. PROVIDE PRACTICAL ALTERNATIVES and ACTIONABLE TIPS

Focus especially on Indian cuisine if detected. Consider fermentation, spice levels, oil content, and digestive complexity.

Return ONLY valid JSON, no additional text.
`;

        console.log('🧠 Sending request to Gemini AI...');

        // Generate content with Gemini
        const result = await model.generateContent([prompt, imageData]);
        const response = await result.response;
        const text = response.text();

        console.log('✅ Received response from Gemini');
        console.log('📝 Raw response:', text.substring(0, 200) + '...');

        // Parse JSON response
        let analysisData;
        try {
            // Clean the response (remove any markdown formatting)
            const cleanedText = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
            analysisData = JSON.parse(cleanedText);
        } catch (parseError) {
            console.error('❌ Failed to parse Gemini response as JSON:', parseError);
            console.log('Raw response:', text);
            
            // Fallback response if JSON parsing fails
            analysisData = {
                name: "Food Analysis",
                category: "unknown",
                confidence: 75,
                spiceLevel: 2,
                gutImpact: "medium",
                fermented: false,
                reaction: "caution",
                explanation: "AI analysis completed but response format needs adjustment. The food appears to be edible but please consult with a nutritionist for personalized advice.",
                alternatives: ["Steamed vegetables", "Plain rice", "Yogurt"],
                tips: ["Eat in moderation", "Monitor your body's response", "Stay hydrated"],
                nutritionalInfo: {
                    calories: "varies",
                    fiber: "medium",
                    probiotics: false,
                    inflammatory: false
                },
                recognitionMethod: "gemini_ai_fallback",
                timestamp: new Date().toISOString(),
                note: "Response parsing issue - using fallback analysis"
            };
        }

        // Add metadata
        analysisData.apiVersion = "1.0";
        analysisData.model = "gemini-2.0-flash-exp";
        analysisData.processingTime = Date.now();

        console.log('🎯 Analysis complete:', analysisData.name);

        // Return successful response
        return res.status(200).json(analysisData);

    } catch (error) {
        console.error('❌ Error in food analysis:', error);

        // Return error response
        return res.status(500).json({
            error: 'Analysis failed',
            message: error.message || 'An unexpected error occurred',
            recognitionMethod: "error",
            timestamp: new Date().toISOString()
        });
    }
}