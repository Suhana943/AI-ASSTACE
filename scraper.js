                    

        // Flipkart ke latest HTML container selectors
        
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrape() {
    console.log("Scraping shuru...");
    
    // Naya URL aur realistic User-Agent
    const url = 'https://www.flipkart.com/search?q=intel+laptop';
    const instance = axios.create({
        timeout: 30000, // 30 second timeout
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://www.google.com/' // Referer dene se lagta hai ki user Google se aaya hai
        }
    });

    try {
        const response = await instance.get(url);
        const $ = cheerio.load(response.data);
        let results = [];

        // Flipkart ka selector update kiya gaya hai
        $('div.tUxRFH').each((i, el) => {
            const title = $(el).find('div.KzDlHZ').text();
            const price = $(el).find('div.Nx9bqj').text();
            
            if (title && title.toLowerCase().includes('intel')) {
                results.push({
                    title: title.trim(),
                    price: price.replace(/[₹,]/g, '').trim(),
                    scraped_at: new Date().toLocaleString()
                });
            }
        });

        if (results.length > 0) {
            fs.writeFileSync('intel-laptops.json', JSON.stringify(results, null, 2));
            console.log(`Success! ${results.length} laptops mil gaye.`);
        } else {
            console.log("Page load hua, par selector match nahi hue.");
        }
    } catch (err) {
        console.error("Scraper Error:", err.message);
        process.exit(1);
    }
}

scrape();
