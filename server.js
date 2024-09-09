const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');

const app = express();

// Serve static files from the 'public' folder
app.use(express.static('public'));

app.get('/scrape', async (req, res) => {
    try {
        // Fetch the webpage content
        const { data } = await axios.get('https://www.genyt.net');
        
        // Load HTML content using cheerio
        const $ = cheerio.load(data);

        // Array to store scraped data
        let songs = [];

        // Find all divs with the class 'col-lg-12 col-md-12 gytbox mb-3'
        $('div.col-lg-12.col-md-12.gytbox.mb-3').each((index, element) => {
            const videoUrl = $(element).find('a').attr('href');
            const videoId = videoUrl.replace('https://video.genyt.net/', '');
            const title = $(element).find('h5.gytTitle a').text().trim();
            const thumbnail = $(element).find('img').attr('src');
            
            songs.push({ videoId, title, thumbnail });
        });

        // Return the scraped data as JSON
        res.json(songs);
    } catch (error) {
        console.error('Error scraping data:', error);
        res.status(500).send('Error scraping data');
    }
});

// Start the Express server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
