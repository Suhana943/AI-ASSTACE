const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function scrapeAmazonHP() {
    console.log("Amazon HP Scraper shuru ho raha hai...");
    const browser = await puppeteer.connect({
        browserWSEndpoint: `wss://chrome.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`,
    });

    const page = await browser.newPage();
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36");

    // Amazon search URL
    await page.goto('https://www.amazon.in/s?k=hp+laptops', { waitUntil: 'networkidle2' });

    const amazonData = await page.evaluate(() => {
        const items = document.querySelectorAll('.s-result-item[data-component-type="s-search-result"]');
        let results = [];

        items.forEach(item => {
            // Pura title lene ke liye 'aria-label' ka use kiya hai
            const titleElem = item.querySelector('h2 a');
            const title = titleElem?.innerText;
            
            const price = item.querySelector('.a-price-whole')?.innerText?.replace(/,/g, '');
            const oldPrice = item.querySelector('.a-text-price .a-offscreen')?.innerText?.replace(/₹|,/g, '') || price;
            const image = item.querySelector('.s-image')?.src;
            const link = "https://www.amazon.in" + item.querySelector('a.a-link-normal')?.getAttribute('href');

            // Sirf HP laptops filter karein
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

    fs.writeFileSync('hp-laptops.json', JSON.stringify(amazonData, null, 2));
    console.log(`Success! Total ${amazonData.length} HP laptops saved.`);
    await browser.close();
}

scrapeAmazonHP();
