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
    "image_url": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?q=80&w=600",
    "amazon_link": "https://www.amazon.in/",
    "price": "99,999",
    "oldPrice": "1,20,000",
    "discount": "15% OFF",
    "intro": "Write a 3-sentence intro.",
    "specs": {{"Processor": "...", "RAM": "...", "Storage": "...", "Display": "...", "Battery": "..."}},
    "pros": ["...", "..."],
    "cons": ["...", "..."],
    "verdict_intro": "...",
    "pro_tip": "...",
    "rating": "4.5/5"
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

        html_content = f"""<!DOCTYPE html>
<html lang="hi">
<head><meta charset="UTF-8"><title>{data['title']} - Review</title>
<style>
    body {{ font-family: sans-serif; background: #f4f4f4; padding: 20px; }}
    .container {{ max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 12px; }}
    .product-img {{ width: 100%; max-width: 400px; display: block; margin: 20px auto; border-radius: 10px; }}
    .buy-btn {{ display: block; width: 220px; margin: 20px auto; padding: 15px; background: #ff9f00; color: white; text-align: center; text-decoration: none; font-weight: bold; border-radius: 8px; }}
    .spec-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
    .spec-table td {{ padding: 12px; border-bottom: 1px solid #eee; }}
    .pros {{ background: #e8f5e9; padding: 20px; margin: 20px 0; }}
    .cons {{ background: #ffebee; padding: 20px; margin: 20px 0; }}
</style></head>
<body>
    <div class="container">
        <h1>{data['title']}</h1>
        <img src="{data['image_url']}" alt="{data['title']}" class="product-img">
        <a href="{data['amazon_link']}" class="buy-btn" target="_blank">🛒 Buy Now on Amazon</a>
        <p>{data['intro']}</p>
        <h2>📋 Specifications</h2>
        <table class="spec-table">{specs_html}</table>
        <div class="pros"><h3>✅ Pros</h3><ul>{pros_html}</ul></div>
        <div class="cons"><h3>❌ Cons</h3><ul>{cons_html}</ul></div>
        <h3>⚖️ Verdict</h3>
        <p>{data['verdict_intro']}</p>
        <p><strong>💡 Pro-Tip:</strong> {data['pro_tip']}</p>
        <p><strong>Rating: {data['rating']}</strong></p>
    </div>
</body></html>"""

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
        
