const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function scrapeLaptops() {
    console.log("Scraping shuru ho raha hai...");
    const browser = await puppeteer.connect({
        browserWSEndpoint: `wss://chrome.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`,
    });

    const page = await browser.newPage();
    let allLaptops = [];

    // 1. AMAZON SCRAPING (HP Laptops)
    console.log("Amazon se data nikal rahe hain...");
    await page.goto('https://www.amazon.in/s?k=hp+laptops', { waitUntil: 'networkidle2' });
    const amazonLaptops = await page.evaluate(() => {
        const items = document.querySelectorAll('.s-result-item');
        let results = [];
        items.forEach(item => {
            const title = item.querySelector('h2')?.innerText;
            if (title && title.toLowerCase().includes('hp')) {
                results.push({
                    title: title,
                    price: item.querySelector('.a-price-whole')?.innerText || "0",
                    image: item.querySelector('.s-image')?.src,
                    amazonLink: item.querySelector('a')?.href,
                    source: 'Amazon'
                });
            }
        });
        return results;
    });

    // 2. FLIPKART SCRAPING (HP Laptops)
    console.log("Flipkart se data nikal rahe hain...");
    await page.goto('https://www.flipkart.com/search?q=hp+laptops', { waitUntil: 'networkidle2' });
    const flipkartLaptops = await page.evaluate(() => {
        const items = document.querySelectorAll('._1AtVbE'); // Flipkart ka common class
        let results = [];
        items.forEach(item => {
            const title = item.querySelector('._4rR01T')?.innerText || item.querySelector('.s1Q9rs')?.innerText;
            if (title && title.toLowerCase().includes('hp')) {
                results.push({
                    title: title,
                    price: item.querySelector('._30jeq3')?.innerText.replace('₹', ''),
                    image: item.querySelector('._396cs4')?.src,
                    amazonLink: item.querySelector('a')?.href, // Link yahan store hoga
                    source: 'Flipkart'
                });
            }
        });
        return results;
    });

    // Combine aur Save
    allLaptops = [...amazonLaptops, ...flipkartLaptops];
    fs.writeFileSync('hp-laptops.json', JSON.stringify(allLaptops, null, 2));
    
    console.log(`Done! Total ${allLaptops.length} HP laptops saved in hp-laptops.json`);
    await browser.close();
}

scrapeLaptops();
