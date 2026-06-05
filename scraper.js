const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrapeWithRetry(url, retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            console.log(`Attempt ${i + 1} - Scraping shuru...`);
            return await axios.get(url, {
                timeout: 20000,
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
                }
            });
        } catch (err) {
            if (err.response && (err.response.status === 529 || err.response.status === 429)) {
                console.log("Rate limited! 15 seconds ruk rahe hain...");
                await new Promise(r => setTimeout(r, 15000));
            } else {
                throw err;
            }
        }
    }
    throw new Error("Maximum retries reach ho gaye.");
}

async function start() {
    const url = 'https://www.flipkart.com/search?q=intel+laptop';
    try {
        const response = await scrapeWithRetry(url);
        const $ = cheerio.load(response.data);
        let results = [];

        $('div.tUxRFH').each((i, el) => {
            const title = $(el).find('div.KzDlHZ').text() || $(el).find('a.wjcEIp').text();
            const price = $(el).find('div.Nx9bqj').text();
            
            if (title && title.toLowerCase().includes('intel')) {
                results.push({ title: title.trim(), price: price.replace(/[₹,]/g, '').trim() });
            }
        });

        if (results.length > 0) {
            fs.writeFileSync('intel-laptops.json', JSON.stringify(results, null, 2));
            console.log(`Success! ${results.length} laptops mil gaye.`);
        } else {
            console.log("Data nahi mila.");
        }
    } catch (err) {
        console.error("Critical Error:", err.message);
        process.exit(1);
    }
}

start();

