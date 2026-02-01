/**
 * Simple health check endpoint with CORS support
 */

export default async function handler(req, res) {
    // Set CORS headers for all requests
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');
    res.setHeader('Access-Control-Max-Age', '86400');

    // Handle preflight OPTIONS request
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    // Return health status
    return res.status(200).json({
        status: 'healthy',
        message: '🦠 GutSense Backend API is running!',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        cors: 'enabled',
        gemini: process.env.GEMINI_API_KEY ? 'configured' : 'not_configured'
    });
}