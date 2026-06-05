            
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrape() {
    // Amazon/Flipkart ka URL jahan se aap data utha rahe hain
    const url = 'YOUR_TARGET_URL_HERE'; 

    try {
        const { data } = await axios.get(url, {
            headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36' }
        });

        const $ = cheerio.load(data);
        let laptops = [];

        // Yahan CSS Selector update karein jo aapke page ke laptop card ko point karta ho
        $('.s-result-item').each((i, el) => {
            const title = $(el).find('h2 a').text().trim();
            const price = $(el).find('.a-price-whole').text().replace(/[,]/g, '');
            const image = $(el).find('img').attr('src');
            const link = 'https://www.amazon.in' + $(el).find('h2 a').attr('href');

            if (title && price) {
                laptops.push({
                    title,
                    price,
                    image,
                    amazonLink: link,
                    discount: "12% OFF" // Aap yahan logic laga sakte hain
                });
            }
        });

        fs.writeFileSync('laptops.json', JSON.stringify(laptops, null, 2));
        console.log("Scraping successful! laptops.json updated.");
    } catch (error) {
        console.error("Scraping Error:", error.message);
    }
}

scrape();
