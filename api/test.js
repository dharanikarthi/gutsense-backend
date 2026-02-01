/**
 * Simple test endpoint to verify Vercel deployment and CORS
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

    // Simple response
    return res.status(200).json({
        status: 'success',
        message: 'Backend is working!',
        timestamp: new Date().toISOString(),
        method: req.method,
        cors: 'enabled'
    });
}