 const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrape() {
    const url = 'https://www.amazon.in/s?k=laptops'; 
    try {
        const { data } = await axios.get(url, {
            headers: { 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36' 
            }
        });
        const $ = cheerio.load(data);
        let laptops = [];

        $('.s-result-item').each((i, el) => {
            const title = $(el).find('h2 a').text().trim();
            const price = $(el).find('.a-price-whole').text().replace(/[,]/g, '');
            const image = $(el).find('img').attr('src');
            const link = 'https://www.amazon.in' + $(el).find('h2 a').attr('href');

            if (title && price) {
                laptops.push({ title, price, image, amazonLink: link });
            }
        });

        fs.writeFileSync('laptops.json', JSON.stringify(laptops, null, 2));
        console.log("Data mil gaya!");
    } catch (error) { console.error("Scraping Error:", error.message); }
}
scrape();

