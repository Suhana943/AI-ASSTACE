                    const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrapeFlipkartIntel() {
    console.log("Flipkart se Intel laptops scrape ho raha hai...");
    const url = 'https://www.flipkart.com/search?q=intel+laptop';

    try {
        const { data } = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            }
        });

        const $ = cheerio.load(data);
        let results = [];

        // Flipkart ke latest HTML container selectors
        $('div.tUxRFH').each((i, el) => {
            const title = $(el).find('div.KzDlHZ').text();
            const price = $(el).find('div.Nx9bqj').text();
            const link = 'https://www.flipkart.com' + $(el).find('a.CGtC6r').attr('href');
            const image = $(el).find('img.DByuf4').attr('src');

            if (title && title.toLowerCase().includes('intel')) {
                results.push({
                    title: title.trim(),
                    price: price.replace(/[₹,]/g, '').trim(),
                    image: image || "",
                    amazonLink: link,
                    discount: "Flipkart Intel Laptop"
                });
            }
        });

        if (results.length > 0) {
            fs.writeFileSync('intel-laptops.json', JSON.stringify(results, null, 2));
            console.log(`Success! Total ${results.length} laptops save ho gaye.`);
        } else {
            console.log("Koi data nahi mila, shayad selectors change ho gaye hain.");
        }
    } catch (err) {
        console.error("Error fetching data:", err.message);
        process.exit(1);
    }
}

scrapeFlipkartIntel();
