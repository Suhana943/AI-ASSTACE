import json
import os
import google.generativeai as genai

# 1. API Configuration
genai.configure(api_key=os.environ["API_1"])
# Model name fix: 3.5 nahi, 1.5 use karein
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
    "image_url": "Provide direct link to an image of the laptop",
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
        # A. HTML Generation
        if not os.path.exists('reviews'): os.makedirs('reviews')
        filename = f"reviews/{laptop_name.replace(' ', '_')}.html"
        
        specs_html = "".join([f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>" for k, v in data['specs'].items()])
        pros_html = "".join([f"<li>{p}</li>" for p in data['pros']])
        cons_html = "".join([f"<li>{c}</li>" for c in data['cons']])

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['title']} - Review</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f4f7f6; color: #333; line-height: 1.6; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: auto; background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a1a1a; font-size: 28px; margin-bottom: 10px; }}
        .product-img {{ width: 100%; border-radius: 8px; margin: 20px 0; border: 1px solid #ddd; }}
        .buy-btn {{ display: block; background: #ff9f00; color: #fff; text-align: center; padding: 15px; text-decoration: none; font-weight: bold; border-radius: 8px; margin: 20px 0; font-size: 18px; }}
        .buy-btn:hover {{ background: #e68e00; }}
        .section-title {{ font-size: 22px; color: #333; margin-top: 30px; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        td {{ padding: 12px; border-bottom: 1px solid #eee; }}
        .pros {{ background: #e8f5e9; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #4caf50; }}
        .cons {{ background: #ffebee; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #f44336; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 8px; }}
        .verdict {{ font-style: italic; color: #555; background: #f9f9f9; padding: 15px; border-radius: 8px; }}
        .rating {{ font-size: 20px; font-weight: bold; color: #d32f2f; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{data['title']}</h1>
        <img src="{data['image_url']}" alt="{data['title']}" class="product-img">
        <a href="{data['amazon_link']}" class="buy-btn" target="_blank">🛒 Buy Now on Amazon</a>
        
        <p>{data['intro']}</p>
        
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
        
        <p><strong>💡 Pro-Tip:</strong> {data['pro_tip']}</p>
        <p class="rating">Rating: {data['rating']}</p>
    </div>
</body>
</html>
"""


        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # B. History Update
        with open(HISTORY_FILE, "a") as f:
            f.write(f"{laptop_name}\n")
        
        # C. JSON Update
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
        
