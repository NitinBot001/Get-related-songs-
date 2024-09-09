const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = 3000;

// Enable CORS for all routes
app.use(cors());

app.get('/fetch-genyt-content', async (req, res) => {
    try {
        const response = await axios.get('https://www.genyt.net');
        res.send(response.data);
    } catch (error) {
        console.error('Error fetching data from www.genyt.net:', error);
        res.status(500).send('Failed to fetch data');
    }
});

// Listen on all network interfaces (0.0.0.0)
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Proxy server is running on http://0.0.0.0:${PORT}`);
});
