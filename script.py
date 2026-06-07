import json
import os
import urllib.parse
import google.generativeai as genai

# 1. API Configuration - Fixed Model Name
genai.configure(api_key=os.environ["API_1"])
model = genai.GenerativeModel('gemini-3.5-flash') 

HISTORY_FILE = "reviewed_laptops.txt"
JSON_FILE = "laptops.json"

def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f.readlines()]
    return []

reviewed_list = get_history()
exclude_string = ", ".join(reviewed_list) if reviewed_list else "None"

# 2. Updated Prompt (Forces Hindi Output)
prompt = f"""
Write a professional laptop review in HINDI language.
IMPORTANT: Do NOT review any of these laptops: {exclude_string}.

INSTRUCTIONS:
1. Output ONLY JSON format.
2. Price and Old Price: Must be in Indian Rupees (e.g., "₹75,000").
3. Content: Write everything (intro, pros, cons, verdict, pro-tip) in fluent HINDI.
4. Image: Use a high-quality product image link. If not possible, use: "https://placehold.co/800x400/png?text=Product+Image"

Structure (JSON only):
{{
    "title": "...",
    "image_url": "...",
    "price": "₹...",
    "oldPrice": "₹...",
    "discount": "...",
    "intro": "Write a 5-sentence intro in Hindi.",
    "specs": {{"Processor": "...", "RAM": "...", "Storage": "...", "Display": "...", "Battery": "..."}},
    "pros": ["...", "..."],
    "cons": ["...", "..."],
    "verdict_intro": "Write in Hindi",
    "pro_tip": "Write in Hindi",
    "rating": "..."
}}
"""

try:
    # 3. Generate Content
    response = model.generate_content(prompt)
    json_text = response.text.replace("```json", "").replace("```", "").strip()
    data = json.loads(json_text)
    
    laptop_name = data['title']
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
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>{data['title']} - Review</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
        .container {{ max-width: 800px; margin: auto; }}
        .buy-btn {{ background: #ff9f00; padding: 15px 30px; color: #fff; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{data['title']}</h1>
        <img src="{data['image_url']}" alt="{data['title']}" style="width:100%;">
        <p><strong>Price: {data['price']}</strong></p>
        <a href="{amazon_link}" class="buy-btn" target="_blank">🛒 Amazon par dekhein</a>
        <p>{data['intro']}</p>
        <table>{specs_html}</table>
        <h3>Pros</h3><ul>{pros_html}</ul>
        <h3>Cons</h3><ul>{cons_html}</ul>
        <h3>Verdict</h3><p>{data['verdict_intro']}</p>
    </div>
</body>
</html>
"""
        
        # B. Save HTML File (with utf-8)
        if not os.path.exists('reviews'): os.makedirs('reviews')
        filename = f"reviews/{laptop_name.replace(' ', '_')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # C. History & JSON Update
        with open(HISTORY_FILE, "a", encoding='utf-8') as f:
            f.write(f"{laptop_name}\n")
        
        laptops = []
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                laptops = json.load(f)

        laptops.append({
            "title": laptop_name,
            "price": data.get('price', '₹0'),
            "amazonLink": amazon_link,
            "review_link": filename
        })

        # CRITICAL: ensure_ascii=False enables Hindi characters
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(laptops, f, indent=4, ensure_ascii=False)
        
        print(f"Success! {laptop_name} added successfully in Hindi.")

except Exception as e:
    print(f"Error: {e}")
        
