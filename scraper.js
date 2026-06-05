const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function scrapeFlipkartLaptops() {
    console.log("Flipkart Scraper shuru ho raha hai...");
    const browser = await puppeteer.connect({
        browserWSEndpoint: `wss://chrome.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`,
    });

    const page = await browser.newPage();
    
    // User Agent zaroori hai taaki Flipkart humein block na kare
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36");

    console.log("Flipkart page load ho raha hai...");
    // Flipkart search URL
    await page.goto('https://www.flipkart.com/search?q=hp+laptops', { waitUntil: 'networkidle2', timeout: 60000 });

    // Page ko thoda scroll karein taaki products load ho sakein (Lazy Loading fix)
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight / 2));
    await new Promise(r => setTimeout(r, 3000)); // 3 seconds wait

    const flipkartData = await page.evaluate(() => {
        // Flipkart ke latest container selectors
        const items = document.querySelectorAll('div[data-id]'); 
        let results = [];
        
        items.forEach(item => {
            const title = item.querySelector('div.KzDlHZ')?.innerText || item.querySelector('a.wjcEIp')?.innerText;
            const price = item.querySelector('div.Nx9bqj')?.innerText?.replace(/₹|,/g, '');
            const oldPrice = item.querySelector('div.yRaY8j')?.innerText?.replace(/₹|,/g, '') || price;
            const image = item.querySelector('img.DByuf4')?.src;
            const linkElement = item.querySelector('a.CGtC6r') || item.querySelector('a.VJA3rP');
            const link = linkElement ? "https://www.flipkart.com" + linkElement.getAttribute('href') : "#";

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

    fs.writeFileSync('hp-laptops.json', JSON.stringify(flipkartData, null, 2));
    console.log(`Success! Total ${flipkartData.length} HP laptops saved from Flipkart.`);
    await browser.close();
}

scrapeFlipkartLaptops();
