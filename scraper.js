const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function scrapeIntelLaptops() {
    console.log("Intel website scrap ho raha hai...");
    const browser = await puppeteer.connect({
        browserWSEndpoint: `wss://chrome.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`,
    });

    const page = await browser.newPage();
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36");

    // Intel India Laptops Search URL
    const url = 'https://www.intel.in/content/www/in/in/products/details/processors/core.html';
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 90000 });

    // Intel website par data load hone ka wait karein
    console.log("Data load hone ka wait kar rahe hain...");
    await page.waitForSelector('.product-item', { timeout: 60000 }).catch(() => console.log("Timeout, shayad selector badal gaya hai."));

    const intelData = await page.evaluate(() => {
        // Intel ke website structure ke hisaab se selectors (Note: Ye website update hote hi badal sakte hain)
        const items = document.querySelectorAll('.product-item'); 
        let results = [];

        items.forEach(item => {
            const title = item.querySelector('.product-title')?.innerText;
            const link = item.querySelector('a')?.href;
            
            if (title) {
                results.push({
                    title: title.trim(),
                    price: "Check Website", // Intel direct price nahi dikhata, wo retailers par bhejta hai
                    image: item.querySelector('img')?.src || "",
                    amazonLink: link || "#",
                    discount: "Official Intel"
                });
            }
        });
        return results;
    });

    if (intelData.length > 0) {
        fs.writeFileSync('intel-laptops.json', JSON.stringify(intelData, null, 2));
        console.log(`Success! Total ${intelData.length} Intel products saved.`);
    } else {
        await page.screenshot({ path: 'intel_debug.png' });
        console.log("Warning: Intel website se data nahi mila.");
        process.exit(1);
    }

    await browser.close();
}

scrapeIntelLaptops();
