const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function scrapeAmazonHP() {
    console.log("Scraping shuru ho raha hai...");
    
    // Browserless connection
    const browser = await puppeteer.connect({
        browserWSEndpoint: `wss://chrome.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`,
    });

    const page = await browser.newPage();
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36");

    console.log("Amazon load ho raha hai...");
    await page.goto('https://www.amazon.in/s?k=hp+laptops', { waitUntil: 'domcontentloaded', timeout: 60000 });

    const amazonData = await page.evaluate(() => {
        const items = document.querySelectorAll('.s-result-item');
        let results = [];

        items.forEach(item => {
            const titleElem = item.querySelector('h2 a');
            const title = titleElem?.innerText;
            
            const price = item.querySelector('.a-price-whole')?.innerText?.replace(/,/g, '');
            const oldPrice = item.querySelector('.a-text-price .a-offscreen')?.innerText?.replace(/₹|,/g, '') || price;
            const image = item.querySelector('.s-image')?.src;
            const link = item.querySelector('a.a-link-normal')?.getAttribute('href');

            // Sirf HP check aur valid title/price
            if (title && title.toLowerCase().includes('hp') && price && price !== "0") {
                results.push({
                    title: title.trim(),
                    price: price.trim(),
                    oldPrice: oldPrice.trim(),
                    image: image || "",
                    amazonLink: link ? "https://www.amazon.in" + link : "#",
                    discount: oldPrice && price ? Math.round(((oldPrice - price) / oldPrice) * 100) + "% OFF" : "0% OFF"
                });
            }
        });
        return results;
    });

    // File save karne ka sahi tarika
    if (amazonData.length > 0) {
        const filePath = path.join(process.cwd(), 'hp-laptops.json');
        fs.writeFileSync(filePath, JSON.stringify(amazonData, null, 2));
        console.log(`Success! Total ${amazonData.length} HP laptops save ho gaye.`);
    } else {
        console.log("Warning: Koi data nahi mila, file nahi banayi.");
        process.exit(1); // Error code 1 dena zaroori hai agar data na mile
    }

    await browser.close();
}

scrapeAmazonHP().catch(err => {
    console.error("Critical Error:", err);
    process.exit(1);
});
