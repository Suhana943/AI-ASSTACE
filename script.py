import json
import os
import urllib.parse
import google.generativeai as genai

# 1. API Configuration
genai.configure(api_key=os.environ["API_1"])
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

INSTRUCTIONS:
1. Output ONLY valid JSON format.
2. Price and Old Price: Must be in Indian Rupees (e.g., "₹75,000").
3. Image URL: Try to find a high-quality direct URL from Amazon and imge compulsary hona chahiye. If not found, use: "https://via.placeholder.com/800x400?text=Laptop+Image+Unavailable"
4. Structure:
{{
    "title": "...",
    "image_url": "...",
    "price": "₹...",
    "oldPrice": "₹...",
    "discount": "...",
    "intro": "Write a 5-sentence intro.",
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

    # Generate a functional Amazon India Search Link
    encoded_name = urllib.parse.quote(laptop_name)
    amazon_link = f"https://www.amazon.in/s?k={encoded_name}"

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
    <title>{data['title']} - Review</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; }}
        .container {{ max-width: 800px; margin: auto; }}
        .buy-btn {{ background: #ff9f00; padding: 15px 30px; color: #fff; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{data['title']}</h1>
        <img src="{data['image_url']}" alt="{data['title']}" style="width:100%;">
        <p><strong>Price: {data['price']}</strong></p>
        <a href="{amazon_link}" class="buy-btn" target="_blank">🛒 View on Amazon India</a>
        <p>{data['intro']}</p>
        <table>{specs_html}</table>
        <h3>Pros</h3><ul>{pros_html}</ul>
        <h3>Cons</h3><ul>{cons_html}</ul>
        <h3>Verdict</h3><p>{data['verdict_intro']}</p>
    </div>
</body>
</html>
"""
        
        # B. Save HTML File
        if not os.path.exists('reviews'): os.makedirs('reviews')
        filename = f"reviews/{laptop_name.replace(' ', '_')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # C. History & JSON Update
        with open(HISTORY_FILE, "a") as f:
            f.write(f"{laptop_name}\n")
        
        laptops = []
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                laptops = json.load(f)

        laptops.append({
            "title": laptop_name,
            "price": data.get('price', 'Check Price'),
            "amazonLink": amazon_link,
            "review_link": filename
        })

        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(laptops, f, indent=4)
        
        print(f"Success! {laptop_name} added.")

except Exception as e:
    print(f"Error: {e}")
        
