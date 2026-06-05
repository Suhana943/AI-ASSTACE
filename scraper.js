const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function scrapeFlipkartIntel() {
    console.log("Flipkart se Intel laptops scrape ho raha hai...");
    const browser = await puppeteer.connect({
        browserWSEndpoint: `wss://chrome.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`,
    });

    const page = await browser.newPage();
    // Real browser jaisa dikhne ke liye User Agent
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36");

    // Flipkart search URL for Intel laptops
    const url = 'https://www.flipkart.com/search?q=intel+laptop';
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 90000 });

    // Page load hone ka wait
    await page.waitForSelector('div.KzDlHZ, a.wjcEIp', { timeout: 60000 });

    const intelData = await page.evaluate(() => {
        const items = document.querySelectorAll('div[data-id]'); 
        let results = [];

        items.forEach(item => {
            const title = item.querySelector('div.KzDlHZ')?.innerText || item.querySelector('a.wjcEIp')?.innerText;
            const price = item.querySelector('div.Nx9bqj')?.innerText?.replace(/₹|,/g, '');
            const image = item.querySelector('img.DByuf4')?.src;
            const linkElement = item.querySelector('a.CGtC6r') || item.querySelector('a.VJA3rP');
            const link = linkElement ? "https://www.flipkart.com" + linkElement.getAttribute('href') : "#";

            // Intel filter
            if (title && title.toLowerCase().includes('intel') && price) {
                results.push({
                    title: title.trim(),
                    price: price.trim(),
                    image: image || "",
                    amazonLink: link, // Field naam same rakha hai taaki code update na karna pade
                    discount: "Flipkart Exclusive"
                });
            }
        });
        return results;
    });

    if (intelData.length > 0) {
        fs.writeFileSync('intel-laptops.json', JSON.stringify(intelData, null, 2));
        console.log(`Success! Total ${intelData.length} Intel laptops saved from Flipkart.`);
    } else {
        await page.screenshot({ path: 'flipkart_debug.png' });
        console.log("Warning: Flipkart se koi data nahi mila.");
        process.exit(1);
    }

    await browser.close();
}

scrapeFlipkartIntel();
