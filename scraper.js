const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function scrapeLaptops() {
    console.log("Scraping shuru ho raha hai...");
    const browser = await puppeteer.connect({
        browserWSEndpoint: `wss://chrome.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`,
    });

    const page = await browser.newPage();
    // Bot detection se bachne ke liye User Agent set karein
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36");

    // AMAZON SCRAPING (HP Laptops)
    console.log("Amazon se data nikal rahe hain...");
    await page.goto('https://www.amazon.in/s?k=hp+laptops', { waitUntil: 'networkidle2' });
    
    const amazonLaptops = await page.evaluate(() => {
        const items = document.querySelectorAll('.s-result-item');
        let results = [];
        items.forEach(item => {
            const title = item.querySelector('h2')?.innerText;
            const price = item.querySelector('.a-price-whole')?.innerText?.replace(/,/g, '');
            const oldPrice = item.querySelector('.a-text-price .a-offscreen')?.innerText?.replace('₹', '')?.replace(/,/g, '') || price;
            const image = item.querySelector('.s-image')?.src;
            const link = item.querySelector('a.a-link-normal')?.href;

            if (title && title.toLowerCase().includes('hp') && price) {
                results.push({
                    title: title.trim(),
                    price: price.trim(),
                    oldPrice: oldPrice.trim(),
                    image: image,
                    amazonLink: link,
                    discount: Math.round(((oldPrice - price) / oldPrice) * 100) + "% OFF"
                });
            }
        });
        return results;
    });

    // Save Data to hp-laptops.json
    fs.writeFileSync('hp-laptops.json', JSON.stringify(amazonLaptops, null, 2));
    
    console.log(`Done! Total ${amazonLaptops.length} HP laptops saved in hp-laptops.json`);
    await browser.close();
}

scrapeLaptops();
