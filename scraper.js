const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function scrapeLaptops() {
    console.log("Scraping shuru ho raha hai...");
    const browser = await puppeteer.connect({
        browserWSEndpoint: `wss://chrome.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`,
    });

    const page = await browser.newPage();
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36");

    let allLaptops = [];

    // --- 1. AMAZON SCRAPING ---
    console.log("Amazon se data nikal rahe hain...");
    await page.goto('https://www.amazon.in/s?k=hp+laptops', { waitUntil: 'networkidle2' });
    const amazonData = await page.evaluate(() => {
        const items = document.querySelectorAll('.s-result-item');
        let results = [];
        items.forEach(item => {
            const titleElem = item.querySelector('h2 a span'); // Pura title extract karne ke liye
            const title = titleElem?.innerText;
            const price = item.querySelector('.a-price-whole')?.innerText?.replace(/,/g, '');
            const oldPrice = item.querySelector('.a-text-price .a-offscreen')?.innerText?.replace('₹', '')?.replace(/,/g, '') || price;
            
            if (title && title.toLowerCase().includes('hp') && price) {
                results.push({
                    title: title.trim(),
                    price: price.trim(),
                    oldPrice: oldPrice.trim(),
                    image: item.querySelector('.s-image')?.src,
                    amazonLink: item.querySelector('a.a-link-normal')?.href,
                    discount: Math.round(((oldPrice - price) / oldPrice) * 100) + "% OFF"
                });
            }
        });
        return results;
    });
    allLaptops = [...allLaptops, ...amazonData];

    // --- 2. FLIPKART SCRAPING ---
    console.log("Flipkart se data nikal rahe hain...");
    await page.goto('https://www.flipkart.com/search?q=hp+laptops', { waitUntil: 'networkidle2' });
    const flipkartData = await page.evaluate(() => {
        const items = document.querySelectorAll('._1AtVbE'); 
        let results = [];
        items.forEach(item => {
            // Flipkart ka title selector
            const title = item.querySelector('._4rR01T')?.innerText; 
            const price = item.querySelector('._30jeq3')?.innerText?.replace(/₹|,/g, '');
            const oldPrice = item.querySelector('._3Ijp_c')?.innerText?.replace(/₹|,/g, '') || price;
            
            if (title && title.toLowerCase().includes('hp') && price) {
                results.push({
                    title: title.trim(),
                    price: price.trim(),
                    oldPrice: oldPrice.trim(),
                    image: item.querySelector('._396cs4')?.src,
                    amazonLink: item.querySelector('a._1fQZEK')?.href, // Product link
                    discount: Math.round(((oldPrice - price) / oldPrice) * 100) + "% OFF"
                });
            }
        });
        return results;
    });
    allLaptops = [...allLaptops, ...flipkartData];

    // Save Data
    fs.writeFileSync('hp-laptops.json', JSON.stringify(allLaptops, null, 2));
    console.log(`Done! Total ${allLaptops.length} HP laptops saved in hp-laptops.json`);
    await browser.close();
}

scrapeLaptops();
