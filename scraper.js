const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function scrapeAmazonHP() {
    console.log("Scraping shuru ho raha hai...");
    const browser = await puppeteer.connect({
        browserWSEndpoint: `wss://chrome.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`,
    });

    const page = await browser.newPage();
    
    // Sabse zaroori: Real browser jaisa dikhne ke liye
    await page.setExtraHTTPHeaders({
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
    });
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36");

    console.log("Amazon search page load kar rahe hain...");
    // Amazon search URL
    const url = 'https://www.amazon.in/s?k=hp+laptops&ref=nb_sb_noss';
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 90000 });

    // Page load hone ka wait karein
    await page.waitForSelector('.s-result-item');

    const amazonData = await page.evaluate(() => {
        const items = document.querySelectorAll('.s-result-item[data-component-type="s-search-result"]');
        let results = [];

        items.forEach(item => {
            const titleElem = item.querySelector('h2 a');
            const title = titleElem?.innerText;
            const price = item.querySelector('.a-price-whole')?.innerText?.replace(/,/g, '');
            const image = item.querySelector('.s-image')?.src;
            const link = item.querySelector('a.a-link-normal')?.getAttribute('href');

            if (title && title.toLowerCase().includes('hp') && price) {
                results.push({
                    title: title.trim(),
                    price: price.trim(),
                    image: image || "",
                    amazonLink: link ? "https://www.amazon.in" + link : "#",
                    discount: "10% OFF" // Default discount agar na mile
                });
            }
        });
        return results;
    });

    if (amazonData.length > 0) {
        fs.writeFileSync('hp-laptops.json', JSON.stringify(amazonData, null, 2));
        console.log(`Success! Total ${amazonData.length} HP laptops saved.`);
    } else {
        // Screenshot lekar dekhein ki Amazon kya dikha raha hai
        await page.screenshot({ path: 'amazon_debug.png', fullPage: true });
        console.log("Warning: Koi data nahi mila.");
        process.exit(1);
    }

    await browser.close();
}

scrapeAmazonHP();
