const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function scrapeAmazonHP() {
    console.log("Scraping shuru ho raha hai...");
    const browser = await puppeteer.connect({
        browserWSEndpoint: `wss://chrome.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`,
    });

    const page = await browser.newPage();
    
    // 1. Randomize headers to look like a real browser
    await page.setExtraHTTPHeaders({
        'accept-language': 'en-US,en;q=0.9',
    });
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36");

    console.log("Amazon load ho raha hai...");
    // 2. Wait for navigation and add a small delay
    await page.goto('https://www.amazon.in/s?k=hp+laptops', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await new Promise(r => setTimeout(r, 5000)); // 5 second ka wait

    const amazonData = await page.evaluate(() => {
        const items = document.querySelectorAll('.s-result-item');
        let results = [];

        items.forEach(item => {
            // 'aria-label' attribute pura title contain karta hai
            const titleElem = item.querySelector('h2 a');
            const title = titleElem?.innerText;
            
            // Price extraction
            const price = item.querySelector('.a-price-whole')?.innerText?.replace(/,/g, '');
            const oldPrice = item.querySelector('.a-text-price .a-offscreen')?.innerText?.replace(/₹|,/g, '') || price;
            const image = item.querySelector('.s-image')?.src;
            const link = item.querySelector('a.a-link-normal')?.getAttribute('href');

            if (title && title.toLowerCase().includes('hp') && price) {
                results.push({
                    title: title.trim(),
                    price: price.trim(),
                    oldPrice: oldPrice.trim(),
                    image: image,
                    amazonLink: link ? "https://www.amazon.in" + link : "#",
                    discount: oldPrice && price ? Math.round(((oldPrice - price) / oldPrice) * 100) + "% OFF" : "0% OFF"
                });
            }
        });
        return results;
    });

    // Check if data is empty
    if (amazonData.length === 0) {
        console.log("Warning: Data empty mila. Amazon ne block kiya ho sakta hai!");
        // Screen ka screenshot lein debug karne ke liye
        await page.screenshot({ path: 'debug.png' });
    } else {
        fs.writeFileSync('hp-laptops.json', JSON.stringify(amazonData, null, 2));
        console.log(`Success! Total ${amazonData.length} laptops save ho gaye.`);
    }

    await browser.close();
}

scrapeAmazonHP();
