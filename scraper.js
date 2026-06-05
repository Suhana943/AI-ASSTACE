                    

        // Flipkart ke latest HTML container selectors
        const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrape() {
    console.log("Scraping shuru ho raha hai...");
    const url = 'https://www.flipkart.com/search?q=intel+laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off';

    try {
        // Flipkart ko lagna chahiye ki ye request browser se aa rahi hai
        const response = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        });

        const $ = cheerio.load(response.data);
        let results = [];

        // Flipkart ke product containers ka generic selector
        // Hum un divs ko select kar rahe hain jo products hold karte hain
        $('div.tUxRFH').each((i, el) => {
            const title = $(el).find('div.KzDlHZ').text() || $(el).find('a.wjcEIp').text();
            const price = $(el).find('div.Nx9bqj').text();
            
            if (title && title.toLowerCase().includes('intel')) {
                results.push({
                    title: title.trim(),
                    price: price.replace(/[₹,]/g, '').trim(),
                    timestamp: new Date().toISOString()
                });
            }
        });

        if (results.length > 0) {
            fs.writeFileSync('intel-laptops.json', JSON.stringify(results, null, 2));
            console.log(`Success! ${results.length} Intel laptops mil gaye.`);
        } else {
            console.log("Data nahi mila. HTML structure check karein.");
            // Log the HTML head to debug
            console.log("Response sample:", $('title').text());
        }
    } catch (err) {
        console.error("Scraper Error:", err.message);
        process.exit(1);
    }
}

scrape();
