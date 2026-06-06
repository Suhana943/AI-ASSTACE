import json
import os
import google.generativeai as genai

# 1. API Configuration
genai.configure(api_key=os.environ["API_1"])
# Model name fix: 1.5-flash
model = genai.GenerativeModel('gemini-3.5-flash')

HISTORY_FILE = "reviewed_laptops.txt"
JSON_FILE = "laptops.json"

# Helper to load history
def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return [line.strip().lower() for line in f.readlines()]
    return []

# 2. Prompt Preparation
reviewed_list = get_history()
exclude_string = ", ".join(reviewed_list) if reviewed_list else "None"

prompt = f"""
Write a professional review for a popular trending laptop.
IMPORTANT: Do NOT review any of these laptops: {exclude_string}.
Output ONLY JSON format, no extra text.
Structure:
{{
    "title": "...",
    "image_url": "Provide a direct URL to a high-quality image of the laptop. If you cannot find a direct image link, return: https://via.placeholder.com/800x400?text=Laptop+Image+Unavailable",

    "amazon_link": "Provide the direct URL to the product on Amazon",
    "price": "...",
    "oldPrice": "...",
    "discount": "...",
    "intro": "Write a 9-sentence intro.",
    "specs": {{"Processor": "...", "RAM": "...", "Storage": "...", "Display": "...", "Battery": "..."}},
    "pros": ["...", "..."],
    "cons": ["...", "..."],
    "verdict_intro": "...",
    "pro_tip": "...",
    "rating": "..."
}}
"""

try:
    # 3. Generate Content
    response = model.generate_content(prompt)
    json_text = response.text.replace("```json", "").replace("```", "").strip()
    data = json.loads(json_text)
    
    laptop_name = data['title']

    # 4. Duplicate Check
    if laptop_name.lower() in reviewed_list:
        print(f"Skipping {laptop_name}, already reviewed.")
    else:
        # A. Prepare HTML Content
        specs_html = "".join([f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>" for k, v in data['specs'].items()])
        pros_html = "".join([f"<li>{p}</li>" for p in data['pros']])
        cons_html = "".join([f"<li>{c}</li>" for c in data['cons']])

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['title']} - Review | LaptopTec.online</title>
    <style>
        body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8f9fa; color: #333; line-height: 1.6; margin: 0; padding: 0; }}
        header {{ background: #1a1a1a; color: #ff9f00; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; border-bottom: 4px solid #ff9f00; }}
        .container {{ width: 95%; margin: 20px auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #1a1a1a; font-size: 32px; margin-bottom: 20px; }}
        .product-img {{ width: 100%; max-width: 800px; border-radius: 8px; margin: 20px 0; display: block; border: 1px solid #ddd; }}
        .buy-btn {{ display: inline-block; background: #ff9f00; color: #fff; padding: 18px 40px; text-decoration: none; font-weight: bold; border-radius: 8px; font-size: 20px; transition: 0.3s; }}
        .buy-btn:hover {{ background: #e68e00; }}
        .section-title {{ font-size: 26px; color: #2c3e50; margin-top: 40px; border-bottom: 2px solid #ff9f00; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: #fff; }}
        td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        .pros, .cons {{ padding: 25px; border-radius: 8px; margin: 20px 0; }}
        .pros {{ background: #f1f8e9; border-left: 6px solid #4caf50; }}
        .cons {{ background: #fff5f5; border-left: 6px solid #f44336; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 10px; font-size: 16px; }}
        .verdict {{ font-style: italic; color: #444; background: #fdfdfd; padding: 20px; border-radius: 8px; border: 1px solid #ddd; }}
        .rating {{ font-size: 24px; font-weight: bold; color: #d32f2f; margin-top: 25px; }}
    </style>
</head>
<body>
    
    <div class="container">
        <h1>{data['title']}</h1>
        <img src="{data['image_url']}" alt="{data['title']}" class="product-img" onerror="this.onerror=null;this.src='https://via.placeholder.com/800x400?text=Image+Unavailable';">
        <a href="{data['amazon_link']}" class="buy-btn" target="_blank">🛒 Buy Now on Amazon</a>
        <p style="font-size: 18px;">{data['intro']}</p>
        <h2 class="section-title">📋 Specifications</h2>
        <table>{specs_html}</table>
        <div class="pros">
            <h3>✅ Pros</h3>
            <ul>{pros_html}</ul>
        </div>
        <div class="cons">
            <h3>❌ Cons</h3>
            <ul>{cons_html}</ul>
        </div>
        <h2 class="section-title">⚖️ Verdict</h2>
        <div class="verdict"><p>{data['verdict_intro']}</p></div>
        <p style="margin-top:20px;"><strong>💡 Pro-Tip:</strong> {data['pro_tip']}</p>
        <p class="rating">Rating: {data['rating']}/10</p>
    </div>
</body>
</html>
"""
        
        # B. Save HTML File
        if not os.path.exists('reviews'): os.makedirs('reviews')
        filename = f"reviews/{laptop_name.replace(' ', '_')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # C. History Update
        with open(HISTORY_FILE, "a") as f:
            f.write(f"{laptop_name}\n")
        
        # D. JSON Update
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                laptops = json.load(f)
        else:
            laptops = []

        laptops.append({
            "title": laptop_name,
            "price": data.get('price', 'Check Price'),
            "oldPrice": data.get('oldPrice', 'N/A'),
            "discount": data.get('discount', '0% OFF'),
            "image": data.get('image_url', ''),
            "amazonLink": data.get('amazon_link', '#'),
            "review_link": filename
        })

        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(laptops, f, indent=4)
        
        print(f"Success! {laptop_name} added to history, HTML generated, and JSON updated.")

except Exception as e:
    print(f"Error: {e}")
        
