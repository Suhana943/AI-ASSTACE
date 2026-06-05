const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function scrape1000Laptops() {
  console.log("GitHub server Browserless se connect ho raha hai...");
  try {
    const browser = await puppeteer.connect({
      // Yeh automatic aapki saved API key utha lega
      browserWSEndpoint: `wss://chrome.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`, 
    });

    const page = await browser.newPage();
    let allLaptops = [];
    
    // Mobile/Server par load kam rakhne ke liye abhi 5 pages scrape karte hain (~100+ laptops)
    for (let i = 1; i <= 5; i++) {
      console.log(`Amazon Page ${i} chal raha hai...`);
      const url = `https://www.amazon.in/s?k=laptops&page=${i}`;
      await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });

      const laptopsOnPage = await page.evaluate(() => {
        const items = document.querySelectorAll('.s-result-item[data-component-type="s-search-result"]');
        let results = [];
        items.forEach((item) => {
          const title = item.querySelector('h2 span')?.innerText;
          const price = item.querySelector('.a-price-whole')?.innerText;
          const oldPrice = item.querySelector('.a-text-price .a-offscreen')?.innerText || "N/A";
          const image = item.querySelector('.s-image')?.src;
          const link = item.querySelector('a.a-link-normal')?.href;

          if (title && price) {
            results.push({
              title: title,
              price: price.trim(),
              oldPrice: oldPrice.replace('₹', '').trim(),
              image: image,
              amazonLink: link,
              discount: "12% OFF"
            });
          }
        });
        return results;
      });
      allLaptops = [...allLaptops, ...laptopsOnPage];
      await new Promise(r => setTimeout(r, 1000));
    }

    fs.writeFileSync('laptops.json', JSON.stringify(allLaptops, null, 2));
    console.log(`Mubarak ho! Total ${allLaptops.length} laptops save ho gaye.`);
    await browser.close();
  } catch (error) {
    console.error("Error:", error.message);
    process.exit(1);
  }
}
scrape1000Laptops();
