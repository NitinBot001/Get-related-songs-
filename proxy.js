const express = require('express');
const request = require('request');
const app = express();

app.get('/fetch-songs', (req, res) => {
    request('https://www.genyt.net', (error, response, body) => {
        if (!error && response.statusCode == 200) {
            res.send(body);
        } else {
            res.status(500).send('Error fetching songs');
        }
    });
});


// Listen on all network interfaces (0.0.0.0)
app.listen(8000, '0.0.0.0', () => {
    console.log(`Proxy server is running on http://0.0.0.0:${PORT}`);
});
