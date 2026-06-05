                    

        // Flipkart ke latest HTML container selectors
        const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrape() {
    console.log("Scraping shuru...");
    const url = 'https://www.flipkart.com/search?q=intel+laptop';

    try {
        const { data } = await axios.get(url, {
            headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' }
        });

        const $ = cheerio.load(data);
        let results = [];

        // Flipkart ka current selector
        $('div.tUxRFH').each((i, el) => {
            const title = $(el).find('div.KzDlHZ').text();
            if (title.toLowerCase().includes('intel')) {
                results.push({ title: title.trim(), price: "check" });
            }
        });

        if (results.length > 0) {
            fs.writeFileSync('intel-laptops.json', JSON.stringify(results, null, 2));
            console.log("File success ke saath bani.");
        } else {
            console.log("Data nahi mila (Selector galat ho sakte hain).");
            process.exit(1); // Yahan error dena zaroori hai
        }
    } catch (err) {
        console.error("Scraper Error:", err.message);
        process.exit(1);
    }
}
scrape();
