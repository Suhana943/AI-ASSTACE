const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function scrape1000Laptops() {
  console.log("Browserless se connect ho rahe hain...");
  
  const browser = await puppeteer.connect({
    // YAHAN APNI BROWSERLESS API KEY DAALEIN
    browserWSEndpoint: `ws://less.browserless.io?token=2UeF67e48SIevkya77b2b57d410a5b65bc5a9c400ea1e4440`, 
  });

  const page = await browser.newPage();
  let allLaptops = [];
  
  // Amazon ke 10 alag-alag pages par loop chalana (Har page par ~22 laptops hote hain)
  // Agar aapko pure 1000 chahiye toh aap i <= 40 tak badha sakte hain
  for (let i = 1; i <= 15; i++) {
    console.log(`Page ${i} scrape ho raha hai...`);
    
    try {
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
              price: price,
              oldPrice: oldPrice.replace('₹', ''),
              image: image,
              amazonLink: link,
              discount: "10% OFF" // Aap isko static ya dynamic rakh sakte hain
            });
          }
        });
        return results;
      });

      allLaptops = [...allLaptops, ...laptopsOnPage];
      console.log(`Page ${i} se ${laptopsOnPage.length} laptops mile.`);
      
      // Amazon ko shak na ho, isliye har page ke baad 2 second ka gap
      await new Promise(r => setTimeout(r, 2000));

    } catch (err) {
      console.log(`Page ${i} par error aaya, skip kar rahe hain.`, err.message);
    }
  }

  // Data ko JSON file me save karna
  fs.writeFileSync('laptops.json', JSON.stringify(allLaptops, null, 2));
  console.log(`Done! Total ${allLaptops.length} laptops ka data 'laptops.json' me save ho gaya.`);

  await browser.close();
}

scrape1000Laptops();
