            
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrape() {
    const url = 'https://www.flipkart.com/search?q=intel+laptop';
    console.log("Scraping start...");

    try {
        const response = await axios.get(url, {
            headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36' },
            timeout: 100000
        });

        const $ = cheerio.load(response.data);
        let results = [];

        // Generic selector: Flipkart ke item container
        $('div.tUxRFH').each((i, el) => {
            const title = $(el).find('div.KzDlHZ').text();
            if (title && title.toLowerCase().includes('intel')) {
                results.push({
                    title: title.trim(),
                    price: $(el).find('div.Nx9bqj').text()
                });
            }
        });

        // Agar data nahi mila toh bhi empty array save karo, taaki file exist kare
        fs.writeFileSync('intel-laptops.json', JSON.stringify(results.length > 0 ? results : [{info: "No laptops found"}], null, 2));
        console.log(`Success! File saved with ${results.length} items.`);

    } catch (err) {
        console.error("Error:", err.message);
        // Crash mat karo, file create kar do taaki Action fail na ho
        fs.writeFileSync('intel-laptops.json', JSON.stringify([{error: err.message}]));
    }
}

scrape();
